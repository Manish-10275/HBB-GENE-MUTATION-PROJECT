"""Service orchestrating core biological analysis, consequence calculation, and evidence integration."""

from dataclasses import dataclass, field
from typing import List, Optional

from app.core.consequences import evaluate_consequence
from app.core.hgvs import parse_hgvs
from app.core.models import (
    AnalysisError,
    AnalysisErrorCode,
    ConsequenceResult,
    NormalizedVariant,
)
from app.core.reference import ReferenceSequence, load_reference
from app.evidence.models import ClinVarEvidenceResult, EvidenceDiscrepancy
from app.services.evidence_service import EvidenceService


@dataclass(frozen=True)
class VariantAnalysisResult:
    """Consolidated outcome of variant interpretation pipeline."""
    input_query: str
    normalized_variant: NormalizedVariant
    consequence: ConsequenceResult
    clinvar_evidence: Optional[ClinVarEvidenceResult] = None
    discrepancies: List[EvidenceDiscrepancy] = field(default_factory=list)


class VariantService:
    """
    Coordinates the core domain pipeline:
    Input -> Reference -> HGVS AST -> Biological Consequence -> Optional Evidence.
    
    Guarantees:
    - Biological calculations remain in app.core
    - External evidence cannot override deterministic consequences
    - Optional evidence failure does not block variant analysis
    """

    def __init__(
        self,
        ref_seq: Optional[ReferenceSequence] = None,
        ng_seq: Optional[ReferenceSequence] = None,
        evidence_service: Optional[EvidenceService] = None,
    ):
        self.ref_seq = ref_seq or load_reference("NM_000518.5")
        self.ng_seq = ng_seq or load_reference("NG_000007.3")
        self.evidence_service = evidence_service

    async def analyze_variant(
        self,
        query: str,
        include_evidence: bool = False,
    ) -> VariantAnalysisResult:
        """
        Executes end-to-end variant interpretation.
        Raises AnalysisError on invalid syntax, reference mismatch, or out-of-bounds coordinates.
        """
        # 1. Deterministic HGVS parsing & validation against reference
        normalized = parse_hgvs(query, ref_seq=self.ref_seq, ng_seq=self.ng_seq)

        # 2. Deterministic protein consequence evaluation
        consequence = evaluate_consequence(normalized, self.ref_seq)

        # 3. Optional evidence retrieval
        clinvar_evidence: Optional[ClinVarEvidenceResult] = None
        discrepancies: List[EvidenceDiscrepancy] = []

        if include_evidence and self.evidence_service:
            try:
                clinvar_evidence = await self.evidence_service.get_clinvar_evidence(
                    query=normalized.hgvs_c,
                    normalized_variant=normalized,
                    deterministic_consequence=consequence.hgvs_p,
                )
                if clinvar_evidence:
                    discrepancies.extend(clinvar_evidence.discrepancies)
            except Exception:
                # Evidence retrieval is strictly non-blocking for core analysis
                clinvar_evidence = None

        return VariantAnalysisResult(
            input_query=query,
            normalized_variant=normalized,
            consequence=consequence,
            clinvar_evidence=clinvar_evidence,
            discrepancies=discrepancies,
        )
