"""Deterministic variant detection, HGVS coordinate mapping, and classification."""

import re
from typing import List, Optional, Tuple
from app.models import CodonChange, DetectedVariant
from app.reference import ReferenceData
from app.consequences import evaluate_substitution_codon_consequence


def _map_genomic_to_cdna_pos(rel_pos: int) -> Tuple[str, str, str]:
    """
    Maps 1-based relative position in HBB genomic gene locus (1..1608) to cDNA notation.
    Exon 1: 1..142 (5' UTR 1..50 -> c.-50..c.-1; Coding 51..142 -> c.1..c.92)
    Intron 1: 143..272 (130 bp) -> c.92+1 .. c.92+130
    Exon 2: 273..495 (223 bp) -> c.93 .. c.315
    Intron 2: 496..1345 (850 bp) -> c.315+1 .. c.315+850
    Exon 3: 1346..1608 (263 bp) -> Coding 1346..1474 (c.316..c.444); 3' UTR 1475..1608 (c.*1..c.*134)
    """
    if rel_pos <= 142:
        if rel_pos <= 50:
            c_pos = str(rel_pos - 51)  # e.g. rel_pos 50 -> -1
            return c_pos, "Exon 1 (5' UTR)", "5' UTR (Non-coding)"
        else:
            c_pos = str(rel_pos - 50)  # e.g. rel_pos 51 -> 1
            return c_pos, "Exon 1", "Coding"
    elif 143 <= rel_pos <= 272:
        offset = rel_pos - 142
        c_pos = f"92+{offset}"
        impact = "Splice Site Defect (Intron 1 donor)" if offset in (1, 2, 5) else "Intronic (Non-coding)"
        return c_pos, "Intron 1 (IVS-1)", impact
    elif 273 <= rel_pos <= 495:
        offset = rel_pos - 273
        c_pos = str(93 + offset)
        return c_pos, "Exon 2", "Coding"
    elif 496 <= rel_pos <= 1345:
        offset = rel_pos - 495
        c_pos = f"315+{offset}"
        impact = "Splice Site Defect (Intron 2 donor)" if offset in (1, 2) else "Intronic (Non-coding)"
        return c_pos, "Intron 2 (IVS-2)", impact
    else:
        offset = rel_pos - 1346
        coding_offset = 316 + offset
        if coding_offset <= 444:
            return str(coding_offset), "Exon 3", "Coding"
        else:
            utr_offset = coding_offset - 444
            return f"*{utr_offset}", "Exon 3 (3' UTR)", "3' UTR (Non-coding)"


