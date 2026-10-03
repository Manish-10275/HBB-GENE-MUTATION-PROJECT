"use client";

import React, { useState } from "react";
import { AlignmentSummary } from "../lib/types";
import { SlidersHorizontal, Check } from "lucide-react";

interface AlignmentViewerProps {
  alignment: AlignmentSummary;
}

export const AlignmentViewer: React.FC<AlignmentViewerProps> = ({ alignment }) => {
  const [showOnlyVariants, setShowOnlyVariants] = useState(false);

  // Filter blocks that have mismatches or gaps if toggled
  const displayedBlocks = showOnlyVariants
    ? alignment.blocks.filter((b) => b.match_line.includes(".") || b.match_line.includes(" "))
    : alignment.blocks;

  return (
    <div className="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
      {/* Alignment Header */}
      <div className="px-5 py-3.5 border-b border-stone-200 bg-stone-50/70 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-serif text-sm font-semibold text-stone-900">
            Pairwise Global Alignment
          </h3>
          <p className="text-xs text-stone-500 font-sans">
            Coordinates reference NM_000518.5 (1..{alignment.ref_length} bp). Vertical bars (|) indicate identities; dots (.) indicate mismatches.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <label className="flex items-center space-x-2 text-xs text-stone-600 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={showOnlyVariants}
              onChange={(e) => setShowOnlyVariants(e.target.checked)}
              className="rounded border-stone-300 text-stone-900 focus:ring-stone-500"
            />
            <span>Filter to mutated blocks only</span>
          </label>
        </div>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-5 divide-x divide-stone-200 border-b border-stone-200 text-xs text-center bg-stone-50/30">
        <div className="p-2.5">
          <span className="text-stone-400 block text-[10px] uppercase font-mono">Identity</span>
          <strong className="text-stone-900 font-mono text-sm">{alignment.identity_percentage}%</strong>
        </div>
        <div className="p-2.5">
          <span className="text-stone-400 block text-[10px] uppercase font-mono">Matches</span>
          <strong className="text-stone-900 font-mono text-sm">{alignment.matches}</strong>
        </div>
        <div className="p-2.5">
          <span className="text-stone-400 block text-[10px] uppercase font-mono">Mismatches</span>
          <strong className="text-rose-700 font-mono text-sm">{alignment.mismatches}</strong>
        </div>
        <div className="p-2.5">
          <span className="text-stone-400 block text-[10px] uppercase font-mono">Gaps / Indels</span>
          <strong className="text-amber-700 font-mono text-sm">{alignment.gaps}</strong>
        </div>
        <div className="p-2.5 col-span-2 sm:col-span-1">
          <span className="text-stone-400 block text-[10px] uppercase font-mono">Score</span>
          <strong className="text-stone-900 font-mono text-sm">{alignment.alignment_score}</strong>
        </div>
      </div>

      {/* Alignment Text Viewer */}
      <div className="p-5 overflow-x-auto custom-scrollbar space-y-6 font-mono text-xs leading-relaxed select-text bg-[#fcfcfb]">
        {displayedBlocks.length === 0 ? (
          <div className="text-center py-6 text-stone-400 text-xs italic">
            No mutated blocks found. Sequence is 100% identical across all blocks.
          </div>
        ) : (
          displayedBlocks.map((block) => (
            <div
              key={block.block_index}
              className="border border-stone-200/80 rounded bg-white p-3 space-y-1 shadow-2xs hover:border-stone-300 transition-colors"
            >
              <div className="flex items-center text-[10px] text-stone-400 pb-1 border-b border-stone-100">
                <span>Block #{block.block_index}</span>
                <span className="mx-2">&bull;</span>
                <span>Ref: {block.ref_start}..{block.ref_end} bp</span>
                <span className="mx-2">&bull;</span>
                <span>Sample: {block.query_start}..{block.query_end} bp</span>
              </div>

              {/* Reference row */}
              <div className="flex items-center space-x-3 pt-1">
                <span className="w-16 shrink-0 text-stone-500 font-semibold text-[11px] text-right">
                  REF {block.ref_start.toString().padStart(4, " ")}:
                </span>
                <span className="text-stone-800 tracking-widest break-all font-mono">
                  {block.ref_seq.split("").map((char, idx) => {
                    const matchChar = block.match_line[idx];
                    const isDiff = matchChar !== "|";
                    return (
                      <span
                        key={idx}
                        className={isDiff ? "bg-stone-200 text-stone-950 font-bold px-0.5 rounded" : ""}
                      >
                        {char}
                      </span>
                    );
                  })}
                </span>
                <span className="text-stone-400 text-[10px] ml-auto shrink-0">{block.ref_end}</span>
              </div>

              {/* Match indicator line */}
              <div className="flex items-center space-x-3 text-stone-400">
                <span className="w-16 shrink-0" />
                <span className="text-stone-500 tracking-widest break-all font-mono">
                  {block.match_line.split("").map((m, idx) => (
                    <span
                      key={idx}
                      className={m === "." ? "text-rose-600 font-bold" : m === " " ? "text-amber-600" : "text-stone-300"}
                    >
                      {m}
                    </span>
                  ))}
                </span>
                <span className="w-8 shrink-0" />
              </div>

              {/* Sample Query row */}
              <div className="flex items-center space-x-3">
                <span className="w-16 shrink-0 text-stone-500 font-semibold text-[11px] text-right">
                  SMP {block.query_start.toString().padStart(4, " ")}:
                </span>
                <span className="text-stone-800 tracking-widest break-all font-mono">
                  {block.query_seq.split("").map((char, idx) => {
                    const matchChar = block.match_line[idx];
                    const isDiff = matchChar !== "|";
                    return (
                      <span
                        key={idx}
                        className={
                          isDiff
                            ? "bg-rose-100 text-rose-900 font-bold px-0.5 rounded border border-rose-300"
                            : ""
                        }
                      >
                        {char}
                      </span>
                    );
                  })}
                </span>
                <span className="text-stone-400 text-[10px] ml-auto shrink-0">{block.query_end}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
