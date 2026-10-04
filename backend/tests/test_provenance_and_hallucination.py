"""Tests specifically for provenance boundaries, hallucination resistance, and evidence layering."""

import pytest
from unittest.mock import MagicMock, patch
from app.config import settings
from app.models import (
    CodonChange,
    DetectedVariant,
    EvidencePacket,
    ClinVarRecord,
    PubMedRecord,
)
from app.ai import (
    synthesize_research_copilot,
    _generate_offline_synthesis,
    format_structured_evidence_context,
    validate_ai_synthesis,
    SYSTEM_PROMPT,
)
from app.pubmed import classify_pubmed_relevance, classify_pubmed_evidence
from app.variants import get_equivalent_nomenclature


def create_c118_test_packet() -> EvidencePacket:
    """Creates a controlled EvidencePacket for the c.118C>T validation variant."""
    return EvidencePacket(
        analysis_id="TEST-PROV-001",
        reference_accession="NM_000518.5",
        gene_symbol="HBB",
        summary={
            "reference_length_bp": 628,
            "sample_length_bp": 628,
            "sequence_identity_pct": 99.84,
            "detected_variants_count": 1,
            "cds_coordinates": "51..494",
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
                conditions=["Beta thalassemia major", "Beta-thalassemia"],
                url="https://www.ncbi.nlm.nih.gov/clinvar/variation/15402/",
                is_exact_match=True,
                evidence_type="Exact Variant Evidence",
            )
        ],
        pubmed_records=[
            PubMedRecord(
                pmid="41255956",
                title="The Masked Thalassemia: A Rare Case of a Patient with Normal HbA2 Levels, β-Thalassemia Pathogenic Variant (CD39 C>T), and a Novel δ-Globin Gene Deletion.",
                authors=["Chetta M", "Salamandra A"],
                journal="Appl Clin Genet",
                pub_date="2025",
                url="https://pubmed.ncbi.nlm.nih.gov/41255956/",
                abstract_snippet=None,
                source="NCBI PubMed",
                is_exact_match=True,
                evidence_type="Exact Variant Evidence",
            ),
            PubMedRecord(
                pmid="34060411",
                title="Analysis of a Novel Mexican Variant of the HBB Gene Associated with β-Thalassemia Using Bioinformatic Tools.",
                authors=["Martínez Villegas O"],
                journal="Hemoglobin",
                pub_date="2021",
                url="https://pubmed.ncbi.nlm.nih.gov/34060411/",
                abstract_snippet=None,
                source="NCBI PubMed",
                is_exact_match=False,
                evidence_type="Related HBB Evidence",
            ),
        ],
        limitations=["In silico pairwise alignment against reference transcript NM_000518.5."],
    )


# 1. AI receives deterministic evidence
def test_1_ai_receives_deterministic_evidence():
    """Verifies that format_structured_evidence_context supplies deterministic findings unambiguously."""
    packet = create_c118_test_packet()
    ctx = format_structured_evidence_context(packet)

    assert "COMPUTED RESULT (DETERMINISTIC BIOINFORMATICS)" in ctx
    assert "NM_000518.5:c.118C>T" in ctx
    assert "p.Gln40Ter" in ctx
    assert "Codon Number: 40" in ctx
    assert "CAG" in ctx
    assert "TAG" in ctx
    assert "Premature Termination (Stop-gain): Yes (Nonsense)" in ctx


# 2. AI receives ClinVar evidence
def test_2_ai_receives_clinvar_evidence():
    """Verifies that ClinVar records with exact accession and significance are passed in."""
    packet = create_c118_test_packet()
    ctx = format_structured_evidence_context(packet)

    assert "NCBI CLINVAR DATABASE EVIDENCE" in ctx
    assert "VCV000015402" in ctx
    assert "Variation ID: 15402" in ctx
    assert "Clinical Significance (Database Record): Pathogenic" in ctx
    assert "Beta thalassemia major" in ctx
    assert "Exact Variant Evidence" in ctx


# 3. AI receives PubMed evidence
def test_3_ai_receives_pubmed_evidence():
    """Verifies that PubMed citations are formatted with PMID, title, and relevance."""
    packet = create_c118_test_packet()
    ctx = format_structured_evidence_context(packet)

    assert "NCBI PUBMED SCIENTIFIC LITERATURE EVIDENCE" in ctx
    assert "PMID: 41255956" in ctx
    assert "CD39 C>T" in ctx
    assert "Relevance Level: Exact Variant Evidence" in ctx
    assert "PMID: 34060411" in ctx
    assert "Relevance Level: Related HBB Evidence" in ctx


