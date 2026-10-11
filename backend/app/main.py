"""FastAPI main application entrypoint for HBB Mutation Analyzer."""

import asyncio
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import settings
from app.models import (
    AiSynthesisStatus,
    AnalyzeRequest,
    AnalyzeResponse,
    ClinVarRecord,
    CopilotRequest,
    CopilotResponse,
    PubMedRecord,
    ReportRequest,
    ReportResponse,
    ScreeningClassification,
    SimulatorGenerateRequest,
    SimulatorGenerateResponse,
    VariantSearchRequest,
    VariantSearchResponse,
)
from app.reference import reference_manager
from app.sequence import normalize_and_validate_sequence
from app.alignment import align_sequences
from app.variants import detect_variants, parse_hgvs_input
from app.clinvar import fetch_clinvar_records
from app.pubmed import fetch_pubmed_records
from app.evidence import assemble_evidence_packet
from app.ai import synthesize_research_copilot
from app.reports import generate_research_report
from app.simulator import (
    classify_screening,
    get_available_mutation_presets,
    simulate_mutated_sequence,
)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Configure CORS (robust local origin matching)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import router as v2_router
app.include_router(v2_router)


@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """Health status and reference configuration check."""
    ref = reference_manager.get_reference(settings.DEFAULT_REFERENCE_ACCESSION)
    return {
        "status": "healthy",
        "service": "HBB Mutation Analyzer API",
        "version": settings.API_VERSION,
        "reference_accession": ref.accession,
        "reference_gene": ref.gene,
        "reference_length_bp": ref.total_length,
        "cds_coordinates": f"{ref.cds_start}..{ref.cds_end}",
        "groq_configured": bool(settings.effective_groq_api_key),
        "groq_model": settings.GROQ_MODEL,
        "ncbi_configured": bool(settings.NCBI_API_KEY),
    }


@app.get("/reference", tags=["Genomic Data"])
async def get_reference_details(
    accession: str = settings.DEFAULT_REFERENCE_ACCESSION
) -> Dict[str, Any]:
    """Retrieves authoritative reference sequence and feature metadata."""
    try:
        ref = reference_manager.get_reference(accession)
        return {
            "gene": ref.gene,
            "organism": ref.organism,
            "accession": ref.accession,
            "molecule_type": ref.molecule_type,
            "total_length": ref.total_length,
            "cds_start": ref.cds_start,
            "cds_end": ref.cds_end,
            "cds_length": ref.cds_length,
            "protein_id": ref.protein_id,
            "protein_length": ref.protein_length,
            "source": ref.source,
            "source_url": ref.source_url,
            "sequence": ref.sequence,
            "cds_sequence": ref.cds_sequence,
            "protein_sequence": ref.protein_sequence,
            "exons": [
                {
                    "number": e.number,
                    "start": e.start,
                    "end": e.end,
                    "genomic_start": e.genomic_start,
                    "genomic_end": e.genomic_end
                }
                for e in ref.exons
            ],
            "introns": ref.introns,
            "genomic_start": ref.genomic_start,
            "genomic_end": ref.genomic_end
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reference accession '{accession}' not supported."
        )


@app.get("/reference/list", tags=["Genomic Data"])
async def list_available_references() -> List[Dict[str, Any]]:
    """Lists available reference sequences with genomic and transcript annotations."""
    return reference_manager.list_references()


@app.get("/mutations/indian", tags=["Indian Thalassemia"])
async def get_indian_mutations_panel() -> Dict[str, Any]:
    """Retrieves the verified four Indian thalassemia mutations panel with full clinical and coordinate data."""
    return reference_manager.get_indian_mutations()


@app.get("/simulator/presets", tags=["Educational Simulator"])
async def get_simulator_presets() -> List[Dict[str, Any]]:
    """Returns available simulation presets including the Indian thalassemia panel and controls."""
    return get_available_mutation_presets()


@app.post("/simulator/generate", response_model=SimulatorGenerateResponse, tags=["Educational Simulator"])
async def generate_simulated_sequence(payload: SimulatorGenerateRequest) -> SimulatorGenerateResponse:
    """Generates an in silico mutated HBB sequence for educational screening simulation."""
    try:
        res = simulate_mutated_sequence(payload.preset_id)
        return SimulatorGenerateResponse(**res)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/examples", tags=["Genomic Data"])
