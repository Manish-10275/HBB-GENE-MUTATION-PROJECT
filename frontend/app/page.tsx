"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { SafetyBanner } from "../components/SafetyBanner";
import { SequenceWorkspace } from "../components/SequenceWorkspace";
import { CodonVisualizer } from "../components/CodonVisualizer";
import { AlignmentViewer } from "../components/AlignmentViewer";
import { VariantsTable } from "../components/VariantsTable";
import { EvidenceWorkspace } from "../components/EvidenceWorkspace";
import { ResearchCopilot } from "../components/ResearchCopilot";
import { DirectVariantSearch } from "../components/DirectVariantSearch";
import { ReportModal } from "../components/ReportModal";
import {
  analyzeSequence,
  fetchExamples,
  fetchReference,
  generateReport,
} from "../lib/api";
import {
  AnalyzeResponse,
  ExampleSequence,
  ReportResponse,
  DetectedVariant,
} from "../lib/types";
import { Dna, Activity, ShieldCheck, Database, Layers } from "lucide-react";

export default function Home() {
  const [sequence, setSequence] = useState("");
  const [examples, setExamples] = useState<ExampleSequence[]>([]);
  const [referenceMeta, setReferenceMeta] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalyzeResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // Modals & Panels
  const [isDirectSearchOpen, setIsDirectSearchOpen] = useState(false);
  const [isReportOpen, setIsReportOpen] = useState(false);
  const [generatedReport, setGeneratedReport] = useState<ReportResponse | null>(null);
  const [copilotSummaryText, setCopilotSummaryText] = useState<string>("");

  // Load initial reference data and example sequences on mount
  useEffect(() => {
    async function loadInitialData() {
      try {
        const [refData, exData] = await Promise.all([
          fetchReference().catch(() => null),
          fetchExamples().catch(() => []),
        ]);
        if (refData) setReferenceMeta(refData);
        if (exData && exData.length > 0) {
          setExamples(exData);
          // Pre-populate with the controlled validation case
          const valCase = exData.find((e: ExampleSequence) => e.is_validation_case);
          if (valCase) {
            setSequence(valCase.sequence);
          } else {
            setSequence(exData[0].sequence);
          }
        }
      } catch (e) {
        console.error("Initialization error:", e);
      }
    }
    loadInitialData();
  }, []);

  const handleRunAnalysis = async () => {
    if (!sequence.trim()) return;

    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      const result = await analyzeSequence(sequence);
      setAnalysisResult(result);
    } catch (err: any) {
      setAnalysisError(err.message || "Sequence analysis encountered an error.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleOpenReport = async () => {
    if (!analysisResult?.evidence_packet) return;

    try {
      const rep = await generateReport(
        analysisResult.evidence_packet,
        copilotSummaryText || undefined
      );
      setGeneratedReport(rep);
      setIsReportOpen(true);
    } catch (err) {
      console.error("Failed to generate report:", err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans">
      <Header
        hasAnalysis={Boolean(analysisResult?.evidence_packet)}
        onOpenReport={handleOpenReport}
        onOpenDirectSearch={() => setIsDirectSearchOpen(true)}
      />

      <SafetyBanner />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Editorial Subheader & Reference Strip */}
        <section className="bg-white border border-stone-200 rounded-lg p-6 shadow-sm">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div>
              <div className="flex items-center space-x-2 text-xs font-mono uppercase tracking-wider text-stone-500 mb-1">
                <span>Human Hemoglobin Subunit Beta</span>
                <span>&bull;</span>
                <span className="text-emerald-700 font-semibold">CCDS7753.1</span>
              </div>
              <h1 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight text-stone-900">
                HBB Mutation Analyzer
              </h1>
              <p className="text-sm text-stone-600 mt-1.5 max-w-2xl font-sans">
                A serious genomic research and educational environment. Deterministically detects nucleotide
                substitutions, computes codon and amino acid consequences, retrieves NCBI evidence, and coordinates
                grounded AI research synthesis.
              </p>
            </div>

            {/* Reference Coordinate Badge Box */}
            <div className="bg-stone-50 border border-stone-200/90 rounded-md p-4 min-w-[280px]">
              <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block mb-2 font-semibold">
                CANONICAL REFERENCE TARGET
              </span>
              <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-xs font-mono">
                <div>
                  <span className="text-stone-400 block text-[10px]">Accession</span>
                  <strong className="text-stone-900">NM_000518.5</strong>
                </div>
                <div>
                  <span className="text-stone-400 block text-[10px]">Total Length</span>
                  <strong className="text-stone-900">628 bp</strong>
                </div>
                <div>
                  <span className="text-stone-400 block text-[10px]">Coding Region (CDS)</span>
                  <strong className="text-stone-900">51..494 bp</strong>
                </div>
                <div>
                  <span className="text-stone-400 block text-[10px]">Protein Product</span>
                  <strong className="text-stone-900">NP_000509.1 (147 aa)</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 1. Sequence Input Workspace */}
        <section>
          <SequenceWorkspace
            sequence={sequence}
            onChangeSequence={setSequence}
            onAnalyze={handleRunAnalysis}
            isLoading={isAnalyzing}
            examples={examples}
            error={analysisError}
          />
        </section>

        {/* Analysis Results View */}
        {analysisResult && (
          <div className="space-y-8 animate-fadeIn">
            {/* Overview Metrics Cards */}
            <section className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-white border border-stone-200 rounded-lg p-4 shadow-2xs">
                <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                  Sequence Identity
                </span>
                <div className="mt-1 flex items-baseline space-x-1">
                  <span className="text-2xl font-bold font-mono text-stone-900">
                    {analysisResult.summary.sequence_identity_pct ?? "N/A"}%
                  </span>
                </div>
                <span className="text-[11px] text-stone-500 font-sans mt-0.5 block">
                  Relative to NM_000518.5
                </span>
              </div>

              <div className="bg-white border border-stone-200 rounded-lg p-4 shadow-2xs">
                <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                  Sample Query Length
                </span>
                <div className="mt-1 flex items-baseline space-x-1">
                  <span className="text-2xl font-bold font-mono text-stone-900">
                    {analysisResult.summary.sample_length_bp ?? sequence.length}
                  </span>
                  <span className="text-xs text-stone-400 font-mono">bp</span>
                </div>
                <span className="text-[11px] text-stone-500 font-sans mt-0.5 block">
                  Reference: 628 bp
                </span>
              </div>

              <div className="bg-white border border-stone-200 rounded-lg p-4 shadow-2xs">
                <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                  Detected Variants
                </span>
                <div className="mt-1 flex items-baseline space-x-1">
                  <span className="text-2xl font-bold font-mono text-rose-700">
                    {analysisResult.variants.length}
                  </span>
                </div>
                <span className="text-[11px] text-stone-500 font-sans mt-0.5 block">
                  Deterministic nucleotide shifts
                </span>
              </div>

              <div className="bg-white border border-stone-200 rounded-lg p-4 shadow-2xs">
                <span className="text-[10px] uppercase font-mono tracking-wider text-stone-400 block">
                  Retrieved Evidence
                </span>
                <div className="mt-1 flex items-baseline space-x-2">
                  <span className="text-2xl font-bold font-mono text-blue-700">
                    {analysisResult.evidence_packet?.clinvar_records.length ?? 0}
                  </span>
                  <span className="text-xs text-stone-400 font-sans">ClinVar</span>
                  <span className="text-2xl font-bold font-mono text-emerald-700 ml-2">
                    {analysisResult.evidence_packet?.pubmed_records.length ?? 0}
                  </span>
                  <span className="text-xs text-stone-400 font-sans">PubMed</span>
                </div>
                <span className="text-[11px] text-stone-500 font-sans mt-0.5 block">
                  NCBI external scientific records
                </span>
              </div>
            </section>

            {/* 2. Detected Variants Table */}
            <section>
              <VariantsTable variants={analysisResult.variants} />
            </section>

            {/* 3. Codon & Protein Consequence Visualizer (Feature Highlight) */}
            <section>
              <CodonVisualizer variants={analysisResult.variants} />
            </section>

            {/* 4. Monospace Alignment Viewer */}
            {analysisResult.alignment && (
              <section>
                <AlignmentViewer alignment={analysisResult.alignment} />
              </section>
            )}

            {/* 5. External Scientific Evidence (ClinVar & PubMed) */}
            {analysisResult.evidence_packet && (
              <section>
                <EvidenceWorkspace
                  clinvarRecords={analysisResult.evidence_packet.clinvar_records}
                  pubmedRecords={analysisResult.evidence_packet.pubmed_records}
                  limitations={analysisResult.evidence_packet.limitations}
                />
              </section>
            )}

            {/* 6. AI Research Copilot */}
            <section>
              <ResearchCopilot
                evidencePacket={analysisResult.evidence_packet || null}
                onUpdateCopilotSummary={setCopilotSummaryText}
              />
            </section>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-stone-200 bg-white py-6 mt-12 text-center text-xs text-stone-500 font-sans">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p className="font-semibold text-stone-700">
            HBB Mutation Analyzer &bull; Understand the sequence. Follow the evidence.
          </p>
          <p>
            NCBI RefSeq NM_000518.5 (GeneID: 3043, CCDS7753.1). Strictly for academic and research evaluation.
          </p>
        </div>
      </footer>

      {/* Direct Variant Investigation Modal */}
      <DirectVariantSearch
        isOpen={isDirectSearchOpen}
        onClose={() => setIsDirectSearchOpen(false)}
      />

      {/* Exportable Research Report Modal */}
      <ReportModal
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        report={generatedReport}
      />
    </div>
  );
}
