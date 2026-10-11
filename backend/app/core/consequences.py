"""Deterministic codon translation and protein consequence evaluation for HBB."""

from typing import Dict, List, Optional, Tuple

from app.core.models import (
    AnalysisError,
    AnalysisErrorCode,
    CodonChange,
    ConsequenceResult,
    MolecularImpact,
    NormalizedVariant,
    VariantType,
)
from app.core.reference import ReferenceSequence

# Standard Genetic Code Table (NCBI Translation Table 1)
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


def evaluate_substitution(
    c_pos: int,
    ref_base: str,
    alt_base: str,
    ref_seq: ReferenceSequence,
) -> ConsequenceResult:
    """
    Deterministically computes codon-level change and protein consequence for a coding substitution.
    
    Parameters:
    - c_pos: 1-based coding nucleotide coordinate (1 to ref_seq.cds_length)
    - ref_base: reference nucleotide
    - alt_base: alternate nucleotide
    - ref_seq: ReferenceSequence object
    """
    cds = ref_seq.cds_sequence
    if c_pos < 1 or c_pos > len(cds):
        raise AnalysisError(
            AnalysisErrorCode.OUT_OF_BOUNDS,
            f"cDNA coordinate c.{c_pos} is outside coding region (1..{len(cds)})."
        )

    codon_number = ((c_pos - 1) // 3) + 1
    codon_start_idx = (codon_number - 1) * 3
    codon_end_idx = codon_start_idx + 3

    if codon_end_idx > len(cds):
        raise AnalysisError(
            AnalysisErrorCode.OUT_OF_BOUNDS,
            f"Codon {codon_number} extends beyond CDS end."
        )

    ref_triplet = cds[codon_start_idx:codon_end_idx]
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

    # HGVS p. nomenclature determination
    if codon_number == 1 and ref_aa_3 == "Met" and sample_aa_3 != "Met":
        # Initiation codon mutation (translation initiation affected)
        hgvs_p = "p.Met1?"
        impact = MolecularImpact.MISSENSE
        consequence_desc = f"Initiation Codon Disruption ({hgvs_p})"
    elif is_stop_gain:
        hgvs_p = f"p.{ref_aa_3}{codon_number}Ter"
        impact = MolecularImpact.NONSENSE
        consequence_desc = f"Nonsense ({hgvs_p})"
    elif is_stop_loss:
        hgvs_p = f"p.{ref_aa_3}{codon_number}{sample_aa_3}ext*?"
        impact = MolecularImpact.UNKNOWN
        consequence_desc = f"Stop Loss ({hgvs_p})"
    elif is_synonymous:
        hgvs_p = "p.(=)"
        impact = MolecularImpact.SYNONYMOUS
        consequence_desc = f"Synonymous (p.{ref_aa_3}{codon_number}=)"
    else:
        hgvs_p = f"p.{ref_aa_3}{codon_number}{sample_aa_3}"
        impact = MolecularImpact.MISSENSE
        consequence_desc = f"Missense ({hgvs_p})"

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
        is_synonymous=is_synonymous,
    )

    return ConsequenceResult(
        hgvs_p=hgvs_p,
        molecular_impact=impact,
        codon_change=codon_change,
        ptc_coordinate=codon_number if is_stop_gain else None,
        confidence="Deterministic",
    )


