"use client";

import React, { useState } from "react";
import {
  Search,
  Loader2,
  Database,
  BookOpen,
  AlertCircle,
  X,
  ExternalLink,
  Dna,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Info,
} from "lucide-react";
import {
  AnalysisApiError,
  analyzeVariantV2,
  classifyEvidenceStatus,
  fetchPubMedEvidence,
} from "../lib/api";
import {
  PubMedArticleDTO,
  VariantAnalysisResponseDTO,
} from "../lib/types";

interface DirectVariantSearchProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DirectVariantSearch: React.FC<DirectVariantSearchProps> = ({
  isOpen,
  onClose,
}) => {
  const [query, setQuery] = useState("c.118C>T");
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<VariantAnalysisResponseDTO | null>(null);
  const [pubmedArticles, setPubmedArticles] = useState<PubMedArticleDTO[]>([]);
  const [pubmedLoading, setPubmedLoading] = useState(false);
  const [error, setError] = useState<{ message: string; code?: string; details?: any } | null>(null);

  if (!isOpen) return null;

  const handleSearch = async (termToSearch?: string) => {
    const q = (termToSearch || query).trim();
    if (!q) return;

    setLoading(true);
    setError(null);
    setAnalysisResult(null);
    setPubmedArticles([]);

    try {
      // 1. Execute deterministic variant analysis with ClinVar evidence retrieval
      const data = await analyzeVariantV2(q, true);
      setAnalysisResult(data);

      // 2. Concurrently fetch PubMed literature
      setPubmedLoading(true);
      fetchPubMedEvidence(q, 5)
        .then((pubRes) => {
          setPubmedArticles(pubRes.articles || []);
        })
        .catch(() => {
          // Literature fetch error is non-fatal
          setPubmedArticles([]);
        })
        .finally(() => {
          setPubmedLoading(false);
        });
    } catch (err: any) {
      if (err instanceof AnalysisApiError) {
        setError({
          message: err.message,
          code: err.errorCode,
          details: err.details,
        });
      } else {
        setError({
          message: err.message || "Failed to analyze variant via v2 service.",
          code: "UNKNOWN_ERROR",
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const presetChips = [
    { label: "c.118C>T (p.Gln40Ter)", query: "c.118C>T" },
    { label: "c.20A>T (p.Glu7Val / HbS)", query: "c.20A>T" },
    { label: "c.126_129del (Cd41/42)", query: "c.126_129del" },
    { label: "c.27dup (Cd8/9)", query: "c.27dup" },
    { label: "c.92+5G>C (IVS1-5)", query: "c.92+5G>C" },
    { label: "c.315+1G>A (IVS2-1)", query: "c.315+1G>A" },
  ];

  const clinvar = analysisResult?.clinvar_evidence;
  const clinvarProvenance = clinvar?.provenance;
  const records = clinvar?.records || [];
  const clinvarStatus = classifyEvidenceStatus(
    clinvar?.status || "not_found",
    records.length,
    clinvarProvenance?.is_fixture || false
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white border border-stone-200 rounded-xl max-w-4xl w-full shadow-2xl overflow-hidden my-8">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-stone-200 bg-stone-50 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] uppercase font-mono tracking-wider bg-stone-900 text-white px-2 py-0.5 rounded font-semibold">
                API V2 ARCHITECTURE
              </span>
              <span className="text-xs text-stone-500 font-mono">
                Deterministic Engine &bull; External Evidence Layer
              </span>
            </div>
            <h3 className="font-serif text-base font-semibold text-stone-900 flex items-center gap-2 mt-1">
              <Dna className="w-4 h-4 text-emerald-700" />
              Direct Variant Investigation &amp; Evidence Audit
            </h3>
            <p className="text-xs text-stone-500">
              Deterministic consequence calculation by the core domain engine with grounded external database evidence and provenance auditing.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-stone-400 hover:text-stone-700 rounded hover:bg-stone-200/50"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Input Bar */}
        <div className="p-6 space-y-4 border-b border-stone-100">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. c.118C>T, c.20A>T, c.126_129del, c.27dup, c.92+5G>C"
              className="flex-1 font-mono text-xs text-stone-900 bg-stone-50 border border-stone-300 rounded px-3 py-2 focus:ring-2 focus:ring-stone-400 focus:outline-none"
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <button
              onClick={() => handleSearch()}
              disabled={loading || !query.trim()}
              className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-stone-900 hover:bg-stone-800 rounded disabled:bg-stone-300 transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Analyzing v2...
                </>
              ) : (
                <>
                  <Search className="w-3.5 h-3.5" />
                  Analyze Variant
                </>
              )}
            </button>
          </div>

          {/* Quick presets */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-[11px] text-stone-500 uppercase font-mono mr-1">Presets:</span>
            {presetChips.map((chip) => (
              <button
                key={chip.query}
                onClick={() => {
                  setQuery(chip.query);
                  handleSearch(chip.query);
                }}
                className="px-2 py-0.5 bg-stone-100 hover:bg-stone-200 border border-stone-200 rounded font-mono text-[11px] text-stone-700 transition-colors"
              >
                {chip.label}
              </button>
            ))}
          </div>

          {/* Structured Domain Error Alert */}
          {error && (
            <div className="p-3.5 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 space-y-1">
              <div className="flex items-center gap-2 font-semibold">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>
                  {error.code ? `Error [${error.code}]: ` : "Analysis Error: "}
                  {error.message}
                </span>
              </div>
              {error.details && Object.keys(error.details).length > 0 && (
                <div className="mt-1 pl-6 text-[11px] font-mono text-rose-700 bg-rose-100/50 p-2 rounded">
                  {Object.entries(error.details).map(([k, val]) => (
                    <div key={k}>
                      <strong>{k}:</strong> {String(val)}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Results Container */}
        <div className="p-6 max-h-[62vh] overflow-y-auto space-y-6">
          {!analysisResult && !loading && !error && (
            <div className="text-center py-12 text-stone-400 text-xs">
              Enter an HGVS cDNA variant query (e.g. <code className="font-mono bg-stone-100 px-1 py-0.5 rounded">c.118C&gt;T</code>) and click &ldquo;Analyze Variant&rdquo;.
            </div>
          )}

          {analysisResult && (
            <div className="space-y-6">
              {/* 1. Deterministic Core Interpretation Card */}
              <div className="bg-white border-2 border-stone-800 rounded-lg p-4 space-y-3 shadow-xs">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono uppercase bg-emerald-100 text-emerald-900 border border-emerald-300 px-2 py-0.5 rounded font-bold">
                      DETERMINISTIC FACT
                    </span>
                    <h4 className="font-serif text-sm font-bold text-stone-900">
                      Core Sequence Engine Interpretation
                    </h4>
                  </div>
                  <span className="text-[11px] font-mono text-stone-500">
                    Authority: Sole Source of Truth
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                  <div>
                    <span className="text-[10px] uppercase text-stone-400 block">HGVS cDNA</span>
                    <strong className="text-stone-900 text-sm">{analysisResult.normalized_hgvs_c}</strong>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase text-stone-400 block">Protein Change</span>
                    <strong className="text-stone-900 text-sm">
                      {analysisResult.hgvs_p || "None"}
                    </strong>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase text-stone-400 block">Molecular Impact</span>
                    <span className="inline-block px-1.5 py-0.5 rounded text-[11px] font-semibold bg-rose-50 text-rose-800 border border-rose-200">
                      {analysisResult.molecular_impact}
                    </span>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase text-stone-400 block">Region / Type</span>
                    <span className="text-stone-800">
                      {analysisResult.region} ({analysisResult.variant_type})
                    </span>
                  </div>
                </div>

                {/* Codon Alteration Strip */}
                {analysisResult.codon_change && (
                  <div className="p-2.5 bg-stone-50 border border-stone-200 rounded text-xs font-mono flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <span className="text-stone-500">Codon {analysisResult.codon_change.codon_number}: </span>
                      <strong className="text-stone-900">
                        {analysisResult.codon_change.ref_codon} ({analysisResult.codon_change.ref_aa}) &rarr; {analysisResult.codon_change.sample_codon} ({analysisResult.codon_change.sample_aa})
                      </strong>
                    </div>
                    <div className="flex gap-2">
                      {analysisResult.codon_change.is_stop_gain && (
                        <span className="bg-rose-100 text-rose-900 px-1.5 py-0.5 rounded text-[10px] font-bold">
                          Stop Gain (PTC)
                        </span>
                      )}
                      {analysisResult.codon_change.is_synonymous && (
                        <span className="bg-emerald-100 text-emerald-900 px-1.5 py-0.5 rounded text-[10px] font-bold">
                          Synonymous
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Genomic & Nomenclature Meta */}
                <div className="text-[11px] font-mono text-stone-500 flex flex-wrap items-center gap-x-4 gap-y-1">
                  <span>Reference: <strong>{analysisResult.transcript_accession}</strong></span>
                  {analysisResult.genomic_accession && (
                    <span>
                      Genomic: <strong>{analysisResult.genomic_accession}:g.{analysisResult.genomic_coordinate}</strong>
                    </span>
                  )}
                  {analysisResult.equivalent_nomenclature.length > 0 && (
                    <span>Alias: {analysisResult.equivalent_nomenclature.join(", ")}</span>
                  )}
                </div>
              </div>

              {/* 2. Discrepancy Alert Box (Explicitly Displayed, Never Overriding Core) */}
              {analysisResult.discrepancies && analysisResult.discrepancies.length > 0 && (
                <div className="p-4 bg-amber-50 border-2 border-amber-400 rounded-lg text-xs space-y-2">
                  <div className="flex items-center gap-2 text-amber-900 font-bold">
                    <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>Scientific Discrepancy Detected between Deterministic Engine and ClinVar</span>
                  </div>
                  <p className="text-stone-700 leading-relaxed font-sans">
                    The external database annotation differs from the deterministic codon calculation.
                    <strong> The deterministic engine consequence calculation remains authoritative.</strong>
                  </p>
                  <div className="space-y-1.5 pt-1">
                    {analysisResult.discrepancies.map((d, i) => (
                      <div key={i} className="p-2.5 bg-white border border-amber-200 rounded font-mono text-[11px] space-y-1">
                        <div className="flex justify-between">
                          <span className="text-stone-500">Field: <strong>{d.field_name}</strong></span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-[10px]">
                          <div className="bg-emerald-50 text-emerald-900 p-1.5 rounded border border-emerald-200">
                            <strong>Deterministic Value:</strong> {d.deterministic_value}
                          </div>
                          <div className="bg-amber-50 text-amber-900 p-1.5 rounded border border-amber-200">
                            <strong>ClinVar Value:</strong> {d.evidence_value}
                          </div>
                        </div>
                        <div className="text-stone-600 font-sans text-[11px] pt-1">
                          {d.description}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 3. External ClinVar Evidence Layer with Provenance */}
              <div className="space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 pb-2">
                  <h4 className="font-serif text-sm font-semibold text-stone-900 flex items-center gap-1.5">
                    <Database className="w-4 h-4 text-blue-600" />
                    NCBI ClinVar Evidence ({records.length})
                  </h4>

                  {/* Provenance Badge */}
                  {clinvarProvenance && (
                    <div className="flex items-center gap-2 text-[10px] font-mono">
                      <span className="bg-stone-100 text-stone-700 border border-stone-200 px-2 py-0.5 rounded">
                        Provider: <strong>{clinvarProvenance.provider}</strong> ({clinvarProvenance.mode})
                      </span>
                      {clinvarProvenance.is_fixture ? (
                        <span className="bg-amber-100 text-amber-900 border border-amber-200 px-2 py-0.5 rounded font-semibold">
                          Offline Fixture
                        </span>
                      ) : (
                        <span className="bg-emerald-100 text-emerald-900 border border-emerald-200 px-2 py-0.5 rounded font-semibold">
                          Live NCBI
                        </span>
                      )}
                    </div>
                  )}
                </div>

                {/* Tri-state Availability Banners */}
                {clinvarStatus === "not_found" && (
                  <div className="p-3 bg-stone-50 border border-stone-200 rounded text-xs text-stone-600 flex items-center gap-2">
                    <Info className="w-4 h-4 text-stone-400 shrink-0" />
                    <span>No evidence found in ClinVar for variant <strong className="font-mono">{analysisResult.normalized_hgvs_c}</strong>.</span>
                  </div>
                )}

                {clinvarStatus === "fixture_unavailable" && (
                  <div className="p-3 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800 flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>Offline fixture unavailable for variant <strong className="font-mono">{analysisResult.normalized_hgvs_c}</strong>. Switch to live mode or update fixtures.</span>
                  </div>
                )}

                {clinvarStatus === "unretrievable" && (
                  <div className="p-3 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                    <span>Evidence could not be retrieved from ClinVar: {clinvar?.error_message || "Upstream query failure"}.</span>
                  </div>
                )}

                {/* Records Listing */}
                {records.map((c) => (
                  <div
                    key={c.variation_id}
                    className="border border-stone-200 rounded-lg p-3.5 text-xs space-y-2 bg-stone-50/40"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <a
                          href={c.url}
                          target="_blank"
                          rel="noreferrer"
                          className="font-bold text-stone-900 hover:text-blue-700 flex items-center gap-1 leading-snug"
                        >
                          {c.title}
                          <ExternalLink className="w-3 h-3 text-stone-400 shrink-0" />
                        </a>
                        <div className="text-[11px] text-stone-500 font-mono mt-0.5">
                          Accession: {c.accession} | Variation ID: {c.variation_id} | Review: {c.review_status}
                        </div>
                      </div>
                      <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold text-[10px] shrink-0">
                        {c.clinical_significance}
                      </span>
                    </div>

                    {c.conditions.length > 0 && (
                      <div className="text-[11px] text-stone-600">
                        <strong>Reported Phenotypes:</strong> {c.conditions.join(", ")}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* 4. PubMed Literature Layer */}
              <div className="space-y-3">
                <div className="flex items-center justify-between border-b border-stone-200 pb-2">
                  <h4 className="font-serif text-sm font-semibold text-stone-900 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-emerald-600" />
                    PubMed Literature ({pubmedArticles.length})
                  </h4>
                  {pubmedLoading && (
                    <span className="text-[11px] font-mono text-stone-500 flex items-center gap-1">
                      <Loader2 className="w-3 h-3 animate-spin" /> Querying NCBI...
                    </span>
                  )}
                </div>

                {!pubmedLoading && pubmedArticles.length === 0 && (
                  <div className="p-3 bg-stone-50 border border-stone-200 rounded text-xs text-stone-500 italic">
                    No matching PubMed literature retrieved for this query.
                  </div>
                )}

                {pubmedArticles.map((p) => (
                  <div
                    key={p.pmid}
                    className="border border-stone-200 rounded p-3 text-xs space-y-1.5 bg-stone-50/40"
                  >
                    <a
                      href={p.url}
                      target="_blank"
                      rel="noreferrer"
                      className="font-bold text-stone-900 hover:text-emerald-700 flex items-center gap-1"
                    >
                      {p.title}
                      <ExternalLink className="w-3 h-3 text-stone-400 shrink-0" />
                    </a>
                    <div className="text-[11px] text-stone-500 font-mono flex flex-wrap gap-x-3">
                      <span>PMID: <strong>{p.pmid}</strong></span>
                      {p.journal && <span>Journal: {p.journal}</span>}
                      {p.pub_date && <span>Date: {p.pub_date}</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