async def list_example_sequences() -> List[Dict[str, Any]]:
    """Returns curated validation sequences and benchmarks."""
    examples_dir = settings.EXAMPLES_DIR
    items: List[Dict[str, Any]] = []

    file_meta = [
        {
            "filename": "validation_c118C_T.fasta",
            "title": "Controlled Validation Case (c.118C>T / p.Gln40Ter)",
            "description": "Benchmark synthetic nonsense mutation producing premature termination codon at Gln40.",
            "is_validation_case": True,
            "category": "Controlled Benchmark"
        },
        {
            "filename": "wildtype_HBB.fasta",
            "title": "Wild-Type Reference Sequence",
            "description": "Complete 628 bp canonical NM_000518.5 transcript with 100% identity.",
            "is_validation_case": False,
            "category": "Wild-Type"
        },
        {
            "filename": "sickle_cell_c20A_T.fasta",
            "title": "Sickle Cell Hemoglobin (HbS c.20A>T / p.Glu7Val)",
            "description": "Canonical sickle cell trait substitution at codon 7 changing Glutamate to Valine.",
            "is_validation_case": False,
            "category": "Pathogenic Variant"
        },
        {
            "filename": "hemoglobin_c_c19G_A.fasta",
            "title": "Hemoglobin C (HbC c.19G>A / p.Glu7Lys)",
            "description": "Hemoglobin C substitution at codon 7 changing Glutamate to Lysine.",
            "is_validation_case": False,
            "category": "Pathogenic Variant"
        },
        {
            "filename": "frameshift_insertion.fasta",
            "title": "Synthetic Frameshift Insertion (c.117_118insA)",
            "description": "Synthetic 1-bp insertion demonstrating out-of-frame disruption.",
            "is_validation_case": False,
            "category": "Synthetic Test"
        },
        {
            "filename": "frameshift_deletion.fasta",
            "title": "Synthetic Frameshift Deletion (c.118delC)",
            "description": "Synthetic 1-bp deletion demonstrating coding truncation.",
            "is_validation_case": False,
            "category": "Synthetic Test"
        }
    ]

    for meta in file_meta:
        path = examples_dir / meta["filename"]
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            items.append({
                **meta,
                "sequence": content
            })

    return items


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Bioinformatics"])
async def analyze_sequence(payload: AnalyzeRequest) -> AnalyzeResponse:
    """
    Core sequence analysis endpoint.
    1. Normalizes and validates sequence.
    2. Deterministically aligns against NM_000518.5.
    3. Calls variants and computes codon/protein consequences.
    4. Retrieves ClinVar and PubMed evidence.
    5. Assembles EvidencePacket.
    """
    # 1. Validation & normalization
    norm = normalize_and_validate_sequence(payload.sequence)
    if not norm.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Sequence validation failed", "errors": norm.validation_errors}
        )

    # 2. Reference retrieval
    try:
        ref_data = reference_manager.get_reference(payload.reference_accession)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported reference accession '{payload.reference_accession}'."
        )

    # 3. Alignment
    summary, aligned_ref, aligned_query = align_sequences(
        ref_data.sequence, norm.clean_sequence
    )

    # 4. Variant detection & codon consequences
    variants = detect_variants(aligned_ref, aligned_query, ref_data)

    # 5. External evidence retrieval (ClinVar and PubMed)
    clinvar_records: List[ClinVarRecord] = []
    pubmed_records: List[PubMedRecord] = []

    if variants:
        # Query for up to first 3 variants
        for v in variants[:3]:
            if v.variant_type == "substitution":
                c_term = f"c.{v.c_position}{v.ref_allele}>{v.alt_allele}"
            elif v.variant_type in ("deletion", "duplication", "insertion"):
                c_term = v.hgvs_c.split(":")[-1] if ":" in v.hgvs_c else v.hgvs_c
            else:
                c_term = v.hgvs_c
            cv_res = await fetch_clinvar_records(
                query_term=c_term,
                transcript_accession=ref_data.accession,
                variant_aliases=v.equivalent_nomenclature,
                protein_change=v.hgvs_p,
            )
            for r in cv_res:
                if not any(existing.id == r.id for existing in clinvar_records):
                    clinvar_records.append(r)

            pm_res = await fetch_pubmed_records(c_term, variant_aliases=v.equivalent_nomenclature)
            for r in pm_res:
                if not any(existing.pmid == r.pmid for existing in pubmed_records):
                    pubmed_records.append(r)

    # 6. Screening classification based on zygosity
    screening_classification = classify_screening(
        detected_variants=variants,
        zygosity=payload.zygosity or "heterozygous"
    )

    # 7. Assemble evidence packet
    packet = assemble_evidence_packet(
        ref_data=ref_data,
        alignment_summary=summary,
        variants=variants,
        clinvar_records=clinvar_records,
        pubmed_records=pubmed_records,
        screening_classification=screening_classification
    )

    ref_metadata = {
        "accession": ref_data.accession,
        "gene": ref_data.gene,
        "molecule_type": ref_data.molecule_type,
        "total_length": ref_data.total_length,
        "exons": [
            {
                "number": e.number,
                "start": e.start,
                "end": e.end,
                "genomic_start": e.genomic_start,
                "genomic_end": e.genomic_end,
            }
            for e in ref_data.exons
        ],
        "introns": ref_data.introns,
        "genomic_start": ref_data.genomic_start,
        "genomic_end": ref_data.genomic_end,
    }

    # 8. Automated AI Synthesis Explanation
    ai_status = None
    if getattr(payload, "include_ai", True):
        if variants:
            primary_v = variants[0]
            question = (
                f"Explain the molecular and biological consequence of the variant {primary_v.hgvs_c} "
                f"({primary_v.hgvs_p or 'non-coding'}) based on the retrieved evidence."
            )
        else:
            question = "Summarize the wild-type beta globin sequence analysis and confirm reference alignment."

        try:
            cop_res = await synthesize_research_copilot(question, packet, [])
            ai_status = AiSynthesisStatus(
                available=bool(settings.GROQ_API_KEY),
                provider="groq",
                model=settings.GROQ_MODEL,
                status=cop_res.status,
                answer=cop_res.answer,
                fallback=cop_res.fallback,
                evidence_used=cop_res.evidence_used,
                provenance_sections=cop_res.provenance_sections,
                provenance_label=cop_res.provenance_label
            )
        except Exception:
            ai_status = AiSynthesisStatus(
                available=bool(settings.GROQ_API_KEY),
                provider="groq",
                model=settings.GROQ_MODEL,
                status="error",
                answer="AI synthesis was temporarily unavailable.",
                fallback=True,
                evidence_used=["Deterministic Sequence Engine"],
                provenance_sections=[
                    "DIRECT SCIENTIFIC ANSWER",
                    "A. COMPUTED FACTS",
                    "B. DATABASE EVIDENCE",
                    "C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
                    "D. AI SYNTHESIS",
                    "EVIDENCE LIMITATIONS",
                ],
                provenance_label="Deterministic synthesis"
            )

    return AnalyzeResponse(
        success=True,
        summary=packet.summary,
        alignment=summary,
        variants=variants,
        evidence_packet=packet,
        screening_classification=screening_classification,
        reference_metadata=ref_metadata,
        ai=ai_status
    )


