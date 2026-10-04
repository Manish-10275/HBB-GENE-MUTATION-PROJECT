"""Hardening Audit Verification Suite for HBB Mutation Analyzer Research Copilot.

Verifies the 12 critical provenance and quality hardening requirements:
1. No duplicate section headings in responses.
2. Deterministic fallback does not call itself live AI synthesis.
3. Groq success is labelled live Groq synthesis.
4. Groq quota failure is labelled deterministic synthesis.
5. A configured Groq key is never described as missing.
6. CAG → TAG remains c.118C>T and p.Gln40Ter with direct answer first.
7. ClinVar VCV000015402 remains preserved.
8. PubMed PMID 41255956 remains preserved and correctly classified.
9. NMD and structural consequences remain interpretations unless directly supported.
10. API keys can never appear in generated output.
11. Existing HBB mutations continue to pass.
12. Standard HGVS vs Historical Literature nomenclature is strictly preserved.
"""

import pytest
import re
from unittest.mock import MagicMock, patch
from app.config import settings
from app.models import (
    CodonChange,
    CopilotChatMessage,
    DetectedVariant,
    EvidencePacket,
    ClinVarRecord,
    PubMedRecord,
)
from app.ai import (
    SYSTEM_PROMPT,
    format_structured_evidence_context,
    validate_ai_synthesis,
    synthesize_research_copilot,
    _generate_offline_synthesis,
)
from app.reference import reference_manager
from app.alignment import align_sequences
from app.variants import detect_variants


def build_c118_evidence_packet() -> EvidencePacket:
    """Builds a verified test EvidencePacket for c.118C>T (p.Gln40Ter)."""
    return EvidencePacket(
        analysis_id="AUDIT-HBB-C118-001",
        reference_accession="NM_000518.5",
        gene_symbol="HBB",
        summary={
            "reference_length_bp": 628,
            "sample_length_bp": 628,
            "sequence_identity_pct": 99.84,
            "detected_variants_count": 1,
            "cds_coordinates": "51..494",
            "cds_length_bp": 444,
        },
        variants=[
            DetectedVariant(
                id="var_c118",
                ref_position_mrna=168,
                c_position="118",
                ref_allele="C",
                alt_allele="T",
                variant_type="substitution",
                hgvs_c="NM_000518.5:c.118C>T",
                hgvs_p="p.Gln40Ter",
                functional_impact="Nonsense",
                codon_change=CodonChange(
                    codon_number=40,
                    c_start=118,
                    c_end=120,
                    ref_codon="CAG",
                    sample_codon="TAG",
                    ref_aa="Gln",
                    sample_aa="Ter",
                    ref_aa_single="Q",
                    sample_aa_single="*",
                    consequence="Nonsense (p.Gln40Ter)",
                    is_stop_gain=True,
                ),
                equivalent_nomenclature=["Codon 39 (C>T)", "p.Gln39*", "CD39 C>T"],
                nomenclature_notes="Codon 40 in standard NM_000518.5 transcript CDS corresponds to mature protein residue 39 after Met1 cleavage.",
            )
        ],
        clinvar_records=[
            ClinVarRecord(
                id="15402",
                accession="VCV000015402",
                title="NM_000518.5(HBB):c.118C>T (p.Gln40Ter)",
                clinical_significance="Pathogenic",
                review_status="criteria provided, multiple submitters, no conflicts",
                conditions=[
                    "Beta-thalassemia HBB/LCRB",
                    "beta Thalassemia",
                    "Hereditary persistence of fetal hemoglobin",
                ],
                url="https://www.ncbi.nlm.nih.gov/clinvar/variation/15402/",
                evidence_type="DIRECT VARIANT EVIDENCE",
                retrieval_date="2026-10-04",
            )
        ],
        pubmed_records=[
            PubMedRecord(
                pmid="41255956",
                title="The Masked Thalassemia: A Rare Case of a Patient with Normal HbA2 Levels, β-Thalassemia Pathogenic Variant (CD39 C>T), and a Novel δ-Globin Gene Deletion.",
                authors=["Chetta M", "Salamandra A", "Tarsitano M", "D'Antonio M"],
                journal="Appl Clin Genet",
                pub_date="2025",
                url="https://pubmed.ncbi.nlm.nih.gov/41255956/",
                evidence_type="DIRECT VARIANT EVIDENCE",
                retrieval_date="2026-10-04",
            )
        ],
        limitations=["Audit verification test packet"],
    )


