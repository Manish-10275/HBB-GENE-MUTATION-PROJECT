"use client";

import React from "react";
import { ArrowDown, AlertOctagon, CheckCircle2, Info } from "lucide-react";
import { DetectedVariant } from "../lib/types";

interface CodonVisualizerProps {
  variants: DetectedVariant[];
}

export const CodonVisualizer: React.FC<CodonVisualizerProps> = ({ variants }) => {
  const codingVariants = variants.filter((v) => v.codon_change !== null);

  if (codingVariants.length === 0) {
    if (variants.length > 0) {
      return (
        <div className="bg-stone-50 border border-stone-200 rounded-lg p-6 text-center text-xs text-stone-500">
          <Info className="w-5 h-5 mx-auto text-stone-400 mb-2" />
          <p className="font-semibold text-stone-700">Non-Coding Sequence Variations Detected</p>
          <p className="mt-1">
            The detected variants reside within the 5' or 3' untranslated regions (UTRs) and do not alter coding triplets.
          </p>
        </div>
      );
    }
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-stone-200 pb-2">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-serif text-base font-semibold text-stone-900">
              Codon & Protein Consequence Architecture
            </h3>
            <p className="text-xs text-stone-500">
              Deterministic translation based on NCBI Standard Genetic Code (Table 1) and NM_000518.5 CDS coordinates.
            </p>
          </div>
          <span className="text-[11px] font-mono bg-stone-100 text-stone-700 border border-stone-200 px-2 py-0.5 rounded">
            COMPUTED RESULT
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {codingVariants.map((v, idx) => {
          const c = v.codon_change!;
          const isStopGain = c.is_stop_gain;
          const isMissense = !c.is_stop_gain && !c.is_synonymous;
          const isSynonymous = c.is_synonymous;

          // Find which nucleotide index within the 3-base codon was mutated
          const cPosNum = parseInt(v.c_position, 10);
          const mutBaseIdxInCodon = !isNaN(cPosNum) ? (cPosNum - 1) % 3 : -1;

          return (
            <div
              key={v.id || idx}
              className="bg-white border-2 border-stone-300 rounded-xl p-5 shadow-sm hover:border-stone-400 transition-colors"
            >
              {/* Header meta */}
              <div className="flex items-center justify-between mb-4 border-b border-stone-100 pb-3">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-xs font-bold text-stone-800 bg-stone-100 px-2 py-0.5 rounded border border-stone-200">
                    Codon {c.codon_number}
                  </span>
                  <span className="font-mono text-xs text-stone-500">
                    c.{c.c_start}..c.{c.c_end}
                  </span>
                </div>

                <div className="flex items-center space-x-1.5">
                  <span
                    className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${
                      isStopGain
                        ? "bg-rose-50 text-rose-700 border-rose-200"
                        : isMissense
                        ? "bg-amber-50 text-amber-700 border-amber-200"
                        : "bg-emerald-50 text-emerald-700 border-emerald-200"
                    }`}
                  >
                    {v.functional_impact}
                  </span>
                </div>
              </div>

              {/* Codon Transition Stage */}
              <div className="bg-stone-50/70 border border-stone-200 rounded-lg p-5">
                <div className="flex flex-col items-center space-y-3">
                  {/* Reference Codon Box */}
                  <div className="w-full text-center bg-white border border-stone-200 rounded p-3 shadow-2xs">
                    <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block mb-1">
                      REFERENCE CODON
                    </span>
                    <div className="font-mono text-2xl font-bold tracking-widest text-stone-900">
                      {c.ref_codon.split("").map((b, i) => (
                        <span
                          key={i}
                          className={i === mutBaseIdxInCodon ? "text-stone-900 underline underline-offset-4 decoration-stone-400" : "text-stone-600"}
                        >
                          {b}
                        </span>
                      ))}
                    </div>
                    <div className="mt-1 text-xs font-serif text-stone-600">
                      <strong>{c.ref_aa}</strong> ({c.ref_aa_single})
                    </div>
                  </div>

                  {/* Transition Indicator */}
                  <div className="flex items-center justify-center text-stone-400 py-0.5">
                    <div className="flex flex-col items-center">
                      <div className="w-0.5 h-3 bg-stone-300" />
                      <ArrowDown className="w-4 h-4 text-stone-600" />
                    </div>
                  </div>

                  {/* Sample Codon Box */}
                  <div
                    className={`w-full text-center rounded p-3 border shadow-2xs ${
                      isStopGain
                        ? "bg-rose-50/70 border-rose-300"
                        : isMissense
                        ? "bg-amber-50/70 border-amber-300"
                        : "bg-emerald-50/70 border-emerald-300"
                    }`}
                  >
                    <span className="text-[10px] uppercase font-mono tracking-wider text-stone-500 block mb-1">
                      SAMPLE CODON
                    </span>
                    <div className="font-mono text-2xl font-bold tracking-widest">
                      {c.sample_codon.split("").map((b, i) => (
                        <span
                          key={i}
                          className={
                            i === mutBaseIdxInCodon
                              ? isStopGain
                                ? "text-rose-700 bg-rose-200/60 px-1 rounded"
                                : "text-amber-800 bg-amber-200/60 px-1 rounded"
                              : "text-stone-700"
                          }
                        >
                          {b}
                        </span>
                      ))}
                    </div>
                    <div className="mt-1 text-xs font-serif">
                      <strong className={isStopGain ? "text-rose-700 text-sm font-bold tracking-wide" : "text-stone-800"}>
                        {c.sample_aa === "Ter" ? "STOP (Ter)" : c.sample_aa}
                      </strong>{" "}
                      ({c.sample_aa_single})
                    </div>
                  </div>
                </div>
              </div>

              {/* Consequence Summary Callout */}
              <div className="mt-4 pt-3 border-t border-stone-200 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                    PROTEIN NOMENCLATURE
                  </span>
                  <span className="font-mono text-sm font-bold text-stone-900">
                    {v.hgvs_p || "p.(=)"}
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                    HGVS cDNA
                  </span>
                  <span className="font-mono text-xs text-stone-700">
                    c.{v.c_position}{v.ref_allele}&gt;{v.alt_allele}
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
