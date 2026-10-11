"""Unit tests for pure HGVS syntax parsing, validation pipeline, and normalization."""

import pytest
from app.core.hgvs import parse_hgvs
from app.core.models import AnalysisError, AnalysisErrorCode, VariantType


def test_parse_coding_snv():
    v = parse_hgvs("c.118C>T")
    assert v.transcript_accession == "NM_000518.5"
    assert v.c_position == "118"
    assert v.variant_type == VariantType.SUBSTITUTION
    assert v.ref_allele == "C"
    assert v.alt_allele == "T"
    assert v.hgvs_c == "NM_000518.5:c.118C>T"
    assert v.region == "Exon 2"
    assert v.mrna_position == 168


def test_parse_with_accession_prefix():
    v = parse_hgvs("NM_000518.5:c.20A>T")
    assert v.transcript_accession == "NM_000518.5"
    assert v.c_position == "20"
    assert v.variant_type == VariantType.SUBSTITUTION
    assert v.ref_allele == "A"
    assert v.alt_allele == "T"
    assert v.region == "Exon 1"


def test_parse_utr_snvs():
    v5 = parse_hgvs("c.-50A>G")
    assert v5.variant_type == VariantType.REGULATORY_UTR
    assert v5.region == "5' UTR"
    assert v5.ref_allele == "A"
    assert v5.alt_allele == "G"

    v3 = parse_hgvs("c.*10C>T")
    assert v3.variant_type == VariantType.REGULATORY_UTR
    assert v3.region == "3' UTR"
    assert v3.ref_allele == "C"
    assert v3.alt_allele == "T"


def test_parse_splice_intronic_snvs():
    v1 = parse_hgvs("c.92+5G>C")
    assert v1.variant_type == VariantType.SPLICE
    assert v1.ref_allele == "G"
    assert v1.alt_allele == "C"
    assert v1.region == "Intron 1"
    assert v1.genomic_accession == "NG_000007.3"
    assert v1.genomic_coordinate == 70691

    v2 = parse_hgvs("c.315+1G>A")
    assert v2.variant_type == VariantType.SPLICE
    assert v2.ref_allele == "G"
    assert v2.alt_allele == "A"
    assert v2.region == "Intron 2"
    assert v2.genomic_coordinate == 71040


def test_parse_deletions():
    # Range deletion without explicit bases
    v_del = parse_hgvs("c.126_129del")
    assert v_del.variant_type == VariantType.DELETION
    assert v_del.ref_allele == "CTTT"
    assert v_del.alt_allele == "-"
    assert v_del.c_position == "126_129"

    # Range deletion with matching explicit bases
    v_del_spec = parse_hgvs("c.126_129delCTTT")
    assert v_del_spec.variant_type == VariantType.DELETION
    assert v_del_spec.ref_allele == "CTTT"

    # Single deletion
    v_single = parse_hgvs("c.9del")
    assert v_single.variant_type == VariantType.DELETION
    assert v_single.ref_allele == "T"
    assert v_single.c_position == "9"


def test_parse_duplication():
    v_dup = parse_hgvs("c.27dup")
    assert v_dup.variant_type == VariantType.DUPLICATION
    assert v_dup.ref_allele == "G"
    assert v_dup.alt_allele == "G"
    assert v_dup.c_position == "27"


def test_parse_insertion():
    v_ins = parse_hgvs("c.27_28insG")
    assert v_ins.variant_type == VariantType.INSERTION
    assert v_ins.ref_allele == "-"
    assert v_ins.alt_allele == "G"
    assert v_ins.c_position == "27_28"


def test_reference_mismatch_detection():
    # Stated 'A' at c.118, but reference has 'C'
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.118A>T")
    assert exc.value.code == AnalysisErrorCode.REFERENCE_MISMATCH

    # Stated 'AAAA' at c.126_129, but reference has 'CTTT'
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.126_129delAAAA")
    assert exc.value.code == AnalysisErrorCode.REFERENCE_MISMATCH


def test_invalid_coordinate_detection():
    # Base zero is invalid in HGVS
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.0C>T")
    assert exc.value.code == AnalysisErrorCode.INVALID_COORDINATE

    # Inverted range
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.129_126del")
    assert exc.value.code == AnalysisErrorCode.INVALID_COORDINATE

    # Insertion with non-consecutive flanking bases
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.26_28insG")
    assert exc.value.code == AnalysisErrorCode.INVALID_COORDINATE


def test_out_of_bounds_detection():
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.999C>T")
    assert exc.value.code == AnalysisErrorCode.OUT_OF_BOUNDS

    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.92+140G>C")
    assert exc.value.code == AnalysisErrorCode.OUT_OF_BOUNDS


def test_syntax_error_detection():
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("not_a_valid_variant")
    assert exc.value.code == AnalysisErrorCode.SYNTAX_ERROR

    # Invalid base character
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("c.118C>X")
    assert exc.value.code == AnalysisErrorCode.SYNTAX_ERROR


def test_unsupported_transcript():
    with pytest.raises(AnalysisError) as exc:
        parse_hgvs("NM_999999.1:c.100A>G")
    assert exc.value.code == AnalysisErrorCode.UNSUPPORTED_VARIANT
