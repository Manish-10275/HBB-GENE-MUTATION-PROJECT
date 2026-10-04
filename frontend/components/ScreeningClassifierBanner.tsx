"use client";

import React from "react";
import { ScreeningClassification } from "../lib/types";
import { ShieldAlert, Activity, Dna, Info } from "lucide-react";

interface ScreeningClassifierBannerProps {
  classification: ScreeningClassification | null;
  currentZygosity: string;
  onZygosityChange?: (newZygosity: string) => void;
}

export const ScreeningClassifierBanner: React.FC<ScreeningClassifierBannerProps> = ({
  classification,
  currentZygosity,
  onZygosityChange,
}) => {
  if (!classification) return null;

  const isHomozygous = currentZygosity.toLowerCase() === "homozygous";
  const isNormal = classification.severity === "Normal";
  const isMajor = classification.severity.toLowerCase().includes("major") || classification.severity.toLowerCase().includes("severe");
  const isCarrier = classification.severity.toLowerCase().includes("carrier") || classification.severity.toLowerCase().includes("minor");

  // Determine badge styling based on clinical severity
  let badgeClasses = "bg-stone-100 text-stone-800 border-stone-300";
  let borderHighlight = "border-stone-200";

  if (isNormal) {
    badgeClasses = "bg-emerald-50 text-emerald-800 border-emerald-300";
    borderHighlight = "border-emerald-200";
  } else if (isMajor) {
    badgeClasses = "bg-rose-50 text-rose-800 border-rose-300";
    borderHighlight = "border-rose-300";
  } else if (isCarrier) {
    badgeClasses = "bg-amber-50 text-amber-900 border-amber-300";
    borderHighlight = "border-amber-300";
  }

  return (
    <div className={`bg-white border ${borderHighlight} rounded-lg p-4 sm:p-5 shadow-sm space-y-4`}>
      {/* Header Strip */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-stone-200 pb-3">
        <div className="space-y-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[10px] font-mono uppercase tracking-wider font-semibold px-2 py-0.5 rounded border bg-stone-50 text-stone-700 border-stone-200 flex items-center gap-1">
              <Dna className="w-3 h-3 text-stone-500" />
              EDUCATIONAL SCREENING MODEL
            </span>
            <span className={`text-[10px] font-mono uppercase tracking-wider font-bold px-2 py-0.5 rounded border ${badgeClasses}`}>
              {classification.thalassemia_type}
            </span>
            <span className={`text-[10px] font-mono uppercase font-semibold px-2 py-0.5 rounded border ${badgeClasses}`}>
              {classification.severity}
            </span>
          </div>

          <h3 className="font-serif text-lg font-bold text-stone-900 leading-snug">
            {classification.condition_name}
          </h3>
        </div>

        {/* Interactive Zygosity Toggle */}
        {!isNormal && onZygosityChange && (
          <div className="flex items-center gap-2 bg-stone-50 border border-stone-200 p-1.5 rounded-lg shrink-0">
            <span className="text-[11px] font-mono text-stone-500 font-medium pl-1">
              Zygosity:
            </span>
            <div className="inline-flex rounded-md shadow-sm">
              <button
                type="button"
                onClick={() => onZygosityChange("heterozygous")}
                className={`px-2.5 py-1 text-xs font-mono font-medium rounded-l border ${
                  !isHomozygous
                    ? "bg-amber-100 text-amber-900 border-amber-300 font-bold"
                    : "bg-white text-stone-600 border-stone-200 hover:bg-stone-50"
                }`}
              >
                Heterozygous (Carrier)
              </button>
              <button
                type="button"
                onClick={() => onZygosityChange("homozygous")}
                className={`px-2.5 py-1 text-xs font-mono font-medium rounded-r border-t border-b border-r ${
                  isHomozygous
                    ? "bg-rose-100 text-rose-900 border-rose-300 font-bold"
                    : "bg-white text-stone-600 border-stone-200 hover:bg-stone-50"
                }`}
              >
                Homozygous (Affected)
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Clinical Narrative */}
      <div className="text-xs text-stone-700 leading-relaxed font-sans">
        <p>{classification.clinical_summary}</p>
      </div>

      {/* Laboratory Indices Correlation */}
      {classification.laboratory_correlations && classification.laboratory_correlations.length > 0 && (
        <div className="bg-stone-50 border border-stone-200/80 rounded-md p-3 space-y-2">
          <div className="flex items-center gap-1.5 text-stone-700 text-xs font-mono font-semibold">
            <Activity className="w-3.5 h-3.5 text-blue-600" />
            <span>Expected Laboratory &amp; Chromatography Correlates (Educational):</span>
          </div>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1.5 text-xs text-stone-600 font-mono list-disc list-inside">
            {classification.laboratory_correlations.map((lab, i) => (
              <li key={i} className="text-[11px]">
                {lab}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Mandatory Regulatory & Educational Disclaimer */}
      <div className="flex items-start gap-2 pt-1 border-t border-stone-100 text-[11px] text-stone-500 font-sans">
        <ShieldAlert className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
        <p>
          <strong className="text-stone-700">Educational Simulation Disclaimer:</strong>{" "}
          {classification.educational_disclaimer}
        </p>
      </div>
    </div>
  );
};
