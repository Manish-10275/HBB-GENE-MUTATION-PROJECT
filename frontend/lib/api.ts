/** Backend API client for HBB Mutation Analyzer */

import {
  AnalysisErrorDTO,
  AnalyzeResponse,
  ClinVarEvidenceResponseDTO,
  CopilotChatMessage,
  CopilotResponse,
  CopilotResponseDTO,
  CopilotSynthesisRequestDTO,
  EvidenceAvailabilityStatus,
  EvidencePacket,
  ExampleSequence,
  HealthDiagnosticsResponseDTO,
  PubMedEvidenceResponseDTO,
  ReportResponse,
  VariantAnalysisResponseDTO,
  VariantSearchResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/** Custom typed error class representing structured domain and HTTP errors from the backend. */
export class AnalysisApiError extends Error {
  public readonly errorCode: string;
  public readonly details: Record<string, any>;

  constructor(message: string, errorCode: string = "UNKNOWN_ERROR", details: Record<string, any> = {}) {
    super(message);
    this.name = "AnalysisApiError";
    this.errorCode = errorCode;
    this.details = details;
    Object.setPrototypeOf(this, AnalysisApiError.prototype);
  }
}

/** Parses structured API errors or returns a fallback AnalysisApiError. */
async function parseErrorResponse(res: Response, fallbackMessage: string): Promise<AnalysisApiError> {
  try {
    const data = await res.json();
    const detail = data?.detail;
    if (detail && typeof detail === "object") {
      const code = detail.error_code || "ANALYSIS_ERROR";
      const msg = detail.message || fallbackMessage;
      const details = detail.details || {};
      return new AnalysisApiError(msg, code, details);
    }
    if (typeof detail === "string") {
      return new AnalysisApiError(detail, "API_ERROR");
    }
    if (data?.message) {
      return new AnalysisApiError(data.message, data.error_code || "API_ERROR", data.details || {});
    }
  } catch {
    // Ignore JSON parsing failure
  }
  return new AnalysisApiError(`${fallbackMessage} (Status: ${res.status})`, "HTTP_ERROR");
}

/**
 * Classifies the retrieval status into one of four unambiguous display categories:
 * - "available": Evidence records were successfully located and returned.
 * - "not_found": Query succeeded, but no records exist in the database for this variant.
 * - "fixture_unavailable": System is in offline mode and the requested variant is not in local fixtures.
 * - "unretrievable": Network failure, upstream NCBI timeout, or retrieval error occurred.
 */
export function classifyEvidenceStatus(
  statusString: string,
  recordsCount: number,
  isFixture: boolean = false
): EvidenceAvailabilityStatus {
  const s = (statusString || "").toLowerCase();
  if (s === "fixture_missing" || s === "fixture_unavailable") {
    return "fixture_unavailable";
  }
  if (s === "error" || s === "unretrievable" || s === "failed") {
    return "unretrievable";
  }
  if (s === "not_found" || recordsCount === 0) {
    if (isFixture && s.includes("missing")) {
      return "fixture_unavailable";
    }
    return "not_found";
  }
  return "available";
}

// ==========================================
// V2 Clean Architecture Endpoints
// ==========================================

/**
 * Deterministically analyzes a cDNA or genomic variant query using the Core Domain Engine.
 * Optionally retrieves external ClinVar evidence and checks for discrepancies.
 */
export async function analyzeVariantV2(
  query: string,
  includeEvidence: boolean = false
): Promise<VariantAnalysisResponseDTO> {
  const trimmed = query.trim();
  if (!trimmed) {
    throw new AnalysisApiError("Variant query string cannot be empty", "INVALID_INPUT");
  }

  const res = await fetch(`${API_BASE}/api/v2/analyze/variant`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: trimmed,
      include_evidence: includeEvidence,
    }),
  });

  if (!res.ok) {
    throw await parseErrorResponse(res, "Variant analysis failed");
  }

  return res.json();
}

/**
 * Retrieves external ClinVar evidence records for a given variant query with full provenance.
 */
