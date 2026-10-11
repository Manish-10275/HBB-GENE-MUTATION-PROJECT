"""FastAPI router for clean v2 API endpoints."""

from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_ai_service, get_evidence_service, get_variant_service
from app.api.schemas import (
    ClinVarEvidenceResponseDTO,
    ClinVarRecordDTO,
    CodonChangeDTO,
    CopilotResponseDTO,
    CopilotSynthesisRequestDTO,
    DiscrepancyDTO,
    HealthDiagnosticsResponse,
    ProvenanceDTO,
    PubMedArticleDTO,
    PubMedEvidenceResponseDTO,
    VariantAnalysisRequest,
    VariantAnalysisResponse,
)
from app.config import settings
from app.core.models import AnalysisError
from app.core.reference import load_reference
from app.services.ai_service import AiCopilotService
from app.services.evidence_service import EvidenceService
from app.services.variant_service import VariantAnalysisResult, VariantService

router = APIRouter(prefix="/api/v2", tags=["v2 Clean Interpretation"])


def _to_analysis_response(result: VariantAnalysisResult) -> VariantAnalysisResponse:
    """Helper to convert domain VariantAnalysisResult into API response DTO."""
    v = result.normalized_variant
    c = result.consequence

    codon_dto: Optional[CodonChangeDTO] = None
    if c.codon_change:
        cc = c.codon_change
        codon_dto = CodonChangeDTO(
            codon_number=cc.codon_number,
            c_start=cc.c_start,
            c_end=cc.c_end,
            ref_codon=cc.ref_codon,
            sample_codon=cc.sample_codon,
            ref_aa=cc.ref_aa,
            sample_aa=cc.sample_aa,
            is_stop_gain=cc.is_stop_gain,
            is_stop_loss=cc.is_stop_loss,
            is_synonymous=cc.is_synonymous,
        )

    discrepancy_dtos = [
        DiscrepancyDTO(
            field_name=d.field_name,
            deterministic_value=d.deterministic_value,
            evidence_value=d.evidence_value,
            description=d.description,
        )
        for d in result.discrepancies
    ]

    clinvar_dto: Optional[ClinVarEvidenceResponseDTO] = None
    if result.clinvar_evidence:
        ce = result.clinvar_evidence
        records_dto = []
        for r in ce.records:
            r_prov: Optional[ProvenanceDTO] = None
            if r.provenance:
                r_prov = ProvenanceDTO(
                    source=r.provenance.source,
                    provider=r.provenance.provider,
                    mode=r.provenance.mode.value,
                    retrieval_status=r.provenance.retrieval_status.value,
                    external_identifier=r.provenance.external_identifier,
                    is_fixture=r.provenance.is_fixture,
                    retrieval_timestamp=r.provenance.retrieval_timestamp,
                )
            records_dto.append(
                ClinVarRecordDTO(
                    variation_id=r.variation_id,
                    accession=r.accession,
                    title=r.title,
                    clinical_significance=r.clinical_significance,
                    review_status=r.review_status,
                    conditions=r.conditions,
                    url=r.url,
                    is_exact_match=r.is_exact_match,
                    retrieval_rank=r.retrieval_rank,
                    provenance=r_prov,
                )
            )

        primary_dto = records_dto[0] if records_dto else None
        overall_prov: Optional[ProvenanceDTO] = None
        if ce.provenance:
            overall_prov = ProvenanceDTO(
                source=ce.provenance.source,
                provider=ce.provenance.provider,
                mode=ce.provenance.mode.value,
                retrieval_status=ce.provenance.retrieval_status.value,
                external_identifier=ce.provenance.external_identifier,
                is_fixture=ce.provenance.is_fixture,
                retrieval_timestamp=ce.provenance.retrieval_timestamp,
            )

        clinvar_dto = ClinVarEvidenceResponseDTO(
            query=ce.query,
            status=ce.status.value,
            records=records_dto,
            primary_record=primary_dto,
            discrepancies=[
                DiscrepancyDTO(
                    field_name=d.field_name,
                    deterministic_value=d.deterministic_value,
                    evidence_value=d.evidence_value,
                    description=d.description,
                )
                for d in ce.discrepancies
            ],
            error_message=ce.error_message,
            provenance=overall_prov,
        )

    return VariantAnalysisResponse(
        input_query=result.input_query,
        normalized_hgvs_c=v.hgvs_c,
        transcript_accession=v.transcript_accession,
        c_position=v.c_position,
        variant_type=v.variant_type.value,
        region=v.region,
        ref_allele=v.ref_allele,
        alt_allele=v.alt_allele,
        mrna_position=v.mrna_position,
        genomic_accession=v.genomic_accession,
        genomic_coordinate=v.genomic_coordinate,
        hgvs_p=c.hgvs_p,
        molecular_impact=c.molecular_impact.value,
        codon_change=codon_dto,
        ptc_coordinate=c.ptc_coordinate,
        confidence=c.confidence,
        equivalent_nomenclature=v.equivalent_nomenclature,
        nomenclature_notes=v.nomenclature_notes,
        evidence_status=result.clinvar_evidence.status.value if result.clinvar_evidence else None,
        clinvar_evidence=clinvar_dto,
        discrepancies=discrepancy_dtos,
    )


