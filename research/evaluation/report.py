"""
Report generator for HBB Scientific Benchmark evaluation.
Emits formatted Markdown tables, latency summaries, and comprehensive benchmark reports.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List


def generate_benchmark_markdown_report(
    eval_summary: Dict[str, Any],
    class_metrics: Dict[str, Any],
    retrieval_metrics: Dict[str, Any],
    latency_metrics: Dict[str, Any],
    split_name: str,
    output_dir: Path
) -> str:
    """Generates the comprehensive benchmark report and individual markdown tables."""
    output_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    total_vars = eval_summary.get("total_variants", 0)
    concordant = eval_summary.get("concordant_variants", 0)
    exact_matches = eval_summary.get("exact_matches", 0)
    acc = eval_summary.get("concordance_rate", 0.0)

    # 1. Table 1: Variant Class Accuracy
    t1_lines = [
        "| Variant Class | Support (N) | Correctly Concordant | Accuracy | Precision | Recall | F1-Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for cls, met in class_metrics.get("per_class", {}).items():
        supp = met.get("support", 0)
        prec = met.get("precision", 0.0)
        rec = met.get("recall", 0.0)
        f1 = met.get("f1_score", 0.0)
        corr = int(rec * supp)
        t1_lines.append(f"| **{cls}** | {supp} | {corr} | {rec * 100:.1f}% | {prec:.4f} | {rec:.4f} | {f1:.4f} |")
    t1_content = "\n".join(t1_lines)
    with open(tables_dir / "table1_variant_class_accuracy.md", "w", encoding="utf-8") as f:
        f.write("# Table 1: Classification Performance by Variant Category\n\n" + t1_content + "\n")

    # 2. Table 2: Consequence Concordance Summary
    t2_lines = [
        "| Metric | Evaluation Result | Target / Standard | Interpretation |",
        "| :--- | :---: | :---: | :--- |",
        f"| **Total Evaluated Variants** | `{total_vars}` | N >= 30 | Full representative panel |",
        f"| **Biological Concordance Rate** | `{acc * 100:.1f}%` | >= 95.0% | Functional & structural agreement |",
        f"| **Exact Protein Sequence Match** | `{exact_matches / total_vars * 100:.1f}%` | >= 90.0% | Exact HGVS p. string match |",
        f"| **Macro-averaged F1 Score** | `{class_metrics.get('macro_f1', 0.0):.4f}` | >= 0.9000 | Balanced across all variant classes |",
        f"| **Negative Control Rejection Specificity** | `{eval_summary.get('specificity', 1.0) * 100:.1f}%` | 100.0% | Graceful error handling of malformed inputs |",
    ]
    t2_content = "\n".join(t2_lines)
    with open(tables_dir / "table2_consequence_concordance.md", "w", encoding="utf-8") as f:
        f.write("# Table 2: Molecular Consequence Concordance Summary\n\n" + t2_content + "\n")

    # 3. Table 3: ClinVar Retrieval Performance
    t3_lines = [
        "| Retrieval Metric | Result | Target Standard | Provenance / Clinical Utility |",
        "| :--- | :---: | :---: | :--- |",
        f"| **ClinVar Hit@1 (Rank-1 Exact Match)** | `{retrieval_metrics.get('hit_at_1', 0.0) * 100:.1f}%` | >= 85.0% | Exact Variation ID prioritized at Rank 0 |",
        f"| **ClinVar Recall@5 (Candidate Inclusion)** | `{retrieval_metrics.get('recall_at_5', 0.0) * 100:.1f}%` | >= 90.0% | True Variation ID in top candidate window |",
        f"| **False Match Rate** | `{retrieval_metrics.get('false_match_rate', 0.0) * 100:.1f}%` | <= 5.0% | False positive exact-match prevention |",
        f"| **Mean Retrieved Records** | `{retrieval_metrics.get('mean_retrieved_records', 0.0)}` | 1 - 5 | Progressive search bounding |",
    ]
    t3_content = "\n".join(t3_lines)
    with open(tables_dir / "table3_clinvar_retrieval_performance.md", "w", encoding="utf-8") as f:
        f.write("# Table 3: ClinVar Evidence Retrieval Performance\n\n" + t3_content + "\n")

    # 4. Table 4: Latency Summary
    t4_lines = [
        "| Execution Step | Mean Latency | Median (p50) | 95th Percentile (p95) | Min / Max |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **Deterministic Bioinformatics Pipeline** | `{latency_metrics.get('mean_ms', 0.0)} ms` | `{latency_metrics.get('median_ms', 0.0)} ms` | `{latency_metrics.get('p95_ms', 0.0)} ms` | `{latency_metrics.get('min_ms', 0.0)} / {latency_metrics.get('max_ms', 0.0)} ms` |"
    ]
    t4_content = "\n".join(t4_lines)
    with open(tables_dir / "table4_latency_summary.md", "w", encoding="utf-8") as f:
        f.write("# Table 4: Computational Execution Latency\n\n" + t4_content + "\n")

    # 5. Master Report
    report_md = f"""# HBB Mutation Analyzer — Scientific Benchmark Evaluation Report

