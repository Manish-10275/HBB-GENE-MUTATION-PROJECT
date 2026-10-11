/**
 * Unit & Integration Tests for Frontend v2 Architecture Integration.
 *
 * Scenarios Tested:
 * 1. Successful variant analysis (analyzeVariantV2 with deterministic typing)
 * 2. Malformed variant (structured AnalysisErrorDTO handling)
 * 3. Reference mismatch (structured AnalysisErrorDTO handling)
 * 4. Evidence unavailable (tri-state status classification)
 * 5. ClinVar discrepancy (recording and rendering without overriding core)
 * 6. AI synthesis (synthesizeCopilotV2 grounded response)
 * 7. AI evidence unavailable (graceful fallback)
 * 8. Provenance rendering (audit metadata verification)
 * 9. Structured API error handling (AnalysisApiError properties and details)
 */

import test from "node:test";
import assert from "node:assert";

import {
  AnalysisApiError,
  analyzeVariantV2,
  classifyEvidenceStatus,
  fetchClinVarEvidence,
  fetchHealthV2,
  fetchPubMedEvidence,
  synthesizeCopilotV2,
} from "../lib/api";
import {
  ClinVarEvidenceResponseDTO,
  CopilotResponseDTO,
  HealthDiagnosticsResponseDTO,
  VariantAnalysisResponseDTO,
} from "../lib/types";

// Helper to temporarily intercept global fetch for isolated testing
function mockFetch(handler: (url: string, init?: RequestInit) => Promise<Response>) {
  const originalFetch = global.fetch;
  global.fetch = handler as any;
  return () => {
    global.fetch = originalFetch;
  };
}

test("Scenario 1: Successful variant analysis with deterministic facts", async () => {
  const mockResponse: VariantAnalysisResponseDTO = {
    input_query: "c.118C>T",
    normalized_hgvs_c: "c.118C>T",
    transcript_accession: "NM_000518.5",
    c_position: "118",
    variant_type: "substitution",
    region: "Exon 2",
    ref_allele: "C",
    alt_allele: "T",
    mrna_position: 168,
    genomic_accession: "NG_000007.3",
    genomic_coordinate: 70842,
    hgvs_p: "p.Gln40Ter",
    molecular_impact: "Nonsense (Stop Gain)",
    codon_change: {
      codon_number: 40,
      c_start: 118,
      c_end: 120,
      ref_codon: "CAG",
      sample_codon: "TAG",
      ref_aa: "Gln",
      sample_aa: "Ter",
      is_stop_gain: true,
      is_stop_loss: false,
      is_synonymous: false,
    },
    ptc_coordinate: 40,
    confidence: "Deterministic",
    equivalent_nomenclature: ["c.118C>T", "p.Gln40*"],
    nomenclature_notes: "Codon 40 nonsense mutation",
    evidence_status: "found",
    clinvar_evidence: null,
    discrepancies: [],
  };

  const restore = mockFetch(async (url, init) => {
    assert.match(url, /\/api\/v2\/analyze\/variant$/);
    assert.strictEqual(init?.method, "POST");
    const body = JSON.parse(init?.body as string);
    assert.strictEqual(body.query, "c.118C>T");
    return new Response(JSON.stringify(mockResponse), { status: 200, headers: { "Content-Type": "application/json" } });
  });

  try {
    const result = await analyzeVariantV2("c.118C>T", false);
    assert.strictEqual(result.normalized_hgvs_c, "c.118C>T");
    assert.strictEqual(result.transcript_accession, "NM_000518.5");
    assert.strictEqual(result.variant_type, "substitution");
    assert.strictEqual(result.molecular_impact, "Nonsense (Stop Gain)");
    assert.strictEqual(result.hgvs_p, "p.Gln40Ter");
    assert.ok(result.codon_change);
    assert.strictEqual(result.codon_change.codon_number, 40);
    assert.strictEqual(result.codon_change.is_stop_gain, true);
    assert.strictEqual(result.codon_change.ref_codon, "CAG");
    assert.strictEqual(result.codon_change.sample_codon, "TAG");
    assert.strictEqual(result.confidence, "Deterministic");
  } finally {
    restore();
  }
});