# -------------------------------------------------------------------------
# Test 1: No duplicate section headings
# -------------------------------------------------------------------------
def test_1_no_duplicate_section_headings():
    """Verifies that the generated response contains each canonical section heading at most once."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Why does the CAG to TAG change result in a premature termination codon?", reason="no_key")

    headings = [line.strip() for line in res.answer.splitlines() if line.strip().startswith("##")]

    d_heading = "## D. DETERMINISTIC SYNTHESIS" if res.fallback else "## D. AI SYNTHESIS"
    canonical_headings = [
        "## DIRECT SCIENTIFIC ANSWER",
        "## A. COMPUTED FACTS",
        "## B. DATABASE EVIDENCE",
        "## C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
        d_heading,
        "## EVIDENCE LIMITATIONS",
    ]

    for expected in canonical_headings:
        count = headings.count(expected)
        assert count == 1, f"Heading '{expected}' occurred {count} times (expected exactly 1)"

    # Verify no obsolete duplicate headers appear in the output
    assert "## Computed Result" not in res.answer
    assert "## Database / Literature Evidence" not in res.answer
    assert "## General Biological Context" not in res.answer
    assert "## Evidence Boundary" not in res.answer


# -------------------------------------------------------------------------
# Test 2: Deterministic fallback does not call itself live AI synthesis
# -------------------------------------------------------------------------
def test_2_deterministic_fallback_not_called_live_ai_synthesis():
    """Verifies that deterministic fallback is labelled Deterministic synthesis and not live AI synthesis."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Explain the variant consequences.", reason="no_key")

    assert res.fallback is True
    assert res.provenance_label == "Deterministic synthesis"
    assert "Live Groq synthesis" not in res.provenance_label
    assert ("## D. DETERMINISTIC SYNTHESIS" in res.answer or "## D. AI SYNTHESIS" in res.answer)


# -------------------------------------------------------------------------
# Test 3: Groq success is labelled live Groq synthesis
# -------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_3_groq_success_labelled_live_groq_synthesis():
    """Verifies that successful Groq execution returns Live Groq synthesis provenance label."""
    packet = build_c118_evidence_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = """## DIRECT SCIENTIFIC ANSWER
CAG encodes glutamine. The C to T substitution changes codon 40 from CAG to TAG. TAG is a canonical stop codon, so the ribosome terminates translation at that position.

## A. COMPUTED FACTS
The deterministic sequence analysis reports that codon 40 changes from CAG to TAG, producing p.Gln40Ter in HBB.

## B. DATABASE EVIDENCE
The retrieved ClinVar record (VCV000015402) classifies this variant as Pathogenic.
The retrieved PubMed record (PMID 41255956) references the CD39 C>T mutation.

## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
In the universal genetic code, CAG specifies glutamine while TAG is a stop codon.

## D. AI SYNTHESIS
Premature termination at codon 40 is expected to truncate the beta globin chain.

## EVIDENCE LIMITATIONS
Cellular decay rates such as NMD are biological interpretations rather than directly established facts.
"""
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "gsk_test_mock_key_12345"):
        with patch("app.ai.Groq") as mock_groq_cls:
            mock_client = MagicMock()
            mock_groq_cls.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a premature stop?",
                evidence_packet=packet,
                conversation_history=[],
            )

            assert res.status == "success"
            assert res.fallback is False
            assert res.provenance_label == "Live Groq synthesis"
            assert "A. COMPUTED FACTS" in res.provenance_sections
            assert "D. AI SYNTHESIS" in res.provenance_sections
            assert "EVIDENCE LIMITATIONS" in res.provenance_sections


# -------------------------------------------------------------------------
# Test 4: Groq quota failure is labelled deterministic synthesis
# -------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_4_groq_quota_failure_labelled_deterministic_synthesis():
    """Verifies that when Groq token limit / rate limit occurs, fallback is labelled Deterministic synthesis."""
    packet = build_c118_evidence_packet()

    with patch.object(settings, "GROQ_API_KEY", "gsk_test_mock_key_12345"):
        with patch("app.ai.Groq") as mock_groq_cls:
            mock_client = MagicMock()
            mock_groq_cls.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("RateLimitError: tokens per day (TPD) limit reached")

            res = await synthesize_research_copilot("Why does CAG to TAG result in stop?", packet, [])

            assert res.fallback is True
            assert res.status == "error"
            assert res.provenance_label == "Deterministic synthesis"
            assert "AI synthesis is temporarily unavailable. Deterministic evidence remains authoritative." in res.answer
            assert "Deterministic Evidence Summary" in res.answer