**Evaluation Split:** `{split_name.upper()}`  
**Execution Timestamp:** `{timestamp}`  
**Dataset Architecture:** Master Manifest partitioned into Development, Validation, and Frozen Test  
**Reference Standards:** RefSeq `NM_000518.5` (transcript) & `NG_000007.3` (genomic locus)  
**Evaluator Engine:** HBB Mutation Analyzer Phase 2B Evaluation Harness  

---

## 1. Executive Summary

This report establishes the empirical performance of the **HBB Mutation Analyzer** against independent, authoritative ground truth derived from **NCBI ClinVar**, **NCBI RefSeq**, and **IthaGenes**.

- **Total Evaluated Variants:** `{total_vars}`
- **Overall Biological Concordance:** `{concordant} / {total_vars}` (**{acc * 100:.1f}%**)
- **Macro-Averaged F1-Score:** **{class_metrics.get('macro_f1', 0.0):.4f}**
- **Negative Control Specificity:** **{eval_summary.get('specificity', 1.0) * 100:.1f}%**
- **ClinVar Rank-1 Exact Match Hit Rate:** **{retrieval_metrics.get('hit_at_1', 0.0) * 100:.1f}%**
- **Mean Computational Latency:** **{latency_metrics.get('mean_ms', 0.0)} ms** (Local-first deterministic in silico execution)

---

## 2. Table 1: Category-Stratified Classification Performance

{t1_content}

---

## 3. Table 2: Molecular Consequence Concordance

{t2_content}

---

## 4. Table 3: External Evidence Retrieval (NCBI ClinVar)

{t3_content}

---

## 5. Table 4: Latency & Computational Efficiency

{t4_content}

---

## 6. Discrepancy & Error Analysis

The evaluation logged `{eval_summary.get('discrepancy_count', 0)}` discrepancies out of `{total_vars}` evaluated items.
{eval_summary.get('discrepancies_formatted', 'All variants passed with zero discrepancies.')}

---

## 7. Scientific Limitations & Boundaries

1. **Large Structural Deletions (> 100 bp):** Structural variants such as the 619 bp deletion (`g.71609_72227del619`) or multi-gene fusion variants (e.g. Hb Lepore) require paired-end breakpoint calling and remain outside the single-transcript cDNA model.
2. **External Tool Cross-Validation Note:** General-purpose external APIs (e.g. Mutalyzer 3 / Ensembl VEP) were not invoked during offline benchmark execution to prevent external network flakiness. All truth records are grounded directly in RefSeq and ClinVar consensus records.
3. **Clinical Disclaimer:** This benchmark validates computational sequence interpretation accuracy for research and educational applications; it does not constitute clinical diagnostic certification.
"""

    report_path = output_dir / "BENCHMARK_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    return report_md
