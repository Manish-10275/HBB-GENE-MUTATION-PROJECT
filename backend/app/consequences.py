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
    elif op == "delins":
        del_len = c_end - c_start + 1
        ins_len = len(alt_allele)
        mut_seq = full_seq[:c_start - 1] + alt_allele + full_seq[c_end:]
        net_delta = ins_len - del_len
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
        # In-frame change (Option 2 Candidate v3: Full mutant translation, HGVS 3'-shifting, principled stop-loss, and robust prefix/suffix alignment)
        cds_len = len(cds_sequence)
        if c_start < 1 or c_end < 1 or c_start > cds_len or c_end > cds_len or c_start > c_end:
            return None, "Invalid In-frame Indel", None

        if cds_len % 3 != 0:
            return None, "Invalid Reference Sequence", None

        # Build full sequence including 3' UTR for stop-loss and downstream read-through
        full_seq = cds_sequence + (utr3_sequence or "")

        def _translate_to_stop(seq: str) -> Tuple[List[str], bool]:
            aas = []
            reached = False
            for i in range(0, len(seq) - 2, 3):
                codon = seq[i : i + 3]
                aa = translate_codon(codon)[0]
                aas.append(aa)
                if aa == "Ter":
                    reached = True
                    break
            return aas, reached

        wt_protein = [translate_codon(cds_sequence[i : i + 3])[0] for i in range(0, cds_len - 2, 3)]
        if not wt_protein or wt_protein[-1] != "Ter":
            return None, "Invalid Reference Sequence", None

        wt_stop_pos = len(wt_protein)

        try:
            # 1. cDNA 3'-shifting and mutant sequence reconstruction
            if op == "duplication":
                dup_len = c_end - c_start + 1
                pos = c_end
                s_start, s_end = c_start, c_end
                while pos < cds_len and cds_sequence[pos] == cds_sequence[pos - dup_len]:
                    pos += 1
                    s_start += 1
                    s_end += 1
                dup_seq_sh = cds_sequence[s_start - 1 : s_end]
                mut_seq = full_seq[:s_end] + dup_seq_sh + full_seq[s_end:]
            elif op == "deletion":
                del_len = c_end - c_start + 1
                pos = c_end
                s_start, s_end = c_start, c_end
                while pos < cds_len and cds_sequence[pos] == cds_sequence[s_start - 1]:
                    pos += 1
                    s_start += 1
                    s_end += 1
                mut_seq = full_seq[:s_start - 1] + full_seq[s_end:]
            elif op == "delins":
                mut_seq = full_seq[:c_start - 1] + alt_allele.upper() + full_seq[c_end:]
            elif op == "insertion":
                mut_seq = full_seq[:c_start] + alt_allele.upper() + full_seq[c_start:]
            else:
                return None, "Unknown Indel", None

            mut_protein, reached_stop = _translate_to_stop(mut_seq)

            delta_codons = net_delta // 3
            expected_stop = wt_stop_pos + delta_codons

            # 2. Check for premature stop codon (PTC / Nonsense)
            if reached_stop and len(mut_protein) < expected_stop:
                codon_pos = len(mut_protein)
                wt_aa = wt_protein[codon_pos - 1] if codon_pos <= len(wt_protein) else "Ter"
                hgvs_p = f"p.{wt_aa}{codon_pos}Ter"
                return hgvs_p, "Nonsense", hgvs_p

            # 3. Check for Stop Loss (Terminal Extension into 3' UTR)
            # Occurs when translation fails to stop at pos <= expected_stop (reads past normal stop)
            if (not reached_stop) or (len(mut_protein) > expected_stop):
                if reached_stop:
                    new_stop_pos = len(mut_protein)
                    first_ext_aa = mut_protein[wt_stop_pos - 1] if len(mut_protein) >= wt_stop_pos else "Ter"
                    ext_dist = new_stop_pos - wt_stop_pos
                    if ext_dist > 0:
                        hgvs_p = f"p.Ter{wt_stop_pos}{first_ext_aa}extTer{ext_dist}"
                        return hgvs_p, "Extension", hgvs_p
                else:
                    # Transcript sequence ended without reaching a stop codon (e.g. CDS-only or truncated 3' UTR)
                    hgvs_p = f"p.Ter{wt_stop_pos}extTer?"
                    return hgvs_p, "Incomplete Sequence", hgvs_p

            # 4. Check for pure in-frame tandem duplication
            if op == "duplication":
                num_aa = (c_end - c_start + 1) // 3
                best_p_end = None
                for end_idx in range(len(mut_protein) - 1, num_aa - 1, -1):
                    block1 = mut_protein[end_idx - 2 * num_aa + 1 : end_idx - num_aa + 1]
                    block2 = mut_protein[end_idx - num_aa + 1 : end_idx + 1]
                    if block1 == block2 and "Ter" not in block1:
                        reconstructed = mut_protein[:end_idx - num_aa + 1] + mut_protein[end_idx + 1:]
                        if reconstructed == wt_protein:
                            best_p_end = end_idx - num_aa + 1
                            break

                if best_p_end is not None:
                    p_start = best_p_end - num_aa + 1
                    if num_aa == 1:
                        hgvs_p = f"p.{wt_protein[p_start - 1]}{p_start}dup"
                    else:
                        hgvs_p = f"p.{wt_protein[p_start - 1]}{p_start}_{wt_protein[best_p_end - 1]}{best_p_end}dup"
                    return hgvs_p, "In-frame Duplication", hgvs_p

            # 5. Check for pure in-frame deletion
            if op == "deletion":
                num_aa = (c_end - c_start + 1) // 3
                best_p_start = None
                for start_idx in range(len(wt_protein) - num_aa, -1, -1):
                    test_mut = wt_protein[:start_idx] + wt_protein[start_idx + num_aa:]
                    if test_mut == mut_protein:
                        best_p_start = start_idx + 1
                        break

                if best_p_start is not None:
                    p_end = best_p_start + num_aa - 1
                    if num_aa == 1:
                        hgvs_p = f"p.{wt_protein[best_p_start - 1]}{best_p_start}del"
                    else:
                        hgvs_p = f"p.{wt_protein[best_p_start - 1]}{best_p_start}_{wt_protein[p_end - 1]}{p_end}del"
                    return hgvs_p, "In-frame Deletion", hgvs_p

            # 6. General prefix / suffix alignment fallback (replaces unsafe naive coordinate fallback)
            # Handles hybrid codon events (e.g. c.5_7del -> p.Val2_His3delinsAsp, c.6_8dup -> p.Val2_His3insGln)
            # and clean delins.
            pfx = 0
            while pfx < len(wt_protein) and pfx < len(mut_protein) and wt_protein[pfx] == mut_protein[pfx]:
                pfx += 1

            sfx = 0
            while (
                sfx < len(wt_protein) - pfx
                and sfx < len(mut_protein) - pfx
                and wt_protein[len(wt_protein) - 1 - sfx] == mut_protein[len(mut_protein) - 1 - sfx]
            ):
                sfx += 1

            wt_diff = wt_protein[pfx : len(wt_protein) - sfx]
            mut_diff = mut_protein[pfx : len(mut_protein) - sfx]

            if not wt_diff and not mut_diff:
                return "p.(=)", "Synonymous", "p.(=)"

            if wt_diff and not mut_diff:
                start_p = pfx + 1
                end_p = pfx + len(wt_diff)
                if len(wt_diff) == 1:
                    hgvs_p = f"p.{wt_diff[0]}{start_p}del"
                else:
                    hgvs_p = f"p.{wt_diff[0]}{start_p}_{wt_diff[-1]}{end_p}del"
                return hgvs_p, "In-frame Deletion", hgvs_p

            if not wt_diff and mut_diff:
                k = len(mut_diff)
                if pfx >= k and wt_protein[pfx - k : pfx] == mut_diff:
                    dup_start = pfx - k + 1
                    dup_end = pfx
                    hgvs_p = f"p.{mut_diff[0]}{pfx}dup" if k == 1 else f"p.{mut_diff[0]}{dup_start}_{mut_diff[-1]}{dup_end}dup"
                    return hgvs_p, "In-frame Duplication", hgvs_p
                left_pos = pfx
                right_pos = pfx + 1
                ins_str = "".join(mut_diff)
                left_aa = wt_protein[left_pos - 1] if left_pos > 0 else "Met"
                right_aa = wt_protein[right_pos - 1] if right_pos <= len(wt_protein) else "Ter"
                hgvs_p = f"p.{left_aa}{left_pos}_{right_aa}{right_pos}ins{ins_str}"
                return hgvs_p, "In-frame Insertion", hgvs_p

            if wt_diff and mut_diff:
                start_p = pfx + 1
                end_p = pfx + len(wt_diff)
                mut_str = "".join(mut_diff)
                if len(wt_diff) == 1 and len(mut_diff) == 1:
                    hgvs_p = f"p.{wt_diff[0]}{start_p}{mut_diff[0]}"
                elif len(wt_diff) == 1:
                    hgvs_p = f"p.{wt_diff[0]}{start_p}delins{mut_str}"
                else:
                    hgvs_p = f"p.{wt_diff[0]}{start_p}_{wt_diff[-1]}{end_p}delins{mut_str}"
                return hgvs_p, "In-frame Indel", hgvs_p

        except (ValueError, IndexError, KeyError):
            return None, "Invalid In-frame Indel", None

        return None, "Unsupported In-frame Indel", None
