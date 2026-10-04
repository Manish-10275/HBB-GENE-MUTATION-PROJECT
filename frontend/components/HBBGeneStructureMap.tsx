"use client";

import React, { useState } from "react";
import { DetectedVariant } from "../lib/types";
import { MapPin, Info, Layers, ExternalLink, ArrowRight, CheckCircle } from "lucide-react";

interface MutationMarker {
  id: string;
  name: string;
  c_pos: string;
  transcript_pos_bp: number; // 1-based on NM_000518.5 (628 bp)
  genomic_rel_bp: number;    // 1-based on NG_000007.3 gene locus (1608 bp)
  genomic_abs_bp: number;    // 1-based NG_000007.3 genomic coordinate
  region: string;
  type: string;
  consequence: string;
  clinvar_id: string;
  isIntronicOnly?: boolean;
}

const CURATED_MUTATIONS: MutationMarker[] = [
  {
    id: "c20a_t",
    name: "c.20A>T (p.Glu7Val)",
    c_pos: "20",
    transcript_pos_bp: 70,
    genomic_rel_bp: 70,
    genomic_abs_bp: 70614,
    region: "Exon 1",
    type: "Missense",
    consequence: "Sickle Cell Variant (HbS)",
    clinvar_id: "15333",
  },
  {
    id: "c19g_a",
    name: "c.19G>A (p.Glu7Lys)",
    c_pos: "19",
    transcript_pos_bp: 69,
    genomic_rel_bp: 69,
    genomic_abs_bp: 70613,
    region: "Exon 1",
    type: "Missense",
    consequence: "Hemoglobin C Variant (HbC)",
    clinvar_id: "15126",
  },
  {
    id: "cd8-9",
    name: "Cd8/9 (+G) / c.27dup",
    c_pos: "27",
    transcript_pos_bp: 77,
    genomic_rel_bp: 77,
    genomic_abs_bp: 70621,
    region: "Exon 1",
    type: "Frameshift Insertion",
    consequence: "p.Ser10fs (β0 Thalassemia)",
    clinvar_id: "36308",
  },
  {
    id: "cd30",
    name: "Cd30 (G>C) / c.93G>C",
    c_pos: "93",
    transcript_pos_bp: 143,
    genomic_rel_bp: 142,
    genomic_abs_bp: 70686,
    region: "Exon 1 / Splice Boundary",
    type: "Splice / Missense",
    consequence: "p.Arg31Ser (β0 / Severe β+)",
    clinvar_id: "869321",
  },
  {
    id: "ivs1-5",
    name: "IVS1-5 (G>C) / c.92+5G>C",
    c_pos: "92+5",
    transcript_pos_bp: -1, // Intronic, not in spliced cDNA
    genomic_rel_bp: 147,
    genomic_abs_bp: 70691,
    region: "Intron 1 (IVS-1)",
    type: "Splice Donor Defect",
    consequence: "Severe Aberrant Splicing (β+ Thalassemia)",
    clinvar_id: "15447",
    isIntronicOnly: true,
  },
  {
    id: "c118c_t",
    name: "c.118C>T (p.Gln40Ter)",
    c_pos: "118",
    transcript_pos_bp: 168,
    genomic_rel_bp: 298,
    genomic_abs_bp: 70842,
    region: "Exon 2",
    type: "Nonsense (Stop Gain)",
    consequence: "p.Gln40Ter (β0 Thalassemia Benchmark)",
    clinvar_id: "15402",
  },
  {
    id: "cd41-42",
    name: "Cd41/42 (-TCTT) / c.126_129del",
    c_pos: "126_129",
    transcript_pos_bp: 176,
    genomic_rel_bp: 306,
    genomic_abs_bp: 70850,
    region: "Exon 2",
    type: "Frameshift Deletion",
    consequence: "p.Phe42fs (β0 Thalassemia)",
    clinvar_id: "15417",
  },
];

interface HBBGeneStructureMapProps {
  detectedVariants?: DetectedVariant[];
  activeVariantId?: string | null;
  onSelectVariant?: (variantId: string) => void;
  onSelectMutationPreset?: (presetId: string) => void;
  activeReference?: string;
}

