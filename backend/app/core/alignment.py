"""Deterministic sequence alignment and alignment-based variant detection."""

import re
from typing import List, Tuple

from Bio import Align

from app.core.models import (
    AlignmentBlock,
    AlignmentSummary,
    AnalysisError,
    AnalysisErrorCode,
    NormalizedVariant,
    VariantType,
)
from app.core.reference import ReferenceSequence


def clean_sequence(raw: str) -> str:
    """Strips FASTA headers, whitespace, and validates nucleotide characters."""
    lines = raw.strip().splitlines()
    seq_lines = [l.strip() for l in lines if not l.strip().startswith(">")]
    joined = "".join(seq_lines).upper()
    cleaned = re.sub(r"[^ACGTN]", "", joined)
    if not cleaned:
        raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, "No valid sequence data found.")
    return cleaned


def align_sequences(
    ref_seq: str,
    query_seq: str,
    block_size: int = 60,
) -> Tuple[AlignmentSummary, str, str]:
    """
    Performs deterministic pairwise global alignment between reference and query.
    
    Returns:
    - AlignmentSummary with formatted display blocks
    - Full aligned reference string
    - Full aligned query string
    """
    ref_clean = clean_sequence(ref_seq)
    query_clean = clean_sequence(query_seq)

    ref_len = len(ref_clean)
    query_len = len(query_clean)

    if ref_clean == query_clean:
        aligned_ref = ref_clean
        aligned_query = query_clean
        score = float(ref_len * 2)
        matches = ref_len
        mismatches = 0
        gaps = 0
        identity = 100.0
    else:
        aligner = Align.PairwiseAligner()
        aligner.mode = "global"
        aligner.match_score = 2.0
        aligner.mismatch_score = -1.0
        aligner.open_gap_score = -2.5
        aligner.extend_gap_score = -1.0

        alignments = aligner.align(ref_clean, query_clean)
        if not alignments:
            raise AnalysisError(
                AnalysisErrorCode.UNSUPPORTED_VARIANT,
                "Unable to align sequence against reference."
            )

        top = alignments[0]
        score = float(top.score)
        aligned_ref = str(top[0])
        aligned_query = str(top[1])

        matches = 0
        mismatches = 0
        gaps = 0

        for r, q in zip(aligned_ref, aligned_query):
            if r == "-" or q == "-":
                gaps += 1
            elif r == q:
                matches += 1
            else:
                mismatches += 1

        denom = max(ref_len, query_len)
        identity = round((matches / denom) * 100, 2) if denom > 0 else 0.0

    # Build display blocks
    blocks: List[AlignmentBlock] = []
    total_len = len(aligned_ref)
    ref_pos = 0
    query_pos = 0

    for i in range(0, total_len, block_size):
        chunk_ref = aligned_ref[i : i + block_size]
        chunk_query = aligned_query[i : i + block_size]

        c_ref_len = len(chunk_ref.replace("-", ""))
        c_qry_len = len(chunk_query.replace("-", ""))

        b_ref_start = ref_pos + 1 if c_ref_len > 0 else ref_pos
        b_ref_end = ref_pos + c_ref_len
        ref_pos = b_ref_end

        b_qry_start = query_pos + 1 if c_qry_len > 0 else query_pos
        b_qry_end = query_pos + c_qry_len
        query_pos = b_qry_end

        match_chars = []
        for r, q in zip(chunk_ref, chunk_query):
            if r != "-" and q != "-" and r == q:
                match_chars.append("|")
            elif r == "-" or q == "-":
                match_chars.append(" ")
            else:
                match_chars.append(".")
        match_line = "".join(match_chars)

        blocks.append(
            AlignmentBlock(
                block_index=len(blocks) + 1,
                ref_start=b_ref_start,
                ref_end=b_ref_end,
                query_start=b_qry_start,
                query_end=b_qry_end,
                ref_seq=chunk_ref,
                query_seq=chunk_query,
                match_line=match_line,
            )
        )

    summary = AlignmentSummary(
        ref_length=ref_len,
        query_length=query_len,
        matches=matches,
        mismatches=mismatches,
        gaps=gaps,
        identity_percentage=identity,
        alignment_score=score,
        blocks=blocks,
    )

    return summary, aligned_ref, aligned_query


