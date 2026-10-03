"use client";

import React, { useState } from "react";
import { Search, Loader2, Database, BookOpen, AlertCircle, X, ExternalLink } from "lucide-react";
import { searchVariantDirect } from "../lib/api";
import { VariantSearchResponse } from "../lib/types";

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
  const [result, setResult] = useState<VariantSearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSearch = async (termToSearch?: string) => {
    const q = (termToSearch || query).trim();
    if (!q) return;

    setLoading(true);
    setError(null);
    try {
      const data = await searchVariantDirect(q);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to query external evidence databases.");
    } finally {
      setLoading(false);
    }
  };

  const presetChips = [
    { label: "c.118C>T (p.Gln40Ter)", query: "c.118C>T" },
    { label: "c.20A>T (p.Glu7Val / HbS)", query: "c.20A>T" },
    { label: "c.19G>A (p.Glu7Lys / HbC)", query: "c.19G>A" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white border border-stone-200 rounded-xl max-w-3xl w-full shadow-2xl overflow-hidden my-8">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-stone-200 bg-stone-50 flex items-center justify-between">
          <div>
            <h3 className="font-serif text-base font-semibold text-stone-900 flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-600" />
              Direct Variant Investigation
            </h3>
            <p className="text-xs text-stone-500">
              Query external scientific evidence databases directly using HGVS nomenclature without uploading full DNA sequence.
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
              placeholder="e.g. NM_000518.5:c.118C>T or c.118C>T"
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
                  Querying NCBI...
                </>
              ) : (
                <>
                  <Search className="w-3.5 h-3.5" />
                  Search Evidence
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

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Results Container */}
        <div className="p-6 max-h-[60vh] overflow-y-auto space-y-6">
          {!result && !loading && !error && (
            <div className="text-center py-10 text-stone-400 text-xs">
              Enter an HGVS cDNA variant query and click &ldquo;Search Evidence&rdquo; to retrieve ClinVar and PubMed records.
            </div>
          )}

          {result && (
            <div className="space-y-6">
              {/* Header meta */}
              <div className="p-3 bg-stone-50 border border-stone-200 rounded flex flex-wrap items-center justify-between text-xs font-mono">
                <div>
                  <span className="text-stone-400">Query: </span>
                  <strong className="text-stone-900">{result.query}</strong>
                </div>
                {result.standardized_hgvs_c && (
                  <div>
                    <span className="text-stone-400">Standardized: </span>
                    <strong className="text-stone-900">{result.standardized_hgvs_c}</strong>
                  </div>
                )}
                <div>
                  <span className="text-stone-400">Source: </span>
                  <span className="text-stone-700">{result.source}</span>
                </div>
              </div>

              {/* ClinVar Cards */}
              <div className="space-y-3">
                <h4 className="font-serif text-sm font-semibold text-stone-900 flex items-center gap-1.5 border-b border-stone-200 pb-2">
                  <Database className="w-4 h-4 text-blue-600" />
                  ClinVar Records ({result.clinvar_records.length})
                </h4>
                {result.clinvar_records.length === 0 ? (
                  <p className="text-xs text-stone-500 italic p-3 bg-stone-50 rounded">
                    No matching ClinVar records retrieved.
                  </p>
                ) : (
                  result.clinvar_records.map((c) => (
                    <div key={c.id} className="border border-stone-200 rounded p-3 text-xs space-y-2 bg-stone-50/40">
                      <div className="flex items-start justify-between">
                        <a
                          href={c.url}
                          target="_blank"
                          rel="noreferrer"
                          className="font-bold text-stone-900 hover:text-blue-700 flex items-center gap-1"
                        >
                          {c.title}
                          <ExternalLink className="w-3 h-3 text-stone-400" />
                        </a>
                        <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold text-[10px]">
                          {c.clinical_significance}
                        </span>
                      </div>
                      <div className="text-[11px] text-stone-500 font-mono">
                        Accession: {c.accession || `VCV${c.id}`} | Review: {c.review_status}
                      </div>
                      {c.conditions.length > 0 && (
                        <div className="text-[11px] text-stone-600">
                          <strong>Conditions:</strong> {c.conditions.join(", ")}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>

              {/* PubMed Cards */}
              <div className="space-y-3">
                <h4 className="font-serif text-sm font-semibold text-stone-900 flex items-center gap-1.5 border-b border-stone-200 pb-2">
                  <BookOpen className="w-4 h-4 text-emerald-600" />
                  PubMed Literature ({result.pubmed_records.length})
                </h4>
                {result.pubmed_records.length === 0 ? (
                  <p className="text-xs text-stone-500 italic p-3 bg-stone-50 rounded">
                    No matching PubMed evidence was retrieved.
                  </p>
                ) : (
                  result.pubmed_records.map((p) => (
                    <div key={p.pmid} className="border border-stone-200 rounded p-3 text-xs space-y-1.5 bg-stone-50/40">
                      <a
                        href={p.url}
                        target="_blank"
                        rel="noreferrer"
                        className="font-bold text-stone-900 hover:text-emerald-700 flex items-center gap-1"
                      >
                        {p.title}
                        <ExternalLink className="w-3 h-3 text-stone-400 shrink-0" />
                      </a>
                      <div className="text-[11px] text-stone-500 font-mono">
                        PMID: {p.pmid} | Journal: {p.journal} ({p.pub_date})
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
