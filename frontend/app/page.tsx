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
    <div className="min-h-screen flex flex-col font-sans bg-[#fbfbfa]">
      <Header
        hasAnalysis={Boolean(analysisResult?.evidence_packet)}
        onOpenReport={handleOpenReport}
        onOpenDirectSearch={() => setIsDirectSearchOpen(true)}
      />

      <SafetyBanner />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-7">
        {/* Editorial Subheader & Reference Strip */}
        <section className="bg-white border border-stone-200 rounded-lg p-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center space-x-2 text-xs font-mono uppercase tracking-wider text-stone-500 mb-1">
                <span>Homo sapiens HBB</span>
                <span>&bull;</span>
                <span className="text-stone-700 font-semibold">RefSeq MANE Select</span>
                <span>&bull;</span>
                <span className="text-emerald-700 font-semibold">CCDS7753.1</span>
              </div>
              <h1 className="font-serif text-2xl font-semibold tracking-tight text-stone-900">
                HBB Mutation Analyzer
              </h1>
              <p className="text-xs text-stone-600 mt-1 max-w-3xl font-sans">
                A serious genomic research environment for deterministic variant calling, codon transformation analysis, external NCBI database annotations, and evidence-grounded research synthesis.
              </p>
            </div>

            {/* Reference Coordinate Badge Strip */}
            <div className="bg-stone-50 border border-stone-200 rounded p-3 text-xs font-mono flex flex-wrap items-center gap-x-5 gap-y-1 shrink-0">
              <div>
                <span className="text-stone-400 text-[10px] block">Target</span>
                <strong className="text-stone-900">NM_000518.5</strong>
              </div>
              <div>
                <span className="text-stone-400 text-[10px] block">Length</span>
                <strong className="text-stone-900">628 bp</strong>
              </div>
              <div>
                <span className="text-stone-400 text-[10px] block">CDS Span</span>
                <strong className="text-stone-900">51..494 bp</strong>
              </div>
              <div>
                <span className="text-stone-400 text-[10px] block">Protein</span>
                <strong className="text-stone-900">NP_000509.1 (147 aa)</strong>
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
          <div className="space-y-7">
            {/* 2. Overview Metrics Strip (Crisp horizontal summary, avoiding excessive cards) */}
            <section className="bg-white border border-stone-200 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
              <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
                <div>
                  <span className="text-stone-400 text-[10px] uppercase block">Sequence Identity</span>
                  <strong className="text-sm text-stone-900">
                    {analysisResult.summary.sequence_identity_pct ?? "N/A"}%
                  </strong>
                </div>
                <div>
                  <span className="text-stone-400 text-[10px] uppercase block">Sample Length</span>
                  <strong className="text-sm text-stone-900">
                    {analysisResult.summary.sample_length_bp ?? sequence.length} bp
                  </strong>
                </div>
                <div>
                  <span className="text-stone-400 text-[10px] uppercase block">Alignment Score</span>
                  <strong className="text-sm text-stone-900">
                    {analysisResult.summary.alignment_score ?? "N/A"}
                  </strong>
                </div>
                <div>
                  <span className="text-stone-400 text-[10px] uppercase block">Detected Variants</span>
                  <strong className="text-sm text-rose-700">
                    {analysisResult.variants.length}
                  </strong>
                </div>
              </div>

              <div className="flex items-center gap-3 text-stone-600 border-t sm:border-t-0 sm:border-l border-stone-200 pt-2 sm:pt-0 sm:pl-4">
                <span className="text-stone-400 text-[10px] uppercase block">NCBI Evidence:</span>
                <span className="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded text-[11px] font-semibold">
                  ClinVar: {analysisResult.evidence_packet?.clinvar_records.length ?? 0}
                </span>
                <span className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-semibold">
                  PubMed: {analysisResult.evidence_packet?.pubmed_records.length ?? 0}
                </span>
              </div>
            </section>

            {/* 3. Detected Variant Summary (Immediately Visible) */}
            <section>
              <VariantsTable variants={analysisResult.variants} />
            </section>

            {/* 4. PRIMARY VISUAL INSIGHT: Codon Transformation & Protein Consequence */}
            <section>
              <CodonVisualizer variants={analysisResult.variants} />
            </section>

            {/* 5. Collapsible Pairwise Alignment */}
            {analysisResult.alignment && (
              <section>
                <AlignmentViewer alignment={analysisResult.alignment} defaultExpanded={false} />
              </section>
            )}

            {/* 6. External Scientific Evidence Layer (Collapsible ClinVar & PubMed with Summaries) */}
            {analysisResult.evidence_packet && (
              <section>
                <EvidenceWorkspace
                  clinvarRecords={analysisResult.evidence_packet.clinvar_records}
                  pubmedRecords={analysisResult.evidence_packet.pubmed_records}
                  limitations={analysisResult.evidence_packet.limitations}
                />
              </section>
            )}

            {/* 7. AI Research Copilot (Kept at the end of the workflow) */}
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
            NCBI RefSeq NM_000518.5 (GeneID: 3043, CCDS7753.1). Strictly for academic and educational evaluation.
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
