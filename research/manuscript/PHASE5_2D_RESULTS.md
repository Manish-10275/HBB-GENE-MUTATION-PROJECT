# Phase 5.2D — Results Section Draft

> **Document Type:** MANUSCRIPT RESULTS SECTION DRAFT  
> **Target Manuscript:** HBB Gene Mutation Analyzer Research Manuscript  
> **Stage:** Phase 5.2D (Results Section Authoring)  
> **Governing Baseline:** `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md`, `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`, `research/results/phase2c_benchmark_summary.json`, `research/results/PHASE2C_CLASS_RESULTS.md`, `research/results/PHASE2C_ERROR_REGISTER.md`, `research/results/PHASE2C_ROBUSTNESS_REPORT.md`, `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md`  
> **Primary Dataset:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Benchmark Protocol SHA256:** `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`  
> **Engine Git Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`  
> **Execution Timestamp:** 2026-10-08T17:28:01.897905+00:00  
> **Quality Standard:** Absolute numerical traceability to stored artifacts; zero post-hoc recalculation; strict separation of comparators ($A$ vs $C$ vs $B$); explicit disclosure of curation selection constraints.

---

# Results

## 1. Frozen Cohort and Evaluation Integrity
The benchmark was executed strictly against the pre-frozen primary evaluation cohort under the immutable protocol locked in Checkpoint CP3. Pre-execution cryptographic verification confirmed that the primary manifest (`research/manifest/phase2c_primary.json`, 59,605 bytes, $N = 55$) matched its locked SHA256 checksum (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`). The benchmark protocol (`research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`) matched its pre-registered SHA256 checksum (`e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`), and software execution was pinned to engine commit `845f595cc039e006d74237945450c7b4a9569ee6`. Cross-referencing against historical development datasets confirmed zero candidate overlap with the Phase 2B test cohort (`research/manifest/frozen_test.json`, SHA256: `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994`).

All 55 primary cohort variants originated from curated NCBI ClinVar records under RefSeq accession `NM_000518.5`. Review status stratification confirmed that 54 of 55 variants (98.18%) possessed $\ge 2$-star review status (criteria provided, multiple submitters, no conflicts), and 1 variant (1.82%; candidate `HBB-CP2-072`, $c.67G>T$, $p.Glu23Ter$) possessed 3-star expert panel review status. As documented in the study design, 100% of candidates were derived from ClinVar; exactly 0 variants possessed independent non-ClinVar biological corroboration dossiers. Furthermore, because candidate eligibility during CP2.2 curation was conditioned on deterministic engine concordance (`comparison_status == "EXACT_AGREEMENT"`), the evaluated cohort represents an enriched, quality-constrained subset evaluating computational rule execution fidelity and external database annotation alignment rather than an unselected prospective clinical sample.

---

## 2. Primary Molecular Consequence Concordance
The primary evaluation endpoint evaluated concordance between runtime deterministic engine output (Entity $A$) and normalized external ClinVar molecular annotations (Entity $C$). Stored deterministic expected outputs (Entity $B$) were isolated from the evaluation loop and did not participate in determining concordance.

Across the frozen primary cohort of 55 curated *HBB* variants, runtime molecular consequence predictions achieved 100.00% concordance with curated ClinVar-derived external molecular annotations (55/55 matches, 0 discrepancies; Table 1). The exact two-sided 95% Clopper-Pearson binomial confidence interval was [93.51%, 100.00%].

### Table 1: Primary Molecular Consequence Evaluation Summary
| Evaluation Metric | Observed Value | Percentage (%) | Exact 95% Clopper-Pearson CI | Evidentiary Basis |
|---|:---:|:---:|:---:|---|
| **Primary Cohort Denominator ($N$)** | 55 | 100.00% | — | Frozen manifest `phase2c_primary.json` |
| **Molecular Consequence Matches ($k$)** | 55 | 100.00% | **[93.51%, 100.00%]** | Runtime Entity $A$ vs Normalized External Entity $C$ |
| **Molecular Consequence Discrepancies** | 0 | 0.00% | [0.00%, 6.49%] | Zero discordance across 7 represented classes |
| **Execution Failures (`ENGINE_ERROR`)** | 0 | 0.00% | [0.00%, 6.49%] | Zero runtime exceptions or unhandled failures |
| **Syntax / Reference Rejections** | 0 | 0.00% | [0.00%, 6.49%] | All 55 variants valid under `NM_000518.5` |