export function isVariantMatch(v: DetectedVariant, m: MutationMarker): boolean {
  const hgvs = (v.hgvs_c || "").toLowerCase();
  const cPos = (v.c_position || "").toLowerCase();
  const pStr = (v.hgvs_p || "").toLowerCase();

  if (m.c_pos === v.c_position) return true;
  if (m.id === "c118c_t" && (hgvs.includes("118c>t") || pStr.includes("gln40ter") || cPos === "118")) return true;
  if (m.id === "c20a_t" && (hgvs.includes("20a>t") || pStr.includes("glu7val") || pStr.includes("glu6val") || cPos === "20")) return true;
  if (m.id === "c19g_a" && (hgvs.includes("19g>a") || pStr.includes("glu7lys") || pStr.includes("glu6lys") || cPos === "19")) return true;
  if (m.id === "ivs1-5" && (hgvs.includes("92+5") || cPos === "92+5" || hgvs.includes("ivs1-5"))) return true;
  if (m.id === "cd41-42" && (hgvs.includes("126_129") || hgvs.includes("cd41") || pStr.includes("phe42fs") || cPos === "126_129")) return true;
  if (m.id === "cd8-9" && (hgvs.includes("27dup") || hgvs.includes("cd8") || cPos === "27" || pStr.includes("ser10fs") || hgvs.includes("27_28insg"))) return true;
  if (m.id === "cd30" && (hgvs.includes("93g>c") || hgvs.includes("cd30") || pStr.includes("arg31ser") || cPos === "93")) return true;
  return false;
}

