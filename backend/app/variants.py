"""Deterministic variant detection, HGVS coordinate mapping, and classification."""

import re
from typing import List, Optional, Tuple
from app.models import CodonChange, DetectedVariant
from app.reference import ReferenceData
from app.consequences import evaluate_substitution_codon_consequence


def detect_variants(
    aligned_ref: str,
    aligned_query: str,
    ref_data: ReferenceData
) -> List[DetectedVariant]:
    """
    Scans aligned sequences and identifies all nucleotide variants.
    Deterministically computes coordinates, HGVS c. and p. notations, and codon consequences.
    """
    variants: List[DetectedVariant] = []
    i = 0
    align_len = len(aligned_ref)

    ref_mrna_pos = 0  # 1-based non-gap reference mRNA coordinate

    while i < align_len:
        r = aligned_ref[i]
        q = aligned_query[i]

        if r != "-":
            ref_mrna_pos += 1

        # Case 1: Match
        if r == q:
            i += 1
            continue

        # Case 2: Single Nucleotide Substitution
        if r != "-" and q != "-":
            c_pos_str = ref_data.mrna_pos_to_c_pos(ref_mrna_pos)
            hgvs_c = f"{ref_data.accession}:c.{c_pos_str}{r}>{q}"

            codon_change: Optional[CodonChange] = None
            hgvs_p: Optional[str] = None
            impact = "Non-coding"

            # Check if within CDS
            if ref_data.cds_start <= ref_mrna_pos <= ref_data.cds_end:
                try:
                    c_numeric = int(c_pos_str)
                    codon_change, hgvs_p, impact = evaluate_substitution_codon_consequence(
                        c_numeric, r, q, ref_data.cds_sequence
                    )
                except ValueError:
                    impact = "Unknown"
            elif ref_mrna_pos < ref_data.cds_start:
                impact = "5' UTR (Non-coding)"
            else:
                impact = "3' UTR (Non-coding)"

            variants.append(
                DetectedVariant(
                    id=f"var_sub_{ref_mrna_pos}_{r}_{q}",
                    variant_type="substitution",
                    ref_position_mrna=ref_mrna_pos,
                    c_position=c_pos_str,
                    ref_allele=r,
                    alt_allele=q,
                    hgvs_c=hgvs_c,
                    hgvs_p=hgvs_p,
                    codon_change=codon_change,
                    functional_impact=impact,
                    confidence="Deterministic"
                )
            )
            i += 1
            continue

        # Case 3: Deletion in query (gap in query, base in ref)
        if r != "-" and q == "-":
            del_start_mrna = ref_mrna_pos
            del_ref_bases = [r]
            j = i + 1
            while j < align_len and aligned_ref[j] != "-" and aligned_query[j] == "-":
                ref_mrna_pos += 1
                del_ref_bases.append(aligned_ref[j])
                j += 1

            del_end_mrna = ref_mrna_pos
            del_seq = "".join(del_ref_bases)
            del_len = len(del_seq)

            c_start_str = ref_data.mrna_pos_to_c_pos(del_start_mrna)
            c_end_str = ref_data.mrna_pos_to_c_pos(del_end_mrna)

            if del_len == 1:
                hgvs_c = f"{ref_data.accession}:c.{c_start_str}del"
                c_pos_display = c_start_str
            else:
                hgvs_c = f"{ref_data.accession}:c.{c_start_str}_{c_end_str}del"
                c_pos_display = f"{c_start_str}_{c_end_str}"

            # Assess impact
            in_cds = (
                ref_data.cds_start <= del_start_mrna <= ref_data.cds_end
                or ref_data.cds_start <= del_end_mrna <= ref_data.cds_end
            )
            if in_cds:
                impact = "In-frame Deletion" if del_len % 3 == 0 else "Frameshift Deletion"
                hgvs_p = f"p.({c_start_str}del_fs)" if del_len % 3 != 0 else f"p.({c_start_str}del)"
            else:
                impact = "Non-coding Deletion"
                hgvs_p = None

            variants.append(
                DetectedVariant(
                    id=f"var_del_{del_start_mrna}_{del_len}",
                    variant_type="deletion",
                    ref_position_mrna=del_start_mrna,
                    c_position=c_pos_display,
                    ref_allele=del_seq,
                    alt_allele="-",
                    hgvs_c=hgvs_c,
                    hgvs_p=hgvs_p,
                    codon_change=None,
                    functional_impact=impact,
                    confidence="Deterministic"
                )
            )
            i = j
            continue

        # Case 4: Insertion in query (base in query, gap in ref)
        if r == "-" and q != "-":
            ins_bases = [q]
            j = i + 1
            while j < align_len and aligned_ref[j] == "-" and aligned_query[j] != "-":
                ins_bases.append(aligned_query[j])
                j += 1

            ins_seq = "".join(ins_bases)
            ins_len = len(ins_seq)

            # Flanking ref position is the last seen ref_mrna_pos
            flank_left = ref_mrna_pos
            flank_right = ref_mrna_pos + 1

            c_left_str = ref_data.mrna_pos_to_c_pos(flank_left) if flank_left > 0 else "0"
            c_right_str = (
                ref_data.mrna_pos_to_c_pos(flank_right)
                if flank_right <= ref_data.total_length
                else f"*{flank_right - ref_data.cds_end}"
            )

            hgvs_c = f"{ref_data.accession}:c.{c_left_str}_{c_right_str}ins{ins_seq}"
            c_pos_display = f"{c_left_str}_{c_right_str}"

            in_cds = ref_data.cds_start <= flank_left < ref_data.cds_end
            if in_cds:
                impact = "In-frame Insertion" if ins_len % 3 == 0 else "Frameshift Insertion"
                hgvs_p = f"p.({c_left_str}ins_fs)" if ins_len % 3 != 0 else f"p.({c_left_str}ins)"
            else:
                impact = "Non-coding Insertion"
                hgvs_p = None

            variants.append(
                DetectedVariant(
                    id=f"var_ins_{flank_left}_{ins_len}",
                    variant_type="insertion",
                    ref_position_mrna=flank_left,
                    c_position=c_pos_display,
                    ref_allele="-",
                    alt_allele=ins_seq,
                    hgvs_c=hgvs_c,
                    hgvs_p=hgvs_p,
                    codon_change=None,
                    functional_impact=impact,
                    confidence="Deterministic"
                )
            )
            i = j
            continue

        i += 1

    return variants


