# Phase 2C Benchmark Execution Report

> **Document Status:** FACTUAL BENCHMARK EVALUATION REPORT  
> **Protocol:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (Locked)  
> **Protocol SHA256:** `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`  
> **Frozen Primary Dataset:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Engine Software Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`  
> **Execution Environment:** Python 3.14.7 on Windows 10  
> **Execution Timestamp:** `2026-10-08T17:28:01.897905+00:00`

---

## 1. Executive Summary & Status Block

```
PHASE 2C BENCHMARK STATUS:
COMPLETED

PRIMARY N:
55

C12 ROBUSTNESS N:
18

CONDITIONAL N:
64

DATASET SHA256:
39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96

PROTOCOL SHA256:
e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969

ENGINE COMMIT:
845f595cc039e006d74237945450c7b4a9569ee6

DATASET MODIFIED:
NO

PROTOCOL MODIFIED:
NO

ENGINE MODIFIED:
NO

PRODUCTION CODE MODIFIED:
NO
```

---

## 2. Primary Endpoint Result

### Molecular Consequence Concordance Against Frozen External Annotations

```
PRIMARY MOLECULAR CONCORDANCE:
55 / 55
100.00%
95% Exact Clopper-Pearson CI: [93.51%, 100.0%]
Molecular Matches: 55
Molecular Discrepancies: 0
Unresolved / Error / Unsupported States: 0
```

- **Observed Result:** Under the locked comparison rules, all **55 frozen primary candidates** achieved molecular consequence category concordance between the runtime deterministic engine output and the frozen external comparison annotations under `NM_000518.5`.
- **Scientific Caution:** In strict adherence to scientific integrity principles, an observed concordance of 55/55 ($100.00\%$) against this quality-constrained external comparison cohort cannot be extrapolated as universal generalization across all possible human HBB variants or unrepresented mutation classes.

---

## 3. Secondary Endpoints

### A. Protein Consequence Concordance
- **Exact Protein Nomenclature Matches:** 28 / 55 (50.91%) [95% Exact Clopper-Pearson CI: 37.07%, 64.65%]
- **Protein Format Differences (Truncated Frameshifts):** 20 / 55 (36.36%)
- **Incomplete External Protein Annotations (Class C09 Splice):** 5 / 55 (9.09%)
- **Non-Coding Variants (Class C11 3' UTR, Protein N/A):** 2 / 55 (3.64%)
- **Separation Guarantee:** In accordance with Section 5 of CP4.1, missing external protein strings for canonical splice variants are treated as incomplete external annotations and do not taint the primary molecular consequence concordance.

### B. Predefined Category Distribution

| Predefined Category | Count | Proportion | Impact on Primary Endpoint |
|---|:---:|:---:|:---:|
| **`EXACT_MOLECULAR_AGREEMENT`** | **30** | 54.5% | MATCH |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | **20** | 36.4% | MATCH |
| **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | **0** | 0.0% | DISCREPANCY |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | **5** | 9.1% | MATCH (Splice) / DISCREPANCY (Missing Mol) |
| **`EXTERNAL_CONFLICT`** | **0** | 0.0% | DISCREPANCY |
| **`REFERENCE_MISMATCH`** | **0** | 0.0% | DISCREPANCY |
| **`HGVS_AMBIGUITY`** | **0** | 0.0% | DISCREPANCY |
| **`ENGINE_UNSUPPORTED`** | **0** | 0.0% | DISCREPANCY |
| **`ENGINE_ERROR`** | **0** | 0.0% | DISCREPANCY |
| **`UNRESOLVED`** | **0** | 0.0% | DISCREPANCY |
| **TOTAL** | **55** | **100.0%** | |

---

## 4. Class-Stratified Results

| Class ID | Variant Class Name | Cohort $n$ | Molecular Matches ($k$) | Discrepancies | Concordance (%) | Exact 95% Clopper-Pearson CI | Scientific Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | **14** | **14** | 0 | **100.0%** | [76.84%, 100.0%] | Adequately represented |
| **C02** | Nonsense (Stop-Gain) | **3** | **3** | 0 | **100.0%** | [29.24%, 100.0%] | Wide uncertainty due to small $N$ |
| **C03** | Synonymous (Silent) | **10** | **10** | 0 | **100.0%** | [69.15%, 100.0%] | Adequately represented |
| **C04** | Frameshift Deletions | **9** | **9** | 0 | **100.0%** | [66.37%, 100.0%] | Adequately represented |
| **C05** | In-Frame Indels / Deletions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C06** | Frameshift Duplications / Insertions | **12** | **12** | 0 | **100.0%** | [73.54%, 100.0%] | Adequately represented |
| **C07** | In-Frame Insertions / Duplications | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C08** | Splice Donor Disruptions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C09** | Splice Acceptor Disruptions | **5** | **5** | 0 | **100.0%** | [47.82%, 100.0%] | Adequately represented |
| **C10** | 5' UTR Regulatory Variants | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C11** | 3' UTR Regulatory Variants | **2** | **2** | 0 | **100.0%** | [15.81%, 100.0%] | Wide uncertainty due to small $N$ |
| **TOTAL** | **All 11 Biological Classes** | **55** | **55** | **0** | **100.0%** | **[93.51%, 100.0%]** | **Primary Evaluation Cohort** |

---

## 5. Experiment D: Adversarial Robustness Results
- **Cohort:** The 18 synthetic negative controls in `C12` (`HBB-CP2-297`..`314`).
- **Separation Guarantee:** Robustness controls were executed in an isolated experiment and are **strictly segregated from the biological primary denominator**.
- **Rejection Concordance:** **18 / 18** (100.0%) [95% Exact Clopper-Pearson CI: 81.47%, 100.00%].
- All 18 synthetic malformed inputs (invalid coordinates, out-of-bounds, syntax errors, and reference mismatches) were rejected with explicit `AnalysisError` codes without silent mispredictions or runtime crashes.

---

## 6. Isolated Software Regression Check
- **Regression Concordance ($A == B$):** **55 / 55** (100.0%).
- **Isolation Guarantee:** Stored expected outputs (Field B) were compared against runtime outputs (Field A) exclusively for software self-consistency verification. Field B did not participate in biological concordance evaluation.

---

## 7. Audit & Immutability Verification
- **Frozen Dataset Verification:** SHA256 of `research/manifest/phase2c_primary.json` verified byte-for-byte identical (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`).
- **Protocol Verification:** SHA256 of `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` verified byte-for-byte identical (`e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`).
- **Historical Manifest Integrity:** Historical `frozen_test.json` SHA256 verified unchanged (`2f6b8842...`).
- **Zero Code Modifications:** Zero production files altered in `backend/` or `frontend/`.
- **Zero Post-Hoc Alterations:** No candidates added, removed, or reclassified.