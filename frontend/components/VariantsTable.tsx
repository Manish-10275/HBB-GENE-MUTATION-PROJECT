"use client";

import React from "react";
import { DetectedVariant } from "../lib/types";
import { ArrowRight, Search } from "lucide-react";

interface VariantsTableProps {
  variants: DetectedVariant[];
  activeVariantId?: string | null;
  onSelectVariant?: (variantId: string) => void;
  onSelectVariantForEvidence?: (variant: DetectedVariant) => void;
}

export const VariantsTable: React.FC<VariantsTableProps> = ({
  variants,
  activeVariantId,
  onSelectVariant,
  onSelectVariantForEvidence,
}) => {
  if (variants.length === 0) {
    return (
      <div className="bg-white border border-stone-200 rounded-lg p-5 text-center text-xs text-stone-500">
        <strong className="text-stone-800 font-semibold block mb-0.5">No Sequence Variants Detected</strong>
        <span>Input sequence demonstrates 100% identity across all 628 base pairs of the NM_000518.5 canonical reference.</span>
      </div>
    );
  }

  return (
    <div className="bg-white border border-stone-200 rounded-lg overflow-hidden">
      {/* Table Header Strip */}
      <div className="px-5 py-3 border-b border-stone-200 bg-stone-50/70 flex items-center justify-between">
        <div>
          <h3 className="font-serif text-sm font-semibold text-stone-900">
            Detected Variant Summary
          </h3>
          <p className="text-xs text-stone-500 font-sans">
            Deterministic differences called against NM_000518.5 coordinates. Click a variant to synchronize with the Mutation Map.
          </p>
        </div>
        <span className="text-xs font-mono font-bold bg-stone-900 text-white px-2 py-0.5 rounded">
          {variants.length} {variants.length === 1 ? "Variant" : "Variants"}
        </span>
      </div>

      <div className="overflow-x-auto custom-scrollbar">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-stone-50 border-b border-stone-200 font-mono text-stone-600 uppercase text-[10px] tracking-wider">
              <th className="py-2.5 px-4 font-semibold">HGVS cDNA</th>
              <th className="py-2.5 px-4 font-semibold">Position</th>
              <th className="py-2.5 px-4 font-semibold">Change</th>
              <th className="py-2.5 px-4 font-semibold">Functional Impact</th>
              <th className="py-2.5 px-4 font-semibold">Protein (p.)</th>
              <th className="py-2.5 px-4 font-semibold">Codon Shift</th>
              {onSelectVariantForEvidence && (
                <th className="py-2.5 px-4 font-semibold text-right">Action</th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100 font-sans">
            {variants.map((v) => {
              const isNonsense = v.functional_impact.toLowerCase().includes("nonsense");
              const isMissense = v.functional_impact.toLowerCase().includes("missense");
              const isSynonymous = v.functional_impact.toLowerCase().includes("synonymous");
              const isActive = activeVariantId ? v.id === activeVariantId : false;

              return (
                <tr
                  key={v.id}
                  onClick={() => onSelectVariant && onSelectVariant(v.id)}
                  className={`transition-colors cursor-pointer ${
                    isActive
                      ? "bg-amber-50/90 font-medium border-l-4 border-amber-500"
                      : "hover:bg-stone-50/60"
                  }`}
                >
                  <td className="py-2.5 px-4 font-mono font-bold text-stone-900">
                    <span className="inline-flex items-center gap-1.5">
                      <span>{v.hgvs_c}</span>
                      {isActive && (
                        <span className="text-[9px] font-mono uppercase bg-amber-200 text-amber-900 px-1 py-0.2 rounded font-bold">
                          MAP ACTIVE
                        </span>
                      )}
                    </span>
                  </td>
                  <td className="py-2.5 px-4 font-mono text-stone-600">
                    c.{v.c_position}
                    <span className="text-[10px] text-stone-400 block">
                      (mRNA: {v.ref_position_mrna})
                    </span>
                  </td>
                  <td className="py-2.5 px-4 font-mono">
                    <span className="inline-flex items-center gap-1 font-bold">
                      <span className="text-stone-500">{v.ref_allele}</span>
                      <ArrowRight className="w-3 h-3 text-stone-400" />
                      <span className="text-stone-900">{v.alt_allele}</span>
                    </span>
                  </td>
                  <td className="py-2.5 px-4">
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
                  <td className="py-2.5 px-4 font-mono font-bold text-stone-900">
                    {v.hgvs_p || <span className="text-stone-400 font-normal">None</span>}
                  </td>
                  <td className="py-2.5 px-4 font-mono text-stone-700">
                    {v.codon_change ? (
                      <span>
                        Codon {v.codon_change.codon_number}:{" "}
                        <strong className="text-stone-900">{v.codon_change.ref_codon}</strong> ({v.codon_change.ref_aa}) &rarr;{" "}
                        <strong className="text-stone-900">{v.codon_change.sample_codon}</strong> ({v.codon_change.sample_aa})
                      </span>
                    ) : (
                      <span className="text-stone-400 italic">Non-coding</span>
                    )}
                  </td>
                  {onSelectVariantForEvidence && (
                    <td className="py-2.5 px-4 text-right">
                      <button
                        onClick={() => onSelectVariantForEvidence(v)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-stone-700 bg-stone-100 hover:bg-stone-200 border border-stone-200 rounded"
                        title="Query direct evidence for this variant"
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