# 4. System prompt strictly forbids fabricating ClinVar records or accessions
def test_4_prompt_forbids_fabricating_clinvar():
    """Verifies that system prompt explicitly bars fabricating ClinVar records or accessions."""
    assert "Never invent evidence." in SYSTEM_PROMPT
    assert "Never fabricate ClinVar records." in SYSTEM_PROMPT
    assert "Never attribute a statement to ClinVar unless that statement exists in the supplied ClinVar record." in SYSTEM_PROMPT


# 5. System prompt strictly forbids fabricating PMIDs
def test_5_prompt_forbids_fabricating_pmids():
    """Verifies that system prompt explicitly bars fabricating PubMed citations and PMIDs."""
    assert "Never fabricate PubMed citations." in SYSTEM_PROMPT
    assert "Never attribute a statement to PubMed unless the supplied PubMed metadata or abstract supports it." in SYSTEM_PROMPT


# 6. AI does not label general knowledge as ClinVar evidence
def test_6_prompt_separates_general_knowledge_from_clinvar():
    """Verifies system prompt bars presenting general biological knowledge as ClinVar evidence."""
    assert "Never present general biological knowledge as though it came from the retrieved database evidence." in SYSTEM_PROMPT
    assert "When using established general biological knowledge, label it explicitly as GENERAL BIOLOGICAL CONTEXT." in SYSTEM_PROMPT


# 7. AI does not label general knowledge as PubMed evidence
def test_7_prompt_separates_general_knowledge_from_pubmed():
    """Verifies system prompt bars presenting general biological knowledge as PubMed evidence."""
    assert "Summarize individual papers strictly to the extent justified by the supplied title, metadata, or abstract snippet." in SYSTEM_PROMPT
    assert "Never claim that a paper proves a specific cellular mechanism unless the supplied text contains it." in SYSTEM_PROMPT


# 8. AI clearly distinguishes computed result from database evidence
def test_8_prompt_distinguishes_computed_from_database():
    """Verifies canonical sections are defined in system prompt instructions."""
    assert "A. COMPUTED FACTS" in SYSTEM_PROMPT
    assert "B. DATABASE EVIDENCE" in SYSTEM_PROMPT
    assert "C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in SYSTEM_PROMPT
    assert "## A. COMPUTED FACTS" in SYSTEM_PROMPT
    assert "## B. DATABASE EVIDENCE" in SYSTEM_PROMPT
    assert "## C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in SYSTEM_PROMPT
    assert "## D. AI SYNTHESIS" in SYSTEM_PROMPT
    assert "## EVIDENCE LIMITATIONS" in SYSTEM_PROMPT


# 9. AI identifies missing evidence when necessary
def test_9_ai_identifies_missing_evidence():
    """Verifies that offline synthesis and system prompt explicitly state when evidence is absent."""
    packet = create_c118_test_packet()
    packet.clinvar_records = []
    packet.pubmed_records = []

    res = _generate_offline_synthesis(packet, "What is the clinical classification?", reason="no_key")
    assert "No matching ClinVar records were retrieved." in res.answer
    assert "No matching PubMed literature was retrieved." in res.answer
    assert "EVIDENCE LIMITATIONS" in res.provenance_sections
    assert "That detail is not directly established by the supplied evidence." in SYSTEM_PROMPT


# 10. Deterministic fallback remains functional and populates provenance sections
def test_10_deterministic_fallback_populates_provenance():
    """Verifies that _generate_offline_synthesis outputs all canonical provenance sections."""
    packet = create_c118_test_packet()
    res = _generate_offline_synthesis(packet, "Why does CAG to TAG result in stop?", reason="no_key")

    assert res.status == "no_key"
    assert res.fallback is True
    assert "## DIRECT SCIENTIFIC ANSWER" in res.answer
    assert "## A. COMPUTED FACTS" in res.answer
    assert "## B. DATABASE EVIDENCE" in res.answer
    assert "## C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in res.answer
    assert ("## D. DETERMINISTIC SYNTHESIS" in res.answer or "## D. AI SYNTHESIS" in res.answer)
    assert "## EVIDENCE LIMITATIONS" in res.answer
    assert "A. COMPUTED FACTS" in res.provenance_sections
    assert "B. DATABASE EVIDENCE" in res.provenance_sections
    assert "C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in res.provenance_sections
    assert ("D. DETERMINISTIC SYNTHESIS" in res.provenance_sections or "D. AI SYNTHESIS" in res.provenance_sections)
    assert "EVIDENCE LIMITATIONS" in res.provenance_sections


