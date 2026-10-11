"""Unit tests verifying canonical provenance labeling and section structure."""

import pytest
from app.ai import normalize_canonical_sections, _generate_offline_synthesis
from app.core.models import (
    CodonChange,
    ConsequenceResult,
    MolecularImpact,
    NormalizedVariant,
    VariantType,
)
from app.services.variant_service import VariantAnalysisResult


def test_normalize_canonical_sections_enforces_order_and_deduplication():
    """Verifies that normalize_canonical_sections orders headers correctly and merges duplicates."""
    raw_text = (
        "## B. DATABASE EVIDENCE\n"
        "ClinVar reports pathogenic.\n\n"
        "## DIRECT SCIENTIFIC ANSWER\n"
        "The variant is nonsense.\n\n"
        "## A. COMPUTED FACTS\n"
        "Codon 40 CAG to TAG.\n\n"
        "## B. DATABASE EVIDENCE\n"
        "PubMed paper retrieved.\n\n"
        "## EVIDENCE LIMITATIONS\n"
        "In silico only.\n\n"
        "## C. ESTABLISHED BIOLOGICAL KNOWLEDGE\n"
        "Stop codons terminate translation.\n\n"
        "## D. DETERMINISTIC SYNTHESIS\n"
        "Premature termination leads to truncation."
    )

    normalized = normalize_canonical_sections(raw_text)

    # Check that headings appear in canonical order
    idx_direct = normalized.find("## DIRECT SCIENTIFIC ANSWER")
    idx_comp = normalized.find("## A. COMPUTED FACTS")
    idx_db = normalized.find("## B. DATABASE EVIDENCE")
    idx_bio = normalized.find("## C. ESTABLISHED BIOLOGICAL KNOWLEDGE")
    idx_synth = normalized.find("## D. DETERMINISTIC SYNTHESIS")
    idx_lim = normalized.find("## EVIDENCE LIMITATIONS")

    assert idx_direct != -1
    assert idx_comp != -1
    assert idx_db != -1
    assert idx_bio != -1
    assert idx_synth != -1
    assert idx_lim != -1

    assert idx_direct < idx_comp < idx_db < idx_bio < idx_synth < idx_lim

    # Verify no duplicate headers
    assert normalized.count("## B. DATABASE EVIDENCE") == 1
    assert normalized.count("## DIRECT SCIENTIFIC ANSWER") == 1


def test_offline_response_provenance_metadata():
    """Verifies that CopilotResponse emitted by fallback contains rigorous provenance metadata."""
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
    cons = ConsequenceResult(
        hgvs_p="p.Gln40Ter",
        molecular_impact=MolecularImpact.NONSENSE,
        confidence="Deterministic",
    )
    res = VariantAnalysisResult(
        input_query="c.118C>T",
        normalized_variant=norm,
        consequence=cons,
    )

    resp = _generate_offline_synthesis(res, "Why does this variant cause thalassemia?", reason="no_key")

    assert resp.fallback is True
    assert resp.status == "no_key"
    assert resp.provenance_label == "Deterministic synthesis"
    assert "DIRECT SCIENTIFIC ANSWER" in resp.provenance_sections
    assert "A. COMPUTED FACTS" in resp.provenance_sections
    assert "B. DATABASE EVIDENCE" in resp.provenance_sections
    assert "C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in resp.provenance_sections
    assert "D. DETERMINISTIC SYNTHESIS" in resp.provenance_sections
    assert "EVIDENCE LIMITATIONS" in resp.provenance_sections
