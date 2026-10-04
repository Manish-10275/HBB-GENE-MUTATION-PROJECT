"""Sequence normalization and strict biological validation module."""

import re
from typing import Set, Tuple, List, Optional
from app.models import SequenceNormalizationResult

# Strictly canonical DNA alphabet
VALID_DNA_BASES: Set[str] = {"A", "C", "G", "T"}


class SequenceValidationError(ValueError):
    """Raised when sequence validation fails with structured messages."""
    pass


def normalize_and_validate_sequence(raw_input: str) -> SequenceNormalizationResult:
    """
    Parses, cleans, and strictly validates raw or FASTA formatted DNA sequence.

    Handles:
    - FASTA headers (lines starting with '>')
    - Whitespace, newlines, tabs, and coordinate numbers
    - Case conversion (lowercase to uppercase)
    - Rejection of RNA ('U') and invalid characters
    """
    if not raw_input or not raw_input.strip():
        return SequenceNormalizationResult(
            raw_sequence=raw_input or "",
            clean_sequence="",
            header=None,
            length=0,
            gc_content=0.0,
            is_valid=False,
            validation_errors=["Sequence input is empty. Please provide a DNA sequence or FASTA text."]
        )

    lines = raw_input.strip().splitlines()
    header: Optional[str] = None
    seq_lines: List[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            if header is None:
                header = stripped[1:].strip()
            continue
        seq_lines.append(stripped)

    if not seq_lines:
        return SequenceNormalizationResult(
            raw_sequence=raw_input,
            clean_sequence="",
            header=header,
            length=0,
            gc_content=0.0,
            is_valid=False,
            validation_errors=["No nucleotide sequence found after FASTA header."]
        )

    # Combine and normalize: remove whitespace and numbers (e.g. GenBank coordinate marks)
    raw_combined = "".join(seq_lines)
    clean_seq = re.sub(r"[\s\d_]", "", raw_combined).upper()

    validation_errors: List[str] = []

    if not clean_seq:
        validation_errors.append("Sequence contains no nucleotide characters.")
        return SequenceNormalizationResult(
            raw_sequence=raw_input,
            clean_sequence="",
            header=header,
            length=0,
            gc_content=0.0,
            is_valid=False,
            validation_errors=validation_errors
        )

    # Detect invalid characters
    invalid_chars = sorted(list(set(clean_seq) - VALID_DNA_BASES))
    if invalid_chars:
        if "U" in invalid_chars:
            validation_errors.append(
                "Uracil ('U') detected. Input appears to be RNA rather than DNA. "
                "Please provide a cDNA or DNA sequence (A, C, G, T)."
            )
        other_invalid = [c for c in invalid_chars if c != "U"]
        if other_invalid:
            validation_errors.append(
                f"Non-canonical characters detected: {', '.join(other_invalid)}. "
                f"Only standard DNA nucleotides (A, C, G, T) are accepted."
            )

    is_valid = len(validation_errors) == 0
    seq_len = len(clean_seq)
    gc_count = clean_seq.count("G") + clean_seq.count("C")
    gc_content = round((gc_count / seq_len) * 100, 2) if seq_len > 0 else 0.0

    return SequenceNormalizationResult(
        raw_sequence=raw_input,
        clean_sequence=clean_seq if is_valid else "",
        header=header,
        length=seq_len if is_valid else 0,
        gc_content=gc_content if is_valid else 0.0,
        is_valid=is_valid,
        validation_errors=validation_errors
    )
