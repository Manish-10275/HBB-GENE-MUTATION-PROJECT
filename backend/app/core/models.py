"""Core domain data models, enums, and typed error taxonomy for HBB Mutation Analyzer."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class VariantType(str, Enum):
    """Structural classification of sequence variants."""
    SUBSTITUTION = "substitution"
    DELETION = "deletion"
    INSERTION = "insertion"
    DUPLICATION = "duplication"
    SPLICE = "splice"
    REGULATORY_UTR = "regulatory_utr"


class MolecularImpact(str, Enum):
    """Molecular consequence of a genomic/transcript change on translation."""
    SYNONYMOUS = "Synonymous"
    MISSENSE = "Missense"
    NONSENSE = "Nonsense"
    FRAMESHIFT = "Frameshift"
    IN_FRAME_INDEL = "In-frame Indel"
    SPLICE_DISRUPTION = "Splice Site Disruption"
    REGULATORY_5_UTR = "5' UTR Regulatory"
    REGULATORY_3_UTR = "3' UTR Regulatory"
    UNKNOWN = "Unknown"


class AnalysisErrorCode(str, Enum):
    """Domain-level error codes distinguishing failure modes without silent guessing."""
    SYNTAX_ERROR = "SYNTAX_ERROR"                             # Malformed HGVS grammar
    REFERENCE_MISMATCH = "REFERENCE_MISMATCH"                 # Query stated reference != actual reference nucleotide
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"                           # Position exceeds physical transcript or intron boundaries
    INVALID_COORDINATE = "INVALID_COORDINATE"                 # Base zero (c.0), inverted ranges (c.200_150del)
    UNSUPPORTED_VARIANT = "UNSUPPORTED_VARIANT"               # Complex multi-locus rearrangements, delins without insert
    AMBIGUOUS_VARIANT = "AMBIGUOUS_VARIANT"                   # Variant with undefined biological resolution
    EXTERNAL_SOURCE_UNAVAILABLE = "EXTERNAL_SOURCE_UNAVAILABLE" # Network offline or missing fixture in offline mode


@dataclass
class AnalysisError(Exception):
    """Structured, typed error emitted by the core bioinformatics engine."""
    code: AnalysisErrorCode
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"[{self.code.value}] {self.message}"


@dataclass(frozen=True)
class Exon:
    """Genomic and transcript boundaries of a single exon."""
    number: int
    start: int  # 1-based start
    end: int    # 1-based end
    genomic_start: Optional[int] = None
    genomic_end: Optional[int] = None


@dataclass(frozen=True)
class CodonChange:
    """Codon triplet and amino acid alteration."""
    codon_number: int       # 1-based codon position in translated protein (1..147)
    c_start: int            # 1-based coding nucleotide start (1..444)
    c_end: int              # 1-based coding nucleotide end (1..444)
    ref_codon: str          # e.g., "CAG"
    sample_codon: str       # e.g., "TAG"
    ref_aa: str             # Three-letter code, e.g., "Gln"
    sample_aa: str          # Three-letter code, e.g., "Ter"
    ref_aa_single: str      # One-letter code, e.g., "Q"
    sample_aa_single: str   # One-letter code, e.g., "*"
    consequence: str        # e.g., "Nonsense"
    is_stop_gain: bool = False
    is_stop_loss: bool = False
    is_synonymous: bool = False


@dataclass(frozen=True)
class NormalizedVariant:
    """Structured, validated variant representation."""
    transcript_accession: str
    c_position: str
    variant_type: VariantType
    ref_allele: str
    alt_allele: str
    hgvs_c: str
    region: str
    mrna_position: Optional[int] = None
    genomic_accession: Optional[str] = None
    genomic_coordinate: Optional[int] = None
    equivalent_nomenclature: List[str] = field(default_factory=list)
    nomenclature_notes: Optional[str] = None


@dataclass(frozen=True)
class ConsequenceResult:
    """Deterministic molecular and protein consequence."""
    hgvs_p: Optional[str]
    molecular_impact: MolecularImpact
    codon_change: Optional[CodonChange] = None
    ptc_coordinate: Optional[int] = None
    confidence: str = "Deterministic"


@dataclass(frozen=True)
class AlignmentBlock:
    """Formatted slice of aligned reference and query for display."""
    block_index: int
    ref_start: int
    ref_end: int
    query_start: int
    query_end: int
    ref_seq: str
    query_seq: str
    match_line: str


@dataclass(frozen=True)
class AlignmentSummary:
    """Global alignment performance and metrics."""
    ref_length: int
    query_length: int
    matches: int
    mismatches: int
    gaps: int
    identity_percentage: float
    alignment_score: float
    blocks: List[AlignmentBlock] = field(default_factory=list)