Classification of the 55 primary records across the pre-specified ten-tier comparison category hierarchy revealed three populated categories:
1. **`EXACT_MOLECULAR_AGREEMENT`:** 30 variants (54.55%) exhibited simultaneous exact molecular consequence concordance and exact protein nomenclature matching.
2. **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`:** 20 variants (36.36%) exhibited exact primary molecular consequence concordance (Frameshift) accompanied by protein nomenclature format divergence resulting from ClinVar truncated frameshift representations.
3. **`EXTERNAL_ANNOTATION_INCOMPLETE`:** 5 variants (9.09%) exhibited exact primary molecular consequence concordance (Splice Acceptor) where the external ClinVar record omitted a protein consequence string.
4. **All Other Categories:** 0 variants (0.00%) were assigned to `ENGINE_ERROR`, `HGVS_AMBIGUITY`, `REFERENCE_MISMATCH`, `ENGINE_UNSUPPORTED`, `EXTERNAL_CONFLICT`, `PROTEIN_AGREEMENT_CLASS_DIFFERENCE`, or `UNRESOLVED`.

This 55/55 result reflects complete concordance on clean, curated ClinVar-derived external molecular annotations. It does not represent independent biological truth, clinical diagnostic accuracy, or pathogenicity prediction performance.

---

## 3. Protein Nomenclature Representation
Secondary evaluation assessed exact concordance between runtime protein consequence predictions and external ClinVar protein annotations across the 55 primary candidates (Table 2).

Exact protein nomenclature agreement was observed for 28 of 55 variants (50.91%, exact 95% Clopper-Pearson CI: [37.07%, 64.65%]). The remaining 27 variants were categorized into three distinct, non-erroneous representation groups:

### Table 2: Secondary Protein Consequence Nomenclature Breakdown
| Protein Endpoint Status | Candidate Count | Percentage (%) | Class Distribution | Methodological Rationale |
|---|:---:|:---:|---|---|
| **`MATCH`** | **28** | **50.91%** | C01 ($n=14$), C02 ($n=3$), C03 ($n=10$), C06 ($n=1$) | Exact string and semantic identity (all missense, nonsense, synonymous, and one premature stop insertion `p.Glu44Ter`). |
| **`DISCREPANCY` (Format)** | **20** | **36.36%** | C04 ($n=9$ deletions), C06 ($n=11$ duplications) | Truncated frameshift notation in ClinVar (e.g., `p.Glu7fs` or `E7fs`) vs full translation syntax (`p.Glu7GlyfsTer13`). |
| **`INCOMPLETE`** | **5** | **9.09%** | C09 ($n=5$ splice acceptors) | External ClinVar records lack a protein consequence string (`p.?`). |
| **`NOT_APPLICABLE`** | **2** | **3.64%** | C11 ($n=2$ 3' UTR variants) | Non-coding sequence alterations with no protein translation product. |
| **TOTAL** | **55** | **100.00%** | All 7 Represented Classes | Secondary protein concordance: 28/55 (50.91%). |

The 20 format discrepancies occurred exclusively among frameshift variants (Classes C04 and C06). In all 20 cases, the deterministic engine computed the complete downstream reading frame translation up to the first termination codon in accordance with HGVS guidelines, whereas ClinVar recorded shorthand single-letter or three-letter truncated strings denoting only the initial affected residue. The underlying molecular consequence classification (Frameshift) was concordant in 100% of these cases; divergence was restricted to repository string formatting conventions.

---

## 4. Results by Represented Variant Class
Stratification of primary molecular consequence concordance across the 11 predefined biological mutation classes is presented in Table 3.

Seven biological mutation classes were represented in the primary cohort, and all seven exhibited 100.0% molecular consequence concordance:
- **Class C01 (Missense SNVs):** 14/14 concordant (100.0%, 95% CI: [76.84%, 100.00%]).
- **Class C02 (Nonsense / Stop-Gain):** 3/3 concordant (100.0%, 95% CI: [29.24%, 100.00%]).
- **Class C03 (Synonymous / Silent):** 10/10 concordant (100.0%, 95% CI: [69.15%, 100.00%]).
- **Class C04 (Frameshift Deletions):** 9/9 concordant (100.0%, 95% CI: [66.37%, 100.00%]).
- **Class C06 (Frameshift Duplications / Insertions):** 12/12 concordant (100.0%, 95% CI: [73.54%, 100.00%]).
- **Class C09 (Splice Acceptor Disruptions):** 5/5 concordant (100.0%, 95% CI: [47.82%, 100.00%]).
- **Class C11 (3' UTR Regulatory Variants):** 2/2 concordant (100.0%, 95% CI: [15.81%, 100.00%]).

### Table 3: Class-Stratified Benchmark Performance
| Class ID | Biological Variant Class | Primary ($n$) | Successes ($k$) | Discrepancies | Concordance (%) | Exact 95% Clopper-Pearson CI | Representation Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | 14 | 14 | 0 | 100.0% | [76.84%, 100.00%] | Represented ($n = 14$) |
| **C02** | Nonsense (Stop-Gain) | 3 | 3 | 0 | 100.0% | [29.24%, 100.00%] | Represented ($n = 3$, wide CI) |
| **C03** | Synonymous (Silent) | 10 | 10 | 0 | 100.0% | [69.15%, 100.00%] | Represented ($n = 10$) |
| **C04** | Frameshift Deletions | 9 | 9 | 0 | 100.0% | [66.37%, 100.00%] | Represented ($n = 9$) |
| **C05** | In-Frame Indels / Deletions | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C06** | Frameshift Duplications | 12 | 12 | 0 | 100.0% | [73.54%, 100.00%] | Represented ($n = 12$) |
| **C07** | In-Frame Duplications | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C08** | Splice Donor Disruptions | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C09** | Splice Acceptor Disruptions | 5 | 5 | 0 | 100.0% | [47.82%, 100.00%] | Represented ($n = 5$, wide CI) |
| **C10** | 5' UTR Regulatory Variants | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C11** | 3' UTR Regulatory Variants | 2 | 2 | 0 | 100.0% | [15.81%, 100.00%] | Represented ($n = 2$, wide CI) |
| **TOTAL** | **Primary Evaluation Cohort** | **55** | **55** | **0** | **100.0%** | **[93.51%, 100.00%]** | **7 Classes Represented** |

### Documentation of Unrepresented Mutation Classes ($n = 0$)
Four biological classes had zero candidates in the primary cohort:
- **Class C05 (In-Frame Deletions, $n = 0$):** Candidate `HBB-CP2-105` (`c.9_83del`, 25 codons) was relegated to the Conditional cohort due to structural deletion length and single-submitter status.
- **Class C07 (In-Frame Duplications, $n = 0$):** Only two clean in-frame duplications existed in the harvested pool; both possessed 0-star ClinVar evidence and were relegated to the Secondary cohort.
- **Class C08 (Splice Donor Disruptions, $n = 0$):** Zero non-conflicting donor variants ($+1, +2, +5$) meeting quality filtering criteria were available in the harvested ClinVar dataset.
- **Class C10 (5' UTR Regulatory Variants, $n = 0$):** All queried promoter variants ($> -50$ bp upstream) exceeded the physical transcript boundary of `NM_000518.5`.

In accordance with protocol rules, these classes are reported as `NOT REPRESENTED IN PRIMARY COHORT`. Algorithmic performance for in-frame indels, splice donor disruptions, and 5' UTR promoter variants is unmeasured in this benchmark.

---

## 5. Synthetic Robustness Controls (Experiment D)
Input validation and error handling were evaluated in an isolated negative-control experiment comprising 18 synthetic malformed inputs (Class C12; candidates `HBB-CP2-297` through `HBB-CP2-314`). These controls were completely segregated from the biological primary cohort and were not included in the primary denominator ($N = 55$).

All 18 synthetic negative controls (100.00%, exact 95% Clopper-Pearson CI: [81.47%, 100.00%]) were gracefully rejected by the engine with explicit, typed `AnalysisError` exceptions (Table 4):
- **`INVALID_COORDINATE` ($n = 8$):** Inverted deletion ranges (`c.150_145del`, `c.400_350del`), inverted duplication ranges (`c.250_240dup`), non-consecutive insertion coordinates (`c.50_53insA`, `c.100_104insGCC`, `c.200_205insTT`), base zero violation (`c.0A>G`), and malformed 3' UTR offset (`c.*0A>G`).
- **`OUT_OF_BOUNDS` ($n = 6$):** Coordinates exceeding transcript length (`c.650A>G`, `c.750del`, `c.800dup`) and intronic offsets exceeding physical intron spans (`c.92+250G>A`, `c.93-200G>A` exceeding 130 bp Intron 1; `c.315+950G>A` exceeding 850 bp Intron 2).
- **`SYNTAX_ERROR` ($n = 2$):** Non-standard DNA base in alternate allele (`c.50A>Z`) and malformed HGVS expression syntax (`c.delA`).
- **`REFERENCE_MISMATCH` ($n = 2$):** Exonic reference base mismatch (`c.70T>A`, reference base G) and intronic reference base mismatch (`c.92+1A>G`, genomic reference base G).

Zero unhandled exceptions, uncaught runtime crashes, or silent mispredictions were observed across the adversarial test battery.

### Table 4: Synthetic Robustness Control Evaluation Breakdown
| Test Category | Tested Inputs ($n$) | Graceful Rejections ($k$) | Error Code Returned | Unhandled Crashes | Result |
|---|:---:|:---:|---|:---:|:---:|
| **Coordinate Geometry & Range Violations** | 8 | 8 | `INVALID_COORDINATE` | 0 | **PASS** |
| **Transcript & Intron Boundary Overflow** | 6 | 6 | `OUT_OF_BOUNDS` | 0 | **PASS** |
| **Malformed Syntax & Non-DNA Bases** | 2 | 2 | `SYNTAX_ERROR` | 0 | **PASS** |
| **Reference Sequence Base Mismatches** | 2 | 2 | `REFERENCE_MISMATCH` | 0 | **PASS** |
| **TOTAL (Experiment D)** | **18** | **18** | **All Typed Errors** | **0** | **100.0% Rejection** |

---

## 6. Software Regression Consistency ($A$ vs $B$)
To verify software execution stability across commits, runtime deterministic engine outputs (Entity $A$) were compared against frozen expected deterministic outputs (Entity $B$) stored in `research/manifest/phase2c_primary.json`.

Runtime outputs reproduced frozen expected values for 100.00% of candidates (55/55 molecular consequence reproductions, 55/55 protein consequence reproductions). This check confirms zero algorithmic drift between dataset freezing and benchmark execution. Because Entity $B$ represents prior engine code outputs rather than external biological truth, this metric serves exclusively as internal software regression metadata and was strictly isolated from external concordance reporting.

---

## 7. Discrepancy and Error Accounting
Across the 55 primary cohort variants:
- **Total Molecular Consequence Discrepancies:** 0
- **Total Execution Crashes (`ENGINE_ERROR`):** 0
- **Total Syntax / Coordinate Parse Failures:** 0
- **Total Exonic / Intronic Reference Mismatches:** 0

### Legacy Nomenclature Tracking
Historical alias records were audited across all 55 candidates (`research/results/PHASE2C_ERROR_REGISTER.md`). Exactly 33 variants (60.00%) possessed traditional codon (CD) designations or mature protein numbering designations in ClinVar (e.g., `CD 6 -A` for `c.20del`, `CD 22 (GAA>TAA)` for `c.67G>T`, `CD 30 (A>G)` for `c.91A>G`, `CD 42/43 (+T)` for `c.129dup`, and `CD 126 GTG>GGG` for `c.380T>G`). The comparison engine confirmed that all 33 legacy designations reflected non-contradictory historical offsets (-1 codon mature protein shift or standard Italian/Greek/Chinese thalassemia notation) and matched the underlying `NM_000518.5` cDNA coordinates without ambiguity.

---

## 8. Summary of Observed Results
Table 5 synthesizes the four distinct evaluation dimensions executed under Phase 2C.

### Table 5: Comprehensive Synthesis of Phase 2C Benchmark Findings
| Evaluation Dimension | Evaluated Entities | Cohort Size ($N$) | Successes ($k$) | Rate (%) | Exact 95% Clopper-Pearson CI | Scientific Interpretation |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Primary Molecular Concordance** | Entity $A$ vs Entity $C$ | **55** | **55** | **100.00%** | **[93.51%, 100.00%]** | Complete concordance between runtime engine and curated ClinVar-derived external molecular annotations across 7 classes. |
| **Secondary Protein Concordance** | Runtime $p.$ vs External $p.$ | **55** | **28** | **50.91%** | **[37.07%, 64.65%]** | Exact protein matching in 28 variants; 20 format differences from truncated frameshifts; 5 incomplete splice strings. |
| **Synthetic Robustness Controls** | Entity $A$ vs Synthetic Malformed | **18** | **18** | **100.00%** | **[81.47%, 100.00%]** | 100% graceful rejection of adversarial inputs via typed `AnalysisError`; zero unhandled runtime crashes. |
| **Software Regression Invariance** | Entity $A$ vs Entity $B$ | **55** | **55** | **100.00%** | — | 100% internal code consistency against frozen expected baseline; zero commit drift. |

### Interpretation Summary
These empirical results demonstrate that within a frozen cohort of 55 curated *HBB* variants, the deterministic engine achieves complete molecular consequence concordance with curated ClinVar-derived external molecular annotations under RefSeq `NM_000518.5`. However, these findings are bounded by the curation incorporation bias inherent to CP2.2 admission, the exclusivity of ClinVar provenance, wide statistical confidence intervals in small-sample classes (C02, C09, C11), and the complete absence of performance data for four unrepresented mutation classes (C05, C07, C08, C10).
