# CP4.4 Scientific Interpretation & Bias Audit

> **Document Type:** SCIENTIFIC METHODOLOGY, PROVENANCE, BIAS, AND CLAIM-VALIDITY AUDIT  
> **Evaluation Subject:** Phase 2C Benchmark Execution ($N = 55$, Molecular Concordance = 100.00%, 95% CI: [93.51%, 100.00%])  
> **Protocol Reference:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (Locked)  
> **Primary Dataset:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Target Software Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`  
> **Audit Status:** COMPLETED

---

## Executive Verdict

```
CP4.4 AUDIT VERDICT: SCIENTIFICALLY QUALIFIED PASS
SCIENTIFIC EVIDENCE RATING: MODERATE EVIDENCE (FOR COMPUTATIONAL DATABASE CONCORDANCE)
BIAS RISK LEVEL: HIGH SELECTION & VERIFICATION BIAS RISK
RECOMMENDED POSITIONING: CONCORDANCE EVALUATION AGAINST A CURATED CLINVAR-DERIVED EXTERNAL ANNOTATION REFERENCE
GENERALIZATION CLAIM STATUS: NOT SUPPORTED ACROSS ALL HBB MUTATION CLASSES
```

The 55/55 (100.00%, 95% Clopper-Pearson CI: [93.51%, 100.00%]) primary molecular consequence concordance result achieved in Phase 2C represents a mathematically verified and software-concordant finding on a quality-constrained, curated evaluation cohort. 

However, rigorous audit of the historical curation artifacts (`cp2_2_verification_records.json`, `cp2_3_human_review_candidates.json`) establishes that:
1. **Verification/Incorporation Bias Exists:** In stage CP2.2, candidate admission into `PROPOSED_PRIMARY` explicitly required runtime deterministic engine agreement (`comparison_status == "EXACT_AGREEMENT"`).
2. **Zero Independent Corroboration:** Exactly 0 of the 55 variants have independent biological corroboration outside of NCBI ClinVar submission records.
3. **Restricted Class Spectrum:** Four biological mutation classes (C05 In-Frame Indels, C07 In-Frame Duplications, C08 Splice Donors, and C10 5' UTR Regulatory) have zero representation ($n = 0$), and two classes (C02 Nonsense, C11 3' UTR) have small sample sizes ($n \le 3$) with wide uncertainty intervals.

Consequently, while the benchmark is **suitable for publication as a computational concordance evaluation against consensus ClinVar annotations**, it **does not support claims of independent biological validation, clinical diagnostic accuracy, or universal generalization across all HBB mutation classes**.

---

## 1. What the 55/55 Result Demonstrates

The observed 55/55 concordance result conclusively demonstrates:

1. **Deterministic Rule Execution Fidelity:** The deterministic consequence engine implemented in `backend/app/core/` correctly operationalizes canonical HGVS and molecular consequence mapping rules under `NM_000518.5` and `NG_000007.3` coordinates.
2. **Concordance with Curated ClinVar Consensus:** For clean, non-conflicting, high-confidence ($\ge 2$ stars) ClinVar records across 7 represented classes, the engine's predicted molecular consequence categories match consensus submitter assertions without discrepancy.
3. **Software Regression Invariance:** The engine reproduced 100% (55/55) of its previously frozen expected outputs (Field $B$), demonstrating absolute internal consistency and reproducibility across versions.
4. **Adversarial Error Handling Robustness:** In isolated Experiment D, the engine rejected 100% (18/18) of synthetic malformed inputs (invalid coordinates, out-of-bounds, syntax errors, and reference mismatches) with explicit, typed `AnalysisError` codes without silent mispredictions or runtime crashes.

---

## 2. What the 55/55 Result Does Not Demonstrate

In strict adherence to scientific integrity principles, the 55/55 result **does NOT** demonstrate:

1. **Independent Biological Validation:** No wet-lab experiments, patient-derived cell assays, cDNA/RNA sequencing, hemoglobin electrophoresis, or functional reporter assays were performed.
2. **Clinical or Diagnostic Accuracy:** The benchmark does not measure clinical sensitivity, clinical specificity, positive predictive value, disease prognosis, or diagnostic utility in a clinical laboratory setting.
3. **Pathogenicity Prediction Accuracy:** The benchmark evaluated molecular consequence classification (e.g. Missense, Nonsense, Splice Site), **not** clinical significance (Pathogenic vs Benign vs VUS).
4. **Universal Generalization Across All HBB Mutations:** The cohort represents only 7 of 11 biological classes, omits deep intronic and promoter variants, and excludes ambiguous or complex indels.
5. **Prospective Clinical Performance:** The evaluation cohort was curated retrospectively from a public database rather than prospectively sampled from consecutive clinical patient encounters.

---

## 3. Provenance Independence

An exhaustive audit of the 55 primary candidates in `research/manifest/phase2c_primary.json` reveals the following provenance profile:

| Provenance Attribute | Value ($N = 55$) | Percentage | Audit Finding |
|---|:---:|:---:|---|
| **Derived from NCBI ClinVar** | **55** | 100.0% | 100% of candidates originate from ClinVar VCV/RCV records |
| **Independent Non-ClinVar Corroboration** | **0** | **0.0%** | Explicitly recorded as `NONE` in manifest metadata |
| **Primary Literature Direct Linkage** | **0** | **0.0%** | Sourced via ClinVar database assertions, not primary trial literature |
| **Expert Panel Evidence (3-Star)** | **1** | 1.82% | Variant `HBB-CP2-072` (`c.67G>T`, `p.Glu23Ter`) |
| **Multiple Submitter Consensus (2-Star)** | **54** | 98.18% | Criteria provided, multiple submitters, no conflicts |
| **Single Submitter Evidence (1-Star)** | **0** | 0.0% | Relegated to Conditional cohort during CP2.3 |
| **No Assertion Criteria (0-Star)** | **0** | 0.0% | Relegated to Secondary cohort during CP2.2 |

### Database Consensus vs. Independent External Validation
The audit highlights a crucial distinction:
- **Database Consensus:** Multiple independent diagnostic laboratories or clinical submitters submitting concordant variant classifications to a central repository (ClinVar).
- **Independent External Validation:** Evaluating the software against an entirely distinct biological cohort, orthogonal database (e.g. LOVD, IthaGenes, HbVar), or prospective sequencing data that played no role in candidate curation.

The 55 primary candidates possess **high database consensus**, but **zero independent external validation**.

---

## 4. Candidate Selection Path

The candidate funnel from initial harvest to frozen primary cohort was reconstructed from historical curation files:

```
Candidate Pool (N = 314)
│
├── Synthetic Negative Controls (Class C12: N = 18) ──> Segregated to Experiment D
│
└── Biological Candidate Pool (N = 296)
    │
    ├── Disqualified in CP2.1/CP2.2 (DO_NOT_USE: N = 53)
    │   ├── Historical Phase 2B Overlap: N = 20
    │   ├── Deep Intronic / Out of Scope: N = 19
    │   └── Phase 2A Prior Exposure: N = 14
    │
    ├── Relegated in CP2.2 (REVIEW_REQUIRED: N = 73)
    │   ├── Engine Unsupported (> -50 bp Promoter): N = 31
    │   ├── HGVS Ambiguity / Complex Syntax: N = 22
    │   ├── Low Evidence Tier (0-Star) / Conflicts: N = 18
    │   └── Ontology / Class Differences: N = 2
    │
    ├── Relegated in CP2.2 (PROPOSED_SECONDARY: N = 42)
    │   └── 0-Star ClinVar records without assertion criteria
    │
    ├── Relegated in CP2.2 (CONDITIONAL: N = 9)
    │   └── Protein differences or incomplete annotations
    │
    └── Eligible Primary Pool in CP2.2 (PROPOSED_PRIMARY: N = 119)
        │
        ├── Relegated in CP2.3 (CONDITIONAL: N = 64)
        │   ├── 1-Star Single Submitter ClinVar Evidence: N = 63
        │   └── Large Multi-Codon Deletion (25 codons): N = 1
        │
        └── Approved in CP2.3 / CP2.3.1 (APPROVED: N = 55)
            └── ≥ 2-Star ClinVar Consensus, Fully Concordant with Engine
                │
                └── Formally Locked in CP2.3.2 & Frozen in CP3
                    └── PRIMARY EVALUATION COHORT (N = 55)