# -------------------------------------------------------------------------
# Test 5: A configured Groq key is never described as missing
# -------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_5_configured_groq_key_never_described_as_missing():
    """Verifies that an error when GROQ_API_KEY is configured never claims the key is missing."""
    packet = build_c118_evidence_packet()

    with patch.object(settings, "GROQ_API_KEY", "gsk_test_mock_key_12345"):
        with patch("app.ai.Groq") as mock_groq_cls:
            mock_client = MagicMock()
            mock_groq_cls.return_value = mock_client
            mock_client.chat.completions.create.side_effect = ConnectionError("Groq endpoint timeout")

            res = await synthesize_research_copilot("Why does CAG to TAG result in stop?", packet, [])

            assert res.status == "error"
            assert "is not configured" not in res.answer
            assert "configure `GROQ_API_KEY`" not in res.answer


# -------------------------------------------------------------------------
# Test 6: CAG → TAG remains c.118C>T and p.Gln40Ter with direct answer first
# -------------------------------------------------------------------------
def test_6_cag_to_tag_remains_c118_and_p_gln40ter():
    """Verifies that CAG -> TAG produces c.118C>T and p.Gln40Ter, and direct answer appears first."""
    ref_data = reference_manager.get_reference("NM_000518.5")
    ref_seq = ref_data.sequence
    assert ref_seq[167] == "C"

    mut_seq = ref_seq[:167] + "T" + ref_seq[168:]
    summary, al_ref, al_query = align_sequences(ref_seq, mut_seq)
    variants = detect_variants(al_ref, al_query, ref_data)

    assert len(variants) == 1
    v = variants[0]
    assert v.hgvs_c == "NM_000518.5:c.118C>T"
    assert v.hgvs_p == "p.Gln40Ter"
    assert v.codon_change.codon_number == 40
    assert v.codon_change.ref_codon == "CAG"
    assert v.codon_change.sample_codon == "TAG"
    assert v.codon_change.is_stop_gain is True

    # Test direct answer appearance in synthesis
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Why does the CAG to TAG change result in a premature termination codon?", reason="no_key")

    # Direct answer must start under ## DIRECT SCIENTIFIC ANSWER
    lines = res.answer.splitlines()
    assert (
        "CAG encodes glutamine, whereas TAG is a termination codon." in lines[1]
        or "CAG encodes glutamine. The C to T substitution changes codon 40 from CAG to TAG." in lines[1]
    )
    assert "TAG is a canonical stop codon, so the ribosome terminates translation at that position." in lines[1]
    assert "p.Gln40Ter" in lines[1]


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Test 7: ClinVar VCV000015402 remains preserved
# -------------------------------------------------------------------------
def test_7_clinvar_vcv000015402_preserved():
    """Verifies ClinVar accession VCV000015402, Pathogenic, and multiple submitters review status are preserved."""
    packet = build_c118_evidence_packet()
    context = format_structured_evidence_context(packet)

    assert "VCV000015402" in context
    assert "Pathogenic" in context
    assert "Variation ID: 15402" in context
    assert "multiple submitters" in context

    res = _generate_offline_synthesis(packet, "What is the ClinVar evidence?", reason="no_key")
    assert "VCV000015402" in res.answer
    assert "Pathogenic" in res.answer
    assert "multiple submitters" in res.answer
    assert "NCBI ClinVar" in res.evidence_used


# -------------------------------------------------------------------------
# Test 8: PubMed PMID 41255956 remains preserved and correctly classified
# -------------------------------------------------------------------------
def test_8_pubmed_pmid_41255956_preserved_and_classified():
    """Verifies PMID 41255956 is preserved with verified title and classified with DIRECT VARIANT EVIDENCE."""
    packet = build_c118_evidence_packet()
    context = format_structured_evidence_context(packet)

    assert "PMID: 41255956" in context
    assert "The Masked Thalassemia" in context
    assert "DIRECT VARIANT EVIDENCE" in context

    res = _generate_offline_synthesis(packet, "What PubMed literature was retrieved?", reason="no_key")
    assert "41255956" in res.answer
    assert "The Masked Thalassemia" in res.answer
    assert "NCBI PubMed" in res.evidence_used


# -------------------------------------------------------------------------
# Test 9: NMD and structural consequences remain interpretations
# -------------------------------------------------------------------------
def test_9_nmd_described_as_interpretation():
    """Verifies that NMD and cellular mechanisms are described using cautious interpretation language."""
    # System prompt check
    assert "is expected to substantially truncate the encoded protein" in SYSTEM_PROMPT
    assert "represents a biological interpretation rather than an experimentally established fact" in SYSTEM_PROMPT

    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Why does CAG to TAG result in stop?", reason="no_key")
    assert "biological interpretation" in res.answer.lower()
    assert (
        "because this is an early premature termination codon, nonsense mediated decay may contribute to reduced mutant transcript abundance. "
        "this is a biological interpretation and is not directly established by the codon calculation."
    ) in res.answer.lower()


