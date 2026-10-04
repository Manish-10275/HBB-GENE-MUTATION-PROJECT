/** Backend API client for HBB Mutation Analyzer */

import {
  AnalyzeResponse,
  CopilotChatMessage,
  CopilotResponse,
  ExampleSequence,
  EvidencePacket,
  ReportResponse,
  VariantSearchResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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
