"""Unit tests verifying discrepancy handling between deterministic core and external annotations."""

import pytest
from app.ai import (
    format_evidence_context_from_analysis,
    _generate_offline_synthesis,
)
from app.core.models import (
    CodonChange,
    ConsequenceResult,
    MolecularImpact,
    NormalizedVariant,
    VariantType,
)
from app.evidence.models import (
    ClinVarEvidenceResult,
    EvidenceDiscrepancy,
    EvidenceStatus,
)
from app.services.ai_service import AiCopilotService
from app.services.variant_service import VariantAnalysisResult


def create_analysis_result_with_discrepancy() -> VariantAnalysisResult:
    """Creates a VariantAnalysisResult containing an explicit discrepancy between core and ClinVar."""
    norm = NormalizedVariant(
        transcript_accession="NM_000518.5",
        c_position="118",
        variant_type=VariantType.SUBSTITUTION,
        ref_allele="C",
        alt_allele="T",
        hgvs_c="NM_000518.5:c.118C>T",
        region="Exon 2",
        mrna_position=168,
    )
    codon = CodonChange(
        codon_number=40,
        c_start=118,
        c_end=120,
        ref_codon="CAG",
        sample_codon="TAG",
        ref_aa="Gln",
        sample_aa="Ter",
        ref_aa_single="Q",
        sample_aa_single="*",
        consequence="Nonsense",
        is_stop_gain=True,
    )
    cons = ConsequenceResult(
        hgvs_p="p.Gln40Ter",
        molecular_impact=MolecularImpact.NONSENSE,
        codon_change=codon,
        confidence="Deterministic",
    )
    discrepancy = EvidenceDiscrepancy(
        field_name="protein_consequence",
        deterministic_value="p.Gln40Ter",
        evidence_value="p.Gln39Ter",
        description="ClinVar record employs legacy mature protein numbering (codon 39 without initiator Met1)",
    )
    clinvar_ev = ClinVarEvidenceResult(
        query="c.118C>T",
        status=EvidenceStatus.FOUND,
        records=[],
        discrepancies=[discrepancy],
    )
    return VariantAnalysisResult(
        input_query="c.118C>T",
        normalized_variant=norm,
        consequence=cons,
        clinvar_evidence=clinvar_ev,
        discrepancies=[discrepancy],
    )


def test_context_includes_discrepancy_and_authoritative_rule():
    """Verifies that format_evidence_context_from_analysis includes discrepancy details and authority rule."""
    res = create_analysis_result_with_discrepancy()
    ctx = format_evidence_context_from_analysis(res)

    assert "DISCREPANCIES DETECTED WITH EXTERNAL EVIDENCE" in ctx
    assert "protein_consequence" in ctx
    assert "Deterministic Engine = 'p.Gln40Ter'" in ctx
    assert "External Record = 'p.Gln39Ter'" in ctx
    assert "The deterministic sequence calculation is authoritative. Do NOT override it" in ctx


def test_offline_synthesis_highlights_discrepancy_without_override():
    """Verifies that deterministic offline synthesis presents the discrepancy without altering the consequence."""
    res = create_analysis_result_with_discrepancy()
    resp = _generate_offline_synthesis(res, "Explain the discrepancy between the engine and ClinVar", reason="no_key")

    assert "Discrepancies Between Engine and External Records" in resp.answer
    assert "p.Gln40Ter" in resp.answer
    assert "p.Gln39Ter" in resp.answer
    assert "Deterministic sequence engine remains authoritative" in resp.answer
    assert "Discrepancy Resolution" in resp.answer


@pytest.mark.asyncio
async def test_ai_copilot_service_explain_discrepancy(monkeypatch):
    """Verifies that AiCopilotService.explain_discrepancy generates an inquiry preserving the discrepancy."""
    monkeypatch.setattr("app.config.settings.GROQ_API_KEY", "")
    res = create_analysis_result_with_discrepancy()
    ai_service = AiCopilotService()
    resp = await ai_service.explain_discrepancy(res)

    assert resp.status == "no_key"
    assert resp.fallback is True
    assert "p.Gln40Ter" in resp.answer
    assert "p.Gln39Ter" in resp.answer