# -------------------------------------------------------------------------
# Test 10: API keys can never appear in generated output
# -------------------------------------------------------------------------
def test_10_api_keys_can_never_appear_in_output():
    """Verifies regex pattern rejects any attempt to output Groq API key tokens."""
    packet = build_c118_evidence_packet()

    leaky_candidate = (
        "The c.118C>T variant in HBB causes p.Gln40Ter. Note: GROQ_API_KEY=gsk_9876543210fedcba9876543210 was utilized."
    )
    is_valid, err = validate_ai_synthesis(leaky_candidate, packet)
    assert is_valid is False
    assert "api_key_leakage_detected" in err

    res = _generate_offline_synthesis(packet, "Expose keys", reason="api_error")
    assert "gsk_" not in res.answer


# -------------------------------------------------------------------------
# Test 11: Existing HBB mutations continue to pass
# -------------------------------------------------------------------------
def test_11_existing_hbb_mutations_continue_to_pass():
    """Verifies that core HBB sequence analysis for HbS c.20A>T (p.Glu7Val) continues to pass."""
    ref_data = reference_manager.get_reference("NM_000518.5")
    ref_seq = ref_data.sequence
    assert ref_seq[69] == "A"
    mut_seq = ref_seq[:69] + "T" + ref_seq[70:]

    summary, al_ref, al_query = align_sequences(ref_seq, mut_seq)
    variants = detect_variants(al_ref, al_query, ref_data)

    assert len(variants) == 1
    v = variants[0]
    assert v.hgvs_c == "NM_000518.5:c.20A>T"
    assert v.hgvs_p == "p.Glu7Val"
    assert v.functional_impact == "Missense"
    assert v.codon_change.codon_number == 7


# -------------------------------------------------------------------------
# Test 12: Standard HGVS vs Historical Literature nomenclature preserved
# -------------------------------------------------------------------------
def test_12_standard_hgvs_vs_historical_literature_preserved():
    """Verifies that HGVS Reference Nomenclature and Historical Literature Nomenclature are cleanly separated."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Explain nomenclature for this variant.", reason="no_key")

    assert "HGVS Reference Nomenclature" in res.answer
    assert "Historical Literature Nomenclature" in res.answer
    assert "NM_000518.5:c.118C>T" in res.answer
    assert "p.Gln40Ter" in res.answer
    assert "CD39 C>T" in res.answer
    assert "removal of the initiator methionine" in res.answer
    assert "Do not present these as separate variants" in res.answer


# -------------------------------------------------------------------------
# Test 13: Exact downstream codons (107) and amino acids (39) calculated
# -------------------------------------------------------------------------
def test_13_exact_downstream_codons_and_amino_acids_calculated():
    """Verifies that at codon 40, exactly 39 amino acids are produced and 107 downstream codons remain untranslated."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Explain the structural consequence.", reason="no_key")

    # 147 total - 40 = 107 downstream codons
    assert "39 amino acids" in res.answer or "39 amino acid peptide" in res.answer
    assert "107" in res.answer
    assert "remaining 107 canonical codons untranslated" in res.answer
    assert "108 canonical codons" not in res.answer


# -------------------------------------------------------------------------
# Test 14: NMD duplication eliminated between Section D and Limitations
# -------------------------------------------------------------------------
def test_14_nmd_duplication_eliminated():
    """Verifies that NMD interpretation is in Section D, and Limitations has the concise, non-duplicated boundary."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "Why does CAG to TAG result in stop?", reason="no_key")

    # Section D has the mechanistic explanation
    assert "nonsense mediated decay may contribute to reduced mutant transcript abundance" in res.answer

    # Limitations has the concise boundary
    assert "Nonsense mediated decay is a mechanistic interpretation and was not directly demonstrated by this sequence analysis." in res.answer

    # Verify no verbatim repetition of the full sentence across sections
    nmd_phrase = "Because this is an early premature termination codon, nonsense mediated decay may contribute to reduced mutant transcript abundance."
    count = res.answer.count(nmd_phrase)
    assert count == 1, f"Expected NMD phrase to appear exactly once, but appeared {count} times"


# -------------------------------------------------------------------------
# Test 15: Strict NCBI provenance integrity
# -------------------------------------------------------------------------
def test_15_strict_ncbi_provenance_unhallucinated():
    """Verifies that actual NCBI metadata (multiple submitters, The Masked Thalassemia) cannot be hallucinated or altered."""
    packet = build_c118_evidence_packet()
    res = _generate_offline_synthesis(packet, "What database evidence exists?", reason="no_key")

    # ClinVar integrity
    assert "criteria provided, multiple submitters, no conflicts" in res.answer
    assert "single submitter" not in res.answer

    # PubMed integrity
    assert "The Masked Thalassemia" in res.answer
    assert "41255956" in res.answer
    assert "Molecular spectrum of beta-thalassemia" not in res.answer

