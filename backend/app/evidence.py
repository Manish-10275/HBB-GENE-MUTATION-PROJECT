"""Assembles the structured EvidencePacket representing the complete scientific context."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.models import (
    AlignmentSummary,
    ClinVarRecord,
    DetectedVariant,
    EvidencePacket,
    PubMedRecord,
)
from app.reference import ReferenceData


STANDARD_LIMITATIONS: List[str] = [
    "Analysis is based on in silico pairwise alignment against reference transcript NM_000518.5 (CCDS7753.1).",
    "Does not evaluate non-coding deep intronic regulatory elements outside the sequenced span.",
    "Database records reflect NCBI ClinVar and PubMed index at retrieval time and are not diagnostic determinations.",
    "Protein consequence predictions assume canonical translation initiation and reading frame.",
    "This tool is strictly designed for research and educational investigation and does not provide clinical diagnoses."
]


def assemble_evidence_packet(
    ref_data: ReferenceData,
    alignment_summary: AlignmentSummary,
    variants: List[DetectedVariant],
    clinvar_records: List[ClinVarRecord],
    pubmed_records: List[PubMedRecord],
    custom_limitations: Optional[List[str]] = None
) -> EvidencePacket:
    """
    Constructs an inspectable, immutable scientific EvidencePacket.
    This serves as the single source of truth for both report generation and AI synthesis.
    """
    analysis_id = f"HBB-EXP-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now(timezone.utc).isoformat()

    summary_info: Dict[str, Any] = {
        "reference_accession": ref_data.accession,
        "reference_length_bp": ref_data.total_length,
        "cds_coordinates": f"{ref_data.cds_start}..{ref_data.cds_end}",
        "cds_length_bp": ref_data.cds_length,
        "sample_length_bp": alignment_summary.query_length,
        "sequence_identity_pct": alignment_summary.identity_percentage,
        "alignment_score": alignment_summary.alignment_score,
        "detected_variants_count": len(variants),
        "clinvar_records_count": len(clinvar_records),
        "pubmed_records_count": len(pubmed_records),
    }

    source_meta: Dict[str, Any] = {
        "engine": "HBB Mutation Analyzer Bioinformatics Pipeline v1.0",
        "alignment_algorithm": "Needleman-Wunsch Global Pairwise Alignment",
        "reference_source": ref_data.source,
        "reference_source_url": ref_data.source_url,
        "evidence_databases": ["NCBI ClinVar", "NCBI PubMed (E-utilities)"],
        "nomenclature_standard": "HGVS Sequence Variant Nomenclature v20.05"
    }

    limitations = list(STANDARD_LIMITATIONS)
    if custom_limitations:
        limitations.extend(custom_limitations)

    return EvidencePacket(
        analysis_id=analysis_id,
        timestamp=timestamp,
        reference_accession=ref_data.accession,
        gene_symbol=ref_data.gene,
        summary=summary_info,
        variants=variants,
        clinvar_records=clinvar_records,
        pubmed_records=pubmed_records,
        limitations=limitations,
        source_metadata=source_meta
    )
