"""Comprehensive unit tests for the deterministic HBB bioinformatics pipeline."""

import pytest
from app.reference import reference_manager
from app.sequence import normalize_and_validate_sequence
from app.alignment import align_sequences
from app.variants import detect_variants, parse_hgvs_input
from app.consequences import (
    translate_codon,
    evaluate_substitution_codon_consequence,
)
from app.evidence import assemble_evidence_packet
from app.models import ClinVarRecord, PubMedRecord


@pytest.fixture
def ref_data():
    return reference_manager.get_reference("NM_000518.5")


def test_reference_loading(ref_data):
    """Verifies that official HBB NM_000518.5 reference data loads accurately."""
    assert ref_data.gene == "HBB"
    assert ref_data.accession == "NM_000518.5"
    assert ref_data.total_length == 628
    assert ref_data.cds_start == 51
    assert ref_data.cds_end == 494
    assert ref_data.cds_length == 444
    assert ref_data.protein_length == 147
    assert ref_data.cds_sequence.startswith("ATG")
    assert ref_data.cds_sequence.endswith("TAA")


def test_sequence_normalization_valid_raw():
    raw = "acg tact gca\nagt"
    res = normalize_and_validate_sequence(raw)
    assert res.is_valid is True
    assert res.clean_sequence == "ACGTACTGCAAGT"
    assert res.length == 13
    assert len(res.validation_errors) == 0


def test_sequence_normalization_fasta():
    fasta = ">NM_000518.5 Test sequence\nACATTTGCTT\nCTGACACAAC\n"
    res = normalize_and_validate_sequence(fasta)
    assert res.is_valid is True
    assert res.header == "NM_000518.5 Test sequence"
    assert res.clean_sequence == "ACATTTGCTTCTGACACAAC"


def test_sequence_validation_empty():
    res = normalize_and_validate_sequence("")
    assert res.is_valid is False
    assert any("empty" in e.lower() for e in res.validation_errors)


def test_sequence_validation_rna_rejected():
    res = normalize_and_validate_sequence("ACGAUGAC")
    assert res.is_valid is False
    assert any("Uracil" in e for e in res.validation_errors)


def test_sequence_validation_invalid_chars():
    res = normalize_and_validate_sequence("ACGTXYZ123")
    assert res.is_valid is False
    assert any("Non-canonical" in e for e in res.validation_errors)


def test_codon_translation():
    assert translate_codon("ATG") == ("Met", "M")
    assert translate_codon("CAG") == ("Gln", "Q")
    assert translate_codon("TAG") == ("Ter", "*")
    assert translate_codon("TAA") == ("Ter", "*")
    assert translate_codon("TGA") == ("Ter", "*")
    assert translate_codon("GAG") == ("Glu", "E")
    assert translate_codon("GTG") == ("Val", "V")
    assert translate_codon("AAG") == ("Lys", "K")


def test_controlled_validation_case_c118C_T(ref_data):
    """
    CRITICAL BENCHMARK TEST:
    CAG -> TAG
    Gln -> STOP (Ter)
    p.Gln40Ter (Nonsense)
    """
    # Base 118 in CDS (1-based) is the first base of codon 40
    # In NM_000518.5 mRNA: cds starts at 51, so index is 50 + 118 - 1 = 167
    ref_seq = ref_data.sequence
    assert ref_seq[167] == "C"

    mut_seq = ref_seq[:167] + "T" + ref_seq[168:]

    norm = normalize_and_validate_sequence(mut_seq)
    assert norm.is_valid is True

    summary, al_ref, al_query = align_sequences(ref_seq, norm.clean_sequence)
    assert summary.mismatches == 1
    assert summary.gaps == 0

    variants = detect_variants(al_ref, al_query, ref_data)
    assert len(variants) == 1

    v = variants[0]
    assert v.hgvs_c == "NM_000518.5:c.118C>T"
    assert v.c_position == "118"
    assert v.ref_allele == "C"
    assert v.alt_allele == "T"
    assert v.functional_impact == "Nonsense"
    assert v.hgvs_p == "p.Gln40Ter"

    # Codon analysis
    assert v.codon_change is not None
    assert v.codon_change.codon_number == 40
    assert v.codon_change.ref_codon == "CAG"
    assert v.codon_change.sample_codon == "TAG"
    assert v.codon_change.ref_aa == "Gln"
    assert v.codon_change.sample_aa == "Ter"
    assert v.codon_change.is_stop_gain is True


def test_sickle_cell_c20A_T(ref_data):
    """Verifies sickle cell canonical mutation: c.20A>T -> p.Glu7Val."""
    ref_seq = ref_data.sequence
    # c.20 is index 50 + 20 - 1 = 69
    assert ref_seq[69] == "A"
    mut_seq = ref_seq[:69] + "T" + ref_seq[70:]

    summary, al_ref, al_query = align_sequences(ref_seq, mut_seq)
    variants = detect_variants(al_ref, al_query, ref_data)
    assert len(variants) == 1

    v = variants[0]
    assert v.hgvs_c == "NM_000518.5:c.20A>T"
    assert v.c_position == "20"
    assert v.functional_impact == "Missense"
    assert v.hgvs_p == "p.Glu7Val"
    assert v.codon_change.ref_codon == "GAG"
    assert v.codon_change.sample_codon == "GTG"


def test_direct_hgvs_parser(ref_data):
    """Tests direct HGVS query investigation without uploading whole sequence."""
    var, err = parse_hgvs_input("NM_000518.5:c.118C>T", ref_data)
    assert err is None
    assert var is not None
    assert var.hgvs_c == "NM_000518.5:c.118C>T"
    assert var.hgvs_p == "p.Gln40Ter"
    assert var.functional_impact == "Nonsense"

    # Test short form: c.20A>T
    var2, err2 = parse_hgvs_input("c.20A>T", ref_data)
    assert err2 is None
    assert var2.hgvs_p == "p.Glu7Val"

    # Test invalid syntax
    var_bad, err_bad = parse_hgvs_input("invalid_query", ref_data)
    assert var_bad is None
    assert err_bad is not None


def test_evidence_packet_assembly(ref_data):
    """Verifies that evidence packet structure is complete and properly annotated."""
    summary, al_ref, al_query = align_sequences(ref_data.sequence, ref_data.sequence)
    variants = detect_variants(al_ref, al_query, ref_data)

    packet = assemble_evidence_packet(
        ref_data=ref_data,
        alignment_summary=summary,
        variants=variants,
        clinvar_records=[],
        pubmed_records=[]
    )

    assert packet.analysis_id.startswith("HBB-EXP-")
    assert packet.reference_accession == "NM_000518.5"
    assert packet.gene_symbol == "HBB"
    assert len(packet.limitations) >= 5
    assert "source_metadata" in packet.model_dump()