def get_equivalent_nomenclature(
    c_pos_str: str,
    ref_allele: str,
    alt_allele: str,
    hgvs_p: Optional[str] = None
) -> Tuple[List[str], Optional[str]]:
    """
    Recognizes equivalent historical, clinical, and literature nomenclature
    for canonical HBB mutations.
    """
    aliases: List[str] = []
    notes: Optional[str] = None

    c_pos_clean = c_pos_str.replace("c.", "")

    if c_pos_clean == "118" and ref_allele == "C" and alt_allele == "T":
        aliases = [
            "c.118C>T",
            "NM_000518.5:c.118C>T",
            "p.Gln40Ter",
            "Gln40Ter",
            "Q40*",
            "Q39*",
            "Gln39Ter",
            "p.Gln39Ter",
            "Codon 39 C>T",
            "CD39 C>T",
            "CD39 (C>T)",
            "codon 39 (C->T)",
        ]
        notes = (
            "The apparent codon 39 versus 40 numbering difference arises because historical "
            "biochemical literature numbered the mature circulating beta-globin protein after enzymatic "
            "cleavage of the initiator methionine (Met1, codon 1), whereas standard HGVS reference sequence "
            "nomenclature (NM_000518.5) numbers from the translation initiation codon ATG (codon 1). "
            "Therefore, mature protein residue 39 corresponds to reference transcript codon 40."
        )
    elif c_pos_clean == "20" and ref_allele == "A" and alt_allele == "T":
        aliases = [
            "c.20A>T",
            "NM_000518.5:c.20A>T",
            "p.Glu7Val",
            "Glu7Val",
            "E7V",
            "Glu6Val",
            "E6V",
            "Codon 6 A>T",
            "CD6 A>T",
            "HbS",
            "Sickle Cell",
        ]
        notes = (
            "Historical literature refers to HbS as codon 6 (Glu6Val) based on mature protein numbering, "
            "whereas standard HGVS numbering designates codon 7 (p.Glu7Val) from initiator Met1."
        )
    elif c_pos_clean == "19" and ref_allele == "G" and alt_allele == "A":
        aliases = [
            "c.19G>A",
            "NM_000518.5:c.19G>A",
            "p.Glu7Lys",
            "Glu7Lys",
            "E7K",
            "Glu6Lys",
            "E6K",
            "Codon 6 G>A",
            "CD6 G>A",
            "HbC",
        ]
        notes = (
            "Historical literature designates HbC as codon 6 (Glu6Lys) based on mature protein numbering, "
            "corresponding to HGVS codon 7 (p.Glu7Lys)."
        )
    elif "92+5" in c_pos_clean:
        aliases = ["c.92+5G>C", "IVS-I-5 G>C", "IVS1-5 G>C", "IVS-1-5"]
    elif "92+1" in c_pos_clean:
        aliases = ["c.92+1G>T", "IVS-I-1 G>T", "IVS1-1 G>T", "IVS-1-1"]
    elif "124_127del" in c_pos_clean or "126_129del" in c_pos_clean:
        aliases = ["c.124_127del", "c.126_129del", "Codon 41/42 (-TCTT)", "CD 41/42", "fs 41/42"]
    elif "27dup" in c_pos_clean or "26_27ins" in c_pos_clean:
        aliases = ["c.27dup", "c.26_27insG", "Codon 8/9 (+G)", "CD 8/9 (+G)"]

    return aliases, notes


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
            codon_change: Optional[CodonChange] = None
            hgvs_p: Optional[str] = None

            if ref_data.accession.startswith("NG_"):
                # Genomic locus NG_000007.3:70545..72152
                c_pos_str, region_name, impact = _map_genomic_to_cdna_pos(ref_mrna_pos)
                hgvs_c = f"NM_000518.5:c.{c_pos_str}{r}>{q}"
            else:
                c_pos_str = ref_data.mrna_pos_to_c_pos(ref_mrna_pos)
                hgvs_c = f"{ref_data.accession}:c.{c_pos_str}{r}>{q}"
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

            eq_aliases, eq_notes = get_equivalent_nomenclature(c_pos_str, r, q, hgvs_p)

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
                    confidence="Deterministic",
                    equivalent_nomenclature=eq_aliases,
                    nomenclature_notes=eq_notes
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

            # HGVS 3' rule: shift deletion as far 3' as possible in repetitive regions
            ref_seq = ref_data.sequence
            while del_end_mrna < len(ref_seq) and ref_seq[del_start_mrna - 1] == ref_seq[del_end_mrna]:
                del_start_mrna += 1
                del_end_mrna += 1

            del_seq = ref_seq[del_start_mrna - 1 : del_end_mrna]
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
            ref_seq = ref_data.sequence
            # HGVS 3' rule: shift insertion as far 3' as possible in repetitive regions
            while flank_left < len(ref_seq) and ref_seq[flank_left] == ins_seq[0]:
                flank_left += 1

            is_dup = (flank_left >= ins_len and ref_seq[flank_left - ins_len : flank_left] == ins_seq)
            c_left_str = ref_data.mrna_pos_to_c_pos(flank_left) if flank_left > 0 else "0"

            if is_dup:
                if ins_len == 1:
                    hgvs_c = f"{ref_data.accession}:c.{c_left_str}dup"
                    c_pos_display = c_left_str
                else:
                    dup_start = flank_left - ins_len + 1
                    c_start_str = ref_data.mrna_pos_to_c_pos(dup_start)
                    hgvs_c = f"{ref_data.accession}:c.{c_start_str}_{c_left_str}dup"
                    c_pos_display = f"{c_start_str}_{c_left_str}"
            else:
                flank_right = flank_left + 1
                c_right_str = (
                    ref_data.mrna_pos_to_c_pos(flank_right)
                    if flank_right <= ref_data.total_length
                    else f"*{flank_right - ref_data.cds_end}"
                )
                hgvs_c = f"{ref_data.accession}:c.{c_left_str}_{c_right_str}ins{ins_seq}"
                c_pos_display = f"{c_left_str}_{c_right_str}"

            in_cds = ref_data.cds_start <= flank_left < ref_data.cds_end
            if in_cds:
                impact = "Frameshift Insertion" if ins_len % 3 != 0 else "In-frame Insertion"
                hgvs_p = f"p.({c_left_str}ins_fs)" if ins_len % 3 != 0 else f"p.({c_left_str}ins)"
            else:
                impact = "Non-coding Insertion"
                hgvs_p = None

            variants.append(
                DetectedVariant(
                    id=f"var_ins_{flank_left}_{ins_len}",
                    variant_type="duplication" if is_dup else "insertion",
                    ref_position_mrna=flank_left,
                    c_position=c_pos_display,
                    ref_allele=ref_seq[flank_left - ins_len : flank_left] if is_dup else "-",
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
        eq_aliases, eq_notes = get_equivalent_nomenclature(c_pos_str, ref_base, alt_base, hgvs_p)

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
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    return None, f"Unsupported HGVS syntax '{raw_query}'. Supported format: 'c.[position][Ref]>[Alt]', e.g. 'c.118C>T'."
