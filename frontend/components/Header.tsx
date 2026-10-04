"use client";

import React from "react";
import { Dna, ShieldCheck, Database, FileText } from "lucide-react";

interface HeaderProps {
  onOpenReport?: () => void;
  hasAnalysis: boolean;
  onOpenDirectSearch?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenReport,
  hasAnalysis,
  onOpenDirectSearch,
}) => {
  return (
    <header className="border-b border-stone-200 bg-white/95 backdrop-blur-sm sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Identity */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-md bg-stone-900 text-white flex items-center justify-center shadow-sm">
              <Dna className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-serif text-lg font-semibold tracking-tight text-stone-900">
                  HBB Mutation Analyzer
                </span>
                <span className="text-[10px] uppercase font-mono tracking-wider bg-stone-100 text-stone-600 px-1.5 py-0.5 rounded border border-stone-200">
                  RefSeq NM_000518.5
                </span>
              </div>
              <p className="text-xs text-stone-500 font-sans">
                Understand the sequence. Follow the evidence.
              </p>
            </div>
          </div>

          {/* Quick Actions & Standards */}
          <div className="flex items-center space-x-3">
            <div className="hidden lg:flex items-center space-x-2 border-r border-stone-200 pr-4">
              <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-stone-100 text-stone-600 text-[10px] font-mono border border-stone-200 select-none" title="Deterministic pairwise alignment & codon translation">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                <span>Deterministic Engine</span>
              </div>
              <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-stone-100 text-stone-600 text-[10px] font-mono border border-stone-200 select-none" title="NCBI ClinVar & PubMed E-utilities integration">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                <span>NCBI E-Utilities</span>
              </div>
            </div>

            {onOpenDirectSearch && (
              <button
                onClick={onOpenDirectSearch}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-stone-700 bg-stone-100 hover:bg-stone-200 border border-stone-300 rounded transition-colors"
                title="Search variant directly by HGVS notation"
              >
                <Database className="w-3.5 h-3.5 text-stone-500" />
                Direct HGVS Search
              </button>
            )}

            {hasAnalysis && onOpenReport && (
              <button
                onClick={onOpenReport}
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold text-white bg-stone-900 hover:bg-stone-800 rounded shadow-sm transition-colors"
              >
                <FileText className="w-3.5 h-3.5 text-emerald-400" />
                Export Research Report
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