@router.post("/analyze/variant", response_model=VariantAnalysisResponse)
async def analyze_variant_post(
    req: VariantAnalysisRequest,
    variant_service: VariantService = Depends(get_variant_service),
) -> VariantAnalysisResponse:
    """Analyzes a sequence variant deterministically with optional evidence retrieval."""
    try:
        result = await variant_service.analyze_variant(
            query=req.query,
            include_evidence=req.include_evidence,
        )
        return _to_analysis_response(result)
    except AnalysisError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": e.code.value,
                "message": e.message,
                "details": e.details,
            },
        )


@router.get("/analyze/variant", response_model=VariantAnalysisResponse)
async def analyze_variant_get(
    query: str = Query(..., description="Variant query string (e.g. 'c.118C>T')"),
    include_evidence: bool = Query(False, description="Whether to include ClinVar evidence"),
    variant_service: VariantService = Depends(get_variant_service),
) -> VariantAnalysisResponse:
    """GET endpoint for variant analysis."""
    try:
        result = await variant_service.analyze_variant(
            query=query,
            include_evidence=include_evidence,
        )
        return _to_analysis_response(result)
    except AnalysisError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": e.code.value,
                "message": e.message,
                "details": e.details,
            },
        )


@router.get("/evidence/clinvar", response_model=ClinVarEvidenceResponseDTO)
async def get_clinvar_evidence(
    query: str = Query(..., description="Variant query string"),
    evidence_service: EvidenceService = Depends(get_evidence_service),
) -> ClinVarEvidenceResponseDTO:
    """Retrieves ClinVar evidence records with explicit status and provenance."""
    result = await evidence_service.get_clinvar_evidence(query=query)

    records_dto = []
    for r in result.records:
        r_prov = None
        if r.provenance:
            r_prov = ProvenanceDTO(
                source=r.provenance.source,
                provider=r.provenance.provider,
                mode=r.provenance.mode.value,
                retrieval_status=r.provenance.retrieval_status.value,
                external_identifier=r.provenance.external_identifier,
                is_fixture=r.provenance.is_fixture,
                retrieval_timestamp=r.provenance.retrieval_timestamp,
            )
        records_dto.append(
            ClinVarRecordDTO(
                variation_id=r.variation_id,
                accession=r.accession,
                title=r.title,
                clinical_significance=r.clinical_significance,
                review_status=r.review_status,
                conditions=r.conditions,
                url=r.url,
                is_exact_match=r.is_exact_match,
                retrieval_rank=r.retrieval_rank,
                provenance=r_prov,
            )
        )

    overall_prov = None
    if result.provenance:
        overall_prov = ProvenanceDTO(
            source=result.provenance.source,
            provider=result.provenance.provider,
            mode=result.provenance.mode.value,
            retrieval_status=result.provenance.retrieval_status.value,
            external_identifier=result.provenance.external_identifier,
            is_fixture=result.provenance.is_fixture,
            retrieval_timestamp=result.provenance.retrieval_timestamp,
        )

    return ClinVarEvidenceResponseDTO(
        query=result.query,
        status=result.status.value,
        records=records_dto,
        primary_record=records_dto[0] if records_dto else None,
        discrepancies=[
            DiscrepancyDTO(
                field_name=d.field_name,
                deterministic_value=d.deterministic_value,
                evidence_value=d.evidence_value,
                description=d.description,
            )
            for d in result.discrepancies
        ],
        error_message=result.error_message,
        provenance=overall_prov,
    )


