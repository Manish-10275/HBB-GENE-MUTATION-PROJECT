"use client";

import React, { useState } from "react";
import { ClinVarRecord, PubMedRecord } from "../lib/types";
import {
  ExternalLink,
  Database,
  BookOpen,
  Calendar,
  Tag,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface EvidenceWorkspaceProps {
  clinvarRecords: ClinVarRecord[];
  pubmedRecords: PubMedRecord[];
  limitations: string[];
}

export const EvidenceWorkspace: React.FC<EvidenceWorkspaceProps> = ({
  clinvarRecords,
  pubmedRecords,
  limitations,
}) => {
  const [clinvarExpanded, setClinvarExpanded] = useState(false);
  const [pubmedExpanded, setPubmedExpanded] = useState(false);

  // Useful summaries for collapsed state
  const primaryClinvarSig = clinvarRecords.length > 0
    ? clinvarRecords[0].clinical_significance
    : "No records";
  const clinvarConditions = Array.from(
    new Set(clinvarRecords.flatMap((c) => c.conditions))
  ).slice(0, 4);

  const pubmedJournals = Array.from(
    new Set(pubmedRecords.map((p) => p.journal).filter(Boolean))
  ).slice(0, 3);

  return (
    <div className="space-y-4">
      {/* Evidence Provenance Header */}
      <div className="border-b border-stone-200 pb-2.5 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase font-mono tracking-wider bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded font-semibold">
              DATABASE EVIDENCE
            </span>
            <span className="text-xs text-stone-500 font-mono">
              NCBI E-Utilities
            </span>
          </div>
          <h3 className="font-serif text-base font-semibold text-stone-900 mt-0.5">
            External Scientific Evidence Layer
          </h3>
          <p className="text-xs text-stone-500 font-sans">
            Direct retrieval from NCBI ClinVar and PubMed. Unaltered database assertions.
          </p>
        </div>
      </div>

      {/* 1. ClinVar Section (Collapsible with Summary) */}
      <div className="bg-white border border-stone-200 rounded-lg overflow-hidden">
        <div className="p-4 bg-stone-50/70 border-b border-stone-200 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-600 shrink-0" />
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-serif text-sm font-semibold text-stone-900">
                  NCBI ClinVar Annotations
                </h4>
                <span className="text-xs font-mono font-medium text-stone-500">
                  ({clinvarRecords.length} {clinvarRecords.length === 1 ? "record" : "records"})
                </span>
              </div>
              {/* Useful summary strip when collapsed or expanded */}
              {clinvarRecords.length > 0 && (
                <div className="flex flex-wrap items-center gap-2 mt-1 text-xs">
                  <span
                    className={`text-[11px] font-bold px-2 py-0.2 rounded border ${
                      primaryClinvarSig.toLowerCase().includes("pathogenic")
                        ? "bg-rose-50 text-rose-800 border-rose-200"
                        : "bg-amber-50 text-amber-800 border-amber-200"
                    }`}
                  >
                    {primaryClinvarSig}
                  </span>
                  {clinvarConditions.length > 0 && (
                    <span className="text-stone-600 text-[11px] font-sans">
                      Conditions: {clinvarConditions.join(", ")}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>

          <button
            onClick={() => setClinvarExpanded(!clinvarExpanded)}
            disabled={clinvarRecords.length === 0}
            className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded disabled:opacity-50"
          >
            {clinvarExpanded ? (
              <>
                <ChevronUp className="w-3.5 h-3.5" />
                <span>Collapse Records</span>
              </>
            ) : (
              <>
                <ChevronDown className="w-3.5 h-3.5" />
                <span>Expand Records ({clinvarRecords.length})</span>
              </>
            )}
          </button>
        </div>

        {clinvarExpanded && (
          <div className="p-4 space-y-3 bg-white">
            {clinvarRecords.map((c) => {
              const sigLower = c.clinical_significance.toLowerCase();
              const isPathogenic = sigLower.includes("pathogenic");

              return (
                <div
                  key={c.id}
                  className="border border-stone-200 rounded p-3.5 bg-stone-50/40 text-xs space-y-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <a
                        href={c.url}
                        target="_blank"
                        rel="noreferrer"
                        className="font-bold text-stone-900 hover:text-blue-700 inline-flex items-center gap-1"
                      >
                        <span>{c.title}</span>
                        <ExternalLink className="w-3 h-3 text-stone-400 shrink-0" />
                      </a>
                      <div className="text-[11px] font-mono text-stone-500 mt-0.5">
                        Accession: {c.accession || `VCV${c.id}`} | Variation ID: {c.id}
                      </div>
                    </div>

                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded border shrink-0 ${
                        isPathogenic
                          ? "bg-rose-50 text-rose-800 border-rose-200"
                          : "bg-amber-50 text-amber-800 border-amber-200"
                      }`}
                    >
                      {c.clinical_significance}
                    </span>
                  </div>

                  <div className="text-[11px] text-stone-600 flex flex-wrap items-center gap-x-4 gap-y-1">
                    <span className="flex items-center gap-1">
                      <Tag className="w-3 h-3 text-stone-400" />
                      Review: <strong>{c.review_status}</strong>
                    </span>
                    {c.last_evaluated && (
                      <span className="flex items-center gap-1 font-mono">
                        <Calendar className="w-3 h-3 text-stone-400" />
                        Last evaluated: {c.last_evaluated}
                      </span>
                    )}
                  </div>

                  {c.conditions.length > 0 && (
                    <div className="pt-2 border-t border-stone-200/60">
                      <span className="text-[10px] uppercase font-mono text-stone-400 block mb-1">
                        Reported Phenotypes:
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {c.conditions.map((cond, i) => (
                          <span
                            key={i}
                            className="text-[10px] bg-white border border-stone-200 px-1.5 py-0.5 rounded text-stone-700"
                          >
                            {cond}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* 2. PubMed Section (Collapsible with Summary) */}
      <div className="bg-white border border-stone-200 rounded-lg overflow-hidden">
        <div className="p-4 bg-stone-50/70 border-b border-stone-200 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-emerald-600 shrink-0" />
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-serif text-sm font-semibold text-stone-900">
                  NCBI PubMed Literature
                </h4>
                <span className="text-xs font-mono font-medium text-stone-500">
                  ({pubmedRecords.length} {pubmedRecords.length === 1 ? "publication" : "publications"})
                </span>
              </div>
              {/* Useful summary strip when collapsed or expanded */}
              {pubmedRecords.length > 0 && (
                <div className="flex flex-wrap items-center gap-2 mt-1 text-xs text-stone-600 font-sans">
                  <span>Primary peer-reviewed citations</span>
                  {pubmedJournals.length > 0 && (
                    <span className="text-stone-500 text-[11px] font-mono">
                      &bull; Journals: {pubmedJournals.join(", ")}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>

          <button
            onClick={() => setPubmedExpanded(!pubmedExpanded)}
            disabled={pubmedRecords.length === 0}
            className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded disabled:opacity-50"
          >
            {pubmedExpanded ? (
              <>
                <ChevronUp className="w-3.5 h-3.5" />
                <span>Collapse Publications</span>
              </>
            ) : (
              <>
                <ChevronDown className="w-3.5 h-3.5" />
                <span>Expand Publications ({pubmedRecords.length})</span>
              </>
            )}
          </button>
        </div>

        {pubmedExpanded && (
          <div className="p-4 space-y-3 bg-white">
            {pubmedRecords.map((p) => (
              <div
                key={p.pmid}
                className="border border-stone-200 rounded p-3.5 bg-stone-50/40 text-xs space-y-1.5"
              >
                <a
                  href={p.url}
                  target="_blank"
                  rel="noreferrer"
                  className="font-bold text-stone-900 hover:text-emerald-800 inline-flex items-start gap-1 leading-snug"
                >
                  <span>{p.title}</span>
                  <ExternalLink className="w-3 h-3 text-stone-400 shrink-0 mt-0.5" />
                </a>

                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-stone-500 font-mono">
                  <span>PMID: <strong className="text-stone-800">{p.pmid}</strong></span>
                  {p.journal && <span>Journal: {p.journal}</span>}
                  {p.pub_date && <span>Date: {p.pub_date}</span>}
                </div>

                {p.authors.length > 0 && (
                  <p className="text-[11px] text-stone-600 italic truncate">
                    Authors: {p.authors.join(", ")}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 3. Scientific Limitations & Boundaries */}
      <div className="bg-stone-50 border border-stone-200 rounded-lg p-4 space-y-2">
        <div className="flex items-center space-x-2 text-stone-700">
          <ShieldAlert className="w-4 h-4 text-stone-500" />
          <h5 className="font-serif text-xs font-semibold uppercase tracking-wider text-stone-700">
            Evidence Limitations &amp; Boundary Constraints
          </h5>
        </div>
        <ul className="text-xs text-stone-600 list-disc list-inside space-y-1 pl-1 font-sans">
          {limitations.map((lim, i) => (
            <li key={i}>{lim}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
