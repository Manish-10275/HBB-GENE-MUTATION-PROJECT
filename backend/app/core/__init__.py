"""Core domain bioinformatics package for HBB Gene Mutation Analyzer."""

from app.core.models import (
    AlignmentBlock,
    AlignmentSummary,
    AnalysisError,
    AnalysisErrorCode,
    CodonChange,
    ConsequenceResult,
    Exon,
    MolecularImpact,
    NormalizedVariant,
    VariantType,
)
from app.core.reference import (
    ReferenceSequence,
    load_reference,
    map_intronic_cdna_to_genomic,
)
from app.core.consequences import (
    CODON_TABLE,
    evaluate_consequence,
    evaluate_indel,
    evaluate_substitution,
    translate_codon,
)
from app.core.hgvs import parse_hgvs
from app.core.alignment import (
    align_sequences,
    clean_sequence,
    detect_variants_from_alignment,
)

__all__ = [
    "AnalysisError",
    "AnalysisErrorCode",
    "AlignmentBlock",
    "AlignmentSummary",
    "CodonChange",
    "ConsequenceResult",
    "Exon",
    "MolecularImpact",
    "NormalizedVariant",
    "VariantType",
    "ReferenceSequence",
    "load_reference",
    "map_intronic_cdna_to_genomic",
    "CODON_TABLE",
    "evaluate_consequence",
    "evaluate_indel",
    "evaluate_substitution",
    "translate_codon",
    "parse_hgvs",
    "align_sequences",
    "clean_sequence",
    "detect_variants_from_alignment",
]
