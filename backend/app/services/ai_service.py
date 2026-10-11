"""Service coordinating AI copilot synthesis strictly bounded by deterministic analysis."""

import logging
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models import CopilotChatMessage, CopilotResponse
    from app.evidence.models import PubMedEvidenceResult
    from app.services.evidence_service import EvidenceService
    from app.services.variant_service import VariantAnalysisResult

logger = logging.getLogger(__name__)


class AiCopilotService:
    """
    Coordinates AI synthesis from deterministic VariantAnalysisResult.
    
    Guarantees:
    - AI receives strictly deterministic calculations as ground truth
    - AI cannot calculate, override, or alter biological consequences
    - Explicit provenance labeling across all outputs
    - Graceful fallback when API key is missing or calls fail
    - Discrepancy explanation without overriding the core engine
    """

    def __init__(self, evidence_service: Optional["EvidenceService"] = None):
        self.evidence_service = evidence_service

    async def synthesize_variant_analysis(
        self,
        analysis_result: "VariantAnalysisResult",
        question: Optional[str] = None,
        conversation_history: Optional[List["CopilotChatMessage"]] = None,
        include_literature: bool = True,
        max_literature_results: int = 5,
    ) -> "CopilotResponse":
        """
        Coordinates evidence-grounded research synthesis for an analyzed variant.
        Ensures the AI is supplied the completed deterministic consequence
        and optional external evidence.
        """
        from app.ai import synthesize_research_copilot
        from app.evidence.models import PubMedEvidenceResult

        pubmed_evidence: Optional[PubMedEvidenceResult] = None
        if include_literature and self.evidence_service:
            try:
                pubmed_evidence = await self.evidence_service.get_pubmed_evidence(
                    query=analysis_result.normalized_variant.hgvs_c,
                    max_results=max_literature_results,
                )
            except Exception as e:
                logger.warning("PubMed literature retrieval failed in AI service: %s", e)
                pubmed_evidence = None

        if not question or not question.strip():
            question = (
                f"Explain the molecular and biological consequence of the variant "
                f"{analysis_result.normalized_variant.hgvs_c} ({analysis_result.consequence.hgvs_p}) "
                f"based on the retrieved evidence."
            )

        return await synthesize_research_copilot(
            question=question,
            evidence_packet=analysis_result,
            conversation_history=conversation_history or [],
            pubmed_evidence=pubmed_evidence,
        )

    async def explain_discrepancy(
        self,
        analysis_result: "VariantAnalysisResult",
        question: Optional[str] = None,
        conversation_history: Optional[List["CopilotChatMessage"]] = None,
    ) -> "CopilotResponse":
        """
        Synthesizes a focused explanation of discrepancies between the deterministic
        core sequence calculation and external database annotations.
        """
        from app.ai import synthesize_research_copilot

        if not question or not question.strip():
            if analysis_result.discrepancies:
                summary_items = [
                    f"{d.field_name}: computed '{d.deterministic_value}' vs external '{d.evidence_value}' ({d.description})"
                    for d in analysis_result.discrepancies
                ]
                question = (
                    f"Explain the discrepancies between the deterministic sequence calculation and the external database "
                    f"evidence for {analysis_result.normalized_variant.hgvs_c} ({'; '.join(summary_items)}). "
                    f"Clarify why the deterministic calculation is authoritative."
                )
            else:
                question = (
                    f"Confirm concordance between the deterministic sequence calculation and external database evidence "
                    f"for {analysis_result.normalized_variant.hgvs_c}."
                )

        return await synthesize_research_copilot(
            question=question,
            evidence_packet=analysis_result,
            conversation_history=conversation_history or [],
            pubmed_evidence=None,
        )
