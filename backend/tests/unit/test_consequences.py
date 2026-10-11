"""Unit tests for deterministic codon translation and protein consequence evaluation."""

from app.core.consequences import (
    evaluate_consequence,
    evaluate_indel,
    evaluate_substitution,
    translate_codon,
)
from app.core.hgvs import parse_hgvs
from app.core.models import MolecularImpact
from app.core.reference import load_reference


def test_translate_codon():
    assert translate_codon("ATG") == ("Met", "M")
    assert translate_codon("TAA") == ("Ter", "*")
    assert translate_codon("TAG") == ("Ter", "*")
    assert translate_codon("TGA") == ("Ter", "*")
    assert translate_codon("GAG") == ("Glu", "E")
    assert translate_codon("GTG") == ("Val", "V")
    assert translate_codon("CAG") == ("Gln", "Q")
    assert translate_codon("aTg") == ("Met", "M")


def test_nonsense_substitution():
    ref = load_reference("NM_000518.5")
    # c.118C>T (Codon 40 CAG -> TAG)
    res = evaluate_substitution(118, "C", "T", ref)
    assert res.hgvs_p == "p.Gln40Ter"
    assert res.molecular_impact == MolecularImpact.NONSENSE
    assert res.ptc_coordinate == 40
    assert res.codon_change is not None
    assert res.codon_change.codon_number == 40
    assert res.codon_change.is_stop_gain is True


def test_missense_substitution():
    ref = load_reference("NM_000518.5")
    # c.20A>T (Codon 7 GAG -> GTG, HbS)
    res = evaluate_substitution(20, "A", "T", ref)
    assert res.hgvs_p == "p.Glu7Val"
    assert res.molecular_impact == MolecularImpact.MISSENSE
    assert res.ptc_coordinate is None
    assert res.codon_change is not None
    assert res.codon_change.ref_aa == "Glu"
    assert res.codon_change.sample_aa == "Val"

    # c.19G>A (Codon 7 GAG -> AAG, HbC)
    res_c = evaluate_substitution(19, "G", "A", ref)
    assert res_c.hgvs_p == "p.Glu7Lys"
    assert res_c.molecular_impact == MolecularImpact.MISSENSE


def test_synonymous_substitution():
    ref = load_reference("NM_000518.5")
    # c.9A>G (Codon 3 CTG -> CTG is synonymous)
    # Check what base is at c.9:
    # CDS 1..9: ATG GTG CAC (Met1 Val2 His3)
    # At c.9, base is C (CAC -> His). Let's check c.9 in ref.
    # CAC: C at 7, A at 8, C at 9. If c.9C>T -> CAT (His3His)
    res = evaluate_substitution(9, "C", "T", ref)
    assert res.hgvs_p == "p.(=)"
    assert res.molecular_impact == MolecularImpact.SYNONYMOUS
    assert res.codon_change is not None
    assert res.codon_change.is_synonymous is True


def test_initiation_codon_substitution():
    ref = load_reference("NM_000518.5")
    # c.2T>C (Codon 1 ATG -> ACG / Thr)
    res = evaluate_substitution(2, "T", "C", ref)
    assert res.hgvs_p == "p.Met1?"
    assert res.molecular_impact == MolecularImpact.MISSENSE


def test_frameshift_deletion_downstream_walking():
    ref = load_reference("NM_000518.5")
    # c.126_129del (net delta -4) -> p.Phe42LeufsTer19
    res = evaluate_indel(126, 129, "deletion", "CTTT", "-", ref)
    assert res.hgvs_p == "p.Phe42LeufsTer19"
    assert res.molecular_impact == MolecularImpact.FRAMESHIFT
    assert res.ptc_coordinate == 60  # 42 + 19 - 1 = 60