export const HBBGeneStructureMap: React.FC<HBBGeneStructureMapProps> = ({
  detectedVariants = [],
  activeVariantId,
  onSelectVariant,
  onSelectMutationPreset,
  activeReference = "NM_000518.5",
}) => {
  const [viewMode, setViewMode] = useState<"transcript" | "genomic">(
    activeReference.startsWith("NG_") ? "genomic" : "transcript"
  );
  const [manualLocusId, setManualLocusId] = useState<string | null>(null);

  // Active detected variant from the analysis
  const activeDetectedVariant =
    detectedVariants.find((v) => v.id === activeVariantId) ||
    (detectedVariants.length > 0 ? detectedVariants[0] : null);

  // Match active detected variant to curated mutations
  const activeCuratedMatch = activeDetectedVariant
    ? CURATED_MUTATIONS.find((m) => isVariantMatch(activeDetectedVariant, m)) || null
    : null;

  // Dynamic marker if active variant is uncurated
  const dynamicActiveMarker: MutationMarker | null =
    activeDetectedVariant && !activeCuratedMatch
      ? {
          id: activeDetectedVariant.id,
          name: `${activeDetectedVariant.hgvs_c} ${activeDetectedVariant.hgvs_p ? `(${activeDetectedVariant.hgvs_p})` : ""}`.trim(),
          c_pos: activeDetectedVariant.c_position,
          transcript_pos_bp: activeDetectedVariant.ref_position_mrna,
          genomic_rel_bp: activeDetectedVariant.ref_position_mrna,
          genomic_abs_bp: activeReference.startsWith("NG_")
            ? 70545 + activeDetectedVariant.ref_position_mrna - 1
            : 0,
          region: activeDetectedVariant.codon_change
            ? `Exon (Codon ${activeDetectedVariant.codon_change.codon_number})`
            : activeDetectedVariant.c_position.includes("+") ||
              activeDetectedVariant.c_position.includes("-")
            ? "Intron / Splice Junction"
            : "Exon",
          type: activeDetectedVariant.functional_impact,
          consequence: activeDetectedVariant.codon_change
            ? `${activeDetectedVariant.codon_change.ref_aa} → ${activeDetectedVariant.codon_change.sample_aa} (${activeDetectedVariant.functional_impact})`
            : activeDetectedVariant.functional_impact,
          clinvar_id: "",
          isIntronicOnly:
            activeDetectedVariant.c_position.includes("+") ||
            activeDetectedVariant.c_position.includes("-"),
        }
      : null;

  // Resolved marker to display in inspector card
  let selectedMutation: MutationMarker | null = null;
  if (manualLocusId) {
    selectedMutation = CURATED_MUTATIONS.find((m) => m.id === manualLocusId) || null;
  }
  if (!selectedMutation) {
    selectedMutation = activeCuratedMatch || dynamicActiveMarker || CURATED_MUTATIONS[0];
  }

  // When active variant or analysis changes, reset manual locus selection
  React.useEffect(() => {
    setManualLocusId(null);
  }, [activeVariantId, detectedVariants]);

  // View mode synchronization
  React.useEffect(() => {
    if (
      activeReference.startsWith("NG_") ||
      activeDetectedVariant?.c_position.includes("+") ||
      selectedMutation?.isIntronicOnly
    ) {
      setViewMode("genomic");
    } else if (activeReference.startsWith("NM_")) {
      setViewMode("transcript");
    }
  }, [activeReference, activeDetectedVariant?.c_position, selectedMutation?.isIntronicOnly]);

  const isGenomic = viewMode === "genomic";
  const totalLength = isGenomic ? 1608 : 628;

  // Check if selectedMutation matches a variant in the active analysis
  const sampleMatchForSelected = selectedMutation
    ? detectedVariants.find((v) => isVariantMatch(v, selectedMutation!) || v.id === selectedMutation!.id)
    : null;

  // Uncurated variants that need dynamic pins
  const uncuratedVariants = detectedVariants.filter(
    (v) => !CURATED_MUTATIONS.some((m) => isVariantMatch(v, m))
  );

  return (
    <div className="bg-white border border-stone-200 rounded-lg p-5 space-y-5 shadow-sm">
      {/* Header and View Mode Toggle */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-stone-200 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono uppercase tracking-wider bg-indigo-50 text-indigo-800 border border-indigo-200 px-2 py-0.5 rounded font-semibold">
              GENE ARCHITECTURE &amp; MUTATION MAP
            </span>
            <span className="text-xs text-stone-500 font-mono">
              {isGenomic ? "NG_000007.3 (1,608 bp locus)" : "NM_000518.5 (628 bp mRNA)"}
            </span>
            {activeDetectedVariant && (
              <span className="text-[10px] font-mono bg-emerald-50 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded font-bold">
                SYNCHRONIZED WITH ANALYSIS
              </span>
            )}
          </div>
          <h3 className="font-serif text-base font-semibold text-stone-900 mt-0.5">
            Human HBB Exon / Intron Structure &amp; Mutation Loci
          </h3>
        </div>

        {/* View Switcher */}
        <div className="flex items-center gap-1.5 bg-stone-100 p-1 rounded-md text-xs font-mono shrink-0">
          <button
            type="button"
            onClick={() => setViewMode("transcript")}
            className={`px-3 py-1 rounded font-medium transition-colors ${
              !isGenomic
                ? "bg-white text-stone-900 shadow-xs font-semibold"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            Transcript View (628 bp)
          </button>
          <button
            type="button"
            onClick={() => setViewMode("genomic")}
            className={`px-3 py-1 rounded font-medium transition-colors ${
              isGenomic
                ? "bg-white text-stone-900 shadow-xs font-semibold"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            Genomic Locus View (1,608 bp)
          </button>
        </div>
      </div>

      {/* Gene Structure Track Visualizer */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-[11px] font-mono text-stone-500">
          <span>5&apos; End (Pos 1)</span>
          <span className="font-medium text-stone-700">
            {isGenomic ? "NG_000007.3 Locus (70,545 .. 72,152 bp)" : "cDNA NM_000518.5 (1 .. 628 bp)"}
          </span>
          <span>3&apos; End (Pos {totalLength} bp)</span>
        </div>

        {/* Proportional Segment Bar */}
        <div className="relative h-12 w-full bg-stone-100 rounded border border-stone-300 overflow-hidden flex">
          {isGenomic ? (
            // Genomic Track: Exon 1, Intron 1, Exon 2, Intron 2, Exon 3
            <>
              {/* Exon 1 (1..142 bp = 8.8%) */}
              <div
                style={{ width: `${(142 / 1608) * 100}%` }}
                className="h-full bg-blue-600 border-r border-blue-700 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-700 cursor-pointer"
                title="Exon 1: 142 bp (5' UTR 50 bp + Coding 92 bp)"
              >
                <span>Exon 1</span>
                <span className="text-[9px] font-normal opacity-80">142 bp</span>
              </div>

              {/* Intron 1 (143..272 bp = 8.1%) */}
              <div
                style={{ width: `${(130 / 1608) * 100}%` }}
                className="h-full bg-stone-200 border-r border-stone-300 text-stone-600 flex flex-col items-center justify-center text-[10px] font-mono hover:bg-stone-300 cursor-pointer"
                title="Intron 1 (IVS-1): 130 bp (Contains IVS1-5 splice site)"
              >
                <span className="font-semibold text-[9px]">Intron 1</span>
                <span className="text-[8px] opacity-75">130 bp</span>
              </div>

              {/* Exon 2 (273..495 bp = 13.9%) */}
              <div
                style={{ width: `${(223 / 1608) * 100}%` }}
                className="h-full bg-blue-600 border-r border-blue-700 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-700 cursor-pointer"
                title="Exon 2: 223 bp (Contains Cd41/42 and c.118C>T)"
              >
                <span>Exon 2</span>
                <span className="text-[9px] font-normal opacity-80">223 bp</span>
              </div>

              {/* Intron 2 (496..1345 bp = 52.9%) */}
              <div
                style={{ width: `${(850 / 1608) * 100}%` }}
                className="h-full bg-stone-200 border-r border-stone-300 text-stone-600 flex flex-col items-center justify-center text-[10px] font-mono hover:bg-stone-300 cursor-pointer"
                title="Intron 2 (IVS-2): 850 bp"
              >
                <span className="font-semibold text-[9px]">Intron 2 (IVS-2)</span>
                <span className="text-[8px] opacity-75">850 bp</span>
              </div>

              {/* Exon 3 (1346..1608 bp = 16.3%) */}
              <div
                style={{ width: `${(263 / 1608) * 100}%` }}
                className="h-full bg-blue-600 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-700 cursor-pointer"
                title="Exon 3: 263 bp (Coding 129 bp + 3' UTR 134 bp)"
              >
                <span>Exon 3</span>
                <span className="text-[9px] font-normal opacity-80">263 bp</span>
              </div>
            </>
          ) : (
            // Transcript Track: Exon 1 (with 5' UTR), Exon 2, Exon 3 (with 3' UTR)
            <>
              {/* Exon 1 (1..142 bp = 22.6%) */}
              <div
                style={{ width: `${(142 / 628) * 100}%` }}
                className="h-full bg-blue-600 border-r border-blue-700 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-700 cursor-pointer"
                title="Exon 1: 142 bp (5' UTR: 1..50 bp, Coding: 51..142 bp)"
              >
                <span>Exon 1</span>
                <span className="text-[9px] font-normal opacity-80">1..142 bp</span>
              </div>

              {/* Exon 2 (143..365 bp = 35.5%) */}
              <div
                style={{ width: `${(223 / 628) * 100}%` }}
                className="h-full bg-blue-700 border-r border-blue-800 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-800 cursor-pointer"
                title="Exon 2: 223 bp (Coding: 143..365 bp)"
              >
                <span>Exon 2</span>
                <span className="text-[9px] font-normal opacity-80">143..365 bp</span>
              </div>

              {/* Exon 3 (366..628 bp = 41.9%) */}
              <div
                style={{ width: `${(263 / 628) * 100}%` }}
                className="h-full bg-blue-600 text-white flex flex-col items-center justify-center text-[10px] font-mono font-bold hover:bg-blue-700 cursor-pointer"
                title="Exon 3: 263 bp (Coding: 366..494 bp, 3' UTR: 495..628 bp)"
              >
                <span>Exon 3</span>
                <span className="text-[9px] font-normal opacity-80">366..628 bp</span>
              </div>
            </>
          )}

          {/* Render Curated Mutation Pins */}
          {CURATED_MUTATIONS.map((m) => {
            const pos = isGenomic ? m.genomic_rel_bp : m.transcript_pos_bp;
            if (pos <= 0) return null; // e.g. intronic in transcript view

            const leftPct = (pos / totalLength) * 100;
            const sampleVariantMatch = detectedVariants.find((v) => isVariantMatch(v, m));
            const isSampleDetected = Boolean(sampleVariantMatch);
            const isMarkerActive = selectedMutation?.id === m.id;

            return (
              <button
                key={m.id}
                type="button"
                onClick={() => {
                  if (sampleVariantMatch && onSelectVariant) {
                    onSelectVariant(sampleVariantMatch.id);
                  }
                  setManualLocusId(m.id);
                }}
                style={{ left: `${leftPct}%` }}
                className="absolute top-0 bottom-0 -ml-1.5 w-3 z-10 flex flex-col items-center justify-between group cursor-pointer focus:outline-none"
                title={`${m.name} (${m.region}) ${isSampleDetected ? "[Sample Match]" : ""}`}
              >
                <div
                  className={`transition-all ${
                    isSampleDetected
                      ? isMarkerActive
                        ? "w-3.5 h-3.5 rounded-full bg-rose-600 ring-4 ring-rose-400 scale-125 shadow-md animate-pulse"
                        : "w-3 h-3 rounded-full bg-rose-600 ring-2 ring-white shadow hover:scale-125"
                      : isMarkerActive
                      ? "w-3 h-3 rounded-full bg-amber-400 ring-4 ring-amber-300 scale-125 shadow-md"
                      : "w-2.5 h-2.5 rounded-full bg-amber-300 ring-1 ring-amber-500 hover:scale-125"
                  }`}
                />
                <div
                  className={`w-0.5 h-full ${
                    isSampleDetected ? "bg-rose-500/80" : "bg-amber-400/80"
                  }`}
                />
              </button>
            );
          })}

          {/* Render Uncurated Sample Detected Variants Pins */}
          {uncuratedVariants.map((v) => {
            const pos = v.ref_position_mrna;
            if (pos <= 0 || pos > totalLength) return null;
            const leftPct = (pos / totalLength) * 100;
            const isActive = activeDetectedVariant?.id === v.id;

            return (
              <button
                key={v.id}
                type="button"
                onClick={() => onSelectVariant && onSelectVariant(v.id)}
                style={{ left: `${leftPct}%` }}
                className="absolute top-0 bottom-0 -ml-1.5 w-3 z-20 flex flex-col items-center justify-between group cursor-pointer focus:outline-none"
                title={`Detected Variant in Sample: ${v.hgvs_c}`}
              >
                <div
                  className={`transition-all rounded-full bg-rose-600 shadow ${
                    isActive
                      ? "w-3.5 h-3.5 ring-4 ring-rose-400 scale-125 animate-pulse"
                      : "w-3 h-3 ring-2 ring-white hover:scale-125"
                  }`}
                />
                <div className="w-0.5 h-full bg-rose-600" />
              </button>
            );
          })}
        </div>

        {/* Track Legend & Intronic Notice */}
        <div className="flex flex-wrap items-center justify-between gap-3 text-[11px] font-mono text-stone-600 pt-1">
          <div className="flex flex-wrap items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-3 bg-blue-600 rounded-xs inline-block" />
              Coding Exon
            </span>
            {isGenomic && (
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 bg-stone-200 border border-stone-300 rounded-xs inline-block" />
                Intron (IVS)
              </span>
            )}
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-amber-400 rounded-full inline-block" />
              Curated Mutation Loci
            </span>
            {detectedVariants.length > 0 && (
              <span className="flex items-center gap-1.5 text-rose-700 font-semibold">
                <span className="w-2.5 h-2.5 bg-rose-600 ring-1 ring-rose-400 rounded-full inline-block" />
                Sample Variant Match (Active)
              </span>
            )}
          </div>

          {!isGenomic && (
            <button
              type="button"
              onClick={() => setViewMode("genomic")}
              className="text-blue-700 hover:text-blue-900 underline flex items-center gap-1"
            >
              <span>Intronic mutations (e.g., IVS1-5) viewable in Genomic View</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          )}
        </div>
      </div>

      {/* Selected Mutation Inspector Card */}
      {selectedMutation && (
        <div className="bg-stone-50 border border-stone-200 rounded-lg p-4 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-stone-200/80 pb-2">
            <div className="flex items-center gap-2">
              <MapPin
                className={`w-4 h-4 shrink-0 ${
                  sampleMatchForSelected ? "text-rose-600" : "text-amber-600"
                }`}
              />
              <h4 className="font-serif text-sm font-bold text-stone-900">
                {selectedMutation.name}
              </h4>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-200 font-semibold">
                {selectedMutation.region}
              </span>
              {sampleMatchForSelected ? (
                <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold">
                  <CheckCircle className="w-3 h-3 text-emerald-700" />
                  ACTIVE IN CURRENT SAMPLE
                </span>
              ) : (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-stone-100 text-stone-600 border border-stone-200">
                  REFERENCE LOCUS
                </span>
              )}
            </div>

            <div className="flex items-center gap-2 text-xs font-mono">
              {selectedMutation.clinvar_id ? (
                <a
                  href={`https://www.ncbi.nlm.nih.gov/clinvar/variation/${selectedMutation.clinvar_id}/`}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-700 hover:text-blue-900 inline-flex items-center gap-1"
                >
                  <span>ClinVar ID: {selectedMutation.clinvar_id}</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              ) : sampleMatchForSelected ? (
                <span className="text-stone-500">Sample Call: {sampleMatchForSelected.hgvs_c}</span>
              ) : null}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
            <div>
              <span className="text-stone-400 text-[10px] block uppercase">Mutation Type</span>
              <strong className="text-stone-800">{selectedMutation.type}</strong>
            </div>
            <div>
              <span className="text-stone-400 text-[10px] block uppercase">Consequence</span>
              <strong className="text-stone-800">{selectedMutation.consequence}</strong>
            </div>
            <div>
              <span className="text-stone-400 text-[10px] block uppercase">Genomic Position</span>
              <strong className="text-stone-800">
                {selectedMutation.genomic_abs_bp > 0
                  ? `NG_000007.3:g.${selectedMutation.genomic_abs_bp}`
                  : `Relative ${selectedMutation.genomic_rel_bp} bp`}
              </strong>
            </div>
            <div>
              <span className="text-stone-400 text-[10px] block uppercase">cDNA Position</span>
              <strong className="text-stone-800">
                {selectedMutation.isIntronicOnly
                  ? "c.92+5 (Intron 1)"
                  : `c.${selectedMutation.c_pos}`}
              </strong>
            </div>
          </div>

          {/* Action buttons */}
          <div className="pt-2 flex flex-wrap items-center justify-between gap-2 border-t border-stone-200/60">
            {sampleMatchForSelected ? (
              <div className="text-xs font-mono text-emerald-800">
                <span>Observed in sample: </span>
                <strong>{sampleMatchForSelected.hgvs_c}</strong>
                {sampleMatchForSelected.hgvs_p && (
                  <span className="ml-1 font-semibold">({sampleMatchForSelected.hgvs_p})</span>
                )}
              </div>
            ) : onSelectMutationPreset ? (
              <div className="text-xs text-stone-500 font-sans italic">
                Locus not present in currently analyzed sample.
              </div>
            ) : <div />}

            {!sampleMatchForSelected && onSelectMutationPreset && (
              <button
                type="button"
                onClick={() => onSelectMutationPreset(selectedMutation.id)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-stone-800 bg-white hover:bg-stone-100 border border-stone-300 rounded shadow-xs"
              >
                <span>Load this mutation into Analyzer</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
