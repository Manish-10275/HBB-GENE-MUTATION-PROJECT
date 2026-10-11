"""Service orchestrating external evidence retrieval and discrepancy auditing."""

import logging
from typing import Optional, Union

from app.core.models import NormalizedVariant
from app.evidence.clinvar_live import LiveClinVarProvider
from app.evidence.clinvar_offline import OfflineClinVarProvider
from app.evidence.models import ClinVarEvidenceResult, PubMedEvidenceResult
from app.evidence.pubmed_live import LivePubMedProvider
from app.evidence.pubmed_offline import OfflinePubMedProvider

logger = logging.getLogger(__name__)

ClinVarProviderType = Union[OfflineClinVarProvider, LiveClinVarProvider]
PubMedProviderType = Union[OfflinePubMedProvider, LivePubMedProvider]


class EvidenceService:
    """
    Orchestrates retrieval from configured evidence providers.
    
    Guarantees:
    - Injected provider handles execution mode (offline vs live)
    - Discrepancy comparison against deterministic core consequence
    - Non-blocking execution (literature failure does not degrade variant analysis)
    """

    def __init__(
        self,
        clinvar_provider: Optional[ClinVarProviderType] = None,
        pubmed_provider: Optional[PubMedProviderType] = None,
    ):
        self.clinvar_provider = clinvar_provider or OfflineClinVarProvider()
        self.pubmed_provider = pubmed_provider or OfflinePubMedProvider()

    async def get_clinvar_evidence(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant] = None,
        deterministic_consequence: Optional[str] = None,
    ) -> ClinVarEvidenceResult:
        """Retrieves and normalizes ClinVar evidence with discrepancy tracking."""
        if isinstance(self.clinvar_provider, LiveClinVarProvider):
            return await self.clinvar_provider.search_variant(
                query, normalized_variant, deterministic_consequence
            )
        else:
            return self.clinvar_provider.search_variant(
                query, normalized_variant, deterministic_consequence
            )

    async def get_pubmed_evidence(
        self,
        query: str,
        max_results: int = 10,
    ) -> PubMedEvidenceResult:
        """Retrieves and normalizes scholarly literature evidence."""
        if isinstance(self.pubmed_provider, LivePubMedProvider):
            return await self.pubmed_provider.search_literature(query, max_results)
        else:
            return self.pubmed_provider.search_literature(query)
