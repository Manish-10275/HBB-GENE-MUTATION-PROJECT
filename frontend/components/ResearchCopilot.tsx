"use client";

import React, { useState } from "react";
import { Sparkles, Send, Loader2, ShieldCheck, Database, BookOpen, Dna, Info } from "lucide-react";
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
  const [messages, setMessages] = useState<CopilotChatMessage[]>([
    {
      role: "assistant",
      content:
        "Welcome to the **HBB Research Copilot**. I synthesize evidence strictly from the computed sequence alignment, codon transformation, and retrieved NCBI ClinVar & PubMed database records. Ask a question below or choose a suggested research inquiry.",
    },
  ]);
  const [lastEvidenceUsed, setLastEvidenceUsed] = useState<string[]>([
    "Sequence analysis (Deterministic Engine)",
  ]);

  const suggestedQuestions = [
    "Why does this nucleotide change produce a premature stop codon?",
    "What is the exact protein consequence and codon change?",
    "What does the ClinVar record report for this variant?",
    "Which publications were retrieved from PubMed?",
    "How does this variant affect beta-globin synthesis?",
  ];

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
    <div className="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden flex flex-col h-[580px]">
      {/* Header */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-emerald-700" />
            <h3 className="font-serif text-sm font-semibold text-stone-900">
              Research Copilot
            </h3>
            <span className="text-[10px] uppercase font-mono bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.2 rounded font-semibold">
              AI SYNTHESIS
            </span>
          </div>
          <p className="text-xs text-stone-500 font-sans">
            Evidence grounded synthesis &bull; Strictly bounded by deterministic analysis and NCBI databases
          </p>
        </div>
      </div>

      {/* Provenance Banner */}
      <div className="px-5 py-2 bg-stone-50 border-b border-stone-200 text-[11px] flex flex-wrap items-center justify-between gap-2">
        <span className="text-stone-500 font-mono">Evidence utilized:</span>
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

      {/* Messages Container */}
      <div className="flex-1 p-5 overflow-y-auto space-y-4 custom-scrollbar text-xs leading-relaxed bg-[#fbfbfa]">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-lg p-3.5 border shadow-2xs ${
                m.role === "user"
                  ? "bg-stone-900 text-white border-stone-900 rounded-br-xs"
                  : "bg-white text-stone-800 border-stone-200 rounded-bl-xs"
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
            <div className="bg-white border border-stone-200 rounded-lg p-3.5 text-stone-500 flex items-center space-x-2 text-xs">
              <Loader2 className="w-4 h-4 animate-spin text-emerald-600" />
              <span>Consulting evidence packet and synthesizing response...</span>
            </div>
          </div>
        )}
      </div>

      {/* Suggested Questions */}
      <div className="px-4 py-2 border-t border-stone-100 bg-stone-50/50 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
        <span className="text-[10px] uppercase font-mono text-stone-400 shrink-0">Inquiries:</span>
        {suggestedQuestions.map((sq, i) => (
          <button
            key={i}
            onClick={() => handleSend(sq)}
            disabled={loading || !evidencePacket}
            className="text-[11px] whitespace-nowrap bg-white hover:bg-stone-100 border border-stone-200 rounded px-2.5 py-1 text-stone-600 transition-colors shrink-0 disabled:opacity-50"
          >
            {sq}
          </button>
        ))}
      </div>

      {/* Input Form */}
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
                ? "Ask a question about the variant, codon change, or literature..."
                : "Run sequence analysis first to provide evidence context."
            }
            className="flex-1 text-xs bg-stone-50 border border-stone-200 rounded-md px-3.5 py-2 text-stone-900 focus:outline-none focus:ring-2 focus:ring-stone-400 disabled:bg-stone-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={loading || !question.trim() || !evidencePacket}
            className="inline-flex items-center justify-center p-2 rounded-md bg-stone-900 text-white hover:bg-stone-800 disabled:bg-stone-200 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
