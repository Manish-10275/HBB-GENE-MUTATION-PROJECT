"""Comprehensive regression and unit tests for Groq AI Research Copilot and pipeline safety.

Covers:
1. Missing Groq key fallback
2. Invalid Groq model handling
3. Empty Groq response detection
4. Groq reasoning token budget exhaustion handling
5. Successful Groq response parsing
6. Groq API failure fallback
7. NCBI ClinVar unavailable graceful handling
8. NCBI PubMed unavailable graceful handling
9. Deterministic fallback zero-hallucination verification
10. Zero Gemini references in runtime settings and health endpoint
11. Deterministic p.Gln40Ter calculation (CAG -> TAG)
12. Evidence packet structured assembly
13. Live Groq integration (when configured)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.config import settings
from app.models import (
    AlignmentSummary,
    CodonChange,
    CopilotChatMessage,
    DetectedVariant,
    EvidencePacket,
    ClinVarRecord,
    PubMedRecord,
)
from app.ai import synthesize_research_copilot, _generate_offline_synthesis
from app.evidence import assemble_evidence_packet
from app.reference import reference_manager
from app.alignment import align_sequences
from app.variants import detect_variants


def create_sample_packet() -> EvidencePacket:
    """Creates a controlled EvidencePacket for testing."""
    return EvidencePacket(
        analysis_id="TEST-EXP-001",
        reference_accession="NM_000518.5",
        gene_symbol="HBB",
        summary={
            "reference_length_bp": 628,
            "sample_length_bp": 628,
            "sequence_identity_pct": 99.84,
            "detected_variants_count": 1,
        },
        variants=[
            DetectedVariant(
                id="var_1",
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
            )
        ],
        clinvar_records=[
            ClinVarRecord(
                id="15402",
                accession="VCV000015402",
                title="NM_000518.5(HBB):c.118C>T (p.Gln40Ter)",
                clinical_significance="Pathogenic",
                review_status="criteria provided, multiple submitters, no conflicts",
                conditions=["Beta-thalassemia HBB/LCRB", "beta Thalassemia"],
                url="https://www.ncbi.nlm.nih.gov/clinvar/variation/15402/",
            )
        ],
        pubmed_records=[
            PubMedRecord(
                pmid="1042764",
                title="Nonsense mutation in the beta-globin mRNA of a patient with beta0-thalassemia",
                authors=["Chang JC", "Kan YW"],
                journal="Proc Natl Acad Sci U S A",
                pub_date="1979",
                url="https://pubmed.ncbi.nlm.nih.gov/1042764/",
            )
        ],
        limitations=["Controlled test packet"],
    )


# --- 1. Missing Groq key ---
@pytest.mark.asyncio
async def test_regression_missing_groq_key_fallback():
    """Verifies that missing GROQ_API_KEY gracefully defaults to deterministic summary."""
    packet = create_sample_packet()
    with patch.object(settings, "GROQ_API_KEY", None):
        res = await synthesize_research_copilot(
            question="Why does CAG to TAG result in a stop codon?",
            evidence_packet=packet,
            conversation_history=[],
        )
        assert res.status == "no_key"
        assert "Deterministic Evidence Summary" in res.answer
        assert "c.118C>T" in res.answer
        assert "VCV000015402" in res.answer
        assert "1042764" in res.answer


# --- 2. Invalid Groq model ---
@pytest.mark.asyncio
async def test_regression_invalid_groq_model():
    """Verifies that an invalid or 404 Groq model falls back to deterministic summary."""
    packet = create_sample_packet()
    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("model_not_found: The model does not exist")

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a stop codon?",
                evidence_packet=packet,
                conversation_history=[],
            )
            assert res.status == "error"
            assert "Deterministic Evidence Summary" in res.answer
            assert "c.118C>T" in res.answer


# --- 3. Empty Groq response ---
@pytest.mark.asyncio
async def test_regression_empty_groq_response():
    """Verifies that an empty completion string triggers safe deterministic fallback."""
    packet = create_sample_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = ""
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a stop codon?",
                evidence_packet=packet,
                conversation_history=[],
            )
            assert res.status == "error"
            assert "Deterministic Evidence Summary" in res.answer


# --- 4. Groq reasoning consumes token budget ---
@pytest.mark.asyncio
async def test_regression_reasoning_tokens_consumed():
    """Verifies that reasoning models consuming the token budget with empty content fail safely."""
    packet = create_sample_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = ""
    mock_choice.message.reasoning = "Internal reasoning tokens consumed..."
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a stop codon?",
                evidence_packet=packet,
                conversation_history=[],
            )
            assert res.status == "error"
            assert "Deterministic Evidence Summary" in res.answer


# --- 5. Successful Groq response ---
@pytest.mark.asyncio
async def test_regression_successful_groq_response():
    """Verifies that valid Groq output is parsed with provenance and success status."""
    packet = create_sample_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = (
        "COMPUTED RESULT: The variant c.118C>T changes codon 40 from CAG (glutamine) to TAG (stop).\n"
        "DATABASE EVIDENCE: ClinVar record VCV000015402 classifies this variant as Pathogenic.\n"
        "LITERATURE EVIDENCE: Chang & Kan (PMID 1042764) confirmed premature translation termination.\n"
        "AI SYNTHESIS: The nonsense mutation causes truncated beta-globin synthesis."
    )
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a stop codon?",
                evidence_packet=packet,
                conversation_history=[],
            )
            assert res.status == "success"
            assert "COMPUTED RESULT" in res.answer
            assert "Deterministic Evidence Summary" not in res.answer
            assert "NCBI ClinVar" in res.evidence_used
            assert "NCBI PubMed" in res.evidence_used


# --- 6. Groq API failure ---
@pytest.mark.asyncio
async def test_regression_groq_api_failure():
    """Verifies that connection or network failure falls back safely."""
    packet = create_sample_packet()
    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.side_effect = ConnectionError("Connection refused by Groq endpoint")

            res = await synthesize_research_copilot(
                question="Why does CAG to TAG result in a stop codon?",
                evidence_packet=packet,
                conversation_history=[],
            )
            assert res.status == "error"
            assert "Deterministic Evidence Summary" in res.answer


# --- 7. NCBI ClinVar unavailable ---
@pytest.mark.asyncio
async def test_regression_ncbi_clinvar_unavailable():
    """Verifies that evidence packet handles empty ClinVar gracefully."""
    packet = create_sample_packet()
    packet.clinvar_records = []
    summary = _generate_offline_synthesis(packet, "Why does CAG to TAG result in a stop codon?")
    assert "No matching ClinVar records were retrieved" in summary.answer


# --- 8. PubMed unavailable ---
@pytest.mark.asyncio
async def test_regression_pubmed_unavailable():
    """Verifies that evidence packet handles empty PubMed literature gracefully."""
    packet = create_sample_packet()
    packet.pubmed_records = []
    summary = _generate_offline_synthesis(packet, "Why does CAG to TAG result in a stop codon?")
    assert "No matching PubMed literature was retrieved" in summary.answer


# --- 9. Deterministic fallback zero hallucination ---
def test_regression_deterministic_fallback_zero_hallucination():
    """Verifies that deterministic fallback strictly preserves unhallucinated packet facts."""
    packet = create_sample_packet()
    summary = _generate_offline_synthesis(packet, "Explain the consequences.")
    assert "c.118C>T" in summary.answer
    assert "p.Gln40Ter" in summary.answer
    assert "CAG [Gln] → TAG [Ter]" in summary.answer
    assert "VCV000015402" in summary.answer
    assert "1042764" in summary.answer
    assert summary.status == "no_key"


# --- 10. Zero Gemini references in runtime settings and health endpoint ---
def test_regression_zero_gemini_in_runtime_and_config():
    """Verifies that Gemini settings and aliases are absent from active config."""
    assert not hasattr(settings, "GEMINI_API_KEY")
    assert not hasattr(settings, "effective_gemini_api_key")
    assert settings.GROQ_MODEL == "openai/gpt-oss-120b"
    assert settings.GROQ_MAX_TOKENS >= 2000


# --- 11. Deterministic p.Gln40Ter calculation ---
def test_regression_deterministic_p_gln40ter_calculation():
    """
    CRITICAL BIOLOGICAL ACCURACY TEST:
    Verifies that c.118C>T is computed by the Python engine as:
    CAG -> TAG
    Gln -> Ter
    p.Gln40Ter (Nonsense)
    """
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
    assert v.functional_impact == "Nonsense"
    assert v.codon_change.codon_number == 40
    assert v.codon_change.ref_codon == "CAG"
    assert v.codon_change.sample_codon == "TAG"
    assert v.codon_change.ref_aa == "Gln"
    assert v.codon_change.sample_aa == "Ter"
    assert v.codon_change.is_stop_gain is True


# --- 12. Evidence packet structured assembly ---
def test_regression_evidence_packet_assembly():
    """Verifies assemble_evidence_packet creates bounded schema without LLM fabrication."""
    ref_data = reference_manager.get_reference("NM_000518.5")
    ref_seq = ref_data.sequence
    mut_seq = ref_seq[:167] + "T" + ref_seq[168:]
    summary, al_ref, al_query = align_sequences(ref_seq, mut_seq)
    variants = detect_variants(al_ref, al_query, ref_data)

    packet = assemble_evidence_packet(
        ref_data=ref_data,
        alignment_summary=summary,
        variants=variants,
        clinvar_records=[],
        pubmed_records=[],
    )

    assert packet.analysis_id.startswith("HBB-EXP-")
    assert packet.gene_symbol == "HBB"
    assert len(packet.variants) == 1
    assert packet.variants[0].hgvs_p == "p.Gln40Ter"
    assert isinstance(packet.limitations, list)


# --- 13. Live Groq integration (when configured) ---
@pytest.mark.asyncio
async def test_groq_ai_live_integration():
    """
    Live integration test: Runs only if a valid GROQ_API_KEY is configured.
    Skips gracefully if no key is present.
    Verifies that live Groq call succeeds, or falls back to deterministic synthesis
    if daily token limits are reached.
    """
    if not settings.GROQ_API_KEY:
        pytest.skip("GROQ_API_KEY is not configured in environment. Skipping live integration test.")

    packet = create_sample_packet()
    res = await synthesize_research_copilot(
        question="Why does the CAG to TAG change result in a premature termination codon?",
        evidence_packet=packet,
        conversation_history=[],
    )

    if res.fallback:
        # Rate limit or quota exhausted: verify deterministic fallback integrity
        assert res.provenance_label == "Deterministic synthesis"
        assert "CAG" in res.answer or "cag" in res.answer.lower()
        assert "TAG" in res.answer or "tag" in res.answer.lower()
    else:
        assert res.status == "success"
        assert len(res.answer) > 50
        assert "Deterministic Evidence Summary" not in res.answer
        ans_lower = res.answer.lower()
        assert "cag" in ans_lower or "glutamine" in ans_lower or "gln" in ans_lower
        assert "tag" in ans_lower or "stop" in ans_lower or "termination" in ans_lower
