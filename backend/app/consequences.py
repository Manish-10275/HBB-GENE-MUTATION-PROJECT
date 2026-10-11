"""Deterministic codon translation and protein consequence evaluation."""

from typing import Dict, Optional, Tuple
from app.models import CodonChange

# Standard Genetic Code Table (NCBI translation table 1)
CODON_TABLE: Dict[str, Tuple[str, str]] = {
    "TTT": ("Phe", "F"), "TTC": ("Phe", "F"),
    "TTA": ("Leu", "L"), "TTG": ("Leu", "L"),
    "CTT": ("Leu", "L"), "CTC": ("Leu", "L"), "CTA": ("Leu", "L"), "CTG": ("Leu", "L"),
    "ATT": ("Ile", "I"), "ATC": ("Ile", "I"), "ATA": ("Ile", "I"),
    "ATG": ("Met", "M"),
    "GTT": ("Val", "V"), "GTC": ("Val", "V"), "GTA": ("Val", "V"), "GTG": ("Val", "V"),
    "TCT": ("Ser", "S"), "TCC": ("Ser", "S"), "TCA": ("Ser", "S"), "TCG": ("Ser", "S"),
    "CCT": ("Pro", "P"), "CCC": ("Pro", "P"), "CCA": ("Pro", "P"), "CCG": ("Pro", "P"),
    "ACT": ("Thr", "T"), "ACC": ("Thr", "T"), "ACA": ("Thr", "T"), "ACG": ("Thr", "T"),
    "GCT": ("Ala", "A"), "GCC": ("Ala", "A"), "GCA": ("Ala", "A"), "GCG": ("Ala", "A"),
    "TAT": ("Tyr", "Y"), "TAC": ("Tyr", "Y"),
    "TAA": ("Ter", "*"), "TAG": ("Ter", "*"), "TGA": ("Ter", "*"),
    "CAT": ("His", "H"), "CAC": ("His", "H"),
    "CAA": ("Gln", "Q"), "CAG": ("Gln", "Q"),
    "AAT": ("Asn", "N"), "AAC": ("Asn", "N"),
    "AAA": ("Lys", "K"), "AAG": ("Lys", "K"),
    "GAT": ("Asp", "D"), "GAC": ("Asp", "D"),
    "GAA": ("Glu", "E"), "GAG": ("Glu", "E"),
    "TGT": ("Cys", "C"), "TGC": ("Cys", "C"),
    "TGG": ("Trp", "W"),
    "CGT": ("Arg", "R"), "CGC": ("Arg", "R"), "CGA": ("Arg", "R"), "CGG": ("Arg", "R"),
    "AGT": ("Ser", "S"), "AGC": ("Ser", "S"),
    "AGA": ("Arg", "R"), "AGG": ("Arg", "R"),
    "GGT": ("Gly", "G"), "GGC": ("Gly", "G"), "GGA": ("Gly", "G"), "GGG": ("Gly", "G"),
}


def translate_codon(codon: str) -> Tuple[str, str]:
    """Translates a 3-nucleotide codon into (ThreeLetter, OneLetter) amino acid."""
    cleaned = codon.upper()
    return CODON_TABLE.get(cleaned, ("Unknown", "?"))


