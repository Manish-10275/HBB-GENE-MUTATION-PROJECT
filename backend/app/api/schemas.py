"""Pydantic V2 DTO schemas for API request and response models."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VariantAnalysisRequest(BaseModel):
    """Payload for submitting a variant query for analysis."""
    query: str = Field(..., description="HGVS cDNA or genomic query string, e.g. 'c.118C>T'")
    include_evidence: bool = Field(False, description="Whether to also retrieve external ClinVar evidence")


class CodonChangeDTO(BaseModel):
    """Codon triplet and amino acid alteration details."""
    codon_number: int
    c_start: int
    c_end: int
    ref_codon: str
    sample_codon: str
    ref_aa: str
    sample_aa: str
    is_stop_gain: bool = False
    is_stop_loss: bool = False
    is_synonymous: bool = False


class DiscrepancyDTO(BaseModel):
    """Recorded conflict between deterministic calculation and external annotation."""
    field_name: str
    deterministic_value: str
    evidence_value: str
    description: str


class ProvenanceDTO(BaseModel):
    """Audit metadata tracking retrieval method and authenticity."""
    source: str
    provider: str
    mode: str
    retrieval_status: str
    external_identifier: Optional[str] = None
    is_fixture: bool = False
    retrieval_timestamp: Optional[str] = None


class ClinVarRecordDTO(BaseModel):
    """Normalized ClinVar external record."""
    variation_id: str
    accession: str
    title: str
    clinical_significance: str
    review_status: str
    conditions: List[str] = Field(default_factory=list)
    url: str
    is_exact_match: bool
    retrieval_rank: int
    provenance: Optional[ProvenanceDTO] = None


class ClinVarEvidenceResponseDTO(BaseModel):
    """Consolidated ClinVar evidence packet."""
    query: str
    status: str
    records: List[ClinVarRecordDTO] = Field(default_factory=list)
    primary_record: Optional[ClinVarRecordDTO] = None
    discrepancies: List[DiscrepancyDTO] = Field(default_factory=list)
    error_message: Optional[str] = None
    provenance: Optional[ProvenanceDTO] = None


class VariantAnalysisResponse(BaseModel):
    """Deterministic variant interpretation result with optional evidence."""
    input_query: str
    normalized_hgvs_c: str
    transcript_accession: str
    c_position: str
    variant_type: str
    region: str
    ref_allele: str
    alt_allele: str
    mrna_position: Optional[int] = None
    genomic_accession: Optional[str] = None
    genomic_coordinate: Optional[int] = None
    hgvs_p: Optional[str] = None
    molecular_impact: str
    codon_change: Optional[CodonChangeDTO] = None
    ptc_coordinate: Optional[int] = None
    confidence: str = "Deterministic"
    equivalent_nomenclature: List[str] = Field(default_factory=list)
    nomenclature_notes: Optional[str] = None
    evidence_status: Optional[str] = None
    clinvar_evidence: Optional[ClinVarEvidenceResponseDTO] = None
    discrepancies: List[DiscrepancyDTO] = Field(default_factory=list)


class PubMedArticleDTO(BaseModel):
    """Normalized literature citation."""
    pmid: str
    title: str
    journal: Optional[str] = None
    pub_date: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    url: str
    provenance: Optional[ProvenanceDTO] = None


class PubMedEvidenceResponseDTO(BaseModel):
    """Consolidated PubMed evidence response."""
    query: str
    status: str
    articles: List[PubMedArticleDTO] = Field(default_factory=list)
    error_message: Optional[str] = None
    provenance: Optional[ProvenanceDTO] = None


class AnalysisErrorDTO(BaseModel):
    """Structured domain error representation for HTTP 400/422 responses."""
    error_code: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class CopilotSynthesisRequestDTO(BaseModel):
    """Payload for requesting AI copilot synthesis grounded on variant analysis."""
    query: str = Field(..., description="HGVS cDNA query, e.g. 'c.118C>T'")
    question: Optional[str] = Field(None, description="Specific research question, or empty for automatic synthesis")
    include_evidence: bool = Field(True, description="Whether to include ClinVar database evidence")
    include_literature: bool = Field(False, description="Whether to query PubMed literature evidence")


class CopilotResponseDTO(BaseModel):
    """Normalized response schema for AI copilot synthesis."""
    answer: str
    evidence_used: List[str] = Field(default_factory=list)
    limitations_cited: List[str] = Field(default_factory=list)
    status: str
    provider: str
    model: str
    fallback: bool
    provenance_sections: List[str] = Field(default_factory=list)
    provenance_label: str


class HealthDiagnosticsResponse(BaseModel):
    """System diagnostic and reference readiness status."""
    status: str
    service: str
    version: str
    reference_availability: Dict[str, bool]
    evidence_provider_mode: str
    fixture_availability: Dict[str, bool]

