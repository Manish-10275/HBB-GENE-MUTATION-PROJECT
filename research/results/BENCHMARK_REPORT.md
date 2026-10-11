# HBB Mutation Analyzer — Scientific Benchmark Evaluation Report

**Evaluation Split:** `TEST`  
**Execution Timestamp:** `2026-10-06T19:11:49.118043+00:00`  
**Dataset Architecture:** Master Manifest partitioned into Development, Validation, and Frozen Test  
**Reference Standards:** RefSeq `NM_000518.5` (transcript) & `NG_000007.3` (genomic locus)  
**Evaluator Engine:** HBB Mutation Analyzer Phase 2B Evaluation Harness  

---

## 1. Executive Summary

This report establishes the empirical performance of the **HBB Mutation Analyzer** against independent, authoritative ground truth derived from **NCBI ClinVar**, **NCBI RefSeq**, and **IthaGenes**.

- **Total Evaluated Variants:** `36`
- **Overall Biological Concordance:** `36 / 36` (**100.0%**)
- **Macro-Averaged F1-Score:** **1.0000**
- **Negative Control Specificity:** **100.0%**
- **ClinVar Rank-1 Exact Match Hit Rate:** **100.0%**
- **Mean Computational Latency:** **702.74 ms** (Local-first deterministic in silico execution)

---

## 2. Table 1: Category-Stratified Classification Performance

| Variant Class | Support (N) | Correctly Concordant | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3' UTR** | 4 | 4 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **5' UTR** | 2 | 2 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Frameshift** | 5 | 5 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **In-frame Indel** | 1 | 1 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Invalid / Rejected** | 12 | 12 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Missense** | 2 | 2 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Nonsense** | 2 | 2 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Splice Site** | 5 | 5 | 100.0% | 1.0000 | 1.0000 | 1.0000 |
| **Synonymous** | 3 | 3 | 100.0% | 1.0000 | 1.0000 | 1.0000 |

---

## 3. Table 2: Molecular Consequence Concordance

| Metric | Evaluation Result | Target / Standard | Interpretation |
| :--- | :---: | :---: | :--- |
| **Total Evaluated Variants** | `36` | N >= 30 | Full representative panel |
| **Biological Concordance Rate** | `100.0%` | >= 95.0% | Functional & structural agreement |
| **Exact Protein Sequence Match** | `91.7%` | >= 90.0% | Exact HGVS p. string match |
| **Macro-averaged F1 Score** | `1.0000` | >= 0.9000 | Balanced across all variant classes |
| **Negative Control Rejection Specificity** | `100.0%` | 100.0% | Graceful error handling of malformed inputs |

---

## 4. Table 3: External Evidence Retrieval (NCBI ClinVar)

| Retrieval Metric | Result | Target Standard | Provenance / Clinical Utility |
| :--- | :---: | :---: | :--- |
| **ClinVar Hit@1 (Rank-1 Exact Match)** | `100.0%` | >= 85.0% | Exact Variation ID prioritized at Rank 0 |
| **ClinVar Recall@5 (Candidate Inclusion)** | `100.0%` | >= 90.0% | True Variation ID in top candidate window |
| **False Match Rate** | `0.0%` | <= 5.0% | False positive exact-match prevention |
| **Mean Retrieved Records** | `1.0` | 1 - 5 | Progressive search bounding |

---

## 5. Table 4: Latency & Computational Efficiency

| Execution Step | Mean Latency | Median (p50) | 95th Percentile (p95) | Min / Max |
| :--- | :---: | :---: | :---: | :---: |
| **Deterministic Bioinformatics Pipeline** | `702.74 ms` | `0.14 ms` | `2408.59 ms` | `0.02 / 2559.0 ms` |

---

## 6. Discrepancy & Error Analysis

The evaluation logged `0` discrepancies out of `36` evaluated items.


---

## 7. Scientific Limitations & Boundaries

1. **Large Structural Deletions (> 100 bp):** Structural variants such as the 619 bp deletion (`g.71609_72227del619`) or multi-gene fusion variants (e.g. Hb Lepore) require paired-end breakpoint calling and remain outside the single-transcript cDNA model.
2. **External Tool Cross-Validation Note:** General-purpose external APIs (e.g. Mutalyzer 3 / Ensembl VEP) were not invoked during offline benchmark execution to prevent external network flakiness. All truth records are grounded directly in RefSeq and ClinVar consensus records.
3. **Clinical Disclaimer:** This benchmark validates computational sequence interpretation accuracy for research and educational applications; it does not constitute clinical diagnostic certification.
