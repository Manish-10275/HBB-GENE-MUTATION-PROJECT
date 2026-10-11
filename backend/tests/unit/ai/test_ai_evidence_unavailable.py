"""Unit tests verifying explicit declaration of unavailable evidence and zero-hallucination guards."""

import pytest
from app.ai import (
    SYSTEM_PROMPT,
    format_evidence_context_from_analysis,
    validate_ai_synthesis,
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
    EvidenceStatus,
    PubMedEvidenceResult,
)
from app.services.variant_service import VariantAnalysisResult


def create_mock_analysis_result_no_evidence() -> VariantAnalysisResult:
    """Creates a VariantAnalysisResult with unavailable ClinVar evidence."""
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
    clinvar_unavailable = ClinVarEvidenceResult(
        query="c.118C>T",
        status=EvidenceStatus.OFFLINE_DATA_UNAVAILABLE,
        records=[],
    )
    return VariantAnalysisResult(
        input_query="c.118C>T",
        normalized_variant=norm,
        consequence=cons,
        clinvar_evidence=clinvar_unavailable,
    )


def test_context_explicitly_declares_clinvar_unavailable():
    """Verifies that format_evidence_context_from_analysis declares ClinVar unavailable."""
    res = create_mock_analysis_result_no_evidence()
    ctx = format_evidence_context_from_analysis(res, pubmed_evidence=None)

    assert "External ClinVar database evidence was unavailable for this query" in ctx
    assert "No matching ClinVar records retrieved" in ctx
    assert "No external ClinVar claims may be made" in ctx


def test_context_explicitly_declares_pubmed_unavailable():
    """Verifies that format_evidence_context_from_analysis declares PubMed unavailable."""
    res = create_mock_analysis_result_no_evidence()
    ctx = format_evidence_context_from_analysis(res, pubmed_evidence=None)

    assert "External PubMed scientific literature was unavailable for this query" in ctx
    assert "No matching PubMed literature retrieved" in ctx
    assert "No external literature claims or PMIDs may be cited" in ctx


def test_validation_rejects_hallucinated_clinvar_accession():
    """Verifies that validate_ai_synthesis rejects fabricated ClinVar accession when evidence was unavailable."""
    res = create_mock_analysis_result_no_evidence()
    hallucinated_text = (
        "## DIRECT SCIENTIFIC ANSWER\n"
        "NM_000518.5:c.118C>T (p.Gln40Ter) in HBB is a nonsense stop-gain variant. "
        "According to ClinVar record VCV000999999, it is pathogenic for beta-thalassemia."
    )
    is_valid, err = validate_ai_synthesis(hallucinated_text, res, pubmed_evidence=None)
    assert not is_valid
    assert err is not None
    assert "hallucinated_clinvar" in err


def test_validation_rejects_hallucinated_pmid():
    """Verifies that validate_ai_synthesis rejects any cited PMID when no literature evidence was supplied."""
    res = create_mock_analysis_result_no_evidence()
    hallucinated_text = (
        "## DIRECT SCIENTIFIC ANSWER\n"
        "NM_000518.5:c.118C>T (p.Gln40Ter) in HBB is a nonsense stop-gain mutation. "
        "A study published in PMID: 99887766 reported the functional impact of this mutation."
    )
    is_valid, err = validate_ai_synthesis(hallucinated_text, res, pubmed_evidence=None)
    assert not is_valid
    assert err is not None
    assert "hallucinated_pmid" in err


def test_offline_synthesis_declares_unavailable_databases():
    """Verifies that deterministic offline synthesis states unavailable evidence clearly in Section B and Limitations."""
    res = create_mock_analysis_result_no_evidence()
    resp = _generate_offline_synthesis(res, "What database evidence exists for this mutation?", reason="no_key")

    assert "No matching ClinVar records were retrieved" in resp.answer
    assert "No matching PubMed literature were retrieved" in resp.answer or "No matching PubMed literature was retrieved" in resp.answer
    assert "EVIDENCE LIMITATIONS" in resp.provenance_sections