test("Scenario 2: Malformed variant returns structured AnalysisApiError (MALFORMED_HGVS)", async () => {
  const errorPayload = {
    detail: {
      error_code: "MALFORMED_HGVS",
      message: "Invalid HGVS cDNA query: 'c.invalid!'",
      details: { input: "c.invalid!" },
    },
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(errorPayload), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  });

  try {
    await analyzeVariantV2("c.invalid!");
    assert.fail("Should have thrown AnalysisApiError");
  } catch (err: any) {
    assert.ok(err instanceof AnalysisApiError);
    assert.strictEqual(err.errorCode, "MALFORMED_HGVS");
    assert.match(err.message, /Invalid HGVS cDNA query/);
    assert.strictEqual(err.details?.input, "c.invalid!");
  } finally {
    restore();
  }
});

test("Scenario 3: Reference mismatch returns structured AnalysisApiError (REFERENCE_MISMATCH)", async () => {
  const errorPayload = {
    detail: {
      error_code: "REFERENCE_MISMATCH",
      message: "Reference nucleotide mismatch at c.118: expected 'C', query specified 'A'",
      details: { position: "118", expected: "C", found: "A" },
    },
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(errorPayload), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  });

  try {
    await analyzeVariantV2("c.118A>T");
    assert.fail("Should have thrown AnalysisApiError");
  } catch (err: any) {
    assert.ok(err instanceof AnalysisApiError);
    assert.strictEqual(err.errorCode, "REFERENCE_MISMATCH");
    assert.match(err.message, /Reference nucleotide mismatch/);
    assert.strictEqual(err.details?.expected, "C");
    assert.strictEqual(err.details?.found, "A");
  } finally {
    restore();
  }
});

test("Scenario 4: Evidence unavailable distinguishes all three unavailable states", () => {
  // Case A: Query succeeded, zero records found
  const notFoundState = classifyEvidenceStatus("not_found", 0, false);
  assert.strictEqual(notFoundState, "not_found");

  // Case B: Network/server error
  const errorState = classifyEvidenceStatus("error", 0, false);
  assert.strictEqual(errorState, "unretrievable");

  // Case C: Offline mode active, variant missing from local fixtures
  const fixtureMissingState = classifyEvidenceStatus("fixture_missing", 0, true);
  assert.strictEqual(fixtureMissingState, "fixture_unavailable");

  const fixtureUnavailableState = classifyEvidenceStatus("fixture_unavailable", 0, true);
  assert.strictEqual(fixtureUnavailableState, "fixture_unavailable");

  // Case D: Available records
  const availableState = classifyEvidenceStatus("found", 2, false);
  assert.strictEqual(availableState, "available");
});

test("Scenario 5: ClinVar discrepancy is recorded and core consequence is NOT overridden", async () => {
  const mockResponse: VariantAnalysisResponseDTO = {
    input_query: "c.118C>T",
    normalized_hgvs_c: "c.118C>T",
    transcript_accession: "NM_000518.5",
    c_position: "118",
    variant_type: "substitution",
    region: "Exon 2",
    ref_allele: "C",
    alt_allele: "T",
    hgvs_p: "p.Gln40Ter",
    molecular_impact: "Nonsense (Stop Gain)",
    confidence: "Deterministic",
    equivalent_nomenclature: [],
    clinvar_evidence: {
      query: "c.118C>T",
      status: "found",
      records: [
        {
          variation_id: "15402",
          accession: "VCV000015402",
          title: "NM_000518.5:c.118C>T",
          clinical_significance: "Pathogenic",
          review_status: "criteria provided, multiple submitters, no conflicts",
          conditions: ["Beta-thalassemia"],
          url: "https://www.ncbi.nlm.nih.gov/clinvar/variation/15402/",
          is_exact_match: true,
          retrieval_rank: 1,
        },
      ],
      primary_record: null,
      discrepancies: [
        {
          field_name: "consequence",
          deterministic_value: "Nonsense (Stop Gain)",
          evidence_value: "Missense",
          description: "Deterministic codon translation calculates premature stop, but test evidence asserts missense.",
        },
      ],
      error_message: null,
    },
    discrepancies: [
      {
        field_name: "consequence",
        deterministic_value: "Nonsense (Stop Gain)",
        evidence_value: "Missense",
        description: "Deterministic codon translation calculates premature stop, but test evidence asserts missense.",
      },
    ],
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(mockResponse), { status: 200 });
  });

  try {
    const result = await analyzeVariantV2("c.118C>T", true);
    // Core consequence remains authoritative
    assert.strictEqual(result.molecular_impact, "Nonsense (Stop Gain)");
    assert.strictEqual(result.hgvs_p, "p.Gln40Ter");

    // Discrepancy is explicitly populated
    assert.strictEqual(result.discrepancies.length, 1);
    assert.strictEqual(result.discrepancies[0].deterministic_value, "Nonsense (Stop Gain)");
    assert.strictEqual(result.discrepancies[0].evidence_value, "Missense");
  } finally {
    restore();
  }
});

