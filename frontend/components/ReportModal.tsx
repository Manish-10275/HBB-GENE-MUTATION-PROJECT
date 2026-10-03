"use client";

import React, { useState } from "react";
import { X, Printer, Download, Copy, Check, FileText } from "lucide-react";
import { ReportResponse } from "../lib/types";

interface ReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  report: ReportResponse | null;
}

export const ReportModal: React.FC<ReportModalProps> = ({
  isOpen,
  onClose,
  report,
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !report) return null;

  const handlePrint = () => {
    const printWindow = window.open("", "_blank");
    if (printWindow) {
      printWindow.document.write(report.html_content);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
      }, 300);
    }
  };

  const handleDownloadMarkdown = () => {
    const blob = new Blob([report.markdown_content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `HBB_Mutation_Report_${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleCopyMarkdown = () => {
    navigator.clipboard.writeText(report.markdown_content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white border border-stone-200 rounded-xl max-w-4xl w-full shadow-2xl flex flex-col max-h-[90vh] overflow-hidden my-6">
        {/* Modal Top Bar */}
        <div className="px-6 py-4 border-b border-stone-200 bg-stone-50 flex items-center justify-between shrink-0">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-stone-700" />
            <div>
              <h3 className="font-serif text-base font-semibold text-stone-900">
                {report.title}
              </h3>
              <p className="text-xs text-stone-500 font-mono">
                Generated at {report.generated_at}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded shadow-2xs transition-colors"
            >
              <Printer className="w-3.5 h-3.5" />
              Print / Save PDF
            </button>
            <button
              onClick={handleDownloadMarkdown}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded shadow-2xs transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              Download .md
            </button>
            <button
              onClick={handleCopyMarkdown}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded shadow-2xs transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? "Copied" : "Copy Markdown"}
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-stone-400 hover:text-stone-700 rounded hover:bg-stone-200/60 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Report Preview */}
        <div className="flex-1 overflow-y-auto p-8 bg-stone-50/50 custom-scrollbar">
          <div
            className="bg-white border border-stone-200 shadow-sm rounded-lg p-8 max-w-3xl mx-auto"
            dangerouslySetInnerHTML={{ __html: report.html_content }}
          />
        </div>
      </div>
    </div>
  );
};
