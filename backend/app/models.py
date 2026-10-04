"""Pydantic data models for request, response, and scientific analysis."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# Sequence Normalization Models
class SequenceNormalizationResult(BaseModel):
    raw_sequence: str
    clean_sequence: str
    header: Optional[str] = None
    length: int
    gc_content: float
    is_valid: bool
    validation_errors: List[str] = Field(default_factory=list)


# Alignment Models
class AlignmentBlock(BaseModel):
    block_index: int
    ref_start: int
    ref_end: int
    query_start: int
    query_end: int
    ref_seq: str
    query_seq: str
    match_line: str


class AlignmentSummary(BaseModel):
    ref_length: int
    query_length: int
    matches: int
    mismatches: int
    gaps: int
    identity_percentage: float
    alignment_score: float
    blocks: List[AlignmentBlock] = Field(default_factory=list)


# Codon & Variant Models
class CodonChange(BaseModel):
    codon_number: int
    c_start: int
    c_end: int
    ref_codon: str
    sample_codon: str
    ref_aa: str
    sample_aa: str
    ref_aa_single: str
    sample_aa_single: str
    consequence: str
    is_stop_gain: bool = False
    is_stop_loss: bool = False
    is_synonymous: bool = False


class DetectedVariant(BaseModel):
    id: str
    variant_type: str  # "substitution", "insertion", "deletion"
    ref_position_mrna: int  # 1-based mRNA index
    c_position: str  # e.g., "118", "-5", "*12"
    ref_allele: str
    alt_allele: str
    hgvs_c: str  # e.g., "NM_000518.5:c.118C>T"
    hgvs_p: Optional[str] = None  # e.g., "p.Gln40Ter"
    codon_change: Optional[CodonChange] = None
    functional_impact: str  # "Nonsense", "Missense", "Synonymous", "Frameshift", "Non-coding", "Unknown"
    confidence: str = "Deterministic"
    equivalent_nomenclature: List[str] = Field(default_factory=list)
    nomenclature_notes: Optional[str] = None


# Evidence Models
class ClinVarRecord(BaseModel):
    id: str
    title: str
    accession: Optional[str] = None
    clinical_significance: str = "Unknown"
    review_status: str = "no assertion provided"
    conditions: List[str] = Field(default_factory=list)
    last_evaluated: Optional[str] = None
    variation_id: Optional[str] = None
    source: str = "NCBI ClinVar"
    url: str
    is_exact_match: bool = False
    evidence_type: str = "DIRECT VARIANT EVIDENCE"
    retrieval_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))


class PubMedRecord(BaseModel):
    pmid: str
    title: str
    journal: str = ""
    pub_date: str = ""
    authors: List[str] = Field(default_factory=list)
    url: str
    abstract_snippet: Optional[str] = None
    source: str = "NCBI PubMed"
    is_exact_match: bool = False
    is_direct_evidence: bool = False
    evidence_type: str = "RELATED GENE OR DISEASE EVIDENCE"  # "DIRECT VARIANT EVIDENCE", "RELATED GENE OR DISEASE EVIDENCE", "CONTEXTUAL EVIDENCE"
    retrieval_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))


class ScreeningClassification(BaseModel):
    zygosity: str = "Heterozygous"  # "Heterozygous" or "Homozygous"
    condition_name: str
    severity: str  # "Normal", "Carrier / Minor", "Intermediate to Major", "Major / Severe"
    thalassemia_type: str  # "None", "β0 Thalassemia", "β+ Thalassemia", "Sickle Trait", etc.
    clinical_summary: str
    laboratory_correlations: List[str] = Field(default_factory=list)
    educational_disclaimer: str = (
        "Educational and research simulation model only. Clinical diagnosis requires "
        "certified molecular genetic testing, complete blood count (CBC), and "
        "high-performance liquid chromatography (HPLC) hemoglobin electrophoresis."
    )


class EvidencePacket(BaseModel):
    analysis_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reference_accession: str = "NM_000518.5"
    gene_symbol: str = "HBB"
    summary: Dict[str, Any] = Field(default_factory=dict)
    variants: List[DetectedVariant] = Field(default_factory=list)
    clinvar_records: List[ClinVarRecord] = Field(default_factory=list)
    pubmed_records: List[PubMedRecord] = Field(default_factory=list)
    screening_classification: Optional[ScreeningClassification] = None
    limitations: List[str] = Field(default_factory=list)
    source_metadata: Dict[str, Any] = Field(default_factory=dict)


# API Request and Response Models
class AnalyzeRequest(BaseModel):
    sequence: str
    reference_accession: str = "NM_000518.5"
    zygosity: Optional[str] = "heterozygous"  # "heterozygous" or "homozygous"


class AiSynthesisStatus(BaseModel):
    available: bool = True
    provider: str = "groq"
    model: str = "openai/gpt-oss-120b"
    status: str = "success"  # "success", "no_key", "error"
    answer: Optional[str] = None
    fallback: bool = False
    evidence_used: List[str] = Field(default_factory=list)
    provenance_sections: List[str] = Field(default_factory=list)
    provenance_label: str = "AI synthesis grounded in retrieved NCBI evidence"


class AnalyzeResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    summary: Dict[str, Any] = Field(default_factory=dict)
    alignment: Optional[AlignmentSummary] = None
    variants: List[DetectedVariant] = Field(default_factory=list)
    evidence_packet: Optional[EvidencePacket] = None
    screening_classification: Optional[ScreeningClassification] = None
    reference_metadata: Optional[Dict[str, Any]] = None
    ai: Optional[AiSynthesisStatus] = None


class SimulatorPreset(BaseModel):
    id: str
    name: str
    subtitle: str
    category: str
    accession: str
    description: str


class SimulatorGenerateRequest(BaseModel):
    preset_id: str


class SimulatorGenerateResponse(BaseModel):
    sequence: str
    preset_id: str
    name: str
    reference_accession: str
    coordinate_type: str
    description: str


class VariantSearchRequest(BaseModel):
    query: str  # e.g. "NM_000518.5:c.118C>T" or "c.118C>T" or "c.20A>T"


class VariantSearchResponse(BaseModel):
    query: str
    standardized_hgvs_c: Optional[str] = None
    clinvar_records: List[ClinVarRecord] = Field(default_factory=list)
    pubmed_records: List[PubMedRecord] = Field(default_factory=list)
    source: str = "NCBI E-Utilities"
    error: Optional[str] = None


class CopilotChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class CopilotRequest(BaseModel):
    question: str
    evidence_packet: EvidencePacket
    conversation_history: List[CopilotChatMessage] = Field(default_factory=list)


class CopilotResponse(BaseModel):
    answer: str
    evidence_used: List[str] = Field(default_factory=list)
    limitations_cited: List[str] = Field(default_factory=list)
    status: str = "success"  # "success", "no_key", "error"
    provider: str = "groq"
    model: str = "openai/gpt-oss-120b"
    fallback: bool = False
    provenance_sections: List[str] = Field(default_factory=list)
    provenance_label: str = "AI synthesis grounded in retrieved NCBI evidence"


class ReportRequest(BaseModel):
    evidence_packet: EvidencePacket
    copilot_summary: Optional[str] = None


class ReportResponse(BaseModel):
    markdown_content: str
    html_content: str
    generated_at: str
    title: str = "HBB Mutation Research Analysis Report"
