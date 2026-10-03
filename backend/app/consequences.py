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