def test_frameshift_deletion_immediate_termination():
    ref = load_reference("NM_000518.5")
    # c.9del (net delta -1) -> immediate stop at codon 4: p.Leu4Ter
    res = evaluate_indel(9, 9, "deletion", "T", "-", ref)
    assert res.hgvs_p == "p.Leu4Ter"
    assert res.molecular_impact == MolecularImpact.FRAMESHIFT
    assert res.ptc_coordinate == 4


def test_frameshift_duplication():
    ref = load_reference("NM_000518.5")
    # c.27dup (net delta +1) -> p.Ser10ValfsTer14
    res = evaluate_indel(27, 27, "duplication", "G", "G", ref)
    assert res.hgvs_p == "p.Ser10ValfsTer14"
    assert res.molecular_impact == MolecularImpact.FRAMESHIFT
    assert res.ptc_coordinate == 23  # 10 + 14 - 1 = 23


def test_frameshift_insertion():
    ref = load_reference("NM_000518.5")
    # c.27_28insG (net delta +1) -> p.Ser10ValfsTer14
    res = evaluate_indel(27, 28, "insertion", "-", "G", ref)
    assert res.hgvs_p == "p.Ser10ValfsTer14"
    assert res.molecular_impact == MolecularImpact.FRAMESHIFT
    assert res.ptc_coordinate == 23


def test_in_frame_indels():
    ref = load_reference("NM_000518.5")
    # 3 bp in-frame deletion at codon 43 (c.127_129del)
    res_del = evaluate_indel(127, 129, "deletion", "TTT", "-", ref)
    assert res_del.molecular_impact == MolecularImpact.IN_FRAME_INDEL
    assert "del" in (res_del.hgvs_p or "")

    # 3 bp in-frame insertion
    res_ins = evaluate_indel(27, 28, "insertion", "-", "GAG", ref)
    assert res_ins.molecular_impact == MolecularImpact.IN_FRAME_INDEL
    assert "ins" in (res_ins.hgvs_p or "")


def test_evaluate_consequence_dispatch():
    ref = load_reference("NM_000518.5")

    # Splice variant
    v_splice = parse_hgvs("c.92+5G>C")
    res_splice = evaluate_consequence(v_splice, ref)
    assert res_splice.molecular_impact == MolecularImpact.SPLICE_DISRUPTION
    assert res_splice.hgvs_p == "p.?"

    # 5' UTR variant
    v_5utr = parse_hgvs("c.-50A>G")
    res_5utr = evaluate_consequence(v_5utr, ref)
    assert res_5utr.molecular_impact == MolecularImpact.REGULATORY_5_UTR
    assert res_5utr.hgvs_p is None

    # 3' UTR variant
    v_3utr = parse_hgvs("c.*10C>T")
    res_3utr = evaluate_consequence(v_3utr, ref)
    assert res_3utr.molecular_impact == MolecularImpact.REGULATORY_3_UTR
    assert res_3utr.hgvs_p is None


def test_in_frame_deletion_codon_aligned():
    ref = load_reference("NM_000518.5")
    # Codon 18: c.52_54 is AAG (Lys). Clean 3bp deletion.
    res = evaluate_indel(52, 54, "deletion", "AAG", "-", ref)
    assert res.hgvs_p == "p.Lys18del"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL
    assert res.ptc_coordinate is None


