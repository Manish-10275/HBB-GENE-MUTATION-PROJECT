# Phase 5.1 — Manuscript Evidence Matrix

> **Document Type:** SCIENTIFIC EVIDENCE MAPPING & GOVERNANCE MATRIX  
> **Target Manuscript:** HBB Gene Mutation Analyzer Research Manuscript  
> **Stage:** Phase 5.1 (Pre-Drafting Evidence Lock)  
> **Source Evidence Base:** Phase 2C Frozen Benchmark ($N = 55$), Robustness Cohort ($N = 18$), CP2 Curation Audits, CP4 Comparison Corrections, and CP4.3/CP4.3A/CP4.4 Audits  
> **Governing Protocol:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (Locked)  
> **Dataset Hash:** `research/manifest/phase2c_primary.sha256` (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Engine Software Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`  
> **Immutability Status:** READ-ONLY EVIDENCE COMPILATION — NO BENCHMARK RERUNS OR DATA MODIFICATIONS

---

## 1. Executive Summary & Audit Overview

This evidence matrix establishes the mandatory scientific guardrails for manuscript drafting. Every potential scientific assertion, title phrasing, abstract sentence, methodology description, and discussion claim is cross-referenced against the empirical artifacts produced in Phase 2C and audited in CP4.3, CP4.3A, and CP4.4.

### Evidence Status Definitions
- **Status A (Directly Supported):** Directly established by frozen code, manifest data, unit tests, or audited benchmark execution.
- **Status B (Supported with Qualification):** Defensible only when accompanied by explicit boundary conditions, sample size disclosures, or methodological qualifications.
- **Status C (Not Established from Project Artifacts):** Literature or background concepts that the software project itself did not empirically evaluate. Must be cited from external literature or omitted.
- **Status D (Prohibited):** Unsupported or scientifically false claims that materially misrepresent the study. Strictly prohibited from appearing anywhere in the manuscript.

---

## 2. Recommended Central Claim

The entire manuscript must be constructed around a single, scientifically defensible central claim:

> **Recommended Manuscript Central Claim:**  
> *"Concordance evaluation of deterministic HBB molecular consequence prediction against a curated ClinVar-derived external annotation reference."*

### Extended Results Version (for Abstract & Results opening):
> *"Within a frozen primary cohort of 55 curated HBB variants, deterministic molecular consequence predictions were concordant with the corresponding ClinVar-derived external molecular annotations for all 55 variants (100.00%, exact 95% Clopper-Pearson CI: [93.51%, 100.00%])."*

### Mandatory Immediate Qualification (must immediately follow):
> *"This evaluation establishes computational rule fidelity and database consensus concordance on high-confidence, non-conflicting records under NM_000518.5, but does not constitute independent biological validation, clinical diagnostic validation, or performance across unrepresented mutation classes."*

---

## 3. Title Concepts Evaluation

| Claim ID | Title Proposal | Evidence Status | Scientific Risk | Permitted / Not Permitted | Methodological Rationale |
|:---:|---|:---:|:---:|:---:|---|
| **CLM-TIT-01** | *"Validation of an HBB Mutation Analyzer"* | **Status D** | **CRITICAL** | **PROHIBITED** | Uses unqualified "Validation", which falsely implies independent biological or clinical truth. |
| **CLM-TIT-02** | *"Clinical Validation of an HBB Mutation Analyzer"* | **Status D** | **CRITICAL** | **PROHIBITED** | Factually false. Zero patient cohorts, diagnostic sensitivity/specificity, or clinical utility were evaluated. |
| **CLM-TIT-03** | *"Biological Validation of an HBB Mutation Analyzer"* | **Status D** | **CRITICAL** | **PROHIBITED** | Factually false. Zero in vitro assays, cDNA sequencing, or wet-lab experiments were conducted. |
| **CLM-TIT-04** | *"Computational Evaluation of Deterministic HBB Molecular Consequence Prediction"* | **Status B** | **LOW** | **PERMITTED (QUALIFIED)** | Truthful regarding computational nature, but omits the comparator source (ClinVar). |
| **CLM-TIT-05** | *"Concordance Evaluation of Deterministic HBB Molecular Consequence Prediction Against a Curated ClinVar-Derived External Annotation Reference"* | **Status A** | **LOW** | **RECOMMENDED** | **Strongest defensible title.** Fully discloses the evaluation type (concordance), mechanism (deterministic), and comparator (curated ClinVar reference). |

---

## 4. Master Manuscript Evidence Matrix

### 4.1 Abstract Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-ABS-01** | The system performs deterministic HBB molecular consequence prediction. | **A** | `backend/app/core/consequences.py` | Line 15 (`evaluate_consequence`) | "implements a deterministic rule-based molecular consequence engine" | Must state deterministic algorithm based on transcript coordinates | "AI-powered consequence prediction", "biological discovery" | **LOW** |
| **CLM-ABS-02** | The system uses a defined reference transcript. | **A** | `research/manifest/phase2c_primary.json` | Lines 5–7 (`reference_transcript`, `reference_sequences`) | "referenced strictly against RefSeq NM_000518.5 and NG_000007.3" | Must state transcript version explicitly | "universal genome build", "transcript-agnostic" | **LOW** |
| **CLM-ABS-03** | The primary benchmark evaluated exactly 55 variants. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `metadata.cohort_counts.primary_n` | "evaluated across a frozen primary cohort of 55 curated variants" | Must note cohort was curated and quality-filtered | "unselected prospective cohort", "random clinical sample" | **LOW** |
| **CLM-ABS-04** | Primary molecular concordance was 55/55. | **A** | `research/results/phase2c_benchmark_candidate_results.json` | All 55 entries (`primary_endpoint_status: "MATCH"`) | "achieved 55/55 molecular consequence concordance" | Must specify comparator is ClinVar consensus annotations | "55/55 biological accuracy", "55/55 diagnostic successes" | **MEDIUM** |
| **CLM-ABS-05** | Observed molecular concordance was 100%. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.percentage` (100.0) | "yielding 100.00% sample concordance within the frozen cohort" | Must clarify sample percentage on quality-constrained set | "100% accurate", "zero software errors globally" | **HIGH** |
| **CLM-ABS-06** | Exact 95% CI is 93.51% to 100.00%. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.ci_95_clopper_pearson` | "with an exact Clopper-Pearson 95% confidence interval of [93.51%, 100.00%]" | Must explain CI applies to cohort population model, not all HBB variants | Normal approximation intervals (Wald, Wilson) | **MEDIUM** |
| **CLM-ABS-07** | Protein representation differences occurred in frameshifts. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.protein_consequence_concordance` | "secondary protein nomenclature differences occurred in 20 truncated frameshifts" | Must report protein concordance separately (50.91% exact match) | Falsely claiming "100% exact protein agreement" | **MEDIUM** |
| **CLM-ABS-08** | 18 synthetic negative controls were gracefully rejected. | **A** | `research/results/phase2c_robustness_results.json` | All 18 entries (`robustness_status: "GRACEFULLY_REJECTED"`) | "rejected 18/18 synthetic malformed inputs with typed AnalysisError codes" | Must state controls are synthetic and kept separate from primary cohort | Conflating robustness controls with biological specificity | **LOW** |
| **CLM-ABS-09** | The study validates the biological accuracy of the system. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 2, Item 1 | NONE | NONE | "biologically validated", "biological truth", "experimentally verified" | **CRITICAL** |
| **CLM-ABS-10** | The study validates clinical accuracy or utility. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 2, Item 2 | NONE | NONE | "clinically validated", "diagnostic accuracy", "clinical grade" | **CRITICAL** |
| **CLM-ABS-11** | The study validates pathogenicity prediction. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 9 | NONE | NONE | "pathogenicity accuracy", "predicts benign vs pathogenic" | **CRITICAL** |
| **CLM-ABS-12** | The study demonstrates generalization across all HBB mutation classes. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 8 | NONE | NONE | "generalizes to all HBB variants", "class-comprehensive" | **CRITICAL** |
| **CLM-ABS-13** | The evaluation cohort was derived from ClinVar. | **A** | `research/manifest/phase2c_primary.json` | All 55 entries (`clinvar_variation_id`) | "derived from consensus submissions in NCBI ClinVar" | Must state it is a database-derived comparator | "multicenter clinical registry", "prospective patient cohort" | **LOW** |
| **CLM-ABS-14** | Engine agreement influenced primary cohort admission. | **A** | `research/curation/run_independent_verification.py` | Lines 231–246 (`comparison_status == "EXACT_AGREEMENT"`) | "candidate eligibility incorporated deterministic agreement during curation" | Must disclose as potential verification bias | Concealing engine-informed cohort filtering | **CRITICAL** |
| **CLM-ABS-15** | Independent non-ClinVar corroboration was absent. | **A** | `research/manifest/phase2c_primary.json` | Key `independent_non_clinvar_corroboration: "NONE"` | "zero variants possessed independent biological corroboration outside ClinVar" | Must disclose in Abstract and Discussion | Falsely claiming "multi-database cross-validation" | **HIGH** |

---

### 4.2 Introduction Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-INT-01** | HBB variants require precise transcript-specific coordinate interpretation. | **C** | `docs/PHASE_2C_PROTOCOL_SPECIFICATION.md` | Section 1 (Background rationale) | "Standardized HBB variant interpretation relies on coordinate mapping against NM_000518.5" | Must cite HGVS guidelines and ClinGen hemoglobinopathy specs | Claiming the software established the medical necessity | **LOW** |
| **CLM-INT-02** | Deterministic engines eliminate LLM hallucinations in consequence prediction. | **A** | `backend/app/core/consequences.py` | Entire module (pure Python AST, zero LLM calls) | "deterministic rule engines execute consequence logic without generative model stochasticity" | Must clarify AI is used only in evidence summarization layer | "AI performs molecular consequence reasoning" | **LOW** |
| **CLM-INT-03** | Legacy codon numbering creates widespread discordance in hemoglobin records. | **A** | `research/results/PHASE2C_ERROR_REGISTER.md` | Section 3 (33 variants with legacy records) | "33 of 55 variants exhibit legacy codon designations (-1 codon offset)" | Must cite clinical practice of mature protein numbering (e.g. CD 6 vs p.Glu7) | "Engine solved legacy nomenclature ambiguity" | **LOW** |
| **CLM-INT-04** | Reference sequence divergence can cause silent misclassification. | **A** | `backend/app/core/reference.py` | Reference validation logic | "consequence prediction requires strict alignment to validated transcript sequences" | Must specify NM_000518.5 / NG_000007.3 | "Engine operates universally on arbitrary FASTA" | **LOW** |
| **CLM-INT-05** | Molecular consequence must be strictly separated from clinical pathogenicity. | **A** | `research/protocol/CP4_1_DECISION_MATRIX.md` | Section 3.3 (Clinical significance orthogonality) | "molecular impact classification is orthogonal to clinical pathogenicity assertions" | Must note ClinVar assertions often vary while consequence remains fixed | Conflating consequence with ACMG pathogenicity | **LOW** |
| **CLM-INT-06** | Public databases contain variable evidence tiers and conflicting submissions. | **A** | `research/curation/cp2_2_verification_records.json` | 30 conflicts detected across 314 candidates | "database repositories aggregate records ranging from single submitters to expert panels" | Must cite ClinVar star rating system | "ClinVar is completely verified ground truth" | **LOW** |
| **CLM-INT-07** | LLMs should be restricted to literature summarization, not consequence calculation. | **A** | `backend/app/ai.py` | Architecture boundary (calls Gemini for text only) | "generative language models are restricted to evidence retrieval and summarization" | Must emphasize primary endpoint is 100% deterministic | "Gemini computes the molecular consequence" | **LOW** |
| **CLM-INT-08** | Need for auditable, transparent benchmark protocols for clinical genetics software. | **C** | `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | Section 1 (Protocol rationale) | "software benchmarking requires auditable, version-locked evaluation protocols" | Cite FDA / regulatory guidance on computational validity | Claiming Phase 2C is an FDA clearance study | **LOW** |

---

### 4.3 Methods Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-MET-01** | Reference sequence model uses NM_000518.5 and NG_000007.3. | **A** | `backend/app/core/reference.py` | Functions `load_reference`, `load_genomic_reference` | "built upon RefSeq NM_000518.5 (cDNA) and NG_000007.3 (genomic)" | Coordinates strictly 1-based standard RefSeq | "GRCh38 whole genome native" | **LOW** |
| **CLM-MET-02** | Deterministic HGVS parsing handles SNVs, indels, duplications, and splice variants. | **A** | `backend/app/core/hgvs.py` | Function `parse_hgvs` | "parses canonical HGVS cDNA syntax for substitutions, indels, duplications, and splice junctions" | Does not support complex rearrangements or structural inversions | "supports all possible genomic variants" | **LOW** |
| **CLM-MET-03** | Molecular consequence is computed via codon-level translation. | **A** | `backend/app/core/consequences.py` | Functions `_evaluate_coding_snv`, `_evaluate_frameshift` | "evaluates open reading frame alterations using Biopython codon translation tables" | Based on standard genetic code under NM_000518.5 CDS | "machine learning consequence model" | **LOW** |
| **CLM-MET-04** | Evidence layer integrates ClinVar and PubMed with provenance tracking. | **A** | `backend/app/variants.py`, `backend/app/ai.py` | External query logic and caching | "fetches ClinVar VCV records and literature citations with source provenance" | Live external queries separated from deterministic consequence engine | "Engine relies on live internet to classify" | **LOW** |
| **CLM-MET-05** | AI research copilot is strictly decoupled from consequence engine. | **A** | `backend/app/ai.py` | Summarization prompts | "AI copilot performs isolated text summarization without modifying consequence outputs" | Must verify AST isolation of deterministic engine | "AI assists in molecular consequence logic" | **LOW** |
| **CLM-MET-06** | Primary evaluation cohort is frozen at N = 55. | **A** | `research/manifest/phase2c_primary.json` | Dataset header (`candidates: 55 items`) | "primary evaluation cohort was locked and frozen at N = 55" | Must state freeze occurred in CP3 before benchmark execution | "dynamically updated benchmark cohort" | **LOW** |
| **CLM-MET-07** | Dataset immutability is cryptographically enforced via SHA256. | **A** | `research/manifest/phase2c_primary.sha256` | Hash `39eb60de...` | "dataset immutability verified byte-for-byte by SHA256 hash" | Hash verified identical before and after benchmark runs | Any unstaged modification | **LOW** |
| **CLM-MET-08** | Engine software version is locked to Git commit 845f595. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `metadata.engine_commit` (`845f595...`) | "executed against deterministic engine commit 845f595" | Commit verified with zero diffs in backend core | Running modified or uncommitted code | **LOW** |
| **CLM-MET-09** | Benchmark protocol is governed by locked protocol hash e4bad0a. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `metadata.protocol_sha256` (`e4bad0a...`) | "comparison governed by locked protocol PHASE2C_BENCHMARK_PROTOCOL.md" | Protocol locked in CP3 prior to execution | Altering protocol rules post-hoc | **LOW** |
| **CLM-MET-10** | Primary endpoint evaluates A vs C, strictly isolating B. | **A** | `research/curation/phase2c_comparison_engine.py` | Function `evaluate_external_concordance` | "primary endpoint compares runtime engine output (A) directly against external annotation (C)" | Field B used only for isolated software regression | Allowing Field B to influence comparison category | **HIGH** |
| **CLM-MET-11** | Robustness evaluated using 18 synthetic negative controls in Experiment D. | **A** | `research/results/phase2c_robustness_results.json` | 18 records (Class C12) | "adversarial robustness evaluated using 18 synthetic malformed inputs" | Kept strictly segregated from biological primary denominator | Merging C12 into primary 55-variant cohort | **LOW** |
| **CLM-MET-12** | Confidence intervals calculated via exact Clopper-Pearson method. | **A** | `research/curation/run_phase2c_benchmark.py` | Function `clopper_pearson_interval` | "confidence intervals computed using the exact Clopper-Pearson binomial method" | Must note exact binomial formulation without normal approximation | Wald asymptotic approximation | **LOW** |

---

### 4.4 Curation Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-CUR-01** | Initial candidate pool contained 314 variants. | **A** | `research/curation/candidate_pool.json` | Header `candidates: 314 items` | "initial harvested pool comprised 314 variant records" | Comprised 296 biological and 18 synthetic controls | "314 patient cases" | **LOW** |
| **CLM-CUR-02** | Biological candidates totaled 296 entries. | **A** | `research/curation/cp2_2_verification_records.json` | 296 entries with `target_class_id != "C12"` | "296 candidate records represented human biological variants" | Sourced from ClinVar queries for HBB | "296 independent mutations" | **LOW** |
| **CLM-CUR-03** | 53 variants disqualified under exclusion registry. | **A** | `research/curation/exclusion_registry.json` | Keys `total_manifest_records: 140` | "53 candidates disqualified due to historical Phase 2B overlap, prior exposure, or deep intronic coordinates" | Disclosed in CP2.1/CP2.2 | "arbitrarily removed" | **LOW** |
| **CLM-CUR-04** | 73 variants relegated to review required. | **A** | `research/curation/cp2_2_verification_records.json` | Filter `eligibility_state == "REVIEW_REQUIRED"` | "73 candidates placed in review due to promoter boundaries, syntax ambiguity, or ontology conflicts" | Disclosed as boundary limitations | "unexplained exclusions" | **LOW** |
| **CLM-CUR-05** | 64 candidates relegated to conditional status in CP2.3. | **A** | `research/curation/CP2_3_DECISION_SUMMARY.md` | Section 1 (`CONDITIONAL: 64`) | "64 concordant candidates relegated to conditional cohort due to 1-star single submitter status" | Consequence concordant but evidence lower tier | "rejected for engine error" | **MEDIUM** |
| **CLM-CUR-06** | 55 candidates formally approved for primary cohort. | **A** | `research/curation/CP2_3_DECISION_SUMMARY.md` | Section 1 (`APPROVE: 55`) | "55 candidates approved based on ≥ 2-star multi-submitter consensus" | Became the frozen primary cohort | "55 randomly sampled variants" | **LOW** |
| **CLM-CUR-07** | All 55 primary candidates hold ≥ 2-star ClinVar ratings. | **A** | `research/manifest/phase2c_primary.json` | 54 with star=2, 1 with star=3 | "all 55 variants supported by multi-submitter consensus (54) or expert panel (1)" | Zero single-submitter (1-star) or no-criteria (0-star) | "independently validated variants" | **MEDIUM** |
| **CLM-CUR-08** | Zero primary candidates have independent non-ClinVar corroboration. | **A** | `research/manifest/phase2c_primary.json` | All 55 entries (`independent_non_clinvar_corroboration: "NONE"`) | "zero variants possessed independent biological corroboration outside ClinVar records" | Must be explicitly stated as limitation | "corroborated across multiple orthogonal databases" | **HIGH** |
| **CLM-CUR-09** | Multiple submitter consensus represents database agreement, not biological proof. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 3 | "multi-submitter ClinVar assertions reflect diagnostic laboratory consensus" | Consensus can replicate reference biases or shared interpretation rules | "proves biological ground truth" | **HIGH** |
| **CLM-CUR-10** | CP2.2 candidate admission into primary cohort required engine agreement. | **A** | `research/curation/run_independent_verification.py` | Lines 231–246 (`comparison_status == "EXACT_AGREEMENT"`) | "candidate admission to PROPOSED_PRIMARY was conditioned on deterministic engine agreement" | **MANDATORY BIAS DISCLOSURE:** introduces verification / incorporation bias | Concealing engine-informed curation filtering | **CRITICAL** |

---

### 4.5 Results Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-RES-01** | Primary molecular consequence concordance was 55/55 (100.00%). | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.k` (55), `n` (55) | "deterministic engine outputs matched external molecular annotations for 55 of 55 variants" | Evaluated against ClinVar consensus reference under NM_000518.5 | "100% biological accuracy", "perfect clinical performance" | **HIGH** |
| **CLM-RES-02** | Exact 95% Clopper-Pearson CI is [93.51%, 100.00%]. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.ci_95_clopper_pearson` | "exact 95% binomial confidence interval of [93.51%, 100.00%]" | Bounded by sample size N=55 on quality-constrained set | Claiming CI represents general population accuracy | **MEDIUM** |
| **CLM-RES-03** | 30 variants cataloged under EXACT_MOLECULAR_AGREEMENT. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.error_category_distribution.EXACT_MOLECULAR_AGREEMENT` (30) | "30 variants achieved exact agreement in both molecular category and protein nomenclature" | Represents 54.55% of primary cohort | "All 55 had exact protein agreement" | **LOW** |
| **CLM-RES-04** | 20 variants cataloged under MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.error_category_distribution.MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` (20) | "20 frameshift variants exhibited truncated syntax in ClinVar (e.g. E7fs) vs full HGVS in engine" | Primary molecular impact concordant; protein string differs in format | "20 protein errors", "20 misclassifications" | **LOW** |
| **CLM-RES-05** | 5 variants cataloged under EXTERNAL_ANNOTATION_INCOMPLETE. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.error_category_distribution.EXTERNAL_ANNOTATION_INCOMPLETE` (5) | "5 canonical splice acceptor variants lacked external protein consequence strings in ClinVar" | Primary splice disruption concordant; protein string incomplete | "5 missing data failures" | **LOW** |
| **CLM-RES-06** | Zero primary molecular consequence discrepancies were observed. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.discrepancies` (0) | "zero molecular consequence category discrepancies observed within the frozen cohort" | Bounded by the 55 curated variants evaluated | "Zero error rate across human genetics" | **HIGH** |
| **CLM-RES-07** | Exact protein nomenclature concordance was 28/55 (50.91%). | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.protein_consequence_concordance.k` (28) | "exact protein nomenclature matching occurred in 28 of 55 variants (50.91%, 95% CI: [37.07%, 64.65%])" | Reflects non-standard truncated frameshifts and missing splice protein strings in ClinVar | Concealing the 50.91% exact protein match rate | **MEDIUM** |
| **CLM-RES-08** | Class C01 (Missense) concordance was 14/14 (100.0%). | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C01` (k=14, n=14) | "14 of 14 missense variants concordant (100.0%, 95% CI: [76.84%, 100.00%])" | Adequately represented coding class | Generalizing beyond tested codons | **LOW** |
| **CLM-RES-09** | Class C02 (Nonsense) concordance was 3/3 (100.0%). | **B** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C02` (k=3, n=3) | "3 of 3 nonsense variants concordant (100.0%, 95% CI: [29.24%, 100.00%])" | Small sample size ($n=3$); wide confidence interval lower bound of 29.24% | "Robustly established nonsense accuracy" | **HIGH** |
| **CLM-RES-10** | Class C09 (Splice Acceptor) concordance was 5/5 (100.0%). | **B** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C09` (k=5, n=5) | "5 of 5 canonical splice acceptor variants concordant (100.0%, 95% CI: [47.82%, 100.00%])" | Small sample size ($n=5$); 95% CI lower bound of 47.82% | "Proves splice prediction universally" | **MEDIUM** |
| **CLM-RES-11** | Class C11 (3' UTR) concordance was 2/2 (100.0%). | **B** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C11` (k=2, n=2) | "2 of 2 3' UTR variants concordant (100.0%, 95% CI: [15.81%, 100.00%])" | Very small sample size ($n=2$); wide CI lower bound of 15.81% | "Comprehensive non-coding coverage" | **HIGH** |
| **CLM-RES-12** | Adversarial robustness was 18/18 (100.0%). | **A** | `research/results/phase2c_robustness_results.json` | All 18 rejected with typed errors | "18 of 18 synthetic negative controls rejected gracefully (100.0%, 95% CI: [81.47%, 100.00%])" | Standalone experiment; strictly segregated from primary denominator | Merging controls into primary accuracy numerator | **LOW** |
| **CLM-RES-13** | Software regression self-consistency was 55/55 (100.0%). | **A** | `research/results/phase2c_benchmark_summary.json` | Key `software_regression_metadata.k` (55) | "100% reproduction of frozen expected outputs (Field B)" | Software self-consistency metadata only; not biological concordance | Conflating regression with external validation | **MEDIUM** |

---

### 4.6 Claims About Zero-Result Classes

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-ZER-01** | Class C05 (In-Frame Indels) was not represented in primary cohort. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C05.status` | "Class C05 (in-frame deletions) was not represented in the primary cohort (n = 0)" | Performance on multi-codon in-frame deletions is unmeasured | Implying 0 errors equals 100% accuracy; reporting "0% error" | **CRITICAL** |
| **CLM-ZER-02** | Class C07 (In-Frame Duplications) was not represented in primary cohort. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C07.status` | "Class C07 (in-frame duplications) was not represented in the primary cohort (n = 0)" | Sourced variants lacked ≥ 2-star evidence; performance unmeasured | Claiming in-frame duplication support | **CRITICAL** |
| **CLM-ZER-03** | Class C08 (Splice Donor Disruptions) was not represented in primary cohort. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C08.status` | "Class C08 (splice donor disruptions) was not represented in the primary cohort (n = 0)" | Zero canonical donor variants met quality criteria in pool; unmeasured | Claiming splice donor prediction accuracy | **CRITICAL** |
| **CLM-ZER-04** | Class C10 (5' UTR Regulatory) was not represented in primary cohort. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification.C10.status` | "Class C10 (5' UTR regulatory variants) was not represented in the primary cohort (n = 0)" | Queried promoter variants (> -50 bp) exceed NM_000518.5 transcript start | Claiming promoter variant prediction capability | **CRITICAL** |

---

### 4.7 Statistical Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-STA-01** | 55/55 defines exact sample concordance on the frozen dataset. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `primary_endpoint.k` (55), `n` (55) | "represents 100.00% sample concordance on the frozen 55-variant cohort" | Restricted to this specific frozen dataset | Extrapolating to general human genetics | **LOW** |
| **CLM-STA-02** | Clopper-Pearson CI defines exact binomial interval for the cohort population model. | **A** | `research/curation/run_phase2c_benchmark.py` | Line 25 (`clopper_pearson_interval`) | "Clopper-Pearson 95% CI of [93.51%, 100.00%] reflects binomial sampling variance" | Assumes sampling from universe of variants matching cohort inclusion criteria | Extrapolating CI to unrepresented classes or clinical sequencing | **MEDIUM** |
| **CLM-STA-03** | Small-N classes exhibit broad statistical uncertainty. | **A** | `research/results/phase2c_benchmark_summary.json` | Keys `class_stratification.C02`, `C09`, `C11` | "classes with n ≤ 5 exhibit wide confidence intervals despite 100% sample agreement" | C02 lower bound is 29.24%; C11 lower bound is 15.81% | Ignoring small sample size in class claims | **MEDIUM** |
| **CLM-STA-04** | Cohort sample size (N = 55) is sufficient for universal generalization. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 11 | NONE | NONE | "N=55 proves universal generalization", "statistically definitive for all HBB variants" | **CRITICAL** |

---

### 4.8 ClinVar Comparison Reference Claims

| Claim ID | Proposed Claim | Status | Supporting Artifact | Exact Evidence Location | Permitted Wording | Required Qualification | Prohibited Wording | Scientific Risk |
|:---:|---|:---:|---|---|---|---|---|:---:|
| **CLM-CLN-01** | ClinVar consensus submissions serve as an external annotation reference. | **A** | `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | Section 3.1 | "evaluated against an external annotation reference derived from ClinVar consensus records" | External comparison reference, not biological ground truth | "ClinVar ground truth", "gold standard truth" | **HIGH** |
| **CLM-CLN-02** | 2-star ratings denote multiple submitters without conflict. | **A** | `research/manifest/phase2c_primary.json` | Field `clinvar_review_status` (54 records) | "54 variants possessed 2-star ratings denoting criteria provided, multiple submitters, no conflicts" | Reflects diagnostic laboratory submission consensus | Interpreting consensus as wet-lab proof | **MEDIUM** |
| **CLM-CLN-03** | 3-star ratings denote expert panel review. | **A** | `research/manifest/phase2c_primary.json` | Field `clinvar_review_status` (1 record: `HBB-CP2-072`) | "1 variant possessed 3-star expert panel review status" | Represents formal curation panel assertion | "Experimentally validated in our laboratory" | **LOW** |
| **CLM-CLN-04** | ClinVar consensus establishes independent biological truth. | **D** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 3 | NONE | NONE | "ClinVar is biological truth", "independent biological truth" | **CRITICAL** |

---

### 4.9 Limitation Claims (Mandatory Disclosure Register)

| Claim ID | Limitation Description | Status | Supporting Artifact | Exact Evidence Location | Mandatory Disclosure Requirement | Scientific Risk |
|:---:|---|:---:|---|---|---|:---:|
| **CLM-LIM-01** | **Incorporation / Verification Bias:** CP2.2 candidate admission required engine agreement. | **A** | `research/curation/run_independent_verification.py` | Lines 231–246 | Must disclose prominently in Methods & Discussion: primary cohort was filtered by engine concordance. | **CRITICAL** |
| **CLM-LIM-02** | **ClinVar Dependence:** Sourced exclusively from NCBI ClinVar records. | **A** | `research/manifest/phase2c_primary.json` | All entries (`clinvar_variation_id`) | Must state study depends entirely on a single public submission database. | **HIGH** |
| **CLM-LIM-03** | **Zero Independent Non-ClinVar Corroboration:** No secondary registries or orthogonal databases. | **A** | `research/manifest/phase2c_primary.json` | Key `independent_non_clinvar_corroboration: "NONE"` | Must disclose zero non-ClinVar corroborations were obtained. | **HIGH** |
| **CLM-LIM-04** | **Curated vs. Prospective Cohort:** Quality-filtered retrospective set rather than prospective sample. | **A** | `research/curation/CP2_3_DECISION_SUMMARY.md` | Funnel documentation | Must state cohort was curated retrospectively and does not represent prospective prevalence. | **MEDIUM** |
| **CLM-LIM-05** | **Spectrum / Selection Bias:** Complex indels, promoter, and deep intronic variants excluded. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 7 | Must disclose that excluded/conditional variants represent systematically more challenging cases. | **HIGH** |
| **CLM-LIM-06** | **Class Absence (C05, C07, C08, C10):** 4 of 11 biological classes completely unrepresented. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `class_stratification` (n=0 for 4 classes) | Must explicitly enumerate unrepresented classes; performance is unmeasured. | **CRITICAL** |
| **CLM-LIM-07** | **Small Sample Size for C02 and C11:** n=3 and n=2 yield broad statistical uncertainty. | **A** | `research/results/phase2c_benchmark_summary.json` | Keys `class_stratification.C02`, `C11` | Must disclose wide confidence intervals (CI lower bounds of 29.24% and 15.81%). | **HIGH** |
| **CLM-LIM-08** | **No Clinical Validation:** No patient diagnostic performance measured. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 2, Item 2 | Must state software was not evaluated as an in vitro diagnostic (IVD) or clinical tool. | **CRITICAL** |
| **CLM-LIM-09** | **No Wet-Lab Validation:** No sequencing, cDNA cloning, or minigene assays conducted. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 2, Item 1 | Must state no biological or physical laboratory experiments were performed. | **CRITICAL** |
| **CLM-LIM-10** | **No Phenotype Validation:** No clinical phenotype or hematologic severity correlation. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 9 | Must state engine does not predict thalassemia major vs intermedia vs minor. | **HIGH** |
| **CLM-LIM-11** | **No Prospective Independent Dataset:** Held-out prospective testing was not conducted. | **A** | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 15, Item 15 | Must state all testing was retrospective against frozen historical records. | **MEDIUM** |
| **CLM-LIM-12** | **Molecular Consequence Endpoint Only:** Predicts consequence class, not pathogenicity. | **A** | `research/protocol/CP4_1_DECISION_MATRIX.md` | Section 3.1 | Must state benchmark measures molecular impact category only, not pathogenic vs benign. | **HIGH** |
| **CLM-LIM-13** | **Single Transcript Reference:** Operates strictly on NM_000518.5 coordinates. | **A** | `backend/app/core/reference.py` | Model definition | Must disclose non-canonical or alternative transcript isoforms are not modeled. | **LOW** |
| **CLM-LIM-14** | **Protein Nomenclature Disparities:** Secondary exact match rate is 50.91%. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `secondary_endpoints.protein_consequence_concordance` | Must transparently report 20 truncated frameshifts and 5 missing splice protein strings in ClinVar. | **MEDIUM** |
| **CLM-LIM-15** | **Sample Size Boundary (N = 55):** Cannot reveal rare or complex failure modes. | **A** | `research/results/phase2c_benchmark_summary.json` | Key `metadata.cohort_counts.primary_n` | Must acknowledge modest cohort size precludes detecting rare edge-case failure modes. | **MEDIUM** |

---

## 5. Prohibited Claims Register

The following statements are **strictly prohibited** from appearing in the manuscript draft, title, abstract, figures, or supplementary materials:

| Prohibited Claim | Why Prohibited | Empirical Counter-Evidence | Permitted Alternative Phrasing |
|---|---|---|---|
| ❌ *"100% biological accuracy"* | No biological assays, cDNA sequencing, or wet-lab experiments were performed. | CP4.4 Section 2, Item 1 | "100% molecular consequence concordance against consensus ClinVar annotations" |
| ❌ *"100% HBB mutation detection accuracy"* | The software evaluates consequence from known HGVS input; it does not detect variants from raw reads or VCFs. | CP4.4 Section 13 | "deterministic molecular consequence classification from parsed HGVS syntax" |
| ❌ *"Clinical accuracy"* or *"Diagnostic accuracy"* | No patient cohorts, clinical sensitivity/specificity, or diagnostic utility were evaluated. | CP4.4 Section 2, Item 2 | "computational rule concordance" |
| ❌ *"Pathogenicity prediction accuracy"* | The benchmark evaluated molecular consequence (Missense, Splice), not pathogenicity (Pathogenic vs Benign). | CP4.4 Section 9 | "molecular consequence categorization" |
| ❌ *"Universal generalization across all HBB mutation classes"* | Four of 11 mutation classes (C05, C07, C08, C10) had zero candidates ($n = 0$). | CP4.4 Section 8 | "concordance across represented canonical coding and splice acceptor classes" |
| ❌ *"Independent biological validation"* | Sourced exclusively from ClinVar; zero non-ClinVar corroborations; curation filtered by engine agreement. | CP4.4 Section 3, Section 5 | "concordance evaluation against a curated ClinVar-derived external annotation reference" |
| ❌ *"Clinical validation"* | No clinical trial, diagnostic device evaluation, or clinical laboratory protocol was conducted. | CP4.4 Section 6 | "retrospective computational benchmarking" |
| ❌ *"Ground truth"* (used to describe ClinVar) | ClinVar assertions reflect submitter assertions and reference consensus, which may embed historical biases. | CP4.4 Section 6, Section 7 | "external comparison reference", "external annotation consensus" |
| ❌ *"Performance across all HBB mutation classes"* | Four classes unrepresented ($n = 0$); small-$n$ classes have broad uncertainty. | CP4.4 Section 8 | "performance across seven represented biological mutation classes" |
| ❌ *"Diagnostic utility"* | Software has not received IVD clearance, clinical validation, or clinical trial evaluation. | CP4.4 Section 9 | "computational decision-support utility for research workflows" |
| ❌ *"Multi-database cross-validation"* | 100% of candidates derived from NCBI ClinVar; zero variants from LOVD, IthaGenes, or HbVar. | `phase2c_primary.json` | "benchmarked against NCBI ClinVar consensus records" |
| ❌ *"Flawless protein consequence prediction"* | Exact protein nomenclature concordance was 50.91% (28/55) due to truncated frameshift syntax in ClinVar. | `phase2c_benchmark_summary.json` | "exact protein nomenclature matching in 28 of 55 variants, with transparent handling of 20 truncated frameshifts" |

---

## 6. Manuscript Claim Hierarchy

To structure the forthcoming manuscript logically and safely, all findings are organized into three distinct tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ PRIMARY CLAIM (THE CORE FINDING)                                       │
│ "Deterministic molecular consequence predictions generated by the      │
│ HBB Gene Mutation Analyzer achieved 100.00% concordance (55/55;        │
│ exact 95% Clopper-Pearson CI: [93.51%, 100.00%]) with curated ClinVar  │
│ consensus annotations across seven represented biological classes."    │
├────────────────────────────────────────────────────────────────────────┤
│ SECONDARY CLAIMS (SUPPORTED WITH QUALIFICATION)                        │
│ 1. 100% software regression invariance against frozen expected outputs │
│ 2. 100% graceful rejection of 18 synthetic malformed inputs (Exp. D)   │
│ 3. Transparent segregation of 20 truncated frameshift representations  │
│ 4. Transparent handling of 5 canonical splice acceptor protein strings │
│ 5. Strict architectural decoupling of deterministic engine from AI     │
│ 6. Effective resolution of legacy codon nomenclature (-1 offset)       │
├────────────────────────────────────────────────────────────────────────┤
│ NON-CLAIMS (EXPLICIT NEGATIVE BOUNDARIES)                              │
│ 1. The study DOES NOT establish clinical diagnostic accuracy           │
│ 2. The study DOES NOT establish independent biological truth           │
│ 3. The study DOES NOT establish pathogenicity prediction performance   │
│ 4. The study DOES NOT measure performance for C05, C07, C08, or C10    │
│ 5. The study DOES NOT represent an unselected prospective trial        │
│ 6. The study DOES NOT evaluate performance on deep intronic variants   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Scientific Risk Summary

| Risk Level | Claim Count | Nature of Claims | Governance Protocol |
|:---:|:---:|---|---|
| **LOW** | **39** | Factual code mechanics, transcript coordinates, exact counts, software regression results | Permitted directly with standard citation of artifacts |
| **MEDIUM** | **16** | Sample percentages, Clopper-Pearson CI interpretation, protein representation differences | Permitted only with standard sample size and comparator disclosures |
| **HIGH** | **16** | Submitter consensus interpretation, class-stratified claims, limitation disclosures | Permitted only with explicit boundary and uncertainty phrasing |
| **CRITICAL** | **19** | Prohibited validation claims, verification bias disclosures, zero-result class descriptions | Mandatory strict adherence to prohibited wording register; zero tolerance |
| **TOTAL** | **90** | Comprehensive manuscript claim universe | Fully audited and locked |

---

## 8. Authoring Guardrails

All manuscript writing must strictly abide by these 15 authoring rules:

1. **Never describe ClinVar as "ground truth":** Always use *"external comparison reference"*, *"external comparison annotations"*, or *"ClinVar consensus records"*.
2. **Never describe 55/55 as "biological or clinical accuracy":** Always use *"molecular consequence concordance"*.
3. **Always state that the cohort is curated:** Explicitly disclose that variants were selected through quality filtering, not unselected clinical prevalence.
4. **Always disclose engine-informed cohort admission:** Explicitly state in Methods and Discussion that CP2.2 admission into `PROPOSED_PRIMARY` required deterministic engine agreement.
5. **Always disclose zero independent non-ClinVar corroboration:** Explicitly state that 100% of variants originated from ClinVar without orthogonal secondary database corroboration.
6. **Never claim performance for unrepresented classes:** Explicitly report $n = 0$ for C05, C07, C08, and C10; state performance is unmeasured.
7. **Keep molecular and protein endpoints strictly separate:** Report primary molecular concordance (100.0%) and secondary exact protein concordance (50.91%) as distinct metrics.
8. **Keep C12 robustness controls separate from biological validation:** Report the 18 synthetic negative controls strictly as an adversarial robustness experiment, never in the primary denominator.
9. **Keep software regression separate from external concordance:** Report Field B regression checks strictly as software self-consistency metadata.
10. **Do not generalize beyond the frozen cohort:** Restrict conclusions to canonical coding SNVs, small frameshift indels, canonical splice acceptor SNVs, and 3' UTR variants meeting quality criteria under `NM_000518.5`.
11. **Do not call the study "clinically validated":** Explicitly clarify the software is a research tool, not an in vitro diagnostic (IVD).
12. **Do not imply pathogenicity prediction was evaluated:** Reiterate that the engine predicts molecular consequence categories, not clinical disease causality or ACMG classifications.
13. **Preserve the exact confidence interval:** Always cite the Clopper-Pearson 95% CI as `[93.51%, 100.00%]`; do not report asymptotic Wald intervals.
14. **Do not alter historical benchmark artifacts to improve wording:** All manuscript text must cite frozen artifacts AS IS.
15. **Mark unsupported assertions for external literature:** If a background or clinical assertion is not empirically established by project code or manifest data, cite peer-reviewed external literature or remove it.

---

*Phase 5.1 Evidence Matrix successfully compiled and locked. Manuscript drafting is authorized under these explicit constraints.*