@app.get("/variant/search", response_model=VariantSearchResponse, tags=["Evidence"])
@app.post("/variant/search", response_model=VariantSearchResponse, tags=["Evidence"])
async def search_variant_direct(
    query: Optional[str] = Query(None, description="HGVS cDNA query, e.g. c.118C>T or NM_000518.5:c.118C>T"),
    body: Optional[VariantSearchRequest] = None
) -> VariantSearchResponse:
    """Direct variant investigation via HGVS notation."""
    search_query = (query or (body.query if body else "")).strip()
    search_query = re.sub(r"(\d+)\s+(\d+)", r"\1+\2", search_query)
    if not search_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A query term must be provided, e.g. 'c.118C>T' or 'NM_000518.5:c.118C>T'."
        )

    ref = reference_manager.get_reference(settings.DEFAULT_REFERENCE_ACCESSION)
    variant_model, parse_err = parse_hgvs_input(search_query, ref)

    clean_term = search_query
    standard_hgvs = None
    if variant_model:
        standard_hgvs = variant_model.hgvs_c
        if variant_model.variant_type == "substitution":
            clean_term = f"c.{variant_model.c_position}{variant_model.ref_allele}>{variant_model.alt_allele}"
        elif variant_model.variant_type in ("deletion", "duplication", "insertion"):
            clean_term = variant_model.hgvs_c.split(":")[-1] if ":" in variant_model.hgvs_c else variant_model.hgvs_c
        else:
            clean_term = variant_model.hgvs_c

    # Query external scientific evidence
    aliases = variant_model.equivalent_nomenclature if variant_model else None
    protein_change = variant_model.hgvs_p if variant_model else None
    clinvar_task = fetch_clinvar_records(
        query_term=clean_term,
        transcript_accession=ref.accession,
        variant_aliases=aliases,
        protein_change=protein_change,
    )
    pubmed_task = fetch_pubmed_records(clean_term, variant_aliases=aliases)
    cv_records, pm_records = await asyncio.gather(clinvar_task, pubmed_task)

    return VariantSearchResponse(
        query=search_query,
        standardized_hgvs_c=standard_hgvs,
        clinvar_records=cv_records,
        pubmed_records=pm_records,
        source="NCBI E-Utilities",
        error=parse_err
    )


@app.post("/copilot", response_model=CopilotResponse, tags=["AI Research Copilot"])
async def copilot_chat(payload: CopilotRequest) -> CopilotResponse:
    """Grounds user research questions strictly in the supplied EvidencePacket."""
    return await synthesize_research_copilot(
        question=payload.question,
        evidence_packet=payload.evidence_packet,
        conversation_history=payload.conversation_history
    )


@app.post("/report", response_model=ReportResponse, tags=["Reports"])
async def generate_report(payload: ReportRequest) -> ReportResponse:
    """Generates standardized Markdown and printable HTML Research Report."""
    return generate_research_report(
        packet=payload.evidence_packet,
        copilot_summary=payload.copilot_summary
    )
