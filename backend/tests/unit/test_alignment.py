"""Unit tests for alignment engine and variant detection from alignments."""

import pytest
from app.core.alignment import (
    align_sequences,
    clean_sequence,
    detect_variants_from_alignment,
)
from app.core.models import AnalysisError, AnalysisErrorCode, VariantType
from app.core.reference import load_reference


def test_clean_sequence_fasta():
    fasta = ">sample_patient_1\nACGT\nACGT\n"
    assert clean_sequence(fasta) == "ACGTACGT"

    lower = "acgtacgt"
    assert clean_sequence(lower) == "ACGTACGT"

    with_spaces = "  ACGT   TGCA \n"
    assert clean_sequence(with_spaces) == "ACGTTGCA"


def test_clean_sequence_empty():
    with pytest.raises(AnalysisError) as exc_info:
        clean_sequence(">>>header_only\n")
    assert exc_info.value.code == AnalysisErrorCode.SYNTAX_ERROR


def test_align_identical_sequences():
    seq = "ACGTACGTACGT"
    summary, ref_aln, qry_aln = align_sequences(seq, seq)
    assert summary.identity_percentage == 100.0
    assert summary.matches == 12
    assert summary.mismatches == 0
    assert summary.gaps == 0
    assert ref_aln == qry_aln
    assert len(summary.blocks) == 1
    assert summary.blocks[0].match_line == "||||||||||||"


def test_align_with_substitution():
    ref_seq = "ACGTACGT"
    qry_seq = "ACGAACGT"  # T -> A mismatch at pos 4
    summary, ref_aln, qry_aln = align_sequences(ref_seq, qry_seq)
    assert summary.matches == 7
    assert summary.mismatches == 1
    assert summary.gaps == 0
    assert summary.identity_percentage == 87.5


def test_detect_variants_substitution():
    ref = load_reference("NM_000518.5")
    # c.118 is mRNA 168 (index 167)
    mrna_pos = 168
    ref_seq = ref.sequence
    assert ref_seq[mrna_pos - 1] == "C"

    # Mutate C to T at mRNA 168
    mut_seq = ref_seq[:mrna_pos - 1] + "T" + ref_seq[mrna_pos:]

    summary, ref_aln, qry_aln = align_sequences(ref_seq, mut_seq)
    variants = detect_variants_from_alignment(ref_aln, qry_aln, ref)

    assert len(variants) == 1
    v = variants[0]
    assert v.c_position == "118"
    assert v.ref_allele == "C"
    assert v.alt_allele == "T"
    assert v.variant_type == VariantType.SUBSTITUTION
    assert v.hgvs_c == "NM_000518.5:c.118C>T"
    assert v.region == "Exon 2"


def test_detect_variants_deletion():
    ref = load_reference("NM_000518.5")
    # c.126_129 is mRNA 176..179 (CTTT)
    s_mrna = 176
    e_mrna = 179
    ref_seq = ref.sequence
    assert ref_seq[s_mrna - 1 : e_mrna] == "CTTT"

    # Delete CTTT
    mut_seq = ref_seq[:s_mrna - 1] + ref_seq[e_mrna:]

    summary, ref_aln, qry_aln = align_sequences(ref_seq, mut_seq)
    variants = detect_variants_from_alignment(ref_aln, qry_aln, ref)

    assert len(variants) >= 1
    v = variants[0]
    assert v.variant_type == VariantType.DELETION
    assert "126" in v.c_position or "127" in v.c_position or "128" in v.c_position or "129" in v.c_position
