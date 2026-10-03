import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HBB Mutation Analyzer | Understand the sequence. Follow the evidence.",
  description:
    "Genomic research and educational workbench for deterministic sequence alignment, codon consequence analysis, and evidence-grounded research on the human HBB gene.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-[#fafaf9] text-[#1c1917] selection:bg-slate-200">
        {children}
      </body>
    </html>
  );
}
