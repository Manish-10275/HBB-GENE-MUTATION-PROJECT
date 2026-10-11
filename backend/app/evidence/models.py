"""Evidence domain models, provenance metadata, and structured error states."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from app.core.models import NormalizedVariant


class EvidenceStatus(str, Enum):
    """Structured retrieval and availability status for external evidence."""
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    OFFLINE_DATA_UNAVAILABLE = "OFFLINE_DATA_UNAVAILABLE"
    NETWORK_UNAVAILABLE = "NETWORK_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"
    RATE_LIMITED = "RATE_LIMITED"
    INVALID_EXTERNAL_RESPONSE = "INVALID_EXTERNAL_RESPONSE"
    PROVIDER_ERROR = "PROVIDER_ERROR"


class RetrievalMode(str, Enum):
    """Execution mode of the evidence provider."""
    OFFLINE = "offline"
    LIVE = "live"


@dataclass(frozen=True)
class EvidenceProvenance:
    """Rigorous audit and provenance trail for retrieved evidence."""
    source: str                              # "ClinVar", "PubMed"
    provider: str                            # "OfflineClinVarProvider", "LiveClinVarProvider"
    mode: RetrievalMode                      # offline or live
    retrieval_status: EvidenceStatus
    external_identifier: Optional[str] = None # Variation ID, VCV accession, or PMID
    is_fixture: bool = False
    fixture_path: Optional[str] = None
    retrieval_timestamp: Optional[str] = None
    transformations: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceDiscrepancy:
    """Explicit discrepancy between deterministic consequence and external evidence."""
    field_name: str
    deterministic_value: str
    evidence_value: str
    description: str


@dataclass(frozen=True)
class ClinVarRecord:
    """Normalized, strongly typed representation of an external ClinVar record."""
    variation_id: str
    accession: str
    title: str
    clinical_significance: str
    review_status: str
    conditions: List[str]
    last_evaluated: Optional[str]
    url: str
    is_exact_match: bool
    retrieval_rank: int
    provenance: EvidenceProvenance
    raw_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ClinVarEvidenceResult:
    """Consolidated ClinVar evidence packet for a query variant."""
    query: str
    status: EvidenceStatus
    records: List[ClinVarRecord] = field(default_factory=list)
    primary_record: Optional[ClinVarRecord] = None
    normalized_variant: Optional[NormalizedVariant] = None
    discrepancies: List[EvidenceDiscrepancy] = field(default_factory=list)
    error_message: Optional[str] = None
    provenance: Optional[EvidenceProvenance] = None


@dataclass(frozen=True)
class PubMedArticle:
    """Normalized scholarly publication record from PubMed."""
    pmid: str
    title: str
    journal: Optional[str] = None
    pub_date: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    url: str = ""
    abstract_snippet: Optional[str] = None
    provenance: Optional[EvidenceProvenance] = None


@dataclass(frozen=True)
class PubMedEvidenceResult:
    """Consolidated PubMed evidence packet."""
    query: str
    status: EvidenceStatus
    articles: List[PubMedArticle] = field(default_factory=list)
    error_message: Optional[str] = None
    provenance: Optional[EvidenceProvenance] = None
