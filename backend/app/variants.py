"""Deterministic variant detection, HGVS coordinate mapping, and classification."""

import re
from typing import List, Optional, Tuple
from app.models import CodonChange, DetectedVariant
from app.reference import ReferenceData, reference_manager
from app.consequences import (
    evaluate_substitution_codon_consequence,
    evaluate_indel_codon_consequence,
)


def _map_cdna_pos_to_genomic_rel(c_pos_str: str) -> Optional[Tuple[int, str, str]]:
    """
    Maps standard cDNA notation string (including intronic offsets) to:
    (1-based relative position in NG_000007.3 locus 1..1608, region_name, impact_description)

    Genomic relative boundaries in NG_000007.3 (70545..72152):
    - Exon 1: 1..142 (c.-50..c.92)
    - Intron 1: 143..272 (c.92+1..c.92+130)
    - Exon 2: 273..495 (c.93..c.315)
    - Intron 2: 496..1345 (c.315+1..c.315+850)
    - Exon 3: 1346..1608 (c.316..c.*134)
    """
    clean = c_pos_str.replace("c.", "").strip()

    # Donor / Acceptor Intron 1
    m_i1_donor = re.match(r"^92\+(\d+)$", clean)
    if m_i1_donor:
        offset = int(m_i1_donor.group(1))
        if 1 <= offset <= 130:
            rel_pos = 142 + offset
            impact = (
                "Splice Site Disruption (Intron 1 donor invariant GT dinucleotide)"
                if offset in (1, 2)
                else (
                    "Splice Site Defect (Intron 1 donor +5 consensus site)"
                    if offset == 5
                    else "Intronic (Non-coding)"
                )
            )
            return rel_pos, "Intron 1 (IVS-1)", impact
        return None

    m_i1_acc = re.match(r"^93-(\d+)$", clean)
    if m_i1_acc:
        offset = int(m_i1_acc.group(1))
        if 1 <= offset <= 130:
            rel_pos = 273 - offset
            impact = (
                "Splice Site Disruption (Intron 1 acceptor invariant AG dinucleotide)"
                if offset in (1, 2)
                else "Intronic (Non-coding)"
            )
            return rel_pos, "Intron 1 (IVS-1)", impact
        return None

    # Donor / Acceptor Intron 2
    m_i2_donor = re.match(r"^315\+(\d+)$", clean)
    if m_i2_donor:
        offset = int(m_i2_donor.group(1))
        if 1 <= offset <= 850:
            rel_pos = 495 + offset
            impact = (
                "Splice Site Disruption (Intron 2 donor invariant GT dinucleotide)"
                if offset in (1, 2)
                else "Intronic (Non-coding)"
            )
            return rel_pos, "Intron 2 (IVS-2)", impact
        return None

    m_i2_acc = re.match(r"^316-(\d+)$", clean)
    if m_i2_acc:
        offset = int(m_i2_acc.group(1))
        if 1 <= offset <= 850:
            rel_pos = 1346 - offset
            impact = (
                "Splice Site Disruption (Intron 2 acceptor invariant AG dinucleotide)"
                if offset in (1, 2)
                else "Intronic (Non-coding)"
            )
            return rel_pos, "Intron 2 (IVS-2)", impact
        return None

    return None


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
    elif "315+1" in c_pos_clean:
        aliases = ["c.315+1G>A", "IVS-II-1 G>A", "IVS2-1 G>A", "IVS-2-1", "IVS2-1"]
    elif "124_127del" in c_pos_clean or "126_129del" in c_pos_clean:
        aliases = ["c.124_127del", "c.126_129del", "Codon 41/42 (-TCTT)", "CD 41/42", "fs 41/42"]
    elif "27dup" in c_pos_clean or "26_27ins" in c_pos_clean or "27_28ins" in c_pos_clean:
        aliases = ["c.27dup", "c.27_28insG", "c.26_27insG", "Codon 8/9 (+G)", "CD 8/9 (+G)"]
    elif "9del" in c_pos_clean or "8del" in c_pos_clean:
        aliases = ["c.9delT", "c.9del", "c.8delA", "c.8del"]

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
                try:
                    c_s_num = int(c_start_str)
                    c_e_num = int(c_end_str)
                    utr3 = ref_data.sequence[ref_data.cds_end:]
                    hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                        c_s_num, c_e_num, "deletion", del_seq, "-", ref_data.cds_sequence, utr3
                    )
                except ValueError:
                    impact = "In-frame Deletion" if del_len % 3 == 0 else "Frameshift Deletion"
                    hgvs_p = f"p.({c_start_str}del_fs)" if del_len % 3 != 0 else f"p.({c_start_str}del)"
            else:
                impact = "Non-coding Deletion"
                hgvs_p = None

            eq_aliases, eq_notes = get_equivalent_nomenclature(c_pos_display, del_seq, "-", hgvs_p)

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
                    confidence="Deterministic",
                    equivalent_nomenclature=eq_aliases,
                    nomenclature_notes=eq_notes
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
            # Uses cyclic motif permutation to correctly support multi-base tandem duplications
            cur_ins = list(ins_seq)
            while flank_left < len(ref_seq) and ref_seq[flank_left] == cur_ins[0]:
                matched_base = cur_ins.pop(0)
                cur_ins.append(matched_base)
                flank_left += 1
            ins_seq = "".join(cur_ins)

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
                try:
                    c_l_num = int(c_left_str)
                    c_s_num = int(c_start_str) if is_dup and ins_len > 1 else c_l_num
                    op_type = "duplication" if is_dup else "insertion"
                    utr3 = ref_data.sequence[ref_data.cds_end:]
                    hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                        c_s_num, c_l_num, op_type, "-", ins_seq, ref_data.cds_sequence, utr3
                    )
                except ValueError:
                    impact = "Frameshift Insertion" if ins_len % 3 != 0 else "In-frame Insertion"
                    hgvs_p = f"p.({c_left_str}ins_fs)" if ins_len % 3 != 0 else f"p.({c_left_str}ins)"
            else:
                impact = "Non-coding Insertion"
                hgvs_p = None

            ref_all = ref_seq[flank_left - ins_len : flank_left] if is_dup else "-"
            eq_aliases, eq_notes = get_equivalent_nomenclature(c_pos_display, ref_all, ins_seq, hgvs_p)

            variants.append(
                DetectedVariant(
                    id=f"var_ins_{flank_left}_{ins_len}",
                    variant_type="duplication" if is_dup else "insertion",
                    ref_position_mrna=flank_left,
                    c_position=c_pos_display,
                    ref_allele=ref_all,
                    alt_allele=ins_seq,
                    hgvs_c=hgvs_c,
                    hgvs_p=hgvs_p,
                    codon_change=None,
                    functional_impact=impact,
                    confidence="Deterministic",
                    equivalent_nomenclature=eq_aliases,
                    nomenclature_notes=eq_notes
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
    Parses an HGVS cDNA query string and deterministically reconstructs the DetectedVariant model
    with exact biological consequences.

    Supported HGVS forms:
    - Single Nucleotide Substitutions: 'c.118C>T', 'c.20A>T', 'c.-5A>G', 'c.*10T>C'
    - Intronic Splice Substitutions: 'c.92+5G>C', 'c.315+1G>A', 'c.92+1G>T', 'c.93-1G>A'
    - Deletions: 'c.9del', 'c.9delT', 'c.126_129del', 'c.126_129delCTTT', 'c.124_127del'
    - Duplications: 'c.27dup', 'c.27dupG', 'c.20_23dup'
    - Flanked Insertions: 'c.27_28insG', 'c.26_27insG', 'c.117_118insA'
    """
    query = raw_query.strip()
    if ":" in query:
        _, c_part = query.split(":", 1)
    else:
        c_part = query

    c_part = c_part.strip()
    # Normalize spaces that result from URL decoding '+' (e.g. "c.92 5G>C" -> "c.92+5G>C")
    c_part = re.sub(r"(\d+)\s+(\d+)", r"\1+\2", c_part)
    c_part = re.sub(r"\s+", "", c_part)
    if not c_part.startswith("c."):
        if (
            re.match(r"^(\*?-?\d+)[A-Za-z]>[A-Za-z]$", c_part)
            or re.match(r"^(\d+[+-]\d+)[A-Za-z]>[A-Za-z]$", c_part)
            or re.match(r"^\*?-?\d+(?:_\*?-?\d+)?(?:del|dup|ins)", c_part, re.IGNORECASE)
        ):
            c_part = f"c.{c_part}"
        else:
            return None, (
                "Query must follow standard HGVS notation, e.g., 'c.118C>T', 'c.126_129del', "
                "'c.27dup', 'c.92+5G>C', or 'NM_000518.5:c.118C>T'."
            )

    # 1. Match Intronic Splice Substitution: c.92+5G>C, c.315+1G>A, c.93-1G>A, etc.
    splice_sub_match = re.match(r"^c\.(\d+)([+-]\d+)([A-Za-z])>([A-Za-z])$", c_part)
    if splice_sub_match:
        exon_anchor = splice_sub_match.group(1)
        offset_str = splice_sub_match.group(2)
        ref_base = splice_sub_match.group(3).upper()
        alt_base = splice_sub_match.group(4).upper()
        if ref_base not in {"A", "C", "G", "T"} or alt_base not in {"A", "C", "G", "T"}:
            bad_base = ref_base if ref_base not in {"A", "C", "G", "T"} else alt_base
            return None, f"Invalid nucleotide base '{bad_base}' in query. Bases must be standard DNA nucleotides (A, C, G, T)."
        c_pos_str = f"{exon_anchor}{offset_str}"

        gen_mapping = _map_cdna_pos_to_genomic_rel(c_pos_str)
        if not gen_mapping:
            return None, (
                f"Intronic coordinate 'c.{c_pos_str}' is outside supported HBB gene boundaries or introns "
                f"(supported: Intron 1 c.92+1..c.92+130 / c.93-1..c.93-130; Intron 2 c.315+1..c.315+850 / c.316-1..c.316-850)."
            )

        rel_pos, region_name, impact = gen_mapping

        try:
            ng_ref = reference_manager.get_reference("NG_000007.3")
            expected_ref = ng_ref.sequence[rel_pos - 1]
        except Exception:
            expected_ref = ref_base

        if expected_ref != ref_base:
            return None, (
                f"Reference base mismatch at c.{c_pos_str}: input states '{ref_base}', "
                f"but genomic reference NG_000007.3 has '{expected_ref}'."
            )

        standard_hgvs = f"NM_000518.5:c.{c_pos_str}{ref_base}>{alt_base}"
        hgvs_p = "p.?"
        eq_aliases, eq_notes = get_equivalent_nomenclature(c_pos_str, ref_base, alt_base, hgvs_p)

        variant = DetectedVariant(
            id=f"direct_splice_{rel_pos}_{ref_base}_{alt_base}",
            variant_type="substitution",
            ref_position_mrna=rel_pos,
            c_position=c_pos_str,
            ref_allele=ref_base,
            alt_allele=alt_base,
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes or (
                "Splice site variant in non-coding intronic region. Exact transcript splicing defect "
                "requires experimental RNA analysis; in silico protein translation is unresolved (p.?)."
            )
        )
        return variant, None

    # 2. Match Single Nucleotide Substitution: c.118C>T or c.-5A>G or c.*10T>C
    sub_match = re.match(r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$", c_part)
    if sub_match:
        c_pos_str = sub_match.group(1)
        ref_base = sub_match.group(2).upper()
        alt_base = sub_match.group(3).upper()
        if ref_base not in {"A", "C", "G", "T"} or alt_base not in {"A", "C", "G", "T"}:
            bad_base = ref_base if ref_base not in {"A", "C", "G", "T"} else alt_base
            return None, f"Invalid nucleotide base '{bad_base}' in query. Bases must be standard DNA nucleotides (A, C, G, T)."

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

    # 2b. Match Deletion-Insertion (delins): c.19_20delinsAT or c.385_388delinsCCACA or c.25delinsT
    delins_match = re.match(r"^c\.(\*?-?\d+)(?:_(\*?-?\d+))?delins([A-Za-z]+)$", c_part, re.IGNORECASE)
    if delins_match:
        c_start_str = delins_match.group(1)
        c_end_str = delins_match.group(2) or c_start_str
        ins_seq = delins_match.group(3).upper()
        if any(b not in {"A", "C", "G", "T"} for b in ins_seq):
            return None, f"Invalid nucleotide sequence '{ins_seq}' in deletion-insertion. Bases must be standard DNA nucleotides (A, C, G, T)."

        try:
            start_num = int(c_start_str)
            end_num = int(c_end_str)
            if start_num > end_num:
                return None, f"Invalid coordinate range in 'c.{c_start_str}_{c_end_str}delins': start coordinate must precede end coordinate."
        except ValueError:
            pass

        mrna_start = ref_data.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_data.c_pos_to_mrna_pos(c_end_str)

        if mrna_start is None or mrna_end is None or mrna_start < 1 or mrna_end > ref_data.total_length:
            return None, f"Deletion-insertion coordinates 'c.{c_start_str}_{c_end_str}' are out of bounds for reference {ref_data.accession}."

        expected_seq = ref_data.sequence[mrna_start - 1 : mrna_end]
        c_pos_display = c_start_str if c_start_str == c_end_str else f"{c_start_str}_{c_end_str}"

        in_cds = (
            ref_data.cds_start <= mrna_start <= ref_data.cds_end
            and ref_data.cds_start <= mrna_end <= ref_data.cds_end
        )
        if in_cds:
            utr3 = ref_data.sequence[ref_data.cds_end:]
            hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                int(c_start_str), int(c_end_str), "delins", expected_seq, ins_seq, ref_data.cds_sequence, utr3
            )
        else:
            impact = "Non-coding Delins"
            hgvs_p = None

        standard_hgvs = f"{ref_data.accession}:c.{c_pos_display}delins{ins_seq}"
        eq_aliases, eq_notes = get_equivalent_nomenclature(f"{c_pos_display}delins", expected_seq, ins_seq, hgvs_p)

        variant = DetectedVariant(
            id=f"direct_delins_{mrna_start}_{len(expected_seq)}_{len(ins_seq)}",
            variant_type="delins",
            ref_position_mrna=mrna_start,
            c_position=c_pos_display,
            ref_allele=expected_seq,
            alt_allele=ins_seq,
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    # 3. Match Range Deletion: c.126_129del or c.126_129delCTTT
    range_del_match = re.match(r"^c\.(\*?-?\d+)_(\*?-?\d+)del(?!(?:ins))([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if range_del_match:
        c_start_str = range_del_match.group(1)
        c_end_str = range_del_match.group(2)
        specified_bases = range_del_match.group(3).upper() if range_del_match.group(3) else None
        if specified_bases and any(b not in {"A", "C", "G", "T"} for b in specified_bases):
            return None, f"Invalid nucleotide sequence '{specified_bases}' in deletion. Bases must be standard DNA nucleotides (A, C, G, T)."

        try:
            start_num = int(c_start_str)
            end_num = int(c_end_str)
            if start_num >= end_num:
                return None, f"Invalid coordinate range in 'c.{c_start_str}_{c_end_str}del': start coordinate must precede end coordinate."
        except ValueError:
            pass

        mrna_start = ref_data.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_data.c_pos_to_mrna_pos(c_end_str)

        if mrna_start is None or mrna_end is None or mrna_start < 1 or mrna_end > ref_data.total_length:
            return None, f"Deletion coordinates 'c.{c_start_str}_{c_end_str}' are out of bounds for reference {ref_data.accession}."

        expected_seq = ref_data.sequence[mrna_start - 1 : mrna_end]
        if specified_bases and expected_seq != specified_bases:
            return None, (
                f"Reference sequence mismatch at c.{c_start_str}_{c_end_str}: query states '{specified_bases}', "
                f"but reference {ref_data.accession} has '{expected_seq}'."
            )

        ref_allele = expected_seq
        del_len = len(ref_allele)
        c_pos_display = f"{c_start_str}_{c_end_str}"

        in_cds = (
            ref_data.cds_start <= mrna_start <= ref_data.cds_end
            and ref_data.cds_start <= mrna_end <= ref_data.cds_end
        )
        if in_cds:
            utr3 = ref_data.sequence[ref_data.cds_end:]
            hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                int(c_start_str), int(c_end_str), "deletion", ref_allele, "-", ref_data.cds_sequence, utr3
            )
        else:
            impact = "Non-coding Deletion"
            hgvs_p = None

        standard_hgvs = f"{ref_data.accession}:c.{c_pos_display}del"
        eq_aliases, eq_notes = get_equivalent_nomenclature(f"{c_pos_display}del", ref_allele, "-", hgvs_p)

        variant = DetectedVariant(
            id=f"direct_del_{mrna_start}_{del_len}",
            variant_type="deletion",
            ref_position_mrna=mrna_start,
            c_position=c_pos_display,
            ref_allele=ref_allele,
            alt_allele="-",
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    # 4. Match Single Base Deletion: c.9del or c.9delT
    single_del_match = re.match(r"^c\.(\*?-?\d+)del(?!(?:ins))([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if single_del_match:
        c_pos_str = single_del_match.group(1)
        specified_bases = single_del_match.group(2).upper() if single_del_match.group(2) else None
        if specified_bases and any(b not in {"A", "C", "G", "T"} for b in specified_bases):
            return None, f"Invalid nucleotide sequence '{specified_bases}' in deletion. Bases must be standard DNA nucleotides (A, C, G, T)."

        mrna_pos = ref_data.c_pos_to_mrna_pos(c_pos_str)
        if mrna_pos is None or mrna_pos < 1 or mrna_pos > ref_data.total_length:
            return None, f"Deletion coordinate 'c.{c_pos_str}' is out of bounds for reference {ref_data.accession}."

        expected_base = ref_data.sequence[mrna_pos - 1]
        if specified_bases and expected_base != specified_bases:
            return None, (
                f"Reference base mismatch at c.{c_pos_str}: query states '{specified_bases}', "
                f"but reference {ref_data.accession} has '{expected_base}'."
            )

        ref_allele = expected_base
        in_cds = ref_data.cds_start <= mrna_pos <= ref_data.cds_end
        if in_cds:
            c_num = int(c_pos_str)
            utr3 = ref_data.sequence[ref_data.cds_end:]
            hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                c_num, c_num, "deletion", ref_allele, "-", ref_data.cds_sequence, utr3
            )
        else:
            impact = "Non-coding Deletion"
            hgvs_p = None

        standard_hgvs = f"{ref_data.accession}:c.{c_pos_str}del"
        eq_aliases, eq_notes = get_equivalent_nomenclature(f"{c_pos_str}del", ref_allele, "-", hgvs_p)

        variant = DetectedVariant(
            id=f"direct_del_{mrna_pos}_1",
            variant_type="deletion",
            ref_position_mrna=mrna_pos,
            c_position=c_pos_str,
            ref_allele=ref_allele,
            alt_allele="-",
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    # 5. Match Duplication: c.27dup or c.27dupG or c.20_23dup
    dup_match = re.match(r"^c\.(\*?-?\d+)(?:_(\*?-?\d+))?dup([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if dup_match:
        c_start_str = dup_match.group(1)
        c_end_str = dup_match.group(2) or c_start_str
        specified_bases = dup_match.group(3).upper() if dup_match.group(3) else None
        if specified_bases and any(b not in {"A", "C", "G", "T"} for b in specified_bases):
            return None, f"Invalid nucleotide sequence '{specified_bases}' in duplication. Bases must be standard DNA nucleotides (A, C, G, T)."

        mrna_start = ref_data.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_data.c_pos_to_mrna_pos(c_end_str)
        if mrna_start is None or mrna_end is None or mrna_start < 1 or mrna_end > ref_data.total_length:
            return None, f"Duplication coordinates 'c.{c_start_str}_{c_end_str}' are out of bounds for reference {ref_data.accession}."

        try:
            start_num = int(c_start_str)
            end_num = int(c_end_str)
            if start_num > end_num:
                return None, f"Invalid range in duplication 'c.{c_start_str}_{c_end_str}dup': start coordinate must precede end coordinate."
        except ValueError:
            start_num = mrna_start - ref_data.cds_start + 1
            end_num = mrna_end - ref_data.cds_start + 1

        expected_seq = ref_data.sequence[mrna_start - 1 : mrna_end]
        if specified_bases and expected_seq != specified_bases:
            return None, (
                f"Reference sequence mismatch at duplication c.{c_start_str}_{c_end_str}: "
                f"query states '{specified_bases}', but reference {ref_data.accession} has '{expected_seq}'."
            )

        alt_allele = expected_seq
        c_pos_display = c_start_str if c_start_str == c_end_str else f"{c_start_str}_{c_end_str}"
        standard_hgvs = (
            f"{ref_data.accession}:c.{c_start_str}dup"
            if c_start_str == c_end_str
            else f"{ref_data.accession}:c.{c_pos_display}dup"
        )

        in_cds = ref_data.cds_start <= mrna_start <= ref_data.cds_end and ref_data.cds_start <= mrna_end <= ref_data.cds_end
        if in_cds:
            utr3 = ref_data.sequence[ref_data.cds_end:]
            hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                start_num, end_num, "duplication", "-", alt_allele, ref_data.cds_sequence, utr3
            )
        else:
            impact = "Non-coding Duplication"
            hgvs_p = None

        eq_aliases, eq_notes = get_equivalent_nomenclature(f"{c_pos_display}dup", "-", alt_allele, hgvs_p)

        variant = DetectedVariant(
            id=f"direct_dup_{mrna_start}_{len(alt_allele)}",
            variant_type="duplication",
            ref_position_mrna=mrna_start,
            c_position=c_pos_display,
            ref_allele="-",
            alt_allele=alt_allele,
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    # 6. Match Flanked Insertion: c.27_28insG or c.117_118insA
    ins_match = re.match(r"^c\.(\*?-?\d+)_(\*?-?\d+)ins([A-Za-z]+)$", c_part, re.IGNORECASE)
    if ins_match:
        c_start_str = ins_match.group(1)
        c_end_str = ins_match.group(2)
        ins_seq = ins_match.group(3).upper()
        if any(b not in {"A", "C", "G", "T"} for b in ins_seq):
            return None, f"Invalid nucleotide sequence '{ins_seq}' in insertion. Bases must be standard DNA nucleotides (A, C, G, T)."

        mrna_start = ref_data.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_data.c_pos_to_mrna_pos(c_end_str)
        if mrna_start is None or mrna_end is None or mrna_start < 1 or mrna_end > ref_data.total_length:
            return None, f"Insertion coordinates 'c.{c_start_str}_{c_end_str}' are out of bounds for reference {ref_data.accession}."

        try:
            start_num = int(c_start_str)
            end_num = int(c_end_str)
            if end_num != start_num + 1:
                return None, (
                    f"Invalid insertion coordinates 'c.{c_start_str}_{c_end_str}ins': "
                    f"HGVS insertion coordinates must be two consecutive flanking positions."
                )
        except ValueError:
            pass

        flank_left = mrna_start
        ref_seq = ref_data.sequence
        is_dup = flank_left >= len(ins_seq) and ref_seq[flank_left - len(ins_seq) : flank_left] == ins_seq
        op_type = "duplication" if is_dup else "insertion"

        c_pos_display = f"{c_start_str}_{c_end_str}"
        standard_hgvs = (
            f"{ref_data.accession}:c.{c_start_str}dup"
            if is_dup and len(ins_seq) == 1
            else f"{ref_data.accession}:c.{c_pos_display}ins{ins_seq}"
        )

        in_cds = ref_data.cds_start <= mrna_start < ref_data.cds_end
        if in_cds:
            c_num = int(c_start_str)
            utr3 = ref_data.sequence[ref_data.cds_end:]
            hgvs_p, impact, _ = evaluate_indel_codon_consequence(
                c_num, c_num, op_type, "-", ins_seq, ref_data.cds_sequence, utr3
            )
        else:
            impact = "Non-coding Insertion"
            hgvs_p = None

        eq_aliases, eq_notes = get_equivalent_nomenclature(
            f"{c_start_str}dup" if is_dup else f"{c_pos_display}ins", "-", ins_seq, hgvs_p
        )
        if c_start_str in ("26", "27") and ins_seq == "G":
            if "c.27_28insG" not in eq_aliases:
                eq_aliases.append("c.27_28insG")
            if "c.27dup" not in eq_aliases:
                eq_aliases.append("c.27dup")

        variant = DetectedVariant(
            id=f"direct_ins_{mrna_start}_{len(ins_seq)}",
            variant_type="duplication" if is_dup else "insertion",
            ref_position_mrna=mrna_start,
            c_position=c_pos_display,
            ref_allele="-",
            alt_allele=ins_seq,
            hgvs_c=standard_hgvs,
            hgvs_p=hgvs_p,
            codon_change=None,
            functional_impact=impact,
            confidence="Deterministic",
            equivalent_nomenclature=eq_aliases,
            nomenclature_notes=eq_notes
        )
        return variant, None

    return None, (
        f"Unsupported HGVS syntax '{raw_query}'. Supported formats include substitutions (e.g. 'c.118C>T'), "
        f"intronic splice variants (e.g. 'c.92+5G>C', 'c.315+1G>A'), deletions (e.g. 'c.9del', 'c.126_129del'), "
        f"duplications (e.g. 'c.27dup'), and insertions (e.g. 'c.27_28insG')."
    )

