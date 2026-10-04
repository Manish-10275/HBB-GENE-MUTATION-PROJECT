"use client";

import React, { useState, useMemo } from "react";
import { Play, RotateCcw, AlertCircle, Copy, Check, CheckCircle, Dna, Sparkles } from "lucide-react";
import { ExampleSequence, SimulatorPreset } from "../lib/types";

interface SequenceWorkspaceProps {
  sequence: string;
  onChangeSequence: (seq: string) => void;
  onAnalyze: () => void;
  isLoading: boolean;
  examples: ExampleSequence[];
  simulatorPresets?: SimulatorPreset[];
  onSelectSimulatorPreset?: (presetId: string) => void;
  referenceAccession?: string;
  onChangeReferenceAccession?: (ref: string) => void;
  zygosity?: string;
  onChangeZygosity?: (zyg: string) => void;
  error?: string | null;
}

export const SequenceWorkspace: React.FC<SequenceWorkspaceProps> = ({
  sequence,
  onChangeSequence,
  onAnalyze,
  isLoading,
  examples,
  simulatorPresets = [],
  onSelectSimulatorPreset,
  referenceAccession = "NM_000518.5",
  onChangeReferenceAccession,
  zygosity = "heterozygous",
  onChangeZygosity,
  error,
}) => {
  const [copied, setCopied] = useState(false);
  const [presetDropdownOpen, setPresetDropdownOpen] = useState(false);

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
    if (onChangeReferenceAccession) {
      onChangeReferenceAccession("NM_000518.5");
    }
  };

  const handleSelectPreset = (presetId: string) => {
    if (onSelectSimulatorPreset) {
      onSelectSimulatorPreset(presetId);
    }
    setPresetDropdownOpen(false);
  };

  return (
    <div className="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
      {/* Workspace Header */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold font-sans text-stone-900 flex items-center gap-2">
            <span>Sequence Input &amp; Screening Simulator</span>
          </h2>
          <p className="text-xs text-stone-500">
            Accepts raw DNA or FASTA. Supports transcript (NM_000518.5, 628 bp) and genomic locus (NG_000007.3, 1,608 bp).
          </p>
        </div>

        {/* Quick Pickers & Indian Panel Controls */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Reference Mode Selector */}
          {onChangeReferenceAccession && (
            <div className="flex items-center text-xs font-mono bg-white border border-stone-200 rounded px-2 py-1 shadow-2xs">
              <span className="text-stone-400 mr-1.5 text-[10px] uppercase">Ref:</span>
              <select
                value={referenceAccession}
                onChange={(e) => onChangeReferenceAccession(e.target.value)}
                className="bg-transparent text-stone-800 font-semibold focus:outline-none cursor-pointer"
              >
                <option value="NM_000518.5">NM_000518.5 (cDNA, 628 bp)</option>
                <option value="NG_000007.3">NG_000007.3 (Genomic, 1608 bp)</option>
              </select>
            </div>
          )}

          {/* Screening Zygosity Selector */}
          {onChangeZygosity && (
            <div className="flex items-center text-xs font-mono bg-white border border-stone-200 rounded px-2 py-1 shadow-2xs">
              <span className="text-stone-400 mr-1.5 text-[10px] uppercase">Zygosity:</span>
              <select
                value={zygosity}
                onChange={(e) => onChangeZygosity(e.target.value)}
                className="bg-transparent text-stone-800 font-semibold focus:outline-none cursor-pointer"
              >
                <option value="heterozygous">Heterozygous (Carrier)</option>
                <option value="homozygous">Homozygous (Affected)</option>
              </select>
            </div>
          )}

          {/* Indian Panel & Simulator Presets Dropdown */}
          {simulatorPresets.length > 0 && (
            <div className="relative">
              <button
                type="button"
                onClick={() => setPresetDropdownOpen(!presetDropdownOpen)}
                className="text-xs px-2.5 py-1 rounded font-mono font-semibold transition-all border bg-indigo-50 text-indigo-900 border-indigo-200 hover:bg-indigo-100 flex items-center gap-1.5 shadow-2xs"
              >
                <Dna className="w-3.5 h-3.5 text-indigo-700" />
                <span>Simulate Mutation Preset</span>
                <span className="text-[10px]">▾</span>
              </button>

              {presetDropdownOpen && (
                <div className="absolute right-0 mt-1 w-72 bg-white border border-stone-200 rounded-md shadow-lg z-30 py-1 text-xs">
                  <div className="px-3 py-1 text-[10px] font-mono text-stone-400 uppercase tracking-wider font-semibold border-b border-stone-100">
                    Indian Thalassemia &amp; Controls
                  </div>
                  {simulatorPresets.map((p) => (
                    <button
                      key={p.id}
                      type="button"
                      onClick={() => handleSelectPreset(p.id)}
                      className="w-full text-left px-3 py-1.5 hover:bg-stone-50 flex flex-col transition-colors border-b border-stone-50"
                    >
                      <span className="font-semibold text-stone-900 font-mono">{p.name}</span>
                      <span className="text-[10px] text-stone-500 font-sans">{p.subtitle}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Validation Case Benchmark Button */}
          {examples.length > 0 && (
            <button
              onClick={() => {
                const valCase = examples.find((e) => e.is_validation_case) || examples[0];
                handleLoadExample(valCase);
              }}
              className="text-xs px-2.5 py-1 rounded font-mono font-semibold transition-all border bg-amber-100 text-amber-900 border-amber-300 hover:bg-amber-200 shadow-2xs"
              title="Controlled validation benchmark: c.118C>T (p.Gln40Ter)"
            >
              ★ Benchmark c.118C&gt;T
            </button>
          )}
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
            <div>
              <span className="text-stone-400 font-mono">Target: </span>
              <strong className="text-stone-800 font-mono">{referenceAccession}</strong>
            </div>
            {stats.header && (
              <div className="max-w-xs truncate" title={stats.header}>
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
              <span
                className="text-[10px] uppercase font-mono text-stone-500 hidden sm:inline select-none"
                title="Deterministic pairwise alignment & codon translation"
              >
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
                    Aligning &amp; Computing...
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
