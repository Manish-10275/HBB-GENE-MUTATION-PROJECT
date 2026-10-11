"""Pure HGVS parser and validator for HBB sequence variants."""

import re
from typing import Optional

from app.core.models import (
    AnalysisError,
    AnalysisErrorCode,
    NormalizedVariant,
    VariantType,
)
from app.core.reference import (
    ReferenceSequence,
    load_reference,
    map_intronic_cdna_to_genomic,
)

# Valid DNA nucleotides set
DNA_BASES = {"A", "C", "G", "T"}


def _validate_dna_sequence(seq: str, context: str) -> None:
    """Validates that all characters in a sequence are valid DNA bases."""
    for base in seq.upper():
        if base not in DNA_BASES:
            raise AnalysisError(
                AnalysisErrorCode.SYNTAX_ERROR,
                f"Invalid nucleotide '{base}' in {context}. Must be standard DNA bases (A, C, G, T)."
            )


def parse_hgvs(
    query: str,
    ref_seq: Optional[ReferenceSequence] = None,
    ng_seq: Optional[ReferenceSequence] = None,
) -> NormalizedVariant:
    """
    Parses an HGVS variant query string through a strict biological validation pipeline:
    1. Input sanitization & transcript accession verification
    2. Formal syntax grammar parsing
    3. Biological coordinate boundary & range integrity checks
    4. Reference sequence base confirmation
    5. Canonical normalization into NormalizedVariant
    
    Raises AnalysisError on any syntax error, reference mismatch, or invalid coordinate.
    """
    if ref_seq is None:
        ref_seq = load_reference("NM_000518.5")

    raw = query.strip()
    if not raw:
        raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, "Empty variant query string.")

    # 1. Accession prefix parsing
    accession = "NM_000518.5"
    if ":" in raw:
        prefix, c_part = raw.split(":", 1)
        prefix = prefix.strip()
        c_part = c_part.strip()
        if prefix not in ("NM_000518.5", "NG_000007.3", "NM_000518"):
            raise AnalysisError(
                AnalysisErrorCode.UNSUPPORTED_VARIANT,
                f"Unsupported transcript/reference accession '{prefix}'. "
                f"Only HBB canonical transcripts (NM_000518.5, NG_000007.3) are supported."
            )
    else:
        c_part = raw

    # Normalize whitespace & URL-encoded '+'
    c_part = re.sub(r"(\d+)\s+(\d+)", r"\1+\2", c_part)
    c_part = re.sub(r"\s+", "", c_part)

    # Ensure 'c.' prefix
    if not c_part.startswith("c."):
        # Check if caller omitted 'c.'
        if (
            re.match(r"^(\*?-?\d+)[A-Za-z]>[A-Za-z]$", c_part)
            or re.match(r"^(\d+[+-]\d+)[A-Za-z]>[A-Za-z]$", c_part)
            or re.match(r"^\*?-?\d+(?:_\*?-?\d+)?(?:del|dup|ins)", c_part, re.IGNORECASE)
        ):
            c_part = f"c.{c_part}"
        else:
            raise AnalysisError(
                AnalysisErrorCode.SYNTAX_ERROR,
                f"Malformed HGVS query '{raw}'. Expected cDNA notation starting with 'c.', e.g. 'c.118C>T'."
            )

    # Base zero check
    if re.search(r"c\.0(?![0-9])|c\.[+-]0(?![0-9])|_0(?![0-9])", c_part):
        raise AnalysisError(
            AnalysisErrorCode.INVALID_COORDINATE,
            "HGVS nomenclature does not recognize base zero (c.0). Nucleotide preceding c.1 is c.-1."
        )

    # ---------------------------------------------------------
    # Rule 1: Intronic Splice Substitution (e.g. c.92+5G>C, c.315+1G>A)
    # ---------------------------------------------------------
    splice_sub_match = re.match(r"^c\.(\d+)([+-]\d+)([A-Za-z])>([A-Za-z])$", c_part)
    if splice_sub_match:
        exon_anchor = splice_sub_match.group(1)
        offset_str = splice_sub_match.group(2)
        ref_base = splice_sub_match.group(3).upper()
        alt_base = splice_sub_match.group(4).upper()

        _validate_dna_sequence(ref_base, "reference allele")
        _validate_dna_sequence(alt_base, "alternate allele")

        if ng_seq is None:
            ng_seq = load_reference("NG_000007.3")

        c_pos_str = f"{exon_anchor}{offset_str}"
        rel_pos, genomic_pos, region_name = map_intronic_cdna_to_genomic(c_pos_str, ng_seq)

        expected_ref = ng_seq.sequence[rel_pos - 1]
        if expected_ref != ref_base:
            raise AnalysisError(
                AnalysisErrorCode.REFERENCE_MISMATCH,
                f"Reference base mismatch at c.{c_pos_str}: query states '{ref_base}', "
                f"but genomic reference NG_000007.3 has '{expected_ref}'."
            )

        canonical_hgvs = f"NM_000518.5:c.{c_pos_str}{ref_base}>{alt_base}"
        notes = (
            f"Splice site variant in {region_name}. Exact transcript splicing defect "
            f"requires experimental RNA analysis; in silico protein translation is unresolved (p.?)."
        )

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_pos_str,
            variant_type=VariantType.SPLICE,
            ref_allele=ref_base,
            alt_allele=alt_base,
            hgvs_c=canonical_hgvs,
            region=region_name,
            mrna_position=None,
            genomic_accession=ng_seq.accession,
            genomic_coordinate=genomic_pos,
            equivalent_nomenclature=[f"c.{c_pos_str}{ref_base}>{alt_base}"],
            nomenclature_notes=notes,
        )

    # ---------------------------------------------------------
    # Rule 2: Exonic / UTR Substitution (e.g. c.118C>T, c.-12A>G, c.*25T>C)
    # ---------------------------------------------------------
    sub_match = re.match(r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$", c_part)
    if sub_match:
        c_pos_str = sub_match.group(1)
        ref_base = sub_match.group(2).upper()
        alt_base = sub_match.group(3).upper()

        _validate_dna_sequence(ref_base, "reference allele")
        _validate_dna_sequence(alt_base, "alternate allele")

        mrna_pos = ref_seq.c_pos_to_mrna_pos(c_pos_str)
        expected_ref = ref_seq.sequence[mrna_pos - 1]
        if expected_ref != ref_base:
            raise AnalysisError(
                AnalysisErrorCode.REFERENCE_MISMATCH,
                f"Reference base mismatch at c.{c_pos_str}: query states '{ref_base}', "
                f"but reference sequence {ref_seq.accession} has '{expected_ref}'."
            )

        region = ref_seq.get_region_for_c_pos(c_pos_str)
        is_utr = region in ("5' UTR", "3' UTR")
        var_type = VariantType.REGULATORY_UTR if is_utr else VariantType.SUBSTITUTION
        canonical_hgvs = f"{ref_seq.accession}:c.{c_pos_str}{ref_base}>{alt_base}"

        notes = None
        if not is_utr:
            try:
                c_num = int(c_pos_str)
                codon_num = ((c_num - 1) // 3) + 1
                if codon_num >= 2:
                    notes = (
                        f"Historically numbered as codon {codon_num - 1} based on mature "
                        f"circulating beta-globin (Met1 cleaved); HGVS standard numbers from Met1."
                    )
            except ValueError:
                pass

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_pos_str,
            variant_type=var_type,
            ref_allele=ref_base,
            alt_allele=alt_base,
            hgvs_c=canonical_hgvs,
            region=region,
            mrna_position=mrna_pos,
            equivalent_nomenclature=[f"c.{c_pos_str}{ref_base}>{alt_base}"],
            nomenclature_notes=notes,
        )

    # ---------------------------------------------------------
    # Rule 3: Range Deletion (e.g. c.126_129del, c.126_129delCTTT)
    # ---------------------------------------------------------
    range_del_match = re.match(r"^c\.(\*?-?\d+)_(\*?-?\d+)del([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if range_del_match:
        c_start_str = range_del_match.group(1)
        c_end_str = range_del_match.group(2)
        specified_bases = range_del_match.group(3).upper() if range_del_match.group(3) else None

        if specified_bases:
            _validate_dna_sequence(specified_bases, "deleted sequence")

        mrna_start = ref_seq.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_seq.c_pos_to_mrna_pos(c_end_str)

        if mrna_start > mrna_end:
            raise AnalysisError(
                AnalysisErrorCode.INVALID_COORDINATE,
                f"Invalid coordinate range in '{c_part}': start coordinate (mRNA {mrna_start}) "
                f"must precede end coordinate (mRNA {mrna_end})."
            )

        expected_seq = ref_seq.sequence[mrna_start - 1 : mrna_end]
        if specified_bases and expected_seq != specified_bases:
            raise AnalysisError(
                AnalysisErrorCode.REFERENCE_MISMATCH,
                f"Reference sequence mismatch at c.{c_start_str}_{c_end_str}: query states '{specified_bases}', "
                f"but reference sequence {ref_seq.accession} has '{expected_seq}'."
            )

        c_display = f"{c_start_str}_{c_end_str}"
        region = ref_seq.get_region_for_c_pos(c_start_str)
        canonical_hgvs = f"{ref_seq.accession}:c.{c_display}del"

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_display,
            variant_type=VariantType.DELETION,
            ref_allele=expected_seq,
            alt_allele="-",
            hgvs_c=canonical_hgvs,
            region=region,
            mrna_position=mrna_start,
            equivalent_nomenclature=[f"c.{c_display}del"],
            nomenclature_notes=None,
        )

    # ---------------------------------------------------------
    # Rule 4: Single Nucleotide Deletion (e.g. c.15del, c.15delT)
    # ---------------------------------------------------------
    single_del_match = re.match(r"^c\.(\*?-?\d+)del([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if single_del_match:
        c_pos_str = single_del_match.group(1)
        specified_bases = single_del_match.group(2).upper() if single_del_match.group(2) else None

        if specified_bases:
            _validate_dna_sequence(specified_bases, "deleted nucleotide")

        mrna_pos = ref_seq.c_pos_to_mrna_pos(c_pos_str)
        expected_base = ref_seq.sequence[mrna_pos - 1]

        if specified_bases and expected_base != specified_bases:
            raise AnalysisError(
                AnalysisErrorCode.REFERENCE_MISMATCH,
                f"Reference base mismatch at c.{c_pos_str}: query states '{specified_bases}', "
                f"but reference sequence {ref_seq.accession} has '{expected_base}'."
            )

        region = ref_seq.get_region_for_c_pos(c_pos_str)
        canonical_hgvs = f"{ref_seq.accession}:c.{c_pos_str}del"

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_pos_str,
            variant_type=VariantType.DELETION,
            ref_allele=expected_base,
            alt_allele="-",
            hgvs_c=canonical_hgvs,
            region=region,
            mrna_position=mrna_pos,
            equivalent_nomenclature=[f"c.{c_pos_str}del"],
            nomenclature_notes=None,
        )

    # ---------------------------------------------------------
    # Rule 5: Duplication (e.g. c.27dup, c.27dupG, c.20_23dup)
    # ---------------------------------------------------------
    dup_match = re.match(r"^c\.(\*?-?\d+)(?:_(\*?-?\d+))?dup([A-Za-z]+)?$", c_part, re.IGNORECASE)
    if dup_match:
        c_start_str = dup_match.group(1)
        c_end_str = dup_match.group(2) or c_start_str
        specified_bases = dup_match.group(3).upper() if dup_match.group(3) else None

        if specified_bases:
            _validate_dna_sequence(specified_bases, "duplicated sequence")

        mrna_start = ref_seq.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_seq.c_pos_to_mrna_pos(c_end_str)

        if mrna_start > mrna_end:
            raise AnalysisError(
                AnalysisErrorCode.INVALID_COORDINATE,
                f"Invalid coordinate range in '{c_part}': start coordinate must precede or equal end coordinate."
            )

        expected_seq = ref_seq.sequence[mrna_start - 1 : mrna_end]
        if specified_bases and expected_seq != specified_bases:
            raise AnalysisError(
                AnalysisErrorCode.REFERENCE_MISMATCH,
                f"Reference sequence mismatch at c.{c_start_str}_{c_end_str}: query states '{specified_bases}', "
                f"but reference sequence {ref_seq.accession} has '{expected_seq}'."
            )

        c_display = c_start_str if c_start_str == c_end_str else f"{c_start_str}_{c_end_str}"
        region = ref_seq.get_region_for_c_pos(c_start_str)
        canonical_hgvs = f"{ref_seq.accession}:c.{c_display}dup"

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_display,
            variant_type=VariantType.DUPLICATION,
            ref_allele=expected_seq,
            alt_allele=expected_seq,
            hgvs_c=canonical_hgvs,
            region=region,
            mrna_position=mrna_start,
            equivalent_nomenclature=[f"c.{c_display}dup"],
            nomenclature_notes=None,
        )

    # ---------------------------------------------------------
    # Rule 6: Insertion (e.g. c.27_28insG, c.26_27insG)
    # ---------------------------------------------------------
    ins_match = re.match(r"^c\.(\*?-?\d+)_(\*?-?\d+)ins([A-Za-z]+)$", c_part, re.IGNORECASE)
    if ins_match:
        c_start_str = ins_match.group(1)
        c_end_str = ins_match.group(2)
        ins_bases = ins_match.group(3).upper()

        _validate_dna_sequence(ins_bases, "inserted sequence")

        mrna_start = ref_seq.c_pos_to_mrna_pos(c_start_str)
        mrna_end = ref_seq.c_pos_to_mrna_pos(c_end_str)

        if mrna_end != mrna_start + 1:
            raise AnalysisError(
                AnalysisErrorCode.INVALID_COORDINATE,
                f"Insertion coordinates must designate two consecutive flanking nucleotides "
                f"(mRNA {mrna_start} and {mrna_end} given)."
            )

        c_display = f"{c_start_str}_{c_end_str}"
        region = ref_seq.get_region_for_c_pos(c_start_str)
        canonical_hgvs = f"{ref_seq.accession}:c.{c_display}ins{ins_bases}"

        return NormalizedVariant(
            transcript_accession=accession,
            c_position=c_display,
            variant_type=VariantType.INSERTION,
            ref_allele="-",
            alt_allele=ins_bases,
            hgvs_c=canonical_hgvs,
            region=region,
            mrna_position=mrna_start,
            equivalent_nomenclature=[f"c.{c_display}ins{ins_bases}"],
            nomenclature_notes=None,
        )

    # If no recognized grammar pattern matched
    raise AnalysisError(
        AnalysisErrorCode.SYNTAX_ERROR,
        f"Unrecognized or malformed HGVS variant syntax '{raw}'. Supported notations: "
        f"SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), "
        f"duplication ('c.27dup'), and insertion ('c.27_28insG')."
    )
