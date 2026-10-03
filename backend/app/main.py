"""FastAPI main application entrypoint for HBB Mutation Analyzer."""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import settings
from app.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    ClinVarRecord,
    CopilotRequest,
    CopilotResponse,
    PubMedRecord,
    ReportRequest,
    ReportResponse,
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

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "openai_configured": bool(settings.OPENAI_API_KEY)
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
                {"number": e.number, "start": e.start, "end": e.end}
                for e in ref.exons
            ]
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reference accession '{accession}' not supported."
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
            # Try specific HGVS c. notation first
            c_term = f"c.{v.c_position}{v.ref_allele}>{v.alt_allele}" if v.variant_type == "substitution" else v.hgvs_c
            cv_res = await fetch_clinvar_records(c_term)
            for r in cv_res:
                if not any(existing.id == r.id for existing in clinvar_records):
                    clinvar_records.append(r)

            pm_res = await fetch_pubmed_records(c_term)
            for r in pm_res:
                if not any(existing.pmid == r.pmid for existing in pubmed_records):
                    pubmed_records.append(r)

    # 6. Assemble evidence packet
    packet = assemble_evidence_packet(
        ref_data=ref_data,
        alignment_summary=summary,
        variants=variants,
        clinvar_records=clinvar_records,
        pubmed_records=pubmed_records
    )

    return AnalyzeResponse(
        success=True,
        summary=packet.summary,
        alignment=summary,
        variants=variants,
        evidence_packet=packet
    )


@app.get("/variant/search", response_model=VariantSearchResponse, tags=["Evidence"])
@app.post("/variant/search", response_model=VariantSearchResponse, tags=["Evidence"])
async def search_variant_direct(
    query: Optional[str] = Query(None, description="HGVS cDNA query, e.g. c.118C>T or NM_000518.5:c.118C>T"),
    body: Optional[VariantSearchRequest] = None
) -> VariantSearchResponse:
    """Direct variant investigation via HGVS notation."""
    search_query = (query or (body.query if body else "")).strip()
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
        clean_term = f"c.{variant_model.c_position}{variant_model.ref_allele}>{variant_model.alt_allele}"

    # Query external scientific evidence
    clinvar_task = fetch_clinvar_records(clean_term)
    pubmed_task = fetch_pubmed_records(clean_term)
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
