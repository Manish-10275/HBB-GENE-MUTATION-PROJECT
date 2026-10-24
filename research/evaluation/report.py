"""
Report generator for HBB Scientific Benchmark evaluation.
Emits formatted Markdown tables, latency summaries, and comprehensive benchmark reports.
Hardened against None values, zero divisions, and undefined metrics.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _fmt_pct(val: Optional[float], decimals: int = 1) -> str:
    """Safely formats a float probability as a percentage string, or 'N/A' if None."""
    if val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"


def _fmt_float(val: Optional[float], decimals: int = 4) -> str:
    """Safely formats a float to specified decimals, or 'N/A' if None."""
    if val is None:
        return "N/A"
    return f"{val:.{decimals}f}"


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
    acc = eval_summary.get("concordance_rate")

    # 1. Table 1: Variant Class Accuracy
    t1_lines = [
        "| Variant Class | Support (N) | Correctly Concordant | Accuracy | Precision | Recall | F1-Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for cls, met in class_metrics.get("per_class", {}).items():
        supp = met.get("support", 0)
        prec = met.get("precision")
        rec = met.get("recall")
        f1 = met.get("f1_score")
        corr = int(rec * supp) if rec is not None else 0
        acc_str = _fmt_pct(rec, 1)
        prec_str = _fmt_float(prec, 4)
        rec_str = _fmt_float(rec, 4)
        f1_str = _fmt_float(f1, 4)
        t1_lines.append(f"| **{cls}** | {supp} | {corr} | {acc_str} | {prec_str} | {rec_str} | {f1_str} |")
    t1_content = "\n".join(t1_lines)
    with open(tables_dir / "table1_variant_class_accuracy.md", "w", encoding="utf-8") as f:
        f.write("# Table 1: Classification Performance by Variant Category\n\n" + t1_content + "\n")

    # 2. Table 2: Consequence Concordance Summary
    exact_match_pct = _fmt_pct(exact_matches / total_vars if total_vars > 0 else None, 1)
    concordance_pct = _fmt_pct(acc, 1)
    macro_f1_str = _fmt_float(class_metrics.get("macro_f1"), 4)
    spec_str = _fmt_pct(eval_summary.get("specificity"), 1)

    t2_lines = [
        "| Metric | Evaluation Result | Target / Standard | Interpretation |",
        "| :--- | :---: | :---: | :--- |",
        f"| **Total Evaluated Variants** | `{total_vars}` | N >= 30 | Full representative panel |",
        f"| **Biological Concordance Rate** | `{concordance_pct}` | >= 95.0% | Functional & structural agreement |",
        f"| **Exact Protein Sequence Match** | `{exact_match_pct}` | >= 90.0% | Exact HGVS p. string match |",
        f"| **Macro-averaged F1 Score** | `{macro_f1_str}` | >= 0.9000 | Balanced across all variant classes |",
        f"| **Negative Control Rejection Specificity** | `{spec_str}` | 100.0% | Graceful error handling of malformed inputs |",
    ]
    t2_content = "\n".join(t2_lines)
    with open(tables_dir / "table2_consequence_concordance.md", "w", encoding="utf-8") as f:
        f.write("# Table 2: Molecular Consequence Concordance Summary\n\n" + t2_content + "\n")

    # 3. Table 3: ClinVar Retrieval Performance
    hit_1_str = _fmt_pct(retrieval_metrics.get("hit_at_1"), 1)
    rec_5_str = _fmt_pct(retrieval_metrics.get("recall_at_5"), 1)
    fmr_str = _fmt_pct(retrieval_metrics.get("false_match_rate"), 1)
    mean_ret = retrieval_metrics.get("mean_retrieved_records")
    mean_ret_str = str(mean_ret) if mean_ret is not None else "N/A"

    t3_lines = [
        "| Retrieval Metric | Result | Target Standard | Provenance / Clinical Utility |",
        "| :--- | :---: | :---: | :--- |",
        f"| **ClinVar Hit@1 (Rank-1 Exact Match)** | `{hit_1_str}` | >= 85.0% | Exact Variation ID prioritized at Rank 0 |",
        f"| **ClinVar Recall@5 (Candidate Inclusion)** | `{rec_5_str}` | >= 90.0% | True Variation ID in top candidate window |",
        f"| **False Match Rate** | `{fmr_str}` | <= 5.0% | False positive exact-match prevention |",
        f"| **Mean Retrieved Records** | `{mean_ret_str}` | 1 - 5 | Progressive search bounding |",
    ]
    t3_content = "\n".join(t3_lines)
    with open(tables_dir / "table3_clinvar_retrieval_performance.md", "w", encoding="utf-8") as f:
        f.write("# Table 3: ClinVar Evidence Retrieval Performance\n\n" + t3_content + "\n")

    # 4. Table 4: Latency Summary
    mean_lat = latency_metrics.get("mean_ms")
    med_lat = latency_metrics.get("median_ms")
    p95_lat = latency_metrics.get("p95_ms")
    min_lat = latency_metrics.get("min_ms")
    max_lat = latency_metrics.get("max_ms")

    mean_lat_str = f"{mean_lat} ms" if mean_lat is not None else "N/A"
    med_lat_str = f"{med_lat} ms" if med_lat is not None else "N/A"
    p95_lat_str = f"{p95_lat} ms" if p95_lat is not None else "N/A"
    range_lat_str = f"{min_lat} / {max_lat} ms" if min_lat is not None and max_lat is not None else "N/A"

    t4_lines = [
        "| Execution Step | Mean Latency | Median (p50) | 95th Percentile (p95) | Min / Max |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **Deterministic Bioinformatics Pipeline** | `{mean_lat_str}` | `{med_lat_str}` | `{p95_lat_str}` | `{range_lat_str}` |"
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
- **Overall Biological Concordance:** `{concordant} / {total_vars}` (**{concordance_pct}**)
- **Macro-Averaged F1-Score:** **{macro_f1_str}**
- **Negative Control Specificity:** **{spec_str}**
- **ClinVar Rank-1 Exact Match Hit Rate:** **{hit_1_str}**
- **Mean Computational Latency:** **{mean_lat_str}** (Local-first deterministic in silico execution)

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
