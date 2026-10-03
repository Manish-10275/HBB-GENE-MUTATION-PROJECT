"use client";

import React from "react";
import { ArrowDown, Info } from "lucide-react";
import { DetectedVariant } from "../lib/types";

interface CodonVisualizerProps {
  variants: DetectedVariant[];
}

export const CodonVisualizer: React.FC<CodonVisualizerProps> = ({ variants }) => {
  const codingVariants = variants.filter((v) => v.codon_change !== null);

  if (codingVariants.length === 0) {
    if (variants.length > 0) {
      return (
        <div className="bg-stone-50 border border-stone-200 rounded p-5 text-xs text-stone-600">
          <div className="flex items-center gap-2 font-semibold text-stone-800 mb-1">
            <Info className="w-4 h-4 text-stone-500" />
            <span>Non-Coding Sequence Variations</span>
          </div>
          <p>
            The detected variants reside within untranslated regions (5&apos; or 3&apos; UTR) and do not alter coding triplets or amino acid sequences.
          </p>
        </div>
      );
    }
    return null;
  }

  return (
    <div className="border border-stone-300 bg-white rounded-lg p-6 shadow-xs space-y-5">
      {/* Visual Section Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase font-mono tracking-widest bg-stone-900 text-white px-2 py-0.5 rounded font-semibold">
              PRIMARY INSIGHT
            </span>
            <span className="text-[10px] uppercase font-mono tracking-wider bg-stone-100 text-stone-700 border border-stone-300 px-2 py-0.5 rounded font-semibold">
              COMPUTED RESULT
            </span>
          </div>
          <h2 className="font-serif text-lg font-semibold text-stone-900 mt-1">
            Codon Transformation &amp; Protein Consequence
          </h2>
          <p className="text-xs text-stone-500 font-sans">
            Deterministic translation mapped to NM_000518.5 CDS and NCBI Standard Genetic Code (Table 1).
          </p>
        </div>
      </div>

      {/* Primary Codon Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {codingVariants.map((v, idx) => {
          const c = v.codon_change!;
          const isStopGain = c.is_stop_gain;
          const isMissense = !c.is_stop_gain && !c.is_synonymous;

          // Intra-codon offset (0, 1, or 2)
          const cPosNum = parseInt(v.c_position, 10);
          const mutBaseIdx = !isNaN(cPosNum) ? (cPosNum - 1) % 3 : -1;

          return (
            <div
              key={v.id || idx}
              className="border border-stone-300 bg-stone-50/40 rounded-lg p-5 space-y-4"
            >
              {/* Card Meta Bar */}
              <div className="flex items-center justify-between text-xs font-mono border-b border-stone-200 pb-2.5">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-stone-900 bg-white border border-stone-300 px-2 py-0.5 rounded text-[11px]">
                    Codon {c.codon_number} of 148
                  </span>
                  <span className="text-stone-500 text-[11px]">
                    c.{c.c_start}..c.{c.c_end}
                  </span>
                </div>

                <span
                  className={`text-[11px] font-semibold px-2.5 py-0.5 rounded border ${
                    isStopGain
                      ? "bg-rose-50 text-rose-800 border-rose-300"
                      : isMissense
                      ? "bg-amber-50 text-amber-800 border-amber-300"
                      : "bg-emerald-50 text-emerald-800 border-emerald-300"
                  }`}
                >
                  {v.functional_impact}
                </span>
              </div>

              {/* Codon Transition Display */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 items-center">
                {/* Reference Codon */}
                <div className="bg-white border border-stone-200 rounded p-4 text-center">
                  <span className="text-[10px] uppercase font-mono tracking-widest text-stone-400 block mb-1">
                    REFERENCE CODON
                  </span>
                  <div className="font-mono text-3xl font-bold tracking-widest text-stone-900 my-1">
                    {c.ref_codon.split("").map((b, i) => (
                      <span
                        key={i}
                        className={
                          i === mutBaseIdx
                            ? "text-stone-900 border-b-2 border-stone-400"
                            : "text-stone-500"
                        }
                      >
                        {b}
                      </span>
                    ))}
                  </div>
                  <div className="text-xs font-serif text-stone-700 mt-1">
                    <strong>{c.ref_aa}</strong> ({c.ref_aa_single})
                  </div>
                </div>

                {/* Sample Codon */}
                <div
                  className={`border rounded p-4 text-center ${
                    isStopGain
                      ? "bg-rose-50/60 border-rose-300"
                      : isMissense
                      ? "bg-amber-50/60 border-amber-300"
                      : "bg-emerald-50/60 border-emerald-300"
                  }`}
                >
                  <span className="text-[10px] uppercase font-mono tracking-widest text-stone-500 block mb-1">
                    SAMPLE CODON
                  </span>
                  <div className="font-mono text-3xl font-bold tracking-widest my-1">
                    {c.sample_codon.split("").map((b, i) => (
                      <span
                        key={i}
                        className={
                          i === mutBaseIdx
                            ? isStopGain
                              ? "text-rose-800 bg-rose-200/80 px-1 rounded"
                              : "text-amber-800 bg-amber-200/80 px-1 rounded"
                            : "text-stone-600"
                        }
                      >
                        {b}
                      </span>
                    ))}
                  </div>
                  <div className="text-xs font-serif mt-1">
                    <strong className={isStopGain ? "text-rose-800 font-bold" : "text-stone-900"}>
                      {c.sample_aa === "Ter" ? "STOP (Ter)" : c.sample_aa}
                    </strong>{" "}
                    ({c.sample_aa_single})
                  </div>
                </div>
              </div>

              {/* Bottom Consequence Details Bar */}
              <div className="pt-3 border-t border-stone-200 flex flex-wrap items-center justify-between gap-2 text-xs">
                <div>
                  <span className="text-[10px] uppercase font-mono text-stone-400 block">
                    PROTEIN NOMENCLATURE
                  </span>
                  <span className="font-mono text-sm font-bold text-stone-900">
                    {v.hgvs_p || "p.(=)"}
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-[10px] uppercase font-mono text-stone-400 block">
                    HGVS cDNA IDENTIFIER
                  </span>
                  <span className="font-mono text-xs font-semibold text-stone-800">
                    {v.hgvs_c}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