def detect_variants_from_alignment(
    aligned_ref: str,
    aligned_query: str,
    ref_data: ReferenceSequence,
) -> List[NormalizedVariant]:
    """
    Scans aligned sequences and identifies all nucleotide variants deterministically.
    Applies the HGVS 3' rule for repetitive indels.
    """
    variants: List[NormalizedVariant] = []
    i = 0
    align_len = len(aligned_ref)
    ref_mrna_pos = 0

    while i < align_len:
        r = aligned_ref[i]
        q = aligned_query[i]

        if r != "-":
            ref_mrna_pos += 1

        # Match
        if r == q:
            i += 1
            continue

        # Single Nucleotide Substitution
        if r != "-" and q != "-":
            c_pos_str = ref_data.mrna_pos_to_c_pos(ref_mrna_pos)
            region = ref_data.get_region_for_c_pos(c_pos_str)
            is_utr = region in ("5' UTR", "3' UTR")
            var_type = VariantType.REGULATORY_UTR if is_utr else VariantType.SUBSTITUTION
            hgvs_c = f"{ref_data.accession}:c.{c_pos_str}{r}>{q}"

            variants.append(
                NormalizedVariant(
                    transcript_accession=ref_data.accession,
                    c_position=c_pos_str,
                    variant_type=var_type,
                    ref_allele=r,
                    alt_allele=q,
                    hgvs_c=hgvs_c,
                    region=region,
                    mrna_position=ref_mrna_pos,
                    equivalent_nomenclature=[f"c.{c_pos_str}{r}>{q}"],
                )
            )
            i += 1
            continue

        # Deletion in query (gap in query, base in reference)
        if r != "-" and q == "-":
            del_start_mrna = ref_mrna_pos
            j = i + 1
            while j < align_len and aligned_query[j] == "-" and aligned_ref[j] != "-":
                ref_mrna_pos += 1
                j += 1

            del_end_mrna = ref_mrna_pos

            # HGVS 3' rule: shift deletion as far 3' as possible in repetitive tracts
            full_ref = ref_data.sequence
            while del_end_mrna < len(full_ref) and full_ref[del_start_mrna - 1] == full_ref[del_end_mrna]:
                del_start_mrna += 1
                del_end_mrna += 1

            del_seq = full_ref[del_start_mrna - 1 : del_end_mrna]
            del_len = len(del_seq)

            c_start_str = ref_data.mrna_pos_to_c_pos(del_start_mrna)
            c_end_str = ref_data.mrna_pos_to_c_pos(del_end_mrna)

            if del_len == 1:
                c_pos_display = c_start_str
                hgvs_c = f"{ref_data.accession}:c.{c_start_str}del"
            else:
                c_pos_display = f"{c_start_str}_{c_end_str}"
                hgvs_c = f"{ref_data.accession}:c.{c_pos_display}del"

            region = ref_data.get_region_for_c_pos(c_start_str)

            variants.append(
                NormalizedVariant(
                    transcript_accession=ref_data.accession,
                    c_position=c_pos_display,
                    variant_type=VariantType.DELETION,
                    ref_allele=del_seq,
                    alt_allele="-",
                    hgvs_c=hgvs_c,
                    region=region,
                    mrna_position=del_start_mrna,
                    equivalent_nomenclature=[f"c.{c_pos_display}del"],
                )
            )
            i = j
            continue

        # Insertion in query (base in query, gap in reference)
        if r == "-" and q != "-":
            ins_bases = [q]
            j = i + 1
            while j < align_len and aligned_ref[j] == "-" and aligned_query[j] != "-":
                ins_bases.append(aligned_query[j])
                j += 1

            ins_seq = "".join(ins_bases)
            ins_len = len(ins_seq)

            flank_left = ref_mrna_pos
            full_ref = ref_data.sequence

            # HGVS 3' rule: shift insertion as far 3' as possible
            while flank_left < len(full_ref) and full_ref[flank_left] == ins_seq[0]:
                flank_left += 1

            is_dup = (flank_left >= ins_len and full_ref[flank_left - ins_len : flank_left] == ins_seq)
            c_left_str = ref_data.mrna_pos_to_c_pos(flank_left) if flank_left > 0 else "0"

            if is_dup:
                if ins_len == 1:
                    c_pos_display = c_left_str
                    hgvs_c = f"{ref_data.accession}:c.{c_left_str}dup"
                else:
                    dup_start = flank_left - ins_len + 1
                    c_start_str = ref_data.mrna_pos_to_c_pos(dup_start)
                    c_pos_display = f"{c_start_str}_{c_left_str}"
                    hgvs_c = f"{ref_data.accession}:c.{c_pos_display}dup"

                ref_allele = full_ref[flank_left - ins_len : flank_left]
                var_type = VariantType.DUPLICATION
                alt_allele = ref_allele
            else:
                flank_right = flank_left + 1
                c_right_str = (
                    ref_data.mrna_pos_to_c_pos(flank_right)
                    if flank_right <= ref_data.total_length
                    else f"*{flank_right - ref_data.cds_end}"
                )
                c_pos_display = f"{c_left_str}_{c_right_str}"
                hgvs_c = f"{ref_data.accession}:c.{c_pos_display}ins{ins_seq}"
                ref_allele = "-"
                var_type = VariantType.INSERTION
                alt_allele = ins_seq

            region = ref_data.get_region_for_c_pos(c_left_str)

            variants.append(
                NormalizedVariant(
                    transcript_accession=ref_data.accession,
                    c_position=c_pos_display,
                    variant_type=var_type,
                    ref_allele=ref_allele,
                    alt_allele=alt_allele,
                    hgvs_c=hgvs_c,
                    region=region,
                    mrna_position=flank_left,
                    equivalent_nomenclature=[f"c.{c_pos_display}{'dup' if is_dup else 'ins' + ins_seq}"],
                )
            )
            i = j
            continue

        i += 1

    return variants