# 11. Successful Groq synthesis parses provenance sections
@pytest.mark.asyncio
async def test_11_successful_groq_synthesis_parses_provenance():
    """Verifies that valid Groq output with provenance sections is parsed and populated."""
    packet = create_c118_test_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = """## DIRECT SCIENTIFIC ANSWER
CAG encodes glutamine and TAG is a stop codon; changing codon 40 from sense to stop terminates translation prematurely.

## A. COMPUTED FACTS
The deterministic sequence analysis reports that codon 40 changes from CAG to TAG, producing p.Gln40Ter (nonsense mutation).

## B. DATABASE EVIDENCE
The retrieved ClinVar record (VCV000015402) classifies this variant as Pathogenic.
The retrieved PubMed record (PMID 41255956) references the CD39 C>T mutation.

## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
In the standard genetic code, CAG specifies glutamine while TAG is a stop codon. Ribosomes encountering TAG terminate translation.

## D. AI SYNTHESIS
Because the termination signal is introduced at codon 40 instead of the canonical open reading frame terminus, translation produces a truncated polypeptide.

## EVIDENCE LIMITATIONS
Downstream cellular decay pathways such as NMD are not directly reported in the supplied record.
"""
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does the CAG to TAG change result in a premature termination codon?",
                evidence_packet=packet,
                conversation_history=[],
            )

            assert res.status == "success"
            assert res.fallback is False
            assert "A. COMPUTED FACTS" in res.provenance_sections
            assert "B. DATABASE EVIDENCE" in res.provenance_sections
            assert "C. ESTABLISHED BIOLOGICAL KNOWLEDGE" in res.provenance_sections
            assert "D. AI SYNTHESIS" in res.provenance_sections
            assert "EVIDENCE LIMITATIONS" in res.provenance_sections
            assert "NCBI ClinVar" in res.evidence_used
            assert "NCBI PubMed" in res.evidence_used


# 12. Regression test for the validation question
@pytest.mark.asyncio
async def test_12_regression_cag_to_tag_premature_termination():
    """
    CRITICAL REGRESSION TEST:
    Question: 'Why does the CAG to TAG change result in a premature termination codon?'
    Must verify:
    - CAG is present
    - TAG is present
    - p.Gln40Ter is present
    - Explanation of translation termination
    - Does not falsely attribute cellular mechanisms to a PubMed paper whose supplied title doesn't support it
    """
    packet = create_c118_test_packet()
    mock_choice = MagicMock()
    mock_choice.message.content = """## Computed Result
The deterministic analysis computes that cDNA position 118 has a C>T substitution in codon 40 (CAG to TAG), resulting in the nonsense protein consequence p.Gln40Ter.

## Database / Literature Evidence
The retrieved ClinVar record VCV000015402 reports a Pathogenic classification for p.Gln40Ter in beta thalassemia.
The supplied PubMed records include PMID 41255956 (Chetta et al., 2025) which discusses CD39 C>T. The paper title does not describe specific ribosome kinetics.

## General Biological Context
In the universal genetic code, CAG codes for glutamine. TAG is one of three termination codons. When a ribosome encounters TAG, release factors catalyze translation termination.

## AI Synthesis
Because the termination signal occurs at codon 40 instead of normal codon 147, the variant produces premature termination of the polypeptide chain.

## Evidence Boundary
Detailed biochemical kinetics or nonsense-mediated decay rates are not directly established by the supplied evidence packet.
"""
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="Why does the CAG to TAG change result in a premature termination codon?",
                evidence_packet=packet,
                conversation_history=[],
            )

            assert "CAG" in res.answer
            assert "TAG" in res.answer
            assert "p.Gln40Ter" in res.answer
            assert "termination" in res.answer.lower()
            # Verify no false claim that the PubMed paper proved a mechanism not in its title
            assert "not directly established by the supplied evidence" in res.answer or "Evidence Boundary" in res.answer


