"""Unit tests verifying AI authority boundary and non-override constraints."""

import pytest
from app.ai import (
    SYSTEM_PROMPT,
    format_evidence_context_from_analysis,
    validate_ai_synthesis,
)
from app.core.models import (
    CodonChange,
    ConsequenceResult,
    MolecularImpact,
    NormalizedVariant,
    VariantType,
)
from app.services.variant_service import VariantAnalysisResult


def create_mock_analysis_result() -> VariantAnalysisResult:
    """Creates a deterministic VariantAnalysisResult for c.118C>T (p.Gln40Ter)."""
    norm = NormalizedVariant(
        transcript_accession="NM_000518.5",
        c_position="118",
        variant_type=VariantType.SUBSTITUTION,
        ref_allele="C",
        alt_allele="T",
        hgvs_c="NM_000518.5:c.118C>T",
        region="Exon 2",
        mrna_position=168,
        equivalent_nomenclature=["CD39 C>T", "Q39*"],
        nomenclature_notes="Numbered from codon 39 in mature peptide",
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
    return VariantAnalysisResult(
        input_query="c.118C>T",
        normalized_variant=norm,
        consequence=cons,
    )


def test_system_prompt_defines_deterministic_engine_as_authoritative():
    """Verifies that the system prompt explicitly forbids overriding the deterministic core."""
    assert "DETERMINISTIC COMPUTATION IS AUTHORITATIVE" in SYSTEM_PROMPT
    assert "The AI copilot must NEVER alter, override, recalculate, or contradict these deterministic findings" in SYSTEM_PROMPT
    assert "the deterministic calculation remains authoritative" in SYSTEM_PROMPT


def test_format_evidence_context_preserves_deterministic_consequence():
    """Verifies that the formatted prompt context contains exact deterministic facts."""
    res = create_mock_analysis_result()
    ctx = format_evidence_context_from_analysis(res)

    assert "COMPUTED RESULT (DETERMINISTIC BIOINFORMATICS)" in ctx
    assert "NM_000518.5:c.118C>T" in ctx
    assert "p.Gln40Ter" in ctx
    assert "Molecular Consequence: Nonsense" in ctx
    assert "Codon Number: 40 (of 147 canonical codons)" in ctx
    assert "CAG" in ctx
    assert "TAG" in ctx
    assert "Premature Termination (Stop-gain): Yes (Nonsense)" in ctx


def test_validation_rejects_ai_claiming_external_evidence_overrides_engine():
    """Verifies that validate_ai_synthesis rejects text attempting to override the deterministic engine."""
    res = create_mock_analysis_result()
    overriding_text = (
        "## DIRECT SCIENTIFIC ANSWER\n"
        "We note that the deterministic engine is incorrect and ClinVar replaces the computed consequence with missense."
    )
    is_valid, err = validate_ai_synthesis(overriding_text, res)
    assert not is_valid
    assert err is not None
    assert "authority_violation" in err


def test_validation_enforces_consequence_consistency():
    """Verifies that validate_ai_synthesis rejects responses that fail to acknowledge nonsense/stop-gain."""
    res = create_mock_analysis_result()
    inconsistent_text = (
        "## DIRECT SCIENTIFIC ANSWER\n"
        "This variant NM_000518.5:c.118C>T in HBB causes a benign silent substitution with no impact on translation."
    )
    is_valid, err = validate_ai_synthesis(inconsistent_text, res)
    assert not is_valid
    assert err is not None
    assert "consequence_inconsistent" in err
