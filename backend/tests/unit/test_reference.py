"""Unit tests for pure reference sequence loader and coordinate mapping."""

import pytest
from app.core.models import AnalysisError, AnalysisErrorCode
from app.core.reference import (
    ReferenceSequence,
    load_reference,
    map_intronic_cdna_to_genomic,
)


def test_load_nm_reference():
    ref = load_reference("NM_000518.5")
    assert isinstance(ref, ReferenceSequence)
    assert ref.accession == "NM_000518.5"
    assert ref.gene == "HBB"
    assert ref.total_length == 628
    assert ref.cds_start == 51
    assert ref.cds_end == 494
    assert ref.cds_length == 444
    assert ref.protein_length == 147
    assert len(ref.sequence) == 628
    assert len(ref.cds_sequence) == 444
    assert len(ref.exons) == 3


def test_load_ng_reference():
    ng = load_reference("NG_000007.3")
    assert isinstance(ng, ReferenceSequence)
    assert ng.accession == "NG_000007.3"
    assert ng.total_length == 1608
    assert len(ng.exons) == 3


def test_c_pos_to_mrna_pos_coding():
    ref = load_reference("NM_000518.5")
    # c.1 is mRNA 51
    assert ref.c_pos_to_mrna_pos("1") == 51
    assert ref.c_pos_to_mrna_pos("c.1") == 51
    # c.118 is mRNA 51 + 118 - 1 = 168
    assert ref.c_pos_to_mrna_pos("118") == 168
    # c.444 is mRNA 494
    assert ref.c_pos_to_mrna_pos("444") == 494


def test_c_pos_to_mrna_pos_utr():
    ref = load_reference("NM_000518.5")
    # 5' UTR: c.-1 is mRNA 50, c.-50 is mRNA 1
    assert ref.c_pos_to_mrna_pos("-1") == 50
    assert ref.c_pos_to_mrna_pos("-50") == 1
    # 3' UTR: c.*1 is mRNA 495, c.*134 is mRNA 628
    assert ref.c_pos_to_mrna_pos("*1") == 495
    assert ref.c_pos_to_mrna_pos("*134") == 628


def test_c_pos_to_mrna_pos_invalid():
    ref = load_reference("NM_000518.5")
    # Base zero is forbidden
    with pytest.raises(AnalysisError) as exc_info:
        ref.c_pos_to_mrna_pos("0")
    assert exc_info.value.code == AnalysisErrorCode.INVALID_COORDINATE

    # Out of bounds 5' UTR
    with pytest.raises(AnalysisError) as exc_info:
        ref.c_pos_to_mrna_pos("-51")
    assert exc_info.value.code == AnalysisErrorCode.OUT_OF_BOUNDS

    # Out of bounds 3' UTR
    with pytest.raises(AnalysisError) as exc_info:
        ref.c_pos_to_mrna_pos("*135")
    assert exc_info.value.code == AnalysisErrorCode.OUT_OF_BOUNDS


def test_mrna_pos_to_c_pos_roundtrip():
    ref = load_reference("NM_000518.5")
    assert ref.mrna_pos_to_c_pos(1) == "-50"
    assert ref.mrna_pos_to_c_pos(50) == "-1"
    assert ref.mrna_pos_to_c_pos(51) == "1"
    assert ref.mrna_pos_to_c_pos(168) == "118"
    assert ref.mrna_pos_to_c_pos(494) == "444"
    assert ref.mrna_pos_to_c_pos(495) == "*1"
    assert ref.mrna_pos_to_c_pos(628) == "*134"


def test_intronic_mapping():
    ng = load_reference("NG_000007.3")
    # Intron 1 donor: c.92+1 -> rel 143, genomic 70687
    rel, gen, reg = map_intronic_cdna_to_genomic("92+1", ng)
    assert rel == 143
    assert gen == 70687
    assert reg == "Intron 1"

    # Intron 1 donor +5: c.92+5 -> rel 147, genomic 70691
    rel, gen, reg = map_intronic_cdna_to_genomic("c.92+5", ng)
    assert rel == 147
    assert gen == 70691

    # Intron 1 acceptor: c.93-1 -> rel 272, genomic 70816
    rel, gen, reg = map_intronic_cdna_to_genomic("93-1", ng)
    assert rel == 272
    assert gen == 70816

    # Intron 2 donor: c.315+1 -> rel 496, genomic 71040
    rel, gen, reg = map_intronic_cdna_to_genomic("315+1", ng)
    assert rel == 496
    assert gen == 71040
    assert reg == "Intron 2"

    # Intron 2 acceptor: c.316-1 -> rel 1345, genomic 71889
    rel, gen, reg = map_intronic_cdna_to_genomic("316-1", ng)
    assert rel == 1345
    assert gen == 71889


def test_intronic_mapping_out_of_bounds():
    ng = load_reference("NG_000007.3")
    # Intron 1 length is 130 bp
    with pytest.raises(AnalysisError) as exc_info:
        map_intronic_cdna_to_genomic("92+131", ng)
    assert exc_info.value.code == AnalysisErrorCode.OUT_OF_BOUNDS

    # Intron 2 length is 850 bp
    with pytest.raises(AnalysisError) as exc_info:
        map_intronic_cdna_to_genomic("315+851", ng)
    assert exc_info.value.code == AnalysisErrorCode.OUT_OF_BOUNDS