@router.get("/evidence/pubmed", response_model=PubMedEvidenceResponseDTO)
async def get_pubmed_evidence(
    query: str = Query(..., description="Variant query or keyword string"),
    max_results: int = Query(10, ge=1, le=50),
    evidence_service: EvidenceService = Depends(get_evidence_service),
) -> PubMedEvidenceResponseDTO:
    """Retrieves scientific literature citations from PubMed."""
    result = await evidence_service.get_pubmed_evidence(query=query, max_results=max_results)

    articles_dto = []
    for a in result.articles:
        a_prov = None
        if a.provenance:
            a_prov = ProvenanceDTO(
                source=a.provenance.source,
                provider=a.provenance.provider,
                mode=a.provenance.mode.value,
                retrieval_status=a.provenance.retrieval_status.value,
                external_identifier=a.provenance.external_identifier,
                is_fixture=a.provenance.is_fixture,
                retrieval_timestamp=a.provenance.retrieval_timestamp,
            )
        articles_dto.append(
            PubMedArticleDTO(
                pmid=a.pmid,
                title=a.title,
                journal=a.journal,
                pub_date=a.pub_date,
                authors=a.authors,
                url=a.url,
                provenance=a_prov,
            )
        )

    overall_prov = None
    if result.provenance:
        overall_prov = ProvenanceDTO(
            source=result.provenance.source,
            provider=result.provenance.provider,
            mode=result.provenance.mode.value,
            retrieval_status=result.provenance.retrieval_status.value,
            external_identifier=result.provenance.external_identifier,
            is_fixture=result.provenance.is_fixture,
            retrieval_timestamp=result.provenance.retrieval_timestamp,
        )

    return PubMedEvidenceResponseDTO(
        query=result.query,
        status=result.status.value,
        articles=articles_dto,
        error_message=result.error_message,
        provenance=overall_prov,
    )


@router.post("/copilot/synthesize", response_model=CopilotResponseDTO)
async def synthesize_variant_copilot(
    payload: CopilotSynthesisRequestDTO,
    variant_service: VariantService = Depends(get_variant_service),
    ai_service: AiCopilotService = Depends(get_ai_service),
) -> CopilotResponseDTO:
    """
    Synthesizes AI research interpretation grounded strictly on deterministic variant analysis.
    
    Pipeline order:
    1. VariantService executes deterministic consequence analysis (app.core).
    2. Optional external evidence retrieved via EvidenceService.
    3. AiCopilotService synthesizes evidence-grounded explanation.
    """
    try:
        analysis_result = await variant_service.analyze_variant(
            query=payload.query,
            include_evidence=payload.include_evidence,
        )
    except AnalysisError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": e.code.value, "message": e.message, "details": e.details},
        )

    copilot_res = await ai_service.synthesize_variant_analysis(
        analysis_result=analysis_result,
        question=payload.question,
        include_literature=payload.include_literature,
    )

    return CopilotResponseDTO(
        answer=copilot_res.answer,
        evidence_used=copilot_res.evidence_used,
        limitations_cited=copilot_res.limitations_cited,
        status=copilot_res.status,
        provider=copilot_res.provider,
        model=copilot_res.model,
        fallback=copilot_res.fallback,
        provenance_sections=copilot_res.provenance_sections,
        provenance_label=copilot_res.provenance_label,
    )


@router.get("/health", response_model=HealthDiagnosticsResponse)

async def get_extended_health_diagnostics() -> HealthDiagnosticsResponse:
    """Extended diagnostics checking core references, provider modes, and offline fixtures."""
    ref_nm_avail = False
    ref_ng_avail = False
    try:
        load_reference("NM_000518.5")
        ref_nm_avail = True
    except Exception:
        pass

    try:
        load_reference("NG_000007.3")
        ref_ng_avail = True
    except Exception:
        pass

    fixtures_dir = Path(__file__).resolve().parent.parent.parent.parent / "data" / "fixtures"
    clinvar_fix_avail = (fixtures_dir / "clinvar_fixtures.json").exists()
    pubmed_fix_avail = (fixtures_dir / "pubmed_fixtures.json").exists()

    mode = getattr(settings, "EVIDENCE_MODE", "offline").lower()

    return HealthDiagnosticsResponse(
        status="healthy" if (ref_nm_avail and ref_ng_avail) else "degraded",
        service="HBB Mutation Analyzer API v2",
        version="2.0.0",
        reference_availability={
            "NM_000518.5": ref_nm_avail,
            "NG_000007.3": ref_ng_avail,
        },
        evidence_provider_mode=mode,
        fixture_availability={
            "clinvar_fixtures.json": clinvar_fix_avail,
            "pubmed_fixtures.json": pubmed_fix_avail,
        },
    )
