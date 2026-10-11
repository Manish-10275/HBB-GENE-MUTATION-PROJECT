"""Comprehensive Phase 2A test suite for structured HGVS precision upgrade,
indel consequence calculation, frameshift codon translation, and intronic splice resolution.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.reference import reference_manager
from app.variants import parse_hgvs_input, detect_variants
from app.consequences import evaluate_indel_codon_consequence
from app.alignment import align_sequences

client = TestClient(app)


@pytest.fixture
def nm_ref():
    return reference_manager.get_reference("NM_000518.5")


@pytest.fixture
def ng_ref():
    return reference_manager.get_reference("NG_000007.3")


# =========================================================================
# 1. REGRESSION BENCHMARKS (PHASE 1 BASELINE PRESERVATION)
# =========================================================================

def test_regression_c118C_T_benchmark(nm_ref):
    """Verifies that the canonical c.118C>T nonsense mutation continues to parse deterministically."""
    var, err = parse_hgvs_input("c.118C>T", nm_ref)
    assert err is None
    assert var is not None
    assert var.hgvs_c == "NM_000518.5:c.118C>T"
    assert var.c_position == "118"
    assert var.ref_allele == "C"
    assert var.alt_allele == "T"
    assert var.functional_impact == "Nonsense"
    assert var.hgvs_p == "p.Gln40Ter"
    assert var.codon_change is not None
    assert var.codon_change.ref_aa == "Gln"
    assert var.codon_change.sample_aa == "Ter"


def test_regression_c20A_T_sickle(nm_ref):
    """Verifies that c.20A>T (HbS) missense mutation continues to parse deterministically."""
    var, err = parse_hgvs_input("c.20A>T", nm_ref)
    assert err is None
    assert var is not None
    assert var.hgvs_c == "NM_000518.5:c.20A>T"
    assert var.c_position == "20"
    assert var.ref_allele == "A"
    assert var.alt_allele == "T"
    assert var.functional_impact == "Missense"
    assert var.hgvs_p == "p.Glu7Val"


def test_regression_utr_substitutions(nm_ref):
    """Verifies that 5' UTR and 3' UTR substitutions parse deterministically."""
    var_5, err_5 = parse_hgvs_input("c.-5A>G", nm_ref)
    assert err_5 is None
    assert var_5 is not None
    assert var_5.functional_impact == "5' UTR (Non-coding)"

    var_3, err_3 = parse_hgvs_input("c.*10C>T", nm_ref)
    assert err_3 is None
    assert var_3 is not None
    assert var_3.functional_impact == "3' UTR (Non-coding)"


# =========================================================================
# 2. DELETION PARSING & CONSEQUENCES
# =========================================================================

def test_single_deletion_c9del_variants(nm_ref):
    """
    Verifies single base deletion at cDNA 9 (CAT -> His3):
    Base at c.9 is T.
    Deleting T preserves His3 (CAT -> CAC) and creates immediate stop at codon 4 (CTG -> TGA).
    """
    # 1. c.9delT (explicit base)
    var1, err1 = parse_hgvs_input("c.9delT", nm_ref)
    assert err1 is None
    assert var1 is not None
    assert var1.hgvs_c == "NM_000518.5:c.9del"
    assert var1.ref_allele == "T"
    assert var1.hgvs_p == "p.Leu4Ter"
    assert "Immediate Termination" in var1.functional_impact or "Frameshift" in var1.functional_impact

    # 2. c.9del (inferred base)
    var2, err2 = parse_hgvs_input("c.9del", nm_ref)
    assert err2 is None
    assert var2 is not None
    assert var2.ref_allele == "T"
    assert var2.hgvs_p == "p.Leu4Ter"

    # 3. c.8delA (codon 3 'A' deletion)
    var3, err3 = parse_hgvs_input("c.8delA", nm_ref)
    assert err3 is None
    assert var3 is not None
    assert var3.ref_allele == "A"
    assert var3.hgvs_p == "p.His3LeufsTer2"


def test_single_deletion_c9delA_reference_mismatch(nm_ref):
    """
    CRITICAL BENCHMARK: Verifies that c.9delA is rejected because the reference
    nucleotide at c.9 in NM_000518.5 is 'T', not 'A'.
    """
    var, err = parse_hgvs_input("c.9delA", nm_ref)
    assert var is None
    assert err is not None
    assert "Reference base mismatch at c.9" in err
    assert "input states 'A'" in err or "query states 'A'" in err
    assert "has 'T'" in err


def test_range_deletion_cd41_42_c126_129del(nm_ref):
    """
    CRITICAL INDIAN BENCHMARK: Cd41/42 (-TCTT / -CTTT).
    c.126_129delCTTT produces frameshift at Phe42 (mutating to Leu) with stop at codon 60 (distance 19).
    Canonical HGVS: p.Phe42LeufsTer19 (short: p.Phe42fs).
    """
    # 1. With explicit bases
    var1, err1 = parse_hgvs_input("c.126_129delCTTT", nm_ref)
    assert err1 is None
    assert var1 is not None
    assert var1.hgvs_c == "NM_000518.5:c.126_129del"
    assert var1.c_position == "126_129"
    assert var1.ref_allele == "CTTT"
    assert var1.hgvs_p == "p.Phe42LeufsTer19"
    assert var1.functional_impact == "Frameshift Deletion"
    assert "c.126_129del" in var1.equivalent_nomenclature
    assert "Codon 41/42 (-TCTT)" in var1.equivalent_nomenclature

    # 2. Inferred bases
    var2, err2 = parse_hgvs_input("c.126_129del", nm_ref)
    assert err2 is None
    assert var2 is not None
    assert var2.ref_allele == "CTTT"
    assert var2.hgvs_p == "p.Phe42LeufsTer19"

    # 3. Canonical equivalent c.124_127del
    var3, err3 = parse_hgvs_input("c.124_127del", nm_ref)
    assert err3 is None
    assert var3 is not None
    assert var3.ref_allele == "TTCT"
    assert var3.hgvs_p == "p.Phe42LeufsTer19"


def test_in_frame_deletion(nm_ref):
    """Verifies that deletions with net length divisible by 3 are classified as in-frame."""
    # Deleting codon 43 (c.127_129del TTT -> Phe43)
    var, err = parse_hgvs_input("c.127_129delTTT", nm_ref)
    assert err is None
    assert var is not None
    assert var.functional_impact == "In-frame Deletion"
    assert var.hgvs_p == "p.Phe43del"


# =========================================================================
# 3. DUPLICATION & INSERTION PARSING & CONSEQUENCES
# =========================================================================

def test_duplication_cd8_9_c27dup(nm_ref):
    """
    CRITICAL INDIAN BENCHMARK: Cd8/9 (+G) / c.27dup.
    Duplicating G at c.27 alters Codon 10 (Ser10 -> Val) with stop at codon 23 (distance 14).
    Canonical HGVS: p.Ser10ValfsTer14 (short: p.Ser10fs).
    """
    # 1. c.27dup
    var1, err1 = parse_hgvs_input("c.27dup", nm_ref)
    assert err1 is None
    assert var1 is not None
    assert var1.hgvs_c == "NM_000518.5:c.27dup"
    assert var1.c_position == "27"
    assert var1.alt_allele == "G"
    assert var1.hgvs_p == "p.Ser10ValfsTer14"
    assert var1.functional_impact == "Frameshift Duplication"
    assert "c.27dup" in var1.equivalent_nomenclature
    assert "Codon 8/9 (+G)" in var1.equivalent_nomenclature

    # 2. c.27dupG
    var2, err2 = parse_hgvs_input("c.27dupG", nm_ref)
    assert err2 is None
    assert var2 is not None
    assert var2.hgvs_p == "p.Ser10ValfsTer14"


def test_flanked_insertion_recognized_as_duplication(nm_ref):
    """
    Verifies that c.27_28insG is recognized as the canonical equivalent duplication c.27dup
    in accordance with HGVS 3'-duplication rules.
    """
    var, err = parse_hgvs_input("c.27_28insG", nm_ref)
    assert err is None
    assert var is not None
    assert "c.27dup" in var.hgvs_c or "c.27_28ins" in var.hgvs_c
    assert var.hgvs_p == "p.Ser10ValfsTer14"
    assert "c.27dup" in var.equivalent_nomenclature
    assert "c.27_28insG" in var.equivalent_nomenclature


# =========================================================================
# 4. INTRONIC SPLICE VARIANT RESOLUTION & SAFETY
# =========================================================================

def test_splice_variant_ivs1_5_c92_5G_C(nm_ref):
    """
    CRITICAL INDIAN BENCHMARK: IVS1-5 (G>C) / c.92+5G>C.
    Resolves against NG_000007.3 relative position 147 (genomic 70691).
    Ref base must be G. Consequence must be p.? with splice annotation.
    """
    var, err = parse_hgvs_input("c.92+5G>C", nm_ref)
    assert err is None
    assert var is not None
    assert var.c_position == "92+5"
    assert var.ref_allele == "G"
    assert var.alt_allele == "C"
    assert var.hgvs_c == "NM_000518.5:c.92+5G>C"
    assert var.hgvs_p == "p.?"
    assert "Splice Site Defect" in var.functional_impact
    assert "c.92+5G>C" in var.equivalent_nomenclature
    assert "IVS1-5 G>C" in var.equivalent_nomenclature


def test_splice_variant_c315_1G_A(nm_ref):
    """
    CRITICAL BENCHMARK: c.315+1G>A (Intron 2 donor invariant GT dinucleotide).
    Resolves against NG_000007.3 relative position 496 (genomic 71040).
    Ref base must be G. Consequence must be p.? with splice disruption annotation.
    """
    var, err = parse_hgvs_input("c.315+1G>A", nm_ref)
    assert err is None
    assert var is not None
    assert var.c_position == "315+1"
    assert var.ref_allele == "G"
    assert var.alt_allele == "A"
    assert var.hgvs_c == "NM_000518.5:c.315+1G>A"
    assert var.hgvs_p == "p.?"
    assert "Splice Site Disruption" in var.functional_impact
    assert "IVS2-1" in "".join(var.equivalent_nomenclature)


def test_splice_variant_acceptor_sites(nm_ref):
    """Verifies that intronic acceptor sites with minus offsets parse correctly."""
    # c.93-1G>A (Intron 1 acceptor invariant AG dinucleotide)
    var, err = parse_hgvs_input("c.93-1G>A", nm_ref)
    assert err is None
    assert var is not None
    assert var.c_position == "93-1"
    assert var.ref_allele == "G"
    assert var.alt_allele == "A"
    assert var.hgvs_p == "p.?"
    assert "Splice Site Disruption" in var.functional_impact


# =========================================================================
# 5. ERROR HANDLING & VALIDATION CHECKS
# =========================================================================

def test_invalid_syntax_and_ranges(nm_ref):
    """Tests syntax rejections and invalid ranges."""
    # Inverted range
    var_inv, err_inv = parse_hgvs_input("c.129_126del", nm_ref)
    assert var_inv is None
    assert "start coordinate must precede end coordinate" in err_inv

    # Non-consecutive insertion
    var_ins, err_ins = parse_hgvs_input("c.25_28insG", nm_ref)
    assert var_ins is None
    assert "two consecutive flanking positions" in err_ins

    # Out of bounds
    var_oob, err_oob = parse_hgvs_input("c.999del", nm_ref)
    assert var_oob is None
    assert "out of bounds" in err_oob

    # Unsupported syntax
    var_bad, err_bad = parse_hgvs_input("invalid_syntax_123", nm_ref)
    assert var_bad is None
    assert "Unsupported HGVS syntax" in err_bad or "Query must follow" in err_bad


# =========================================================================
# 6. DIRECT VARIANT SEARCH API INTEGRATION
# =========================================================================

def test_api_variant_search_indel_c126_129del():
    """Tests /variant/search for c.126_129del via FastAPI TestClient."""
    response = client.get("/variant/search?query=c.126_129del")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "c.126_129del" in data["standardized_hgvs_c"]
    assert "clinvar_records" in data


def test_api_variant_search_duplication_c27dup():
    """Tests /variant/search for c.27dup via FastAPI TestClient."""
    response = client.get("/variant/search?query=c.27dup")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "c.27dup" in data["standardized_hgvs_c"]
    assert "clinvar_records" in data


def test_api_variant_search_splice_c92_5G_C():
    """Tests /variant/search for c.92+5G>C via FastAPI TestClient."""
    response = client.get("/variant/search?query=c.92+5G>C")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "c.92+5G>C" in data["standardized_hgvs_c"]
    assert "clinvar_records" in data


def test_api_variant_search_splice_c315_1G_A():
    """Tests /variant/search for c.315+1G>A via FastAPI TestClient."""
    response = client.get("/variant/search?query=c.315+1G>A")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "c.315+1G>A" in data["standardized_hgvs_c"]


# =========================================================================
# 7. SEQUENCE ALIGNMENT CALLER INDEL CONSEQUENCES
# =========================================================================

def test_sequence_aligner_detect_variants_indel_consequences(nm_ref):
    """
    Verifies that detect_variants (the sequence pairwise aligner) now produces
    deterministic frameshift protein consequences rather than placeholder strings.
    """
    # Cd41/42 (-TCTT): 4 bp deletion at 126..129
    # In NM_000518.5, cDNA 126 is index 175
    ref_seq = nm_ref.sequence
    mut_seq = ref_seq[:175] + ref_seq[179:]

    _, al_ref, al_query = align_sequences(ref_seq, mut_seq)
    variants = detect_variants(al_ref, al_query, nm_ref)
    assert len(variants) == 1
    v = variants[0]
    assert v.variant_type == "deletion"
    assert "c.126_129del" in v.hgvs_c or "c.124_127del" in v.hgvs_c
    assert v.hgvs_p == "p.Phe42LeufsTer19"
    assert v.functional_impact == "Frameshift Deletion"
