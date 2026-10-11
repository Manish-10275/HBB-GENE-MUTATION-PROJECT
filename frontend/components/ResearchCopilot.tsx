"use client";

import React, { useState, useEffect, useMemo } from "react";
import { Send, Loader2, Database, BookOpen, Dna, HelpCircle, Cpu, AlertCircle, CheckCircle2 } from "lucide-react";
import { askCopilot, fetchHealth, synthesizeCopilotV2 } from "../lib/api";
import { AiSynthesisStatus, CopilotChatMessage, CopilotResponse, CopilotResponseDTO, EvidencePacket } from "../lib/types";

interface ResearchCopilotProps {
  evidencePacket: EvidencePacket | null;
  onUpdateCopilotSummary?: (summary: string) => void;
  initialAiSummary?: AiSynthesisStatus | null;
}

export const ResearchCopilot: React.FC<ResearchCopilotProps> = ({
  evidencePacket,
  onUpdateCopilotSummary,
  initialAiSummary,
}) => {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<CopilotChatMessage[]>([]);
  const [copilotStatus, setCopilotStatus] = useState<"idle" | "no_key" | "success" | "error">("idle");
  const [isFallback, setIsFallback] = useState<boolean>(false);
  const [isGroqConfigured, setIsGroqConfigured] = useState<boolean | null>(null);
  const [groqModel, setGroqModel] = useState<string>("openai/gpt-oss-120b");
  const [lastEvidenceUsed, setLastEvidenceUsed] = useState<string[]>([
    "Deterministic Sequence Engine",
  ]);

  // Check backend Groq configuration state on mount
  useEffect(() => {
    fetchHealth()
      .then((h) => {
        const configured = !!h.groq_configured;
        setIsGroqConfigured(configured);
        if (h.groq_model) setGroqModel(h.groq_model);
        if (!configured) {
          setCopilotStatus("no_key");
          setIsFallback(true);
        } else {
          setCopilotStatus("idle");
        }
      })
      .catch((err) => {
        console.warn("Backend health check pending or offline:", err);
      });
  }, []);

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
    welcome += ` Select an inquiry below or type a custom question grounded in the retrieved evidence.`;

    const qs: string[] = [];
    if (c?.is_stop_gain) {
      qs.push(`Why does ${c.ref_codon} → ${c.sample_codon} produce a premature termination codon?`);
      qs.push(`What does ${v.hgvs_p || "p.Gln40Ter"} mean?`);
      qs.push(`What does the retrieved ClinVar evidence report for this variant?`);
      qs.push(`What evidence was retrieved from PubMed about this variant?`);
      qs.push(`What does the retrieved evidence say about the effect of ${v.hgvs_p || "p.Gln40Ter"} on beta globin?`);
    } else if (c) {
      qs.push(`Why does ${c.ref_codon} → ${c.sample_codon} result in ${c.ref_aa} → ${c.sample_aa}?`);
      qs.push(`What does ${v.hgvs_p || v.hgvs_c} mean?`);
      qs.push(`What does the retrieved ClinVar evidence report for this variant?`);
      qs.push(`What evidence was retrieved from PubMed about this variant?`);
      qs.push(`What does the retrieved evidence say about the effect of ${v.hgvs_p || v.hgvs_c} on beta globin?`);
    } else {
      qs.push(`What genomic position does ${v.hgvs_c} affect relative to the coding sequence?`);
      qs.push(`What does the retrieved ClinVar evidence report for this variant?`);
      qs.push(`What evidence was retrieved from PubMed about this variant?`);
      qs.push(`What does the retrieved evidence say about the effect of ${v.hgvs_c}?`);
    }

    return {
      welcomeMessage: welcome,
      questions: qs,
    };
  }, [evidencePacket]);

  // Set contextual message or automated initial AI synthesis when evidence packet or AI status changes
  useEffect(() => {
    if (initialAiSummary?.answer) {
      setMessages([
        {
          role: "assistant",
          content: initialAiSummary.answer,
        },
      ]);
      if (initialAiSummary.status === "success") {
        setCopilotStatus("success");
        setIsGroqConfigured(true);
      } else if (initialAiSummary.status === "no_key") {
        setCopilotStatus("no_key");
        setIsGroqConfigured(false);
      } else {
        setCopilotStatus("error");
      }
      if (typeof initialAiSummary.fallback === "boolean") {
        setIsFallback(initialAiSummary.fallback);
      }
      if (initialAiSummary.evidence_used && initialAiSummary.evidence_used.length > 0) {
        setLastEvidenceUsed(initialAiSummary.evidence_used);
      }
      if (onUpdateCopilotSummary) {
        onUpdateCopilotSummary(initialAiSummary.answer);
      }
    } else {
      setMessages([
        {
          role: "assistant",
          content: contextualData.welcomeMessage,
        },
      ]);
    }
  }, [initialAiSummary, contextualData.welcomeMessage, onUpdateCopilotSummary]);

  const handleSend = async (queryText?: string) => {
    const q = (queryText || question).trim();
    if (!q || !evidencePacket || loading) return;

    const userMsg: CopilotChatMessage = { role: "user", content: q };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setQuestion("");
    setLoading(true);

    try {
      let res: CopilotResponse | CopilotResponseDTO;
      const primaryV = evidencePacket.variants[0];
      if (primaryV?.hgvs_c) {
        try {
          res = await synthesizeCopilotV2({
            query: primaryV.hgvs_c,
            question: q,
            include_evidence: true,
            include_literature: true,
          });
        } catch {
          res = await askCopilot(q, evidencePacket, updatedMessages);
        }
      } else {
        res = await askCopilot(q, evidencePacket, updatedMessages);
      }

      setCopilotStatus(res.status as any);
      setIsFallback(!!res.fallback);
      const assistantMsg: CopilotChatMessage = {
        role: "assistant",
        content: res.answer,
      };
      setMessages([...updatedMessages, assistantMsg]);
      setLastEvidenceUsed(res.evidence_used || []);
      if (onUpdateCopilotSummary) {
        onUpdateCopilotSummary(res.answer);
      }
    } catch (_err: any) {
      setCopilotStatus("idle");
      setIsFallback(true);
      const primaryV = evidencePacket.variants[0];
      const fallbackText = primaryV
        ? `## DIRECT SCIENTIFIC ANSWER\nDeterministic bioinformatics analysis confirms sequence coordinates and consequence for ${primaryV.hgvs_c}${primaryV.hgvs_p ? ` (${primaryV.hgvs_p})` : ""} in HBB (NM_000518.5).\n\n## A. COMPUTED FACTS\n• HGVS cDNA: ${primaryV.hgvs_c}\n• HGVS Protein: ${primaryV.hgvs_p || "None"}\n• Consequence: ${primaryV.functional_impact}\n\n## D. DETERMINISTIC SYNTHESIS\nDeterministic sequence calculations remain authoritative.`
        : "Deterministic bioinformatics analysis completed with 100% reference identity to NM_000518.5.";
      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content: fallbackText,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const isLiveAi = copilotStatus === "success" && !isFallback;

  const renderAssistantMessage = (content: string) => {
    // Strip notice banner blockquote if present in content
    const noticeRegex = /> \*\*Notice:[^\n]+(?:\n[^\n]+)*/g;
    const mainContent = content.replace(noticeRegex, "").trim();

    const headingRegex = /(?:^|\n)(#{1,4}\s+[^\n]+|(?:\*{2})?(?:DIRECT SCIENTIFIC ANSWER|A\.\s*COMPUTED FACTS|B\.\s*DATABASE EVIDENCE|C\.\s*ESTABLISHED BIOLOGICAL KNOWLEDGE|D\.\s*(?:AI|DETERMINISTIC)\s*SYNTHESIS|EVIDENCE LIMITATIONS)(?:\*{2})?\s*$)/gm;
    const splitPoints: { index: number; heading: string }[] = [];
    let match: RegExpExecArray | null;

    while ((match = headingRegex.exec(mainContent)) !== null) {
      splitPoints.push({
        index: match.index + (match[0].startsWith("\n") ? 1 : 0),
        heading: match[1].replace(/^[#\*\s]+|[#\*\s]+$/g, "").trim(),
      });
    }

    if (splitPoints.length === 0) {
      return (
        <div className="font-sans whitespace-pre-wrap leading-relaxed space-y-2">
          {mainContent}
        </div>
      );
    }

    // Capture preamble before first heading if any
    const firstIndex = splitPoints[0].index;
    const preamble = mainContent.substring(0, firstIndex).trim();

    // Group content by canonical category to guarantee EXACTLY ONE card per category
    interface ProvenanceSectionCategory {
      key: string;
      badgeLabel: string;
      badgeStyle: string;
      order: number;
    }

    const getCategory = (rawTitle: string): ProvenanceSectionCategory => {
      const t = rawTitle.toLowerCase().trim();

      if (t.includes("direct answer") || t.includes("direct scientific")) {
        return {
          key: "DIRECT_ANSWER",
          badgeLabel: "DIRECT SCIENTIFIC ANSWER",
          badgeStyle: "bg-stone-900 text-stone-100 border-stone-800",
          order: 1,
        };
      }
      if (t.includes("database") || t.includes("clinvar") || t.includes("pubmed") || t.includes("ncbi evidence")) {
        return {
          key: "DATABASE_EVIDENCE",
          badgeLabel: "B. DATABASE EVIDENCE",
          badgeStyle: "bg-blue-50 text-blue-800 border-blue-300",
          order: 3,
        };
      }
      if (t.includes("computed") || t.includes("sequence calculation") || t.includes("bioinformatics")) {
        return {
          key: "COMPUTED_FACTS",
          badgeLabel: "A. COMPUTED FACTS",
          badgeStyle: "bg-emerald-50 text-emerald-800 border-emerald-300",
          order: 2,
        };
      }
      if (t.includes("established") || t.includes("general biological") || t.includes("biological knowledge") || t.includes("biological context")) {
        return {
          key: "ESTABLISHED_KNOWLEDGE",
          badgeLabel: "C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
          badgeStyle: "bg-purple-50 text-purple-800 border-purple-300",
          order: 4,
        };
      }
      if (t.includes("synthesis") || t.includes("ai synthesis") || t.includes("grounded synthesis") || t.includes("deterministic")) {
        const isDeterministic = !isLiveAi || t.includes("deterministic");
        return {
          key: "SYNTHESIS_SECTION",
          badgeLabel: isDeterministic ? "D. DETERMINISTIC SYNTHESIS" : "D. AI SYNTHESIS",
          badgeStyle: isDeterministic ? "bg-stone-100 text-stone-800 border-stone-300" : "bg-stone-900 text-stone-100 border-stone-800",
          order: 5,
        };
      }
      if (t.includes("limitation") || t.includes("boundary") || t.includes("limit") || t.includes("constraints")) {
        return {
          key: "LIMITATIONS",
          badgeLabel: "EVIDENCE LIMITATIONS",
          badgeStyle: "bg-amber-50 text-amber-900 border-amber-300",
          order: 6,
        };
      }

      return {
        key: "SECTION_" + rawTitle.replace(/[^a-zA-Z0-9]/g, "_"),
        badgeLabel: rawTitle.toUpperCase(),
        badgeStyle: "bg-stone-100 text-stone-800 border-stone-300",
        order: 99,
      };
    };

    const categoryMap = new Map<
      string,
      {
        category: ProvenanceSectionCategory;
        bodies: string[];
      }
    >();

    for (let i = 0; i < splitPoints.length; i++) {
      const heading = splitPoints[i].heading;
      const startIndex = splitPoints[i].index;
      const headingLineEnd = mainContent.indexOf("\n", startIndex);
      const contentStart = headingLineEnd !== -1 ? headingLineEnd + 1 : mainContent.length;
      const contentEnd = i + 1 < splitPoints.length ? splitPoints[i + 1].index : mainContent.length;
      let body = mainContent.substring(contentStart, contentEnd).trim();

      // Strip redundant repetitive section titles from body
      body = body
        .replace(/(?:^|\n)\s*#{1,4}\s*(?:[A-D]\.?)?\s*(?:COMPUTED|DATABASE|ESTABLISHED|AI|DETERMINISTIC|LIMITATION|DIRECT)[^\n]*/gmi, "")
        .trim();

      const cat = getCategory(heading);

      if (!categoryMap.has(cat.key)) {
        categoryMap.set(cat.key, {
          category: cat,
          bodies: body ? [body] : [],
        });
      } else {
        if (body) {
          categoryMap.get(cat.key)!.bodies.push(body);
        }
      }
    }

    const sortedCategories = Array.from(categoryMap.values()).sort(
      (a, b) => a.category.order - b.category.order
    );

    return (
      <div className="font-sans space-y-3.5">
        {preamble && (
          <div className="whitespace-pre-wrap leading-relaxed text-stone-900 font-medium text-[12px] bg-stone-50/80 p-2.5 rounded border border-stone-200/80">
            {preamble}
          </div>
        )}

        {sortedCategories.map(({ category, bodies }, idx) => {
          const fullBody = bodies.join("\n\n").trim();
          if (!fullBody && bodies.length === 0) return null;

          return (
            <div
              key={category.key || idx}
              className="border-t border-stone-100 pt-2.5 first:border-t-0 first:pt-0"
            >
              <div className="flex items-center gap-1.5 mb-1.5">
                <span
                  className={`inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${category.badgeStyle}`}
                >
                  {category.badgeLabel}
                </span>
              </div>
              <div className="whitespace-pre-wrap leading-relaxed text-stone-800 pl-1 text-[11.5px]">
                {fullBody}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="bg-white border border-stone-200 rounded-lg overflow-hidden flex flex-col h-[560px]">
      {/* Header Strip */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] uppercase font-mono tracking-wider px-2 py-0.5 rounded font-semibold bg-stone-900 text-white">
              {isLiveAi ? "AI ENHANCED" : "DETERMINISTIC"}
            </span>
            <h3 className="font-serif text-sm font-semibold text-stone-900">
              Research Copilot
            </h3>
          </div>
          <p className="text-xs text-stone-500 font-sans mt-0.5">
            Evidence grounded synthesis &bull; Authoritative sequence analysis and retrieved NCBI records
          </p>
        </div>

        {/* Subtle Evidence Mode Indicator */}
        <div className="flex items-center">
          {isLiveAi ? (
            <div className="flex flex-col items-end">
              <span
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-[11px] font-mono font-medium bg-emerald-50 text-emerald-800 border border-emerald-300"
                title={`Live Groq model (${groqModel}) synthesis grounded in retrieved NCBI evidence.`}
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                Evidence Mode: AI Synthesized + Deterministic Evidence
              </span>
            </div>
          ) : (
            <div className="flex flex-col items-end">
              <span
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-[11px] font-mono font-medium bg-stone-100 text-stone-700 border border-stone-300"
                title="AI synthesis unavailable. Answer based on deterministic evidence."
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-stone-600" />
                Evidence Mode: Deterministic
              </span>
              <span
                className="text-[10px] text-stone-500 font-sans mt-0.5"
                title="AI synthesis unavailable. Answer based on deterministic evidence."
              >
                AI synthesis unavailable &bull; Answer based on deterministic evidence
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Provenance Separation Strip */}
      <div className="px-5 py-2 bg-stone-50/90 border-b border-stone-200 text-[11px] flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-stone-500 font-mono font-medium">Evidence Categories:</span>
          <span className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold">
            <Dna className="w-3 h-3 text-emerald-600" />
            A. COMPUTED FACTS
          </span>
          <span className="inline-flex items-center gap-1 bg-blue-50 text-blue-800 border border-blue-200 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold">
            <Database className="w-3 h-3 text-blue-600" />
            B. DATABASE EVIDENCE
          </span>
          <span className="inline-flex items-center gap-1 bg-purple-50 text-purple-800 border border-purple-200 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold">
            <BookOpen className="w-3 h-3 text-purple-600" />
            C. ESTABLISHED BIOLOGICAL KNOWLEDGE
          </span>
          <span className={`inline-flex items-center gap-1 border px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${
            isLiveAi
              ? "bg-stone-900 text-stone-100 border-stone-800"
              : "bg-stone-100 text-stone-800 border-stone-300"
          }`}>
            <Cpu className={`w-3 h-3 ${isLiveAi ? "text-stone-200" : "text-stone-600"}`} />
            {isLiveAi ? "D. AI SYNTHESIS" : "D. DETERMINISTIC SYNTHESIS"}
          </span>
          <span className="inline-flex items-center gap-1 bg-amber-50 text-amber-900 border border-amber-200 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold">
            <AlertCircle className="w-3 h-3 text-amber-600" />
            EVIDENCE LIMITATIONS
          </span>
        </div>
        <div className="flex items-center gap-1.5 flex-wrap">
          {lastEvidenceUsed.map((source, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 bg-white border border-stone-200 px-2 py-0.5 rounded text-stone-700 font-mono text-[10px]"
            >
              {source.includes("Deterministic") || source.includes("Sequence") ? (
                <Dna className="w-3 h-3 text-emerald-600" />
              ) : source.includes("ClinVar") ? (
                <Database className="w-3 h-3 text-blue-500" />
              ) : (
                <BookOpen className="w-3 h-3 text-sky-500" />
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
                  : "bg-white text-stone-800 border-stone-200 shadow-sm"
              }`}
            >
              {m.role === "user" ? (
                <div className="font-sans whitespace-pre-wrap leading-relaxed space-y-2">
                  {m.content}
                </div>
              ) : (
                renderAssistantMessage(m.content)
              )}
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
