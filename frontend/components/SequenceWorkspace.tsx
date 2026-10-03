"use client";

import React, { useState, useMemo } from "react";
import { Play, Sparkles, CheckCircle, RotateCcw, AlertCircle, Copy, Check } from "lucide-react";
import { ExampleSequence } from "../lib/types";

interface SequenceWorkspaceProps {
  sequence: string;
  onChangeSequence: (seq: string) => void;
  onAnalyze: () => void;
  isLoading: boolean;
  examples: ExampleSequence[];
  error?: string | null;
}

export const SequenceWorkspace: React.FC<SequenceWorkspaceProps> = ({
  sequence,
  onChangeSequence,
  onAnalyze,
  isLoading,
  examples,
  error,
}) => {
  const [copied, setCopied] = useState(false);

  // Live stats calculation
  const stats = useMemo(() => {
    const raw = sequence || "";
    const lines = raw.split("\n");
    let clean = "";
    let header: string | null = null;

    for (const line of lines) {
      const stripped = line.trim();
      if (stripped.startsWith(">")) {
        if (!header) header = stripped.substring(1);
        continue;
      }
      clean += stripped.replace(/[\s\d_]/g, "").toUpperCase();
    }

    const total = clean.length;
    const gc = total > 0 ? ((clean.replace(/[^GC]/g, "").length / total) * 100).toFixed(1) : "0.0";
    const nonDnaChars = Array.from(new Set(clean.replace(/[ACGT]/g, "")));

    return {
      length: total,
      gcContent: gc,
      header,
      hasInvalidChars: nonDnaChars.length > 0,
      invalidChars: nonDnaChars,
    };
  }, [sequence]);

  const handleCopy = () => {
    navigator.clipboard.writeText(sequence);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleLoadExample = (example: ExampleSequence) => {
    onChangeSequence(example.sequence);
  };

  return (
    <div className="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
      {/* Workspace Header */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold font-sans text-stone-900 flex items-center gap-2">
            Sequence Input & Validation Workspace
          </h2>
          <p className="text-xs text-stone-500">
            Accepts raw cDNA/DNA or FASTA formatted text. Analyzed strictly against NM_000518.5 (628 bp).
          </p>
        </div>

        {/* Example Pickers */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] font-medium text-stone-500 uppercase tracking-wider mr-1">
            Benchmarks:
          </span>
          {examples.map((ex) => (
            <button
              key={ex.filename}
              onClick={() => handleLoadExample(ex)}
              className={`text-xs px-2.5 py-1 rounded font-mono transition-all border ${
                ex.is_validation_case
                  ? "bg-amber-100/90 text-amber-900 border-amber-300 hover:bg-amber-200 font-semibold shadow-xs"
                  : "bg-white text-stone-700 border-stone-200 hover:bg-stone-100 hover:border-stone-300"
              }`}
              title={ex.description}
            >
              {ex.is_validation_case ? "★ " : ""}
              {ex.title.split("(")[0].trim()}
            </button>
          ))}
        </div>
      </div>

      {/* Editor & Stats Container */}
      <div className="p-5 space-y-4">
        <div className="relative">
          <textarea
            value={sequence}
            onChange={(e) => onChangeSequence(e.target.value)}
            placeholder="Paste your HBB DNA sequence or FASTA text here (e.g., >NM_000518.5...&#10;ACATTTGCTTCTGACACAAC...)"
            rows={8}
            className="w-full font-mono text-xs text-stone-800 bg-stone-50/40 p-4 border border-stone-300 rounded focus:ring-2 focus:ring-stone-400 focus:outline-none transition-all resize-y custom-scrollbar leading-relaxed tracking-wider"
            spellCheck={false}
          />

          <div className="absolute top-2 right-2 flex items-center space-x-1">
            {sequence && (
              <>
                <button
                  onClick={handleCopy}
                  className="p-1.5 text-stone-400 hover:text-stone-700 bg-white border border-stone-200 rounded shadow-2xs text-xs"
                  title="Copy sequence"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
                <button
                  onClick={() => onChangeSequence("")}
                  className="p-1.5 text-stone-400 hover:text-stone-700 bg-white border border-stone-200 rounded shadow-2xs text-xs"
                  title="Clear input"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </>
            )}
          </div>
        </div>

        {/* Live Sequence Statistics Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs bg-stone-50 border border-stone-200 rounded px-4 py-2.5">
          <div className="flex flex-wrap items-center gap-4 text-stone-600">
            <div>
              <span className="text-stone-400 font-mono">Length: </span>
              <strong className="text-stone-800 font-mono">{stats.length}</strong> bp
            </div>
            <div>
              <span className="text-stone-400 font-mono">GC Content: </span>
              <strong className="text-stone-800 font-mono">{stats.gcContent}%</strong>
            </div>
            {stats.header && (
              <div className="max-w-md truncate" title={stats.header}>
                <span className="text-stone-400 font-mono">Header: </span>
                <span className="text-stone-700 font-mono italic">{stats.header}</span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            {stats.hasInvalidChars && (
              <span className="flex items-center text-rose-600 font-medium text-xs gap-1">
                <AlertCircle className="w-3.5 h-3.5" />
                Invalid: {stats.invalidChars.join(", ")}
              </span>
            )}
            {!stats.hasInvalidChars && stats.length > 0 && (
              <span className="flex items-center text-emerald-700 font-medium text-xs gap-1">
                <CheckCircle className="w-3.5 h-3.5" />
                Canonical DNA
              </span>
            )}

            <div className="flex items-center gap-2.5">
              <span className="text-[10px] uppercase font-mono text-stone-500 hidden sm:inline select-none" title="Deterministic pairwise alignment & codon translation">
                Deterministic Engine
              </span>
              <button
                onClick={onAnalyze}
                disabled={isLoading || stats.length === 0 || stats.hasInvalidChars}
                className={`inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold rounded shadow-sm transition-all ${
                  isLoading || stats.length === 0 || stats.hasInvalidChars
                    ? "bg-stone-200 text-stone-400 cursor-not-allowed"
                    : "bg-stone-900 hover:bg-stone-800 text-white active:scale-[0.98]"
                }`}
              >
                {isLoading ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    Aligning & Computing...
                  </>
                ) : (
                  <>
                    <Play className="w-3.5 h-3.5 fill-current" />
                    Analyze Sequence
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Analysis Validation Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
