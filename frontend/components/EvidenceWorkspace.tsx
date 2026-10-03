"use client";

import React from "react";
import { ClinVarRecord, PubMedRecord } from "../lib/types";
import { ExternalLink, Database, BookOpen, AlertCircle, Calendar, Tag, ShieldAlert } from "lucide-react";

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
  return (
    <div className="space-y-6">
      <div className="border-b border-stone-200 pb-2 flex items-center justify-between">
        <div>
          <h3 className="font-serif text-base font-semibold text-stone-900">
            External Scientific Evidence Layer
          </h3>
          <p className="text-xs text-stone-500">
            Retrieved from official NCBI E-utilities APIs without modification or generative fabrication.
          </p>
        </div>
        <span className="text-[11px] font-mono bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded font-semibold">
          DATABASE EVIDENCE
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ClinVar Section */}
        <div className="bg-white border border-stone-200 rounded-lg p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-stone-100 pb-3">
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4 text-blue-600" />
              <h4 className="font-serif text-sm font-semibold text-stone-900">
                NCBI ClinVar Annotations
              </h4>
            </div>
            <span className="text-xs font-mono text-stone-500">
              {clinvarRecords.length} {clinvarRecords.length === 1 ? "Record" : "Records"}
            </span>
          </div>

          {clinvarRecords.length === 0 ? (
            <div className="p-6 bg-stone-50 border border-stone-200 rounded text-center text-xs text-stone-500 italic">
              No matching ClinVar records retrieved for detected variant(s).
            </div>
          ) : (
            <div className="space-y-3">
              {clinvarRecords.map((c) => {
                const sigLower = c.clinical_significance.toLowerCase();
                const isPathogenic = sigLower.includes("pathogenic");
                const isBenign = sigLower.includes("benign");

                return (
                  <div
                    key={c.id}
                    className="border border-stone-200 rounded-lg p-4 bg-stone-50/50 hover:bg-stone-50 transition-colors space-y-2.5"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <a
                          href={c.url}
                          target="_blank"
                          rel="noreferrer"
                          className="font-sans text-xs font-bold text-stone-900 hover:text-blue-700 flex items-center gap-1 leading-snug"
                        >
                          {c.title}
                          <ExternalLink className="w-3 h-3 shrink-0 text-stone-400" />
                        </a>
                        <span className="text-[11px] font-mono text-stone-500">
                          Accession: {c.accession || `VCV${c.id}`} | Variation ID: {c.id}
                        </span>
                      </div>

                      <span
                        className={`text-[11px] font-bold px-2 py-0.5 rounded border shrink-0 ${
                          isPathogenic
                            ? "bg-rose-50 text-rose-800 border-rose-200"
                            : isBenign
                            ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                            : "bg-amber-50 text-amber-800 border-amber-200"
                        }`}
                      >
                        {c.clinical_significance}
                      </span>
                    </div>

                    <div className="text-xs text-stone-600 space-y-1">
                      <div className="flex items-center gap-1.5 text-[11px] text-stone-500">
                        <Tag className="w-3 h-3 text-stone-400" />
                        <span>Review: <strong>{c.review_status}</strong></span>
                      </div>
                      {c.last_evaluated && (
                        <div className="flex items-center gap-1.5 text-[11px] text-stone-500">
                          <Calendar className="w-3 h-3 text-stone-400" />
                          <span>Last evaluated: {c.last_evaluated}</span>
                        </div>
                      )}
                    </div>

                    {c.conditions.length > 0 && (
                      <div className="pt-2 border-t border-stone-200/60">
                        <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block mb-1">
                          Reported Phenotypes & Conditions:
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {c.conditions.map((cond, i) => (
                            <span
                              key={i}
                              className="text-[10px] bg-white border border-stone-200 px-1.5 py-0.5 rounded text-stone-700 font-sans"
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

        {/* PubMed Section */}
        <div className="bg-white border border-stone-200 rounded-lg p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-stone-100 pb-3">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-4 h-4 text-emerald-600" />
              <h4 className="font-serif text-sm font-semibold text-stone-900">
                NCBI PubMed Literature
              </h4>
            </div>
            <span className="text-xs font-mono text-stone-500">
              {pubmedRecords.length} {pubmedRecords.length === 1 ? "Paper" : "Papers"}
            </span>
          </div>

          {pubmedRecords.length === 0 ? (
            <div className="p-6 bg-stone-50 border border-stone-200 rounded text-center text-xs text-stone-500 italic">
              No matching PubMed evidence was retrieved.
            </div>
          ) : (
            <div className="space-y-3">
              {pubmedRecords.map((p) => (
                <div
                  key={p.pmid}
                  className="border border-stone-200 rounded-lg p-4 bg-stone-50/50 hover:bg-stone-50 transition-colors space-y-2"
                >
                  <a
                    href={p.url}
                    target="_blank"
                    rel="noreferrer"
                    className="font-sans text-xs font-bold text-stone-900 hover:text-emerald-800 flex items-start gap-1 leading-snug"
                  >
                    <span>{p.title}</span>
                    <ExternalLink className="w-3 h-3 shrink-0 text-stone-400 mt-0.5" />
                  </a>

                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-stone-500 font-mono">
                    <span>
                      PMID: <strong className="text-stone-800">{p.pmid}</strong>
                    </span>
                    {p.journal && <span>Journal: {p.journal}</span>}
                    {p.pub_date && <span>Date: {p.pub_date}</span>}
                  </div>

                  {p.authors.length > 0 && (
                    <p className="text-[11px] text-stone-600 font-sans italic truncate">
                      Authors: {p.authors.join(", ")}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Scientific Constraints & Limitations */}
      <div className="bg-stone-50 border border-stone-200 rounded-lg p-4 space-y-2">
        <div className="flex items-center space-x-2 text-stone-700">
          <ShieldAlert className="w-4 h-4 text-stone-500" />
          <h5 className="font-serif text-xs font-semibold uppercase tracking-wider text-stone-700">
            Evidence Limitations & Scientific Boundary Disclaimers
          </h5>
        </div>
        <ul className="text-xs text-stone-600 list-disc list-inside space-y-1 pl-1">
          {limitations.map((lim, i) => (
            <li key={i}>{lim}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