export async function fetchClinVarEvidence(query: string): Promise<ClinVarEvidenceResponseDTO> {
  const res = await fetch(`${API_BASE}/api/v2/evidence/clinvar?query=${encodeURIComponent(query.trim())}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw await parseErrorResponse(res, "ClinVar evidence retrieval failed");
  }

  return res.json();
}

/**
 * Retrieves peer-reviewed scientific literature records from PubMed for a given variant.
 */
export async function fetchPubMedEvidence(
  query: string,
  maxResults: number = 10
): Promise<PubMedEvidenceResponseDTO> {
  const res = await fetch(
    `${API_BASE}/api/v2/evidence/pubmed?query=${encodeURIComponent(query.trim())}&max_results=${maxResults}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    throw await parseErrorResponse(res, "PubMed literature retrieval failed");
  }

  return res.json();
}

/**
 * Requests AI Copilot synthesis grounded strictly on deterministic variant analysis results.
 */
export async function synthesizeCopilotV2(
  payload: CopilotSynthesisRequestDTO
): Promise<CopilotResponseDTO> {
  const res = await fetch(`${API_BASE}/api/v2/copilot/synthesize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw await parseErrorResponse(res, "AI copilot synthesis failed");
  }

  return res.json();
}

/**
 * Retrieves system health, reference sequence readiness, and evidence provider diagnostic status.
 */
export async function fetchHealthV2(): Promise<HealthDiagnosticsResponseDTO> {
  const res = await fetch(`${API_BASE}/api/v2/health`, { cache: "no-store" });
  if (!res.ok) {
    throw await parseErrorResponse(res, "V2 health diagnostics check failed");
  }
  return res.json();
}

// ==========================================
// Legacy Endpoints (Preserved for compatibility)
// ==========================================

export async function fetchHealth(): Promise<{
  status: string;
  reference_accession: string;
  groq_configured: boolean;
  groq_model: string;
  ncbi_configured?: boolean;
}> {
  const res = await fetch(`${API_BASE}/health`, { cache: "no-store" });
  if (!res.ok) throw new Error("Backend health check failed");
  return res.json();
}

export async function fetchExamples(): Promise<ExampleSequence[]> {
  const res = await fetch(`${API_BASE}/examples`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load example sequences");
  return res.json();
}

export async function fetchReference(accession: string = "NM_000518.5"): Promise<any> {
  const res = await fetch(`${API_BASE}/reference?accession=${encodeURIComponent(accession)}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load reference sequence");
  return res.json();
}

export async function fetchReferenceList(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/reference/list`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load reference list");
  return res.json();
}

export async function fetchIndianMutations(): Promise<any> {
  const res = await fetch(`${API_BASE}/mutations/indian`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load Indian mutations panel");
  return res.json();
}

export async function fetchSimulatorPresets(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/simulator/presets`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load simulator presets");
  return res.json();
}

export async function generateSimulatedSequence(preset_id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/simulator/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ preset_id }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to generate simulated sequence.");
  }
  return res.json();
}

export async function analyzeSequence(
  sequence: string,
  referenceAccession: string = "NM_000518.5",
  zygosity: string = "heterozygous"
): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sequence,
      reference_accession: referenceAccession,
      zygosity,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const message =
      errorData.detail?.message ||
      (Array.isArray(errorData.detail?.errors)
        ? errorData.detail.errors.join("; ")
        : typeof errorData.detail === "string"
        ? errorData.detail
        : "Failed to analyze sequence.");
    throw new Error(message);
  }

  return res.json();
}

export async function searchVariantDirect(query: string): Promise<VariantSearchResponse> {
  const res = await fetch(`${API_BASE}/variant/search?query=${encodeURIComponent(query)}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Direct variant search failed.");
  }

  return res.json();
}

export async function askCopilot(
  question: string,
  evidence_packet: EvidencePacket,
  conversation_history: CopilotChatMessage[] = []
): Promise<CopilotResponse> {
  const res = await fetch(`${API_BASE}/copilot`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      evidence_packet,
      conversation_history,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Copilot synthesis request failed.");
  }

  return res.json();
}

export async function generateReport(
  evidence_packet: EvidencePacket,
  copilot_summary?: string
): Promise<ReportResponse> {
  const res = await fetch(`${API_BASE}/report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      evidence_packet,
      copilot_summary,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Report generation failed.");
  }

  return res.json();
}