def evaluate_substitution_codon_consequence(
    c_pos: int,
    ref_base: str,
    alt_base: str,
    cds_sequence: str
) -> Tuple[Optional[CodonChange], Optional[str], str]:
    """
    Deterministically computes codon-level change and protein consequence for a coding substitution.

    Parameters:
    - c_pos: 1-based coding nucleotide coordinate (1 to len(cds_sequence))
    - ref_base: reference nucleotide
    - alt_base: alternate sample nucleotide
    - cds_sequence: complete reference coding DNA sequence

    Returns:
    - CodonChange model
    - hgvs_p string (e.g. "p.Gln40Ter")
    - functional_impact string ("Nonsense", "Missense", "Synonymous", etc.)
    """
    if c_pos < 1 or c_pos > len(cds_sequence):
        return None, None, "Non-coding"

    codon_number = ((c_pos - 1) // 3) + 1
    codon_start_idx = (codon_number - 1) * 3
    codon_end_idx = codon_start_idx + 3

    if codon_end_idx > len(cds_sequence):
        return None, None, "Boundary Error"

    ref_triplet = cds_sequence[codon_start_idx:codon_end_idx]
    base_offset_in_triplet = (c_pos - 1) % 3

    sample_triplet = (
        ref_triplet[:base_offset_in_triplet]
        + alt_base
        + ref_triplet[base_offset_in_triplet + 1:]
    )

    ref_aa_3, ref_aa_1 = translate_codon(ref_triplet)
    sample_aa_3, sample_aa_1 = translate_codon(sample_triplet)

    is_stop_gain = (ref_aa_3 != "Ter" and sample_aa_3 == "Ter")
    is_stop_loss = (ref_aa_3 == "Ter" and sample_aa_3 != "Ter")
    is_synonymous = (ref_aa_3 == sample_aa_3)

    if is_stop_gain:
        consequence_desc = f"Nonsense (p.{ref_aa_3}{codon_number}Ter)"
        impact = "Nonsense"
        hgvs_p = f"p.{ref_aa_3}{codon_number}Ter"
    elif is_stop_loss:
        consequence_desc = f"Stop Loss (p.{ref_aa_3}{codon_number}{sample_aa_3}ext*?)"
        impact = "Stop Loss"
        hgvs_p = f"p.{ref_aa_3}{codon_number}{sample_aa_3}ext*?"
    elif is_synonymous:
        consequence_desc = f"Synonymous (p.{ref_aa_3}{codon_number}=)"
        impact = "Synonymous"
        hgvs_p = f"p.(=)"
    else:
        consequence_desc = f"Missense (p.{ref_aa_3}{codon_number}{sample_aa_3})"
        impact = "Missense"
        hgvs_p = f"p.{ref_aa_3}{codon_number}{sample_aa_3}"

    c_start = (codon_number - 1) * 3 + 1
    c_end = codon_number * 3

    codon_change = CodonChange(
        codon_number=codon_number,
        c_start=c_start,
        c_end=c_end,
        ref_codon=ref_triplet,
        sample_codon=sample_triplet,
        ref_aa=ref_aa_3,
        sample_aa=sample_aa_3,
        ref_aa_single=ref_aa_1,
        sample_aa_single=sample_aa_1,
        consequence=consequence_desc,
        is_stop_gain=is_stop_gain,
        is_stop_loss=is_stop_loss,
        is_synonymous=is_synonymous
    )

    return codon_change, hgvs_p, impact


def evaluate_indel_codon_consequence(
    c_start: int,
    c_end: int,
    op: str,  # "deletion", "insertion", "duplication"
    ref_allele: str,
    alt_allele: str,
    cds_sequence: str,
    utr3_sequence: str = ""
) -> Tuple[Optional[str], str, Optional[str]]:
    """
    Deterministically computes codon-level change and protein consequence for an indel in the coding region.

    Parameters:
    - c_start: 1-based coding nucleotide start coordinate (1..len(cds_sequence))
    - c_end: 1-based coding nucleotide end coordinate (1..len(cds_sequence))
    - op: "deletion", "insertion", or "duplication"
    - ref_allele: deleted bases (or "-" for insertion)
    - alt_allele: inserted bases (or "-" for deletion)
    - cds_sequence: complete reference coding DNA sequence (e.g. 444 bp)
    - utr3_sequence: complete 3' UTR sequence for reading past codon 147

    Returns:
    - hgvs_p: canonical HGVS protein string (e.g. "p.Phe42LeufsTer19", "p.Ser10ValfsTer14", "p.Leu4Ter", "p.Phe43del")
    - functional_impact: "Frameshift Deletion", "Frameshift Insertion", "In-frame Deletion", etc.
    - hgvs_p_short: optional abbreviated notation (e.g. "p.Phe42fs", "p.Ser10fs")
    """
    full_seq = cds_sequence + utr3_sequence
    if op == "deletion":
        del_len = c_end - c_start + 1
        mut_seq = full_seq[:c_start - 1] + full_seq[c_end:]
        net_delta = -del_len
    elif op == "insertion":
        ins_len = len(alt_allele)
        mut_seq = full_seq[:c_start] + alt_allele + full_seq[c_start:]
        net_delta = ins_len
    elif op == "duplication":
        dup_len = c_end - c_start + 1
        dup_seq = full_seq[c_start - 1 : c_end]
        mut_seq = full_seq[:c_end] + dup_seq + full_seq[c_end:]
        net_delta = dup_len
    else:
        return None, "Unknown Indel", None

    if net_delta % 3 != 0:
        # Frameshift translation
        first_codon = ((c_start - 1) // 3) + 1
        curr_codon = first_codon
        first_altered = None
        first_wt_aa = None
        first_mut_aa = None

        while (curr_codon * 3) <= len(mut_seq) and (curr_codon * 3) <= len(cds_sequence):
            wt_trip = cds_sequence[(curr_codon - 1) * 3 : curr_codon * 3]
            mut_trip = mut_seq[(curr_codon - 1) * 3 : curr_codon * 3]
            wt_aa = translate_codon(wt_trip)[0]
            mut_aa = translate_codon(mut_trip)[0]
            if wt_aa != mut_aa:
                first_altered = curr_codon
                first_wt_aa = wt_aa
                first_mut_aa = mut_aa
                break
            curr_codon += 1

        if first_altered is None:
            first_altered = curr_codon
            if (first_altered - 1) * 3 < len(cds_sequence):
                first_wt_aa = translate_codon(cds_sequence[(first_altered - 1) * 3 : first_altered * 3])[0]
            else:
                first_wt_aa = "Ter"
            first_mut_aa = translate_codon(mut_seq[(first_altered - 1) * 3 : first_altered * 3])[0]

        if first_mut_aa == "Ter":
            hgvs_p = f"p.{first_wt_aa}{first_altered}Ter"
            hgvs_p_short = f"p.{first_wt_aa}{first_altered}fs"
            impact = f"Frameshift {op.capitalize()} (Immediate Termination)"
            return hgvs_p, impact, hgvs_p_short

        stop_codon_num = None
        walk = first_altered + 1
        while (walk * 3) <= len(mut_seq):
            trip = mut_seq[(walk - 1) * 3 : walk * 3]
            aa = translate_codon(trip)[0]
            if aa == "Ter":
                stop_codon_num = walk
                break
            walk += 1

        if stop_codon_num is not None:
            dist = (stop_codon_num - first_altered) + 1
            hgvs_p = f"p.{first_wt_aa}{first_altered}{first_mut_aa}fsTer{dist}"
            hgvs_p_short = f"p.{first_wt_aa}{first_altered}fs"
        else:
            hgvs_p = f"p.{first_wt_aa}{first_altered}{first_mut_aa}fsTer?"
            hgvs_p_short = f"p.{first_wt_aa}{first_altered}fs"
        impact = f"Frameshift {op.capitalize()}"
        return hgvs_p, impact, hgvs_p_short
    else:
        # In-frame change
        if op == "deletion":
            del_aa_start = ((c_start - 1) // 3) + 1
            del_aa_end = ((c_end - 1) // 3) + 1
            wt_start_aa = translate_codon(cds_sequence[(del_aa_start - 1) * 3 : del_aa_start * 3])[0]
            if del_aa_start == del_aa_end:
                hgvs_p = f"p.{wt_start_aa}{del_aa_start}del"
            else:
                wt_end_aa = translate_codon(cds_sequence[(del_aa_end - 1) * 3 : del_aa_end * 3])[0]
                hgvs_p = f"p.{wt_start_aa}{del_aa_start}_{wt_end_aa}{del_aa_end}del"
            return hgvs_p, "In-frame Deletion", hgvs_p
        elif op == "duplication":
            dup_aa_start = ((c_start - 1) // 3) + 1
            dup_aa_end = ((c_end - 1) // 3) + 1
            wt_start_aa = translate_codon(cds_sequence[(dup_aa_start - 1) * 3 : dup_aa_start * 3])[0]
            if dup_aa_start == dup_aa_end:
                hgvs_p = f"p.{wt_start_aa}{dup_aa_start}dup"
            else:
                wt_end_aa = translate_codon(cds_sequence[(dup_aa_end - 1) * 3 : dup_aa_end * 3])[0]
                hgvs_p = f"p.{wt_start_aa}{dup_aa_start}_{wt_end_aa}{dup_aa_end}dup"
            return hgvs_p, "In-frame Duplication", hgvs_p
        elif op == "insertion":
            flank_left_aa = ((c_start - 1) // 3) + 1
            flank_right_aa = flank_left_aa + 1
            wt_left = translate_codon(cds_sequence[(flank_left_aa - 1) * 3 : flank_left_aa * 3])[0]
            wt_right = translate_codon(cds_sequence[(flank_right_aa - 1) * 3 : flank_right_aa * 3])[0]
            ins_aa_list = [translate_codon(alt_allele[k * 3 : (k + 1) * 3])[0] for k in range(len(alt_allele) // 3)]
            ins_aa_str = "".join(ins_aa_list)
            hgvs_p = f"p.{wt_left}{flank_left_aa}_{wt_right}{flank_right_aa}ins{ins_aa_str}"
            return hgvs_p, "In-frame Insertion", hgvs_p
        return None, "In-frame Variant", None