def evaluate_indel(
    c_start: int,
    c_end: int,
    op: str,  # "deletion", "insertion", "duplication"
    ref_allele: str,
    alt_allele: str,
    ref_seq: ReferenceSequence,
) -> ConsequenceResult:
    """
    Deterministically computes codon-level change and protein consequence for an indel in the coding region.
    
    Walks downstream altered frame to first termination codon to compute canonical HGVS p.
    """
    cds = ref_seq.cds_sequence
    utr3 = ref_seq.sequence[ref_seq.cds_end:]
    full_seq = cds + utr3

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
        raise AnalysisError(
            AnalysisErrorCode.UNSUPPORTED_VARIANT,
            f"Unsupported indel operation '{op}'."
        )

    # 1. Frameshift Indel (net delta not divisible by 3)
    if net_delta % 3 != 0:
        first_codon = ((c_start - 1) // 3) + 1
        curr_codon = first_codon
        first_altered = None
        first_wt_aa = None
        first_mut_aa = None

        while (curr_codon * 3) <= len(mut_seq) and (curr_codon * 3) <= len(cds):
            wt_trip = cds[(curr_codon - 1) * 3 : curr_codon * 3]
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
            if (first_altered - 1) * 3 < len(cds):
                first_wt_aa = translate_codon(cds[(first_altered - 1) * 3 : first_altered * 3])[0]
            else:
                first_wt_aa = "Ter"
            first_mut_aa = translate_codon(mut_seq[(first_altered - 1) * 3 : first_altered * 3])[0]

        # Immediate stop codon
        if first_mut_aa == "Ter":
            hgvs_p = f"p.{first_wt_aa}{first_altered}Ter"
            return ConsequenceResult(
                hgvs_p=hgvs_p,
                molecular_impact=MolecularImpact.FRAMESHIFT,
                ptc_coordinate=first_altered,
                confidence="Deterministic",
            )

        # Walk downstream to find premature termination codon (PTC)
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
            ptc_coord = stop_codon_num
        else:
            hgvs_p = f"p.{first_wt_aa}{first_altered}{first_mut_aa}fsTer?"
            ptc_coord = None

        return ConsequenceResult(
            hgvs_p=hgvs_p,
            molecular_impact=MolecularImpact.FRAMESHIFT,
            ptc_coordinate=ptc_coord,
            confidence="Deterministic",
        )

    # 2. In-Frame Indel (net delta divisible by 3)
    def _translate_to_protein(seq: str) -> List[str]:
        aas = []
        for i in range(0, len(seq) - 2, 3):
            codon = seq[i : i + 3]
            aa3 = translate_codon(codon)[0]
            aas.append(aa3)
            if aa3 == "Ter":
                break
        return aas

    wt_protein = _translate_to_protein(full_seq)
    mut_protein = _translate_to_protein(mut_seq)

    delta_codons = net_delta // 3
    expected_stop = len(wt_protein) + delta_codons

    if mut_protein and mut_protein[-1] == "Ter" and len(mut_protein) < expected_stop:
        codon_pos = len(mut_protein)
        wt_aa = wt_protein[codon_pos - 1] if codon_pos <= len(wt_protein) else "Ter"
        return ConsequenceResult(
            hgvs_p=f"p.{wt_aa}{codon_pos}Ter",
            molecular_impact=MolecularImpact.NONSENSE,
            ptc_coordinate=codon_pos,
            confidence="Deterministic",
        )

    # Prefix match
    pfx = 0
    while pfx < len(wt_protein) and pfx < len(mut_protein) and wt_protein[pfx] == mut_protein[pfx]:
        pfx += 1

    # Suffix match
    sfx = 0
    while (
        (sfx < len(wt_protein) - pfx)
        and (sfx < len(mut_protein) - pfx)
        and wt_protein[len(wt_protein) - 1 - sfx] == mut_protein[len(mut_protein) - 1 - sfx]
    ):
        sfx += 1

    wt_diff = wt_protein[pfx : len(wt_protein) - sfx]
    mut_diff = mut_protein[pfx : len(mut_protein) - sfx]

    if len(wt_diff) == 0 and len(mut_diff) == 0:
        return ConsequenceResult(
            hgvs_p="p.(=)",
            molecular_impact=MolecularImpact.SYNONYMOUS,
            confidence="Deterministic",
        )

    if len(wt_diff) > 0 and len(mut_diff) == 0:
        # Pure deletion
        start_pos = pfx + 1
        end_pos = pfx + len(wt_diff)
        if len(wt_diff) == 1:
            hgvs_p = f"p.{wt_diff[0]}{start_pos}del"
        else:
            hgvs_p = f"p.{wt_diff[0]}{start_pos}_{wt_diff[-1]}{end_pos}del"
        return ConsequenceResult(
            hgvs_p=hgvs_p,
            molecular_impact=MolecularImpact.IN_FRAME_INDEL,
            confidence="Deterministic",
        )

    if len(wt_diff) == 0 and len(mut_diff) > 0:
        # Pure insertion or duplication
        left_pos = pfx
        right_pos = pfx + 1
        k = len(mut_diff)
        if left_pos >= k and wt_protein[pfx - k : pfx] == mut_diff:
            dup_start = pfx - k + 1
            dup_end = pfx
            if k == 1:
                hgvs_p = f"p.{mut_diff[0]}{pfx}dup"
            else:
                hgvs_p = f"p.{mut_diff[0]}{dup_start}_{mut_diff[-1]}{dup_end}dup"
        else:
            ins_str = "".join(mut_diff)
            left_aa = wt_protein[left_pos - 1] if left_pos > 0 else "Met"
            right_aa = wt_protein[right_pos - 1] if right_pos <= len(wt_protein) else "Ter"
            hgvs_p = f"p.{left_aa}{left_pos}_{right_aa}{right_pos}ins{ins_str}"
        return ConsequenceResult(
            hgvs_p=hgvs_p,
            molecular_impact=MolecularImpact.IN_FRAME_INDEL,
            confidence="Deterministic",
        )

    if len(wt_diff) > 0 and len(mut_diff) > 0:
        # Deletion-insertion (delins)
        start_pos = pfx + 1
        end_pos = pfx + len(wt_diff)
        mut_str = "".join(mut_diff)
        if len(wt_diff) == 1:
            hgvs_p = f"p.{wt_diff[0]}{start_pos}delins{mut_str}"
        else:
            hgvs_p = f"p.{wt_diff[0]}{start_pos}_{wt_diff[-1]}{end_pos}delins{mut_str}"
        return ConsequenceResult(
            hgvs_p=hgvs_p,
            molecular_impact=MolecularImpact.IN_FRAME_INDEL,
            confidence="Deterministic",
        )

    return ConsequenceResult(
        hgvs_p=None,
        molecular_impact=MolecularImpact.UNKNOWN,
        confidence="Deterministic",
    )


def evaluate_consequence(
    variant: NormalizedVariant,
    ref_seq: ReferenceSequence,
) -> ConsequenceResult:
    """Dispatches consequence evaluation based on region and variant structure."""
    if variant.variant_type == VariantType.SPLICE:
        return ConsequenceResult(
            hgvs_p="p.?",
            molecular_impact=MolecularImpact.SPLICE_DISRUPTION,
            confidence="Deterministic",
        )

    if variant.variant_type == VariantType.REGULATORY_UTR:
        impact = (
            MolecularImpact.REGULATORY_5_UTR
            if "5'" in variant.region
            else MolecularImpact.REGULATORY_3_UTR
        )
        return ConsequenceResult(
            hgvs_p=None,
            molecular_impact=impact,
            confidence="Deterministic",
        )

    # Exonic coding variant
    if variant.variant_type == VariantType.SUBSTITUTION:
        try:
            c_num = int(variant.c_position)
            return evaluate_substitution(c_num, variant.ref_allele, variant.alt_allele, ref_seq)
        except ValueError:
            # Fallback if non-numeric
            return ConsequenceResult(hgvs_p=None, molecular_impact=MolecularImpact.UNKNOWN)

    if variant.variant_type in (VariantType.DELETION, VariantType.INSERTION, VariantType.DUPLICATION):
        # Parse range or single pos
        c_pos = variant.c_position
        if "_" in c_pos:
            s_str, e_str = c_pos.split("_", 1)
        else:
            s_str, e_str = c_pos, c_pos
        try:
            c_start = int(s_str)
            c_end = int(e_str)
            return evaluate_indel(
                c_start,
                c_end,
                variant.variant_type.value,
                variant.ref_allele,
                variant.alt_allele,
                ref_seq,
            )
        except ValueError:
            return ConsequenceResult(hgvs_p=None, molecular_impact=MolecularImpact.UNKNOWN)

    return ConsequenceResult(hgvs_p=None, molecular_impact=MolecularImpact.UNKNOWN)
