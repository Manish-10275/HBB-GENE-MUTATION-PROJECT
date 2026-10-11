# Phase 2C Benchmark Forensic Follow-Up Audit Report

> **Document Type:** INDEPENDENT FORENSIC AUDIT FOLLOW-UP AND EVALUATION REPORT  
> **Target Investigation:** Continuation of Audit `research/results/CP4_3_RESULT_ARTIFACT_FORENSIC_AUDIT.md`  
> **Key Target Files:**  
> - `research/results/phase2c_benchmark_candidate_results.json` (Candidate-level results, $N = 55$)  
> - `research/results/phase2c_benchmark_summary.json` (Benchmark summary metrics)  
> - `research/results/benchmark_results.json` (Historical Phase 1/2 benchmark results, $N = 36$)  
> - `research/manifest/phase2c_primary.json` (Frozen primary dataset, SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> - `research/protocol/CP4_1_DECISION_MATRIX.md` (Locked comparison rules)  
> - `research/curation/phase2c_comparison_engine.py` (Comparison engine code)  
> - `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` (Current manuscript draft)  
> **Audit Date:** 2026-10-11  
> **Audit Status:** COMPLETED (Read-Only Investigation; Zero Project Code or Data Alterations)

---

## 1. Executive Summary

This follow-up forensic investigation was conducted to address questions regarding the Phase 2C benchmark results for the human *HBB* gene mutation analyzer. Specifically, this audit was commissioned to:
1. Verify whether the benchmark candidate results file on disk truly contains the reported **30 / 20 / 5** comparison categories and **28 / 20 / 5 / 2** protein results.
2. Explain why someone inspecting the results directory might previously have seen different numbers (such as 55 exact matches, or 36/33 counts).
3. Investigate whether the previous forensic audit (`CP4_3_RESULT_ARTIFACT_FORENSIC_AUDIT.md`) truly checked the comparison logic independently or merely re-executed the existing comparison engine.
4. Provide a clear, non-technical explanation of whether the research results can be trusted, what caveats or uncertainties remain, and whether any text or tables in the scientific manuscript need to be revised.

### Headline Findings:
- **The Result File Contains the Exact Reported Numbers:** Direct read-only inspection of `phase2c_benchmark_candidate_results.json` confirms exactly **30** `EXACT_MOLECULAR_AGREEMENT`, **20** `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`, and **5** `EXTERNAL_ANNOTATION_INCOMPLETE` comparison categories, as well as **28** `MATCH`, **20** `DISCREPANCY`, **5** `INCOMPLETE`, and **2** `NOT_APPLICABLE` protein statuses.
- **Why Previous Inspections Looked Different:** There are three clear reasons for the apparent discrepancy: (1) looking at the primary molecular status field (`primary_endpoint_status`), which is 55/55 `MATCH` (100%), rather than the category or protein fields; (2) viewing an older benchmark file in the same folder (`benchmark_results.json`), which tested only 36 variants; or (3) remembering an early software run before October 8, 2026, where a computer bug caused all 55 variants to erroneously report as exact matches.
- **Original Audit Limitation Identified:** The original audit script did **not** write a clean-room independent implementation of the rules; line 140 of the previous report confirms that it re-ran the existing function `phase2c_comparison_engine.evaluate_external_concordance()`. While this confirmed that the file on disk had not been manually modified or corrupted, it was a circular verification of the code itself. In this follow-up audit, we independently checked the raw records against the human-readable decision matrix rules and confirmed that the engine implemented them correctly.
- **Can the Results Be Trusted?** Yes. The software works as described, and the numbers are completely authentic and reproducible. However, because candidates were pre-filtered to ensure clean ClinVar records, and four mutation types are not tested in this cohort, the study proves computational consistency with ClinVar rather than universal clinical diagnostic accuracy.
- **Do You Need to Change the Manuscript?** **No changes are required.** The final manuscript draft (`PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`) already reports the exact numbers (30/20/5 and 28/20/5/2) and already discloses all study limitations and selection biases with complete scientific transparency.

---

## 2. Verification of the Stored Benchmark Result Artifact

We performed a direct, read-only inspection of `research/results/phase2c_benchmark_candidate_results.json` ($N = 55$) and `research/results/phase2c_benchmark_summary.json`. 

### 2.1 Predefined Comparison Categories (55 Variants Total)
When counting the `comparison_category` field across all 55 records in `phase2c_benchmark_candidate_results.json`, the exact counts are:

| Comparison Category | Direct Count in File | Percentage | Meaning in Plain Language |
|---|:---:|:---:|---|
| **`EXACT_MOLECULAR_AGREEMENT`** | **30** | 54.55% | Both the molecular consequence (e.g., Missense) and the predicted protein string matched ClinVar exactly. |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | **20** | 36.36% | The molecular classification (Frameshift) matched ClinVar, but ClinVar used a shorthand protein code (e.g., `E7fs`) while the engine computed the full HGVS code (`p.Glu7ArgfsTer13`). |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | **5** | 9.09% | The molecular classification (Splice Site Disruption) matched ClinVar, but ClinVar provided no protein prediction at all (empty string `""`). |
| **Total Primary Candidates** | **55** | **100.00%** | The file matches the published category counts with 100% precision. |

### 2.2 Secondary Protein Endpoint Status (55 Variants Total)
When counting the `protein_endpoint_status` field across all 55 records in `phase2c_benchmark_candidate_results.json`, the exact counts are:

| Protein Endpoint Status | Direct Count in File | Percentage | Plain Language Explanation |
|---|:---:|:---:|---|
| **`MATCH`** | **28** | 50.91% | 14 Missense + 3 Nonsense + 10 Synonymous + 1 Frameshift insertion that created an immediate stop (`p.Glu44Ter` vs `E44*`). |
| **`DISCREPANCY`** | **20** | 36.36% | 9 Frameshift deletions + 11 Frameshift duplications where ClinVar recorded shorthand single-letter truncated notation (e.g. `E7fs`). |
| **`INCOMPLETE`** | **5** | 9.09% | 5 Splice acceptor variants where ClinVar left the protein prediction field blank. |
| **`NOT_APPLICABLE`** | **2** | 3.64% | 2 Non-coding 3' UTR variants where no protein is made, so protein alteration does not apply. |
| **Total Primary Candidates** | **55** | **100.00%** | The file matches the reported 28 / 20 / 5 / 2 protein breakdown exactly. |

---

## 3. Why Previous Inspections Appeared to Show Different Counts

If you previously opened a result file and saw different counts (such as "all 55 were matches" or counts like 36 and 33), there are three concrete explanations:

### Explanation 1: Overlapping Fields Within the Same File
The main results file (`phase2c_benchmark_candidate_results.json`) contains multiple status columns for each mutation. A simple search or quick glance can easily pick up the wrong column:
- **`primary_endpoint_status`:** Shows `"MATCH"` for **all 55** variants (55/55 = 100%). This measures whether the software got the *overall molecular consequence* right (e.g., did it correctly identify a Missense, Nonsense, or Frameshift mutation?).
- **`regression_concordant`:** Shows `true` for **all 55** variants. This measures whether the software gave the exact same result as it did in earlier software builds.
- **Searching for the word `"MATCH"`:** Because `"MATCH"` appears in `primary_endpoint_status` (55 times) and also in `protein_endpoint_status` (28 times), a simple search (Ctrl+F) hits the word `"MATCH"` over 80 times in the file.
- **`comparison_category`:** Only this specific column contains the **30 / 20 / 5** distribution.
- **`protein_endpoint_status`:** Only this specific column contains the **28 / 20 / 5 / 2** distribution.

### Explanation 2: Opening a Different Result File in the Directory
The `research/results/` directory contains several different benchmark and audit files from different phases of the project:
1. `benchmark_results.json`: This is an earlier benchmark from Phase 1/Phase 2 testing an older test set of **36 variants** (`frozen_test.json`). It reports **36 concordant variants and 33 exact matches**. If you inspected this file, you saw 36 variants instead of 55!
2. `phase2c_benchmark_raw.json`: This file contains raw engine execution records for the 55 variants. It only records whether the engine crashed or succeeded (`execution_status: "SUCCESS"` for all 55). It contains **no comparison categories or protein matching status at all**.
3. `phase2c_robustness_results.json`: This file contains **18 synthetic error controls** (Class C12), testing whether the engine correctly rejected invalid inputs.

### Explanation 3: Memory of the Pre-CP4 Software Flaw
Before October 8, 2026, the benchmark code contained a major circularity flaw: the benchmark script compared the engine against a pre-stored answer that had been generated by the engine itself! In that early run, the script reported **55/55 exact matches for both molecular and protein consequences**. That bug was discovered during an internal audit (`PHASE2C_COMPARISON_IMPLEMENTATION_AUDIT.md`) and fixed under Checkpoint CP4 by comparing directly against ClinVar annotations. Anyone remembering or looking at reports from before October 8 would remember 55 exact matches.

---

## 4. Evaluation of the Original Audit: Independent Check vs. Code Reuse

We examined Section 5 of the original forensic audit report (`CP4_3_RESULT_ARTIFACT_FORENSIC_AUDIT.md`):

### What the Original Audit Did:
In lines 138–142, the original audit states:
> *"Every one of the 55 candidate records in `phase2c_primary.json` was independently re-evaluated through `phase2c_comparison_engine.evaluate_external_concordance()` and compared against the stored values in `phase2c_benchmark_candidate_results.json`..."*

This confirms that the original audit **reused the exact same Python function** (`phase2c_comparison_engine.py`) that was used to create the results file in the first place. 

### Why This Matters:
- Re-running the same code on the same data confirms **file integrity** (i.e., proving that nobody manually edited or corrupted the JSON file after it was generated).
- However, it is a **circular check** of the logic itself. If the Python script had an unintended bias or bug in how it categorized variants, running the script again would simply reproduce the same bug and report "0 discrepancies."

### Our Independent Verification of the Comparison Logic:
To break this circularity, we performed an independent check directly comparing the raw data in the frozen manifest (`phase2c_primary.json`) against the human-readable rules written in the locked protocol (`CP4_1_DECISION_MATRIX.md`), without using `phase2c_comparison_engine.py`:
1. **Missense SNVs (C01, $n=14$):** The engine predicted 3-letter standard codes (`p.Val134Leu`), and ClinVar had 1-letter codes (`V134L`). Under RefSeq rules, Val134Leu and V134L describe the exact same codon and amino acid change. All 14 are legitimate exact matches.
2. **Nonsense (Stop-Gain) (C02, $n=3$):** The engine predicted `p.Gln128Ter`, and ClinVar had `Q128*`. In genetics, `Ter` and `*` both mean a premature stop codon at position 128. All 3 are legitimate exact matches.
3. **Synonymous (Silent) (C03, $n=10$):** The engine predicted `p.(=)` (indicating no amino acid change in the coding sequence), while ClinVar recorded `p.Leu69=` (specifying the exact amino acid unchanged). Both mean zero protein alteration. All 10 are legitimate semantic matches.
4. **Frameshift Deletions & Duplications (C04 & C06, $n=20$):** The engine translated the altered reading frame down to the new stop codon (e.g. `p.Glu7ArgfsTer13`), while ClinVar used shorthand notation (e.g. `E7fs`). Both agree 100% that a frameshift occurred (molecular match), but the protein strings differ in format. They were correctly assigned to `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` with protein `DISCREPANCY`.
5. **Immediate Stop Frameshift (C06, $n=1$):** Variant `c.129dup` (`HBB-CP2-080`) creates an immediate stop codon at position 44. Both the engine (`p.Glu44Ter`) and ClinVar (`E44*`) agreed on the stop codon. It was correctly counted as an exact match.
6. **Splice Acceptor Disruptions (C09, $n=5$):** Both the engine and ClinVar classified the variants as `Splice Site Disruption` (molecular match). Because ClinVar provided no protein string (`""`), these were correctly classified as `EXTERNAL_ANNOTATION_INCOMPLETE` with protein `INCOMPLETE`.
7. **3' UTR Regulatory Variants (C11, $n=2$):** Both agreed on `3' UTR Regulatory`. Because these variants are non-coding, protein alteration does not apply (`NOT_APPLICABLE`).

**Verdict on Logic:** Although the original audit reused the code rather than writing an independent script, our independent manual verification confirms that the comparison logic faithfully and accurately implements the locked scientific decision matrix.

---

## 5. Can the Results Be Trusted, What Remains Uncertain, and What About the Manuscript?

### 5.1 Can the Results Be Trusted?
**YES.** You can be completely confident that:
1. The numbers are real, mathematically correct, and reproducible.
2. The software executes HGVS coordinates and RefSeq rules on the human *HBB* gene with high precision.
3. The discrepancy between full HGVS frameshifts and ClinVar shorthand is a well-understood database formatting convention, not a calculation defect in your software.
4. Malformed inputs, out-of-bounds numbers, and syntax errors are cleanly caught and rejected (18/18 negative controls).

### 5.2 What Remains Uncertain (Scientific Limitations to Keep in Mind):
As documented in the audit reports and manuscript, the study has important scientific boundaries:
1. **Selection (Verification) Bias:** During curation (stage CP2.2), candidate variants were screened by checking whether the software agreed with ClinVar (`comparison_status == "EXACT_AGREEMENT"`). This means the 55 variants evaluated in Phase 2C represent a curated, clean set rather than a random, blind sampling of real-world patient cases.
2. **Missing Mutation Classes ($n=0$):** Four of the eleven biological classes of *HBB* mutations (in-frame deletions C05, in-frame duplications C07, splice donor disruptions C08, and 5' UTR promoter variants C10) have zero variants in this benchmark because no clean, high-confidence variants met the filtering criteria in ClinVar. Performance on these types of mutations is untested.
3. **Small Sample Sizes in Certain Classes:** Nonsense variants have only 3 candidates, and 3' UTR variants have only 2 candidates.
4. **Computational Concordance, Not Biological Ground Truth:** The study compares software predictions against ClinVar submissions. It does not include wet-lab patient samples, RNA sequencing, or functional cell assays.

### 5.3 Should You Change Anything in the Manuscript?
**NO CHANGES ARE REQUIRED.**
We carefully reviewed the final manuscript draft (`research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`) and the results draft (`research/manuscript/PHASE5_2D_RESULTS.md`):
- **Numbers:** The manuscript already reports exactly **30** exact agreements, **20** frameshift representation differences, and **5** incomplete external annotations in Section 2, and exactly **28** matches, **20** format discrepancies, **5** incomplete, and **2** not applicable in Section 3 and Table 2.
- **Transparency:** The manuscript already explicitly discloses the selection bias in the Abstract, Section 1.7, and Section 2.1.
- **Unrepresented Classes:** Table 3 and Section 4 of the manuscript already clearly state that Classes C05, C07, C08, and C10 were not represented ($n=0$) and that performance on those classes remains unmeasured.
- **Scope:** The manuscript explicitly clarifies that this paper is a computational concordance evaluation against ClinVar, and does not claim clinical diagnostic accuracy or biological wet-lab validation.

Everything in the manuscript is already completely truthful, accurate, and aligned with the verified data on disk.

---

## 6. Audit Metadata & Verification Sign-Off

- **Audited Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`
- **Environment:** Windows 10, Python 3.14.7
- **Verification Rule:** Read-only inspection; zero files edited, zero files deleted, zero benchmarks rerun.
- **Artifact Status:** Fully intact, mathematically verified, and ready for publication review.
