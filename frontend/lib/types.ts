/** Type definitions for HBB Mutation Analyzer */

export interface AlignmentBlock {
  block_index: number;
  ref_start: number;
  ref_end: number;
  query_start: number;
  query_end: number;
  ref_seq: string;
  query_seq: string;
  match_line: string;
}

export interface AlignmentSummary {
  ref_length: number;
  query_length: number;
  matches: number;
  mismatches: number;
  gaps: number;
  identity_percentage: number;
  alignment_score: number;
  blocks: AlignmentBlock[];
}

export interface CodonChange {
  codon_number: number;
  c_start: number;
  c_end: number;
  ref_codon: string;
  sample_codon: string;
  ref_aa: string;
  sample_aa: string;
  ref_aa_single: string;
  sample_aa_single: string;
  consequence: string;
  is_stop_gain: boolean;
  is_stop_loss: boolean;
  is_synonymous: boolean;
}

export interface DetectedVariant {
  id: string;
  variant_type: "substitution" | "insertion" | "deletion" | string;
  ref_position_mrna: number;
  c_position: string;
  ref_allele: string;
  alt_allele: string;
  hgvs_c: string;
  hgvs_p?: string | null;
  codon_change?: CodonChange | null;
  functional_impact: string;
  confidence: string;
}

export interface ClinVarRecord {
  id: string;
  title: string;
  accession?: string | null;
  clinical_significance: string;
  review_status: string;
  conditions: string[];
  last_evaluated?: string | null;
  variation_id?: string | null;
  source: string;
  url: string;
  is_exact_match?: boolean;
  evidence_type?: string;
  retrieval_date?: string;
}

export interface PubMedRecord {
  pmid: string;
  title: string;
  journal: string;
  pub_date: string;
  authors: string[];
  url: string;
  abstract_snippet?: string | null;
  source: string;
  is_exact_match?: boolean;
  is_direct_evidence?: boolean;
  evidence_type?: string;
  retrieval_date?: string;
}

export interface ScreeningClassification {
  zygosity: string;
  condition_name: string;
  severity: string;
  thalassemia_type: string;
  clinical_summary: string;
  laboratory_correlations: string[];
  educational_disclaimer: string;
}

export interface SimulatorPreset {
  id: string;
  name: string;
  subtitle: string;
  category: string;
  accession: string;
  description: string;
}

export interface SimulatorGenerateResponse {
  sequence: string;
  preset_id: string;
  name: string;
  reference_accession: string;
  coordinate_type: string;
  description: string;
}

export interface EvidencePacket {
  analysis_id: string;
  timestamp: string;
  reference_accession: string;
  gene_symbol: string;
  summary: {
    reference_accession?: string;
    reference_length_bp?: number;
    cds_coordinates?: string;
    cds_length_bp?: number;
    sample_length_bp?: number;
    sequence_identity_pct?: number;
    alignment_score?: number;
    detected_variants_count?: number;
    clinvar_records_count?: number;
    pubmed_records_count?: number;
    [key: string]: any;
  };
  variants: DetectedVariant[];
  clinvar_records: ClinVarRecord[];
  pubmed_records: PubMedRecord[];
  screening_classification?: ScreeningClassification | null;
  limitations: string[];
  source_metadata: Record<string, any>;
}

export interface AiSynthesisStatus {
  available: boolean;
  provider: string;
  model: string;
  status: "success" | "no_key" | "error";
  answer?: string | null;
  fallback: boolean;
  evidence_used: string[];
  provenance_sections?: string[];
  provenance_label?: string;
}

export interface AnalyzeResponse {
  success: boolean;
  error?: string | null;
  summary: Record<string, any>;
  alignment?: AlignmentSummary | null;
  variants: DetectedVariant[];
  evidence_packet?: EvidencePacket | null;
  screening_classification?: ScreeningClassification | null;
  reference_metadata?: Record<string, any> | null;
  ai?: AiSynthesisStatus | null;
}

export interface VariantSearchResponse {
  query: string;
  standardized_hgvs_c?: string | null;
  clinvar_records: ClinVarRecord[];
  pubmed_records: PubMedRecord[];
  source: string;
  error?: string | null;
}

export interface CopilotChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface CopilotResponse {
  answer: string;
  evidence_used: string[];
  limitations_cited: string[];
  status: "success" | "no_key" | "error";
  provider?: string;
  model?: string;
  fallback?: boolean;
  provenance_sections?: string[];
  provenance_label?: string;
}

export interface ReportResponse {
  markdown_content: string;
  html_content: string;
  generated_at: string;
  title: string;
}

export interface ExampleSequence {
  filename: string;
  title: string;
  description: string;
  is_validation_case: boolean;
  category: string;
  sequence: string;
}