test("Scenario 6: AI synthesis invokes /api/v2/copilot/synthesize and parses CopilotResponseDTO", async () => {
  const mockCopilotResponse: CopilotResponseDTO = {
    answer: "## DIRECT SCIENTIFIC ANSWER\nc.118C>T introduces a premature stop codon p.Gln40Ter.",
    evidence_used: ["Deterministic Sequence Engine", "NCBI ClinVar VCV000015402"],
    limitations_cited: ["RefSeq NM_000518.5 single transcript model"],
    status: "success",
    provider: "groq/openai/gpt-oss-120b",
    model: "openai/gpt-oss-120b",
    fallback: false,
    provenance_sections: ["DIRECT SCIENTIFIC ANSWER", "COMPUTED FACTS", "DATABASE EVIDENCE"],
    provenance_label: "AI Synthesized + Deterministic Evidence",
  };

  const restore = mockFetch(async (url, init) => {
    assert.match(url, /\/api\/v2\/copilot\/synthesize$/);
    const body = JSON.parse(init?.body as string);
    assert.strictEqual(body.query, "c.118C>T");
    assert.strictEqual(body.question, "What is the molecular consequence?");
    return new Response(JSON.stringify(mockCopilotResponse), { status: 200 });
  });

  try {
    const res = await synthesizeCopilotV2({
      query: "c.118C>T",
      question: "What is the molecular consequence?",
      include_evidence: true,
      include_literature: true,
    });
    assert.strictEqual(res.status, "success");
    assert.strictEqual(res.fallback, false);
    assert.match(res.answer, /p\.Gln40Ter/);
    assert.strictEqual(res.evidence_used.length, 2);
    assert.strictEqual(res.provenance_label, "AI Synthesized + Deterministic Evidence");
  } finally {
    restore();
  }
});

test("Scenario 7: AI evidence unavailable falls back gracefully with deterministic synthesis", async () => {
  const fallbackResponse: CopilotResponseDTO = {
    answer: "## DIRECT SCIENTIFIC ANSWER\nDeterministic bioinformatics analysis confirms c.118C>T (p.Gln40Ter).",
    evidence_used: ["Deterministic Sequence Engine"],
    limitations_cited: ["Offline execution"],
    status: "no_key",
    provider: "DeterministicSequenceEngine",
    model: "deterministic-fallback",
    fallback: true,
    provenance_sections: ["DIRECT SCIENTIFIC ANSWER", "A. COMPUTED FACTS", "D. DETERMINISTIC SYNTHESIS"],
    provenance_label: "Deterministic",
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(fallbackResponse), { status: 200 });
  });

  try {
    const res = await synthesizeCopilotV2({
      query: "c.118C>T",
      question: "Explain the mutation.",
    });
    assert.strictEqual(res.status, "no_key");
    assert.strictEqual(res.fallback, true);
    assert.strictEqual(res.provider, "DeterministicSequenceEngine");
    assert.match(res.answer, /Deterministic bioinformatics analysis confirms/);
  } finally {
    restore();
  }
});