```

---

## 5. Selection / Verification Bias Assessment

The audit evaluated six specific mechanisms through which incorporation and verification bias could have entered the evaluation cohort:

| # | Bias Assessment Item | Finding | Evidence & Audit Trail |
|:---:|---|:---:|---|
| **A** | **Candidate selection used the deterministic engine consequence** | **YES** | In `research/curation/run_independent_verification.py` (lines 83–118), every candidate in the pool was evaluated by `evaluate_consequence` to populate `engine_molecular_consequence` and `engine_protein_consequence`. |
| **B** | **Candidate eligibility depended on agreement with deterministic output** | **YES** | In `run_independent_verification.py` (lines 231–246), assignment to `eligibility_state = "PROPOSED_PRIMARY"` explicitly required `comparison_status == "EXACT_AGREEMENT"`. Variants with discrepancies were diverted. |
| **C** | **Human approval depended on agreement with deterministic output** | **YES** | In `run_cp2_3_human_review.py` (lines 8–10, 99–101), the review workflow exclusively ingested candidates from `PROPOSED_PRIMARY` and automatically rejected any candidate with `MOLECULAR_CONSEQUENCE_CONFLICT`. |
| **D** | **External annotation was normalized after seeing deterministic output** | **YES** | During CP4/CP4.1/CP4.2, normalization rules for truncated frameshifts (`E7fs`) and canonical splice acceptors (C09) were defined with full knowledge of the candidate set to accurately represent ClinVar idioms. |
| **E** | **Conflicting candidates were preferentially removed because of engine disagreement** | **YES** | In `run_independent_verification.py` (lines 225–246), candidates where the engine failed (`not engine_success`) or where `conflict_status == "CONFLICT_DETECTED"` were relegated to `REVIEW_REQUIRED` or `DO_NOT_USE`. |
| **F** | **Candidates with engine/external disagreement were moved into conditional/review groups** | **YES** | Variants exhibiting format differences or missing external protein strings were diverted to `CONDITIONAL` or `REVIEW_REQUIRED`, leaving only concordant cases in the primary set. |

### Methodological Interpretation of Verification Bias
In clinical epidemiology, **verification bias** occurs when the outcome of a preliminary assessment influences whether a subject is included in the final evaluation cohort. 

Because candidate eligibility during CP2.2 was conditioned on `comparison_status == "EXACT_AGREEMENT"`, the resulting 55-variant primary cohort is an **artificially enriched, concordant subset**. The 55/55 (100%) result represents **internal pipeline self-consistency and deterministic rule verification**, rather than a blind, unselected prospective test.

---

## 6. ClinVar Dependence

The benchmark is formally characterized as:
> *A deterministic rule-based molecular consequence engine evaluated against a frozen external annotation reference derived from NCBI ClinVar consensus submissions.*

### Descriptor Evaluation:
- **Independent Validation:** **UNSUPPORTED.** Sourced exclusively from ClinVar; no secondary orthogonal dataset; selection was not independent of engine output.
- **External Validation:** **PARTIALLY SUPPORTED / STRICTLY LIMITED.** External in the narrow sense that annotations were authored by third-party ClinVar submitters, but not an independent external cohort in the clinical trial sense.
- **Biological Validation:** **UNSUPPORTED.** No biological material, laboratory testing, or functional assays were involved.
- **Clinical Validation:** **UNSUPPORTED.** No clinical patient outcomes or diagnostic performance characteristics were evaluated.
- **Database Concordance:** **FULLY SUPPORTED.** High concordance against multi-submitter consensus entries in ClinVar.
- **Computational Concordance Against an External Reference:** **FULLY SUPPORTED & PREFERRED.** The most scientifically accurate descriptor.

---

## 7. Exclusion and Conditional Candidate Analysis

Analysis of the 241 candidates excluded from the primary cohort reveals a clear pattern of **spectrum bias**:

1. **Exclusion of Complex Indels:** In-frame indels (Class C05) and duplications (Class C07) were largely excluded or relegated to secondary/review because of multi-codon length, ambiguous alignment, or single-submitter status.
2. **Exclusion of Promoter Variants (Class C10):** All 33 queried promoter variants ($> -50$ bp upstream) were excluded because they physically exceed the 5' transcript boundary of RefSeq `NM_000518.5`.
3. **Exclusion of Deep Intronic Variants:** 19 intronic variants located outside canonical $\pm 1, 2, 5$ splice junctions were excluded as out of deterministic engine scope.
4. **Relegation of Single-Submitter Evidence:** 63 candidates with 1-star ClinVar evidence were placed in `CONDITIONAL`, even though the engine agreed with their molecular annotations.

**Audit Conclusion:** The excluded and conditional candidates represent systematically harder, more ambiguous, or boundary-testing cases. By filtering these cases out, the primary benchmark was restricted to the most straightforward, canonical mutation types.

---

## 8. Class Coverage

The primary cohort exhibits severe class imbalance and representation gaps across the 11 biological classes:

```
Represented Classes (7 / 11):
  C01 (Missense SNVs):                        n = 14 (Adequate)
  C02 (Nonsense / Stop-Gain):                  n = 3  (Small N; wide CI [29.24%, 100.0%])
  C03 (Synonymous / Silent):                  n = 10 (Adequate)
  C04 (Frameshift Deletions):                  n = 9  (Adequate)
  C06 (Frameshift Duplications / Insertions):  n = 12 (Adequate)
  C09 (Splice Acceptor Disruptions):          n = 5  (Small N; wide CI [47.82%, 100.0%])
  C11 (3' UTR Regulatory Variants):           n = 2  (Small N; wide CI [15.81%, 100.0%])

Unrepresented Classes (4 / 11):
  C05 (In-Frame Indels / Deletions):           n = 0  (NOT REPRESENTED)
  C07 (In-Frame Insertions / Duplications):   n = 0  (NOT REPRESENTED)
  C08 (Splice Donor Disruptions):              n = 0  (NOT REPRESENTED)
  C10 (5' UTR Regulatory Variants):           n = 0  (NOT REPRESENTED)
```

### Implications for Claim Scope
- **Claim Across "All HBB Mutation Classes":** **UNSUPPORTED.** Claims cannot span classes where $n = 0$.
- **Small-N Classes:** Classes C02 ($n=3$) and C11 ($n=2$) have exact 95% Clopper-Pearson confidence interval lower bounds of 29.24% and 15.81%, reflecting massive statistical uncertainty despite 100% sample concordance.
- **Defensible Scope:** Claims must be strictly bounded to:
  > *Canonical coding SNVs (missense, nonsense, synonymous), small frameshift indels, canonical splice acceptor disruptions, and 3' UTR noncoding SNVs meeting quality criteria under NM_000518.5.*

---

## 9. Endpoint Validity

The benchmark endpoint is strictly:
$$\\text{Primary Endpoint} = \\text{Deterministic Molecular Consequence Concordance } (A_{\\text{mol}} == C_{\\text{mol}})$$

### Non-Evaluated Domains (Explicitly Confirmed):
- Pathogenicity classification (Pathogenic vs Benign)
- Clinical disease severity (Thalassemia major vs intermedia vs trait)
- Patient phenotype or clinical outcome
- Diagnostic sensitivity and specificity
- Carrier screening performance

### Orthogonality of Clinical Significance:
The benchmark confirmed that clinical significance conflicts (e.g. 8 candidates with conflicting assertions in ClinVar) were kept strictly orthogonal to the molecular endpoint. Variants with differing clinical interpretations were evaluated exclusively on their molecular consequence category without penalizing or biasing the molecular concordance metric.

---

## 10. Protein Endpoint Interpretation

The secondary protein endpoint breakdown ($N = 55$) demonstrates transparent reporting without conflating molecular and protein outcomes:

| Protein Consequence Category | Count | Proportion | Impact on Primary Endpoint | Scientific Meaning |
|---|:---:|:---:|:---:|---|
| **Exact Protein Matches** | **28** | 50.91% | MATCH | Exact nomenclature agreement under RefSeq coordinates |
| **Protein Format Differences** | **20** | 36.36% | MATCH | Truncated frameshift notation (`E7fs`) in ClinVar vs full HGVS in engine |
| **Incomplete External Protein Strings** | **5** | 9.09% | MATCH | Canonical splice acceptor (C09) records where ClinVar provides no protein string |
| **Non-Coding (Not Applicable)** | **2** | 3.64% | MATCH | 3' UTR variants (C11) where no translated protein product exists |

**Audit Confirmation:** Protein format variations and missing ClinVar protein strings were properly segregated into secondary metrics and did not contaminate or inflate the primary molecular consequence concordance.

---

## 11. Statistical Interpretation

### What $N = 55$, $55/55$, 95% CI [93.51%, 100.00%] Means:
- On this specific quality-filtered cohort of 55 variants, the observed sample concordance is 100.00%.
- Under exact binomial sampling assumptions (Clopper-Pearson), the 95% confidence interval indicates that if variants were sampled from a universe identical to this quality-filtered cohort, the true concordance rate would exceed 93.51% with 95% confidence.

### What the Confidence Interval Does NOT Mean:
- It does **not** estimate performance across the general human population or random clinical sequencing runs.
- It does **not** provide any statistical estimate for the 4 unrepresented mutation classes ($n=0$).
- It does **not** account for verification bias introduced during candidate filtering.
- $N = 55$ is insufficient to detect rare edge-case failure modes or establish broad clinical generalizability.

---

## 12. Leakage / Post-Hoc Integrity

Post-benchmark immutability verification confirmed:

- **Dataset Byte-for-Byte Integrity:** SHA256 of `research/manifest/phase2c_primary.json` remains `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` (Unchanged).
- **Protocol Integrity:** SHA256 of `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` remains `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` (Unchanged).
- **Engine Software Immutability:** Engine commit remains `845f595cc039e006d74237945450c7b4a9569ee6` with zero diffs in `backend/app/core/`.
- **Zero Post-Hoc Manipulations:** Zero candidates were added, removed, or reclassified after freeze. Zero benchmark reruns with altered parameters were performed.

---

## 13. Claim Ladder

To guide manuscript preparation and scientific dissemination, claims are stratified into three distinct evidentiary levels:

```
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 1: DIRECTLY SUPPORTED BY EVIDENCE                                │
│ • 100% molecular consequence concordance on the frozen N=55 cohort     │
│ • Exact Clopper-Pearson 95% CI of [93.51%, 100.00%] on frozen cohort   │
│ • Concordance with curated multi-submitter ClinVar consensus           │
│ • Deterministic rule reproduction under NM_000518.5 standards          │
│ • 100% graceful rejection of 18 synthetic negative controls           │
│ • 100% software self-consistency against frozen expected outputs      │
├────────────────────────────────────────────────────────────────────────┤
│ LEVEL 2: REASONABLE BUT LIMITED (REQUIRES EXPLICIT QUALIFICATION)      │
│ • High concordance for canonical coding SNVs and small frameshifts     │
│ • Computational reliability on high-confidence, non-conflicting records│
│ • Robust handling of standard HGVS syntax edge cases                   │
├────────────────────────────────────────────────────────────────────────┤
│ LEVEL 3: NOT SUPPORTED BY EVIDENCE (STRICTLY PROHIBITED IN MANUSCRIPT) │
│ • "100% biological accuracy"                                           │
│ • "100% HBB mutation detection accuracy"                               │
│ • "Clinical accuracy" or "Diagnostic accuracy"                         │
│ • "Pathogenicity prediction accuracy"                                  │
│ • "Universal generalization across all HBB mutation classes"           │
│ • "Independent biological validation"                                  │
│ • "Clinical validation" or "Diagnostic utility"                        │
│ • Use of "Ground truth" to describe ClinVar submissions                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 14. Recommended Paper Positioning

### Candidate Descriptions Evaluated:
- **A. "Validation of an HBB mutation analyzer":** Inaccurate (Overstates validation scope).
- **B. "Clinical validation of an HBB mutation analyzer":** Factually false (No clinical validation occurred).
- **C. "Biological validation of an HBB mutation analyzer":** Factually false (No biological assays performed).
- **D. "Computational evaluation of deterministic HBB molecular consequence prediction":** Acceptable, but misses comparator specificity.
- **E. "Concordance evaluation of deterministic HBB molecular consequence prediction against a curated ClinVar-derived external annotation reference":** **STRONGEST & SCIENTIFICALLY SAFEST.**

### Rationale:
Description E is fully truthful, scientifically precise, and transparent:
1. It replaces "validation" with "concordance evaluation".
2. It explicitly identifies the evaluated capability as "deterministic molecular consequence prediction".
3. It precisely specifies the comparison oracle as a "curated ClinVar-derived external annotation reference".

---

## 15. Formal Limitation Register

The following 15 limitations are formally documented:

1. **ClinVar Dependence:** Sourced exclusively from NCBI ClinVar submission records; no external secondary databases used.
2. **Zero Independent Non-ClinVar Corroboration:** Exactly 0 of 55 variants have corroboration from independent cohorts or registries.
3. **Verification / Selection Bias Risk:** Initial candidate filtering in CP2.2 incorporated deterministic engine agreement into primary cohort eligibility.
4. **Cohort Size ($N = 55$):** $N = 55$ represents a modest sample size that cannot reveal rare boundary edge cases.
5. **Zero Representation of In-Frame Deletions (C05):** $n = 0$; performance on multi-codon in-frame deletions remains unmeasured.
6. **Zero Representation of In-Frame Duplications (C07):** $n = 0$; performance on in-frame duplications remains unmeasured.
7. **Zero Representation of Splice Donors (C08):** $n = 0$; performance on canonical splice donor disruptions remains unmeasured.
8. **Zero Representation of 5' UTR / Promoters (C10):** $n = 0$; performance on upstream promoter variants remains unmeasured.
9. **Small Sample Size for Nonsense (C02) & 3' UTR (C11):** $n = 3$ and $n = 2$ yield wide 95% confidence intervals ([29.24%, 100%] and [15.81%, 100%]).
10. **Curated vs. Prospectively Sampled Cohort:** Selected through quality filtering rather than consecutive unselected clinical sampling.
11. **Molecular Consequence Endpoint Only:** Evaluates consequence classification; does not evaluate pathogenicity, phenotype, or severity.
12. **No Clinical Validation:** No patient cohorts, clinical sensitivity/specificity, or diagnostic utility measured.
13. **No Phenotype Validation:** No correlation with fetal hemoglobin levels, hematologic indices, or clinical presentation.
14. **No Wet-Lab Validation:** No sequencing, functional cloning, minigene assays, or mass spectrometry validation.
15. **No Independent Prospective Dataset:** Evaluation was retrospective without a dedicated held-out prospective cohort.

---

## 16. Scientific Evidence Rating

### Rating Assigned: **B. MODERATE EVIDENCE**

### Evidentiary Rationale:
- **Why NOT "Strong Evidence":** Strong evidence requires independent prospective cohorts, multiple distinct data sources, absence of verification bias, and complete coverage across all mutation classes. The present study exhibits verification bias, zero non-ClinVar corroboration, and 4 unrepresented classes.
- **Why NOT "Insufficient / Preliminary Evidence":** The software demonstrated flawless deterministic execution across 55 quality-audited variants, 100% software regression invariance, 100% graceful rejection of 18 adversarial negative controls, complete AST anti-leakage isolation, and transparent reporting of secondary protein differences.
- **Why "Moderate Evidence":** When accurately scoped as a **computational concordance evaluation against curated ClinVar consensus**, the methodology is rigorous, auditable, and repeatable.

---

## 17. Final Conclusion

The Phase 2C primary benchmark provides **moderate scientific evidence** supporting the computational fidelity and deterministic consequence prediction of the HBB Gene Mutation Analyzer against high-confidence ClinVar consensus records.

The 55/55 ($100.00\%$) result is **suitable for publication in a peer-reviewed research manuscript**, provided that:
1. The study is positioned in accordance with **Description E** (Concordance evaluation against a ClinVar-derived external reference).
2. The **15 formal limitations** are prominently disclosed in the Discussion section.
3. Claims are strictly restricted to **Level 1** and qualified **Level 2** formulations, with complete exclusion of prohibited **Level 3** claims.
4. No further benchmark runs are executed on this dataset prior to manuscript drafting.