def parse_hgvs_input(
    raw_query: str,
    ref_data: ReferenceData
) -> Tuple[Optional[DetectedVariant], Optional[str]]:
    """
    Parses an HGVS cDNA query string (e.g. 'NM_000518.5:c.118C>T' or 'c.118C>T' or 'c.20A>T')
    and deterministically reconstructs the DetectedVariant model with codon consequences.
    """
    query = raw_query.strip()
    # Strip optional accession prefix
    if ":" in query:
        _, c_part = query.split(":", 1)
    else:
        c_part = query

    c_part = c_part.strip()
    if not c_part.startswith("c."):
        if re.match(r"^(\*?-?\d+)[A-Z]>[A-Z]$", c_part, re.IGNORECASE):
            c_part = f"c.{c_part}"
        else:
            return None, "Query must follow standard HGVS notation, e.g., 'c.118C>T' or 'NM_000518.5:c.118C>T'."

    # Match substitution pattern: c.118C>T or c.-5A>G or c.*10T>C
    sub_match = re.match(r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$", c_part)
    if sub_match:
        c_pos_str = sub_match.group(1)
        ref_base = sub_match.group(2).upper()
        alt_base = sub_match.group(3).upper()

        mrna_pos = ref_data.c_pos_to_mrna_pos(c_pos_str)
        if mrna_pos is None or mrna_pos < 1 or mrna_pos > ref_data.total_length:
            return None, f"c. position '{c_pos_str}' is out of bounds for reference {ref_data.accession} (length {ref_data.total_length} bp)."

        expected_ref = ref_data.sequence[mrna_pos - 1]
        if expected_ref != ref_base:
            return None, (
                f"Reference base mismatch at c.{c_pos_str}: input states '{ref_base}', "
                f"but reference {ref_data.accession} has '{expected_ref}'."
            )

        codon_change: Optional[CodonChange] = None
        hgvs_p: Optional[str] = None
        impact = "Non-coding"

        if ref_data.cds_start <= mrna_pos <= ref_data.cds_end:
            try:
                c_num = int(c_pos_str)
                codon_change, hgvs_p, impact = evaluate_substitution_codon_consequence(
                    c_num, ref_base, alt_base, ref_data.cds_sequence
                )
            except ValueError:
                pass
        elif mrna_pos < ref_data.cds_start:
            impact = "5' UTR (Non-coding)"
        else:
            impact = "3' UTR (Non-coding)"

        standard_hgvs = f"{ref_data.accession}:c.{c_pos_str}{ref_base}>{alt_base}"
        variant = DetectedVariant(
            id=f"direct_var_{mrna_pos}_{ref_base}_{alt_base}",
            variant_type="substitution",
            ref_position_mrna=mrna_pos,
            c_position=c_pos_str,
            ref_allele=ref_base,
            alt_allele=alt_base,
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=codon_change,
            functional_impact=impact,
            confidence="Deterministic"
        )
        return variant, None

    return None, f"Unsupported HGVS syntax '{raw_query}'. Supported format: 'c.[position][Ref]>[Alt]', e.g. 'c.118C>T'."
