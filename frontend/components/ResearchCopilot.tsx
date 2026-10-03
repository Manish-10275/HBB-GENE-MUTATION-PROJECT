"use client";

import React, { useState, useEffect, useMemo } from "react";
import { Send, Loader2, Database, BookOpen, Dna, HelpCircle } from "lucide-react";
import { askCopilot } from "../lib/api";
import { CopilotChatMessage, EvidencePacket } from "../lib/types";

interface ResearchCopilotProps {
  evidencePacket: EvidencePacket | null;
  onUpdateCopilotSummary?: (summary: string) => void;
}

export const ResearchCopilot: React.FC<ResearchCopilotProps> = ({
  evidencePacket,
  onUpdateCopilotSummary,
}) => {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<CopilotChatMessage[]>([]);
  const [lastEvidenceUsed, setLastEvidenceUsed] = useState<string[]>([
    "Sequence analysis (Deterministic Engine)",
  ]);

  // Contextual suggested questions based on detected variants
  const contextualData = useMemo(() => {
    if (!evidencePacket) {
      return {
        welcomeMessage:
          "Run sequence analysis above to initialize the evidence packet and enable contextual synthesis.",
        questions: [
          "What is the structure of the human HBB gene in NM_000518.5?",
          "How are globin codon consequences calculated?",
        ],
      };
    }

    const variants = evidencePacket.variants;
    if (variants.length === 0) {
      return {
        welcomeMessage:
          "Analysis identified **100% sequence identity** to reference `NM_000518.5` (628 bp) with zero sequence variants. The wild-type beta-globin reading frame is intact.",
        questions: [
          "What is the canonical function of HBB beta-globin in adult hemoglobin (HbA)?",
          "What are the CDS boundaries and exon structure of NM_000518.5?",
          "What types of mutations in HBB cause beta-thalassemia?",
        ],
      };
    }

    const v = variants[0];
    const c = v.codon_change;
    const clinvarCount = evidencePacket.clinvar_records.length;
    const pubmedCount = evidencePacket.pubmed_records.length;

    let welcome = `Analysis of **${v.hgvs_c}**`;
    if (v.hgvs_p) welcome += ` (${v.hgvs_p})`;
    welcome += ` identified a **${v.functional_impact.toLowerCase()}** substitution`;
    if (c) {
      welcome += ` at codon ${c.codon_number} (${c.ref_codon} [${c.ref_aa}] → ${c.sample_codon} [${c.sample_aa}])`;
    }
    welcome += `. NCBI retrieved **${clinvarCount} ClinVar record${clinvarCount === 1 ? "" : "s"}** and **${pubmedCount} PubMed paper${pubmedCount === 1 ? "" : "s"}**.`;

    const qs: string[] = [];
    if (c?.is_stop_gain) {
      qs.push(`Why does ${c.ref_codon} → ${c.sample_codon} produce a premature termination codon (PTC)?`);
      qs.push(`What does NCBI ClinVar report regarding pathogenicity for ${v.hgvs_c}?`);
      qs.push(`What evidence was retrieved from PubMed for this codon ${c.codon_number} nonsense variant?`);
      qs.push(`How does premature termination at residue ${c.codon_number} disrupt beta-globin synthesis?`);
    } else if (c) {
      qs.push(`What molecular effect does the ${c.ref_aa} → ${c.sample_aa} change have on hemoglobin?`);
      qs.push(`What clinical significance does ClinVar report for ${v.hgvs_c}?`);
      qs.push(`Which primary literature citations were retrieved from PubMed?`);
    } else {
      qs.push(`What regulatory impact can variants in the untranslated region have on HBB expression?`);
      qs.push(`What evidence was retrieved for ${v.hgvs_c}?`);
    }

    return {
      welcomeMessage: welcome,
      questions: qs,
    };
  }, [evidencePacket]);

  // Set contextual welcome message when evidence packet changes
  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        content: contextualData.welcomeMessage,
      },
    ]);
  }, [contextualData.welcomeMessage]);

  const handleSend = async (queryText?: string) => {
    const q = (queryText || question).trim();
    if (!q || !evidencePacket || loading) return;

    const userMsg: CopilotChatMessage = { role: "user", content: q };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setQuestion("");
    setLoading(true);

    try {
      const res = await askCopilot(q, evidencePacket, updatedMessages);
      const assistantMsg: CopilotChatMessage = {
        role: "assistant",
        content: res.answer,
      };
      setMessages([...updatedMessages, assistantMsg]);
      setLastEvidenceUsed(res.evidence_used || []);
      if (onUpdateCopilotSummary) {
        onUpdateCopilotSummary(res.answer);
      }
    } catch (err: any) {
      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content: `**Error communicating with synthesis engine:** ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-stone-200 rounded-lg overflow-hidden flex flex-col h-[560px]">
      {/* Header Strip */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] uppercase font-mono tracking-wider bg-stone-900 text-white px-2 py-0.5 rounded font-semibold">
              AI SYNTHESIS
            </span>
            <h3 className="font-serif text-sm font-semibold text-stone-900">
              Research Copilot
            </h3>
          </div>
          <p className="text-xs text-stone-500 font-sans">
            Evidence grounded synthesis &bull; Derived strictly from the deterministic analysis and NCBI database records
          </p>
        </div>
      </div>

      {/* Provenance Separation Strip */}
      <div className="px-5 py-2 bg-stone-50/90 border-b border-stone-200 text-[11px] flex flex-wrap items-center justify-between gap-2">
        <span className="text-stone-500 font-mono">Evidence inputs bounded to this query:</span>
        <div className="flex items-center gap-1.5 flex-wrap">
          {lastEvidenceUsed.map((source, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 bg-white border border-stone-200 px-2 py-0.5 rounded text-stone-700 font-mono text-[10px]"
            >
              {source.includes("Sequence") ? (
                <Dna className="w-3 h-3 text-stone-500" />
              ) : source.includes("ClinVar") ? (
                <Database className="w-3 h-3 text-blue-500" />
              ) : (
                <BookOpen className="w-3 h-3 text-emerald-500" />
              )}
              {source}
            </span>
          ))}
        </div>
      </div>

      {/* Messages Thread */}
      <div className="flex-1 p-5 overflow-y-auto space-y-4 custom-scrollbar text-xs leading-relaxed bg-[#fbfbfa]">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[88%] rounded-lg p-3.5 border ${
                m.role === "user"
                  ? "bg-stone-900 text-white border-stone-900"
                  : "bg-white text-stone-800 border-stone-200"
              }`}
            >
              <div className="font-sans whitespace-pre-wrap leading-relaxed space-y-2">
                {m.content}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-stone-200 rounded p-3 text-stone-500 flex items-center space-x-2 text-xs">
              <Loader2 className="w-4 h-4 animate-spin text-stone-700" />
              <span>Consulting evidence packet and synthesizing response...</span>
            </div>
          </div>
        )}
      </div>

      {/* Contextual Suggested Questions Strip */}
      <div className="px-4 py-2 border-t border-stone-100 bg-stone-50/70 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
        <HelpCircle className="w-3.5 h-3.5 text-stone-400 shrink-0" />
        <span className="text-[10px] uppercase font-mono text-stone-400 shrink-0">Inquiries:</span>
        {contextualData.questions.map((sq, i) => (
          <button
            key={i}
            onClick={() => handleSend(sq)}
            disabled={loading || !evidencePacket}
            className="text-[11px] whitespace-nowrap bg-white hover:bg-stone-100 border border-stone-200 rounded px-2.5 py-1 text-stone-700 transition-colors shrink-0 disabled:opacity-50"
          >
            {sq}
          </button>
        ))}
      </div>

      {/* Form Input */}
      <div className="p-3 border-t border-stone-200 bg-white">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading || !evidencePacket}
            placeholder={
              evidencePacket
                ? "Ask a question regarding the variant, codon change, or retrieved evidence..."
                : "Run sequence analysis first to provide evidence context."
            }
            className="flex-1 text-xs bg-stone-50 border border-stone-200 rounded px-3.5 py-2 text-stone-900 focus:outline-none focus:ring-1 focus:ring-stone-400 disabled:bg-stone-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={loading || !question.trim() || !evidencePacket}
            className="inline-flex items-center justify-center p-2 rounded bg-stone-900 text-white hover:bg-stone-800 disabled:bg-stone-200 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