# 13. PubMed relevance classification helper
def test_13_pubmed_relevance_classification():
    """Verifies that classify_pubmed_evidence classifies into 3 distinct levels."""
    is_exact, ev_type = classify_pubmed_relevance(
        "A case of beta-thalassemia with CD39 C>T mutation",
        "c.118C>T"
    )
    assert is_exact is True
    assert ev_type == "DIRECT VARIANT EVIDENCE"

    is_exact_rel, ev_type_rel = classify_pubmed_relevance(
        "General review of hemoglobinopathies in Western Mexico",
        "c.118C>T"
    )
    assert is_exact_rel is False
    assert ev_type_rel == "RELATED GENE OR DISEASE EVIDENCE"

    is_exact_ctx, ev_type_ctx = classify_pubmed_relevance(
        "Next generation sequencing protocols in clinical diagnostics",
        "c.118C>T"
    )
    assert is_exact_ctx is False
    assert ev_type_ctx == "CONTEXTUAL EVIDENCE"


# 14. Post-generation validation rejects hallucinated PMIDs
@pytest.mark.asyncio
async def test_14_validation_rejects_hallucinated_pmid():
    """Verifies that citing an unsupplied PMID fails validation and triggers deterministic fallback."""
    packet = create_c118_test_packet()
    mock_choice = MagicMock()
    # Model fabricates PMID 99999999 which is not in packet.pubmed_records
    mock_choice.message.content = """## Computed Result
The deterministic sequence analysis reports HBB c.118C>T (p.Gln40Ter) premature stop codon.

## Database / Literature Evidence
ClinVar VCV000015402 is Pathogenic.
Fake paper (PMID 99999999) proved this variant in 2026.

## AI Synthesis
CAG to TAG creates a premature termination codon terminating translation.
"""
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

            # Must reject hallucinated PMID and fall back safely to deterministic synthesis
            assert res.fallback is True
            assert "PMID 99999999" not in res.answer
            assert res.provenance_label == "Deterministic synthesis"


# 15. Post-generation validation rejects contradictory ClinVar claims
@pytest.mark.asyncio
async def test_15_validation_rejects_contradictory_clinvar_classification():
    """Verifies that falsely claiming a Pathogenic variant is benign fails validation."""
    packet = create_c118_test_packet()
    mock_choice = MagicMock()
    # Model falsely claims variant is benign despite ClinVar Pathogenic record
    mock_choice.message.content = """## Computed Result
The deterministic sequence analysis reports HBB c.118C>T (p.Gln40Ter) nonsense mutation.

## Database / Literature Evidence
ClinVar records indicate this variant is considered benign in all populations.

## AI Synthesis
CAG to TAG stop codon results in premature translation termination.
"""
    mock_choice.message.reasoning = None
    mock_response = MagicMock(choices=[mock_choice])

    with patch.object(settings, "GROQ_API_KEY", "mock_key"):
        with patch("app.ai.Groq") as mock_groq_class:
            mock_client = MagicMock()
            mock_groq_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            res = await synthesize_research_copilot(
                question="What is the clinical significance of this mutation?",
                evidence_packet=packet,
                conversation_history=[],
            )

            # Contradictory assertion must be discarded and replaced with deterministic summary
            assert res.fallback is True
            assert res.provenance_label == "Deterministic synthesis"
            assert "Pathogenic" in res.answer


# 16. Equivalent historical nomenclature for benchmark c.118C>T
def test_16_equivalent_nomenclature_recognition():
    """Verifies equivalent historical aliases (CD39, Q40*, Q39*) and mature protein numbering note."""
    aliases, notes = get_equivalent_nomenclature("118", "C", "T", "p.Gln40Ter")
    assert "CD39 C>T" in aliases
    assert "Q40*" in aliases
    assert "Q39*" in aliases
    assert "Gln40Ter" in aliases
    assert "Gln39Ter" in aliases
    assert "Codon 39 C>T" in aliases
    assert notes is not None
    assert "initiator methionine" in notes
    assert "residue 39" in notes
    assert "codon 40" in notes


# 17. Provenance labels
def test_17_provenance_labels():
    """Verifies distinct provenance labels between live synthesis and deterministic fallback."""
    packet = create_c118_test_packet()
    fallback_res = _generate_offline_synthesis(packet, "Why does CAG to TAG result in stop?", reason="no_key")
    assert fallback_res.provenance_label == "Deterministic synthesis"
    assert fallback_res.fallback is True