test("Scenario 8: Provenance metadata rendering and authenticity flags", async () => {
  const mockClinVar: ClinVarEvidenceResponseDTO = {
    query: "c.118C>T",
    status: "found",
    records: [
      {
        variation_id: "15402",
        accession: "VCV000015402",
        title: "NM_000518.5:c.118C>T",
        clinical_significance: "Pathogenic",
        review_status: "criteria provided",
        conditions: ["Beta-thalassemia"],
        url: "https://www.ncbi.nlm.nih.gov/clinvar/variation/15402/",
        is_exact_match: true,
        retrieval_rank: 1,
        provenance: {
          source: "offline_fixture",
          provider: "ClinVarOfflineProvider",
          mode: "offline",
          retrieval_status: "success",
          external_identifier: "15402",
          is_fixture: true,
          retrieval_timestamp: "2026-10-07T21:00:00Z",
        },
      },
    ],
    discrepancies: [],
    provenance: {
      source: "offline_fixture",
      provider: "ClinVarOfflineProvider",
      mode: "offline",
      retrieval_status: "success",
      is_fixture: true,
      retrieval_timestamp: "2026-10-07T21:00:00Z",
    },
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(mockClinVar), { status: 200 });
  });

  try {
    const res = await fetchClinVarEvidence("c.118C>T");
    assert.strictEqual(res.status, "found");
    assert.ok(res.provenance);
    assert.strictEqual(res.provenance.provider, "ClinVarOfflineProvider");
    assert.strictEqual(res.provenance.mode, "offline");
    assert.strictEqual(res.provenance.is_fixture, true);

    const rec = res.records[0];
    assert.ok(rec.provenance);
    assert.strictEqual(rec.provenance.external_identifier, "15402");
    assert.strictEqual(rec.provenance.is_fixture, true);
  } finally {
    restore();
  }
});

test("Scenario 9: Structured API error handling parses error_code, message, and details", async () => {
  const errorObj = {
    detail: {
      error_code: "CODON_OUT_OF_BOUNDS",
      message: "cDNA coordinate c.9999 exceeds transcript coding bounds",
      details: { requested_c_pos: "9999", max_c_pos: "494" },
    },
  };

  const restore = mockFetch(async () => {
    return new Response(JSON.stringify(errorObj), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  });

  try {
    await analyzeVariantV2("c.9999A>G");
    assert.fail("Expected AnalysisApiError to be thrown");
  } catch (err: any) {
    assert.ok(err instanceof AnalysisApiError);
    assert.strictEqual(err.errorCode, "CODON_OUT_OF_BOUNDS");
    assert.strictEqual(err.message, "cDNA coordinate c.9999 exceeds transcript coding bounds");
    assert.strictEqual(err.details.requested_c_pos, "9999");
    assert.strictEqual(err.details.max_c_pos, "494");
  } finally {
    restore();
  }
});

test("Extended Diagnostics: fetchHealthV2 returns reference readiness and evidence mode", async () => {
  const mockHealth: HealthDiagnosticsResponseDTO = {
    status: "healthy",
    service: "HBB Mutation Analyzer API v2",
    version: "2.0.0",
    reference_availability: {
      "NM_000518.5": true,
      "NG_000007.3": true,
    },
    evidence_provider_mode: "offline",
    fixture_availability: {
      "clinvar_fixtures.json": true,
      "pubmed_fixtures.json": true,
    },
  };

  const restore = mockFetch(async (url) => {
    assert.match(url, /\/api\/v2\/health$/);
    return new Response(JSON.stringify(mockHealth), { status: 200 });
  });

  try {
    const health = await fetchHealthV2();
    assert.strictEqual(health.status, "healthy");
    assert.strictEqual(health.version, "2.0.0");
    assert.strictEqual(health.reference_availability["NM_000518.5"], true);
    assert.strictEqual(health.evidence_provider_mode, "offline");
    assert.strictEqual(health.fixture_availability["clinvar_fixtures.json"], true);
  } finally {
    restore();
  }
});
