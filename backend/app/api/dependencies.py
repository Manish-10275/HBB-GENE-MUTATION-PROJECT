"""Dependency injection providers for FastAPI routes."""

from fastapi import Depends

from app.config import settings
from app.core.reference import load_reference
from app.evidence.clinvar_live import LiveClinVarProvider
from app.evidence.clinvar_offline import OfflineClinVarProvider
from app.evidence.pubmed_live import LivePubMedProvider
from app.evidence.pubmed_offline import OfflinePubMedProvider
from app.services.ai_service import AiCopilotService
from app.services.evidence_service import EvidenceService
from app.services.variant_service import VariantService


def get_evidence_service() -> EvidenceService:

    """Provides configured EvidenceService respecting application settings."""
    mode = getattr(settings, "EVIDENCE_MODE", "offline").lower()

    if mode == "live":
        clinvar_provider = LiveClinVarProvider(
            base_url=settings.NCBI_BASE_URL,
            api_key=settings.NCBI_API_KEY,
            email=settings.NCBI_EMAIL,
        )
        pubmed_provider = LivePubMedProvider(
            base_url=settings.NCBI_BASE_URL,
            api_key=settings.NCBI_API_KEY,
            email=settings.NCBI_EMAIL,
        )
    else:
        clinvar_provider = OfflineClinVarProvider()
        pubmed_provider = OfflinePubMedProvider()

    return EvidenceService(
        clinvar_provider=clinvar_provider,
        pubmed_provider=pubmed_provider,
    )


def get_variant_service(
    evidence_service: EvidenceService = Depends(get_evidence_service),
) -> VariantService:
    """Provides VariantService wired with cached biological reference sequences."""
    ref_nm = load_reference("NM_000518.5")
    ref_ng = load_reference("NG_000007.3")

    return VariantService(
        ref_seq=ref_nm,
        ng_seq=ref_ng,
        evidence_service=evidence_service,
    )


def get_ai_service(
    evidence_service: EvidenceService = Depends(get_evidence_service),
) -> AiCopilotService:
    """Provides AiCopilotService wired with EvidenceService."""
    return AiCopilotService(evidence_service=evidence_service)