def test_in_frame_deletion_splitting_codon_delins():
    ref = load_reference("NM_000518.5")
    # Codon 18 AAG (Lys), Codon 19 GTG (Val).
    # Deleting c.53_55 (AGG) leaves base 52 (A) + bases 56_57 (TG) -> ATG (Met).
    # Two codons replaced by one -> delins.
    res = evaluate_indel(53, 55, "deletion", "AGG", "-", ref)
    assert res.hgvs_p == "p.Lys18_Val19delinsMet"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_in_frame_insertion_codon_aligned():
    ref = load_reference("NM_000518.5")
    # Between codon 18 (Lys) and codon 19 (Val): c.54_55insGCC (Ala).
    res = evaluate_indel(54, 55, "insertion", "-", "GCC", ref)
    assert res.hgvs_p == "p.Lys18_Val19insAla"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_in_frame_insertion_splitting_codon_delins():
    ref = load_reference("NM_000518.5")
    # Inside codon 18 (AAG, Lys): c.53_54insTTT.
    # Base 52 (A), 53 (A), ins (TTT), 54 (G) -> AAT (Asn) + TTG (Leu).
    # Single codon replaced by two -> delins.
    res = evaluate_indel(53, 54, "insertion", "-", "TTT", ref)
    assert res.hgvs_p == "p.Lys18delinsAsnLeu"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_multi_codon_in_frame_deletion():
    ref = load_reference("NM_000518.5")
    # Codons 18 and 19: c.52_57del (AAGGTG, LysVal). Clean 6bp deletion.
    res = evaluate_indel(52, 57, "deletion", "AAGGTG", "-", ref)
    assert res.hgvs_p == "p.Lys18_Val19del"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_multi_codon_in_frame_insertion():
    ref = load_reference("NM_000518.5")
    # Between codon 18 (Lys) and 19 (Val): c.54_55insGCCGCT (AlaAla).
    res = evaluate_indel(54, 55, "insertion", "-", "GCCGCT", ref)
    assert res.hgvs_p == "p.Lys18_Val19insAlaAla"
    assert res.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_in_frame_indel_near_cds_start():
    ref = load_reference("NM_000518.5")
    # Codon 2: c.4_6 is GTG (Val). Clean 3bp deletion at codon 2.
    res_del = evaluate_indel(4, 6, "deletion", "GTG", "-", ref)
    assert res_del.hgvs_p == "p.Val2del"
    assert res_del.molecular_impact == MolecularImpact.IN_FRAME_INDEL

    # Codon 2-3 splitting deletion: c.5_7del (TGC).
    # Codon 2 (GTG) + Codon 3 (CAT) -> G + AT = GAT (Asp).
    res_split = evaluate_indel(5, 7, "deletion", "TGC", "-", ref)
    assert res_split.hgvs_p == "p.Val2_His3delinsAsp"
    assert res_split.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_in_frame_indel_near_cds_end():
    ref = load_reference("NM_000518.5")
    # Codon 146: c.436_438 is TAT (Tyr). Clean 3bp deletion near end.
    res_del = evaluate_indel(436, 438, "deletion", "TAT", "-", ref)
    assert res_del.hgvs_p == "p.Tyr146del"
    assert res_del.molecular_impact == MolecularImpact.IN_FRAME_INDEL

    # Insertion between codon 145 (Lys) and 146 (Tyr): c.435_436insGCC (Ala).
    res_ins = evaluate_indel(435, 436, "insertion", "-", "GCC", ref)
    assert res_ins.hgvs_p == "p.Lys145_Tyr146insAla"
    assert res_ins.molecular_impact == MolecularImpact.IN_FRAME_INDEL


def test_naive_vs_junction_translation_discrepancy():
    ref = load_reference("NM_000518.5")
    # Discrepancy 1: c.53_55del
    # Naive logic: outputs p.Lys18_Val19del (claiming two deleted amino acids).
    # Biologically correct junction translation: p.Lys18_Val19delinsMet (chimeric codon formed).
    res1 = evaluate_indel(53, 55, "deletion", "AGG", "-", ref)
    assert res1.hgvs_p == "p.Lys18_Val19delinsMet"
    assert res1.hgvs_p != "p.Lys18_Val19del"

    # Discrepancy 2: c.53_54insTTT
    # Naive logic: outputs p.Lys18_Val19insPhe (claiming clean insertion between codon 18 and 19).
    # Biologically correct junction translation: p.Lys18delinsAsnLeu (codon 18 split into Asn and Leu).
    res2 = evaluate_indel(53, 54, "insertion", "-", "TTT", ref)
    assert res2.hgvs_p == "p.Lys18delinsAsnLeu"
    assert res2.hgvs_p != "p.Lys18_Val19insPhe"

