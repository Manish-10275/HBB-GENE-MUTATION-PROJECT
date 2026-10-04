"""Deterministic sequence alignment module using pairwise global alignment."""

from typing import List, Tuple
from Bio import Align
from app.models import AlignmentBlock, AlignmentSummary


def align_sequences(
    ref_seq: str,
    query_seq: str,
    block_size: int = 60
) -> Tuple[AlignmentSummary, str, str]:
    """
    Performs deterministic pairwise global alignment between reference and sample query.

    Returns:
    - AlignmentSummary: summary metrics and display blocks
    - aligned_ref: full aligned reference with gap characters
    - aligned_query: full aligned query with gap characters
    """
    ref_len = len(ref_seq)
    query_len = len(query_seq)

    # 1. Quick check for identical sequence
    if ref_seq == query_seq:
        aligned_ref = ref_seq
        aligned_query = query_seq
        score = float(ref_len * 2)
        matches = ref_len
        mismatches = 0
        gaps = 0
        identity = 100.0
    else:
        # 2. Bio.Align PairwiseAligner
        aligner = Align.PairwiseAligner()
        aligner.mode = "global"
        aligner.match_score = 2.0
        aligner.mismatch_score = -1.0
        aligner.open_gap_score = -2.5
        aligner.extend_gap_score = -1.0

        alignments = aligner.align(ref_seq, query_seq)
        top = alignments[0]
        score = float(top.score)

        # Extract aligned strings from alignment coordinates
        aligned_ref_arr: List[str] = []
        aligned_query_arr: List[str] = []

        # Bio.Align alignment formatting / coordinates:
        # top[0] is aligned target, top[1] is aligned query
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

    # 3. Build alignment display blocks with 1-based tracking
    blocks: List[AlignmentBlock] = []
    total_len = len(aligned_ref)
    ref_pos = 0  # 1-based count of non-gap ref bases
    query_pos = 0  # 1-based count of non-gap query bases

    for i in range(0, total_len, block_size):
        chunk_ref = aligned_ref[i : i + block_size]
        chunk_query = aligned_query[i : i + block_size]

        # Calculate coordinates for this block
        chunk_ref_non_gaps = len(chunk_ref.replace("-", ""))
        chunk_query_non_gaps = len(chunk_query.replace("-", ""))

        b_ref_start = ref_pos + 1 if chunk_ref_non_gaps > 0 else ref_pos
        b_ref_end = ref_pos + chunk_ref_non_gaps
        ref_pos = b_ref_end

        b_query_start = query_pos + 1 if chunk_query_non_gaps > 0 else query_pos
        b_query_end = query_pos + chunk_query_non_gaps
        query_pos = b_query_end

        # Match indicator line
        match_chars: List[str] = []
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
                query_start=b_query_start,
                query_end=b_query_end,
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
