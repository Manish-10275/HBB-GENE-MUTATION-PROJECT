"use client";

import React from "react";
import { DetectedVariant } from "../lib/types";
import { Search, ExternalLink, ArrowRight } from "lucide-react";

interface VariantsTableProps {
  variants: DetectedVariant[];
  onSelectVariantForEvidence?: (variant: DetectedVariant) => void;
}

export const VariantsTable: React.FC<VariantsTableProps> = ({
  variants,
  onSelectVariantForEvidence,
}) => {
  if (variants.length === 0) {
    return (
      <div className="bg-white border border-stone-200 rounded-lg p-8 text-center text-stone-500 shadow-sm">
        <p className="text-sm font-semibold text-stone-800">No Sequence Variants Detected</p>
        <p className="text-xs text-stone-500 mt-1">
          The analyzed sequence is 100% identical to the reference transcript NM_000518.5.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex items-center justify-between">
        <div>
          <h3 className="font-serif text-sm font-semibold text-stone-900">
            Detected Sequence Variations
          </h3>
          <p className="text-xs text-stone-500">
            Computed deterministically by comparing sample bases with canonical NM_000518.5 coordinates.
          </p>
        </div>
        <span className="text-xs font-mono bg-stone-900 text-white px-2 py-0.5 rounded font-medium">
          {variants.length} {variants.length === 1 ? "Variant" : "Variants"}
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-stone-50 border-b border-stone-200 font-mono text-stone-600 uppercase text-[10px] tracking-wider">
              <th className="py-3 px-4">HGVS cDNA (c.)</th>
              <th className="py-3 px-4">Position</th>
              <th className="py-3 px-4">Allele Change</th>
              <th className="py-3 px-4">Impact</th>
              <th className="py-3 px-4">Protein (HGVS p.)</th>
              <th className="py-3 px-4">Codon Transformation</th>
              {onSelectVariantForEvidence && <th className="py-3 px-4 text-right">Evidence Action</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100 font-sans">
            {variants.map((v) => {
              const isNonsense = v.functional_impact.toLowerCase().includes("nonsense");
              const isMissense = v.functional_impact.toLowerCase().includes("missense");
              const isSynonymous = v.functional_impact.toLowerCase().includes("synonymous");

              return (
                <tr key={v.id} className="hover:bg-stone-50/80 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-bold text-stone-900">
                    {v.hgvs_c}
                  </td>
                  <td className="py-3.5 px-4 font-mono text-stone-600">
                    c.{v.c_position}
                    <span className="text-[10px] text-stone-400 block font-mono">
                      (mRNA: {v.ref_position_mrna})
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono">
                    <span className="inline-flex items-center gap-1.5 font-bold">
                      <span className="text-stone-500">{v.ref_allele}</span>
                      <ArrowRight className="w-3 h-3 text-stone-400" />
                      <span className="text-stone-900">{v.alt_allele}</span>
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-[11px] font-semibold border ${
                        isNonsense
                          ? "bg-rose-50 text-rose-800 border-rose-200"
                          : isMissense
                          ? "bg-amber-50 text-amber-800 border-amber-200"
                          : isSynonymous
                          ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                          : "bg-stone-100 text-stone-700 border-stone-200"
                      }`}
                    >
                      {v.functional_impact}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-semibold text-stone-900">
                    {v.hgvs_p || <span className="text-stone-400 font-normal">None (Non-coding)</span>}
                  </td>
                  <td className="py-3.5 px-4 font-mono text-stone-600">
                    {v.codon_change ? (
                      <span className="text-xs">
                        Codon {v.codon_change.codon_number}:{" "}
                        <strong className="text-stone-800">{v.codon_change.ref_codon}</strong> ({v.codon_change.ref_aa}) &rarr;{" "}
                        <strong className="text-stone-900">{v.codon_change.sample_codon}</strong> ({v.codon_change.sample_aa})
                      </span>
                    ) : (
                      <span className="text-stone-400 italic">N/A</span>
                    )}
                  </td>
                  {onSelectVariantForEvidence && (
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => onSelectVariantForEvidence(v)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-stone-700 bg-stone-100 hover:bg-stone-200 border border-stone-200 rounded transition-colors"
                      >
                        <Search className="w-3 h-3 text-stone-500" />
                        Evidence
                      </button>
                    </td>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
