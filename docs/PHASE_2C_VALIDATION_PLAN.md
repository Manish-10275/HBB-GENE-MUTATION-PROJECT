# PHASE 2C VALIDATION PLAN: INDEPENDENT VALIDATION & REPRODUCIBILITY
## Architectural Blueprint for a Defensible, Genuinely Blind, and Reproducible Research Benchmark

**Document Version:** 1.0.0  
**Phase:** Phase 2C (Discovery & Validation Architecture)  
**Status:** PROPOSED & APPROVED FOR IMPLEMENTATION PLANNING  
**Current Paper Readiness Baseline:** **NOT PAPER READY** (Pending implementation of Phase 2C independent blind validation)  
**Author:** Computational Biology & Scientific Validation Architecture Team  

---

## 1. CURRENT BASELINE & SCIENTIFIC DEFICITS (PHASE 2B AUDIT SUMMARY)

The independent scientific integrity audit completed in Phase 2B (`docs/PHASE_2B_SCIENTIFIC_INTEGRITY_AUDIT.md`) proved that the HBB Gene Mutation Analyzer is a deterministic, high-precision bioinformatic tool. However, the audit also identified critical methodological weaknesses in the Phase 2B benchmark that preclude submitting the current results to peer review without comprehensive remediation:

1. **Benchmark Contamination & Exposure (30.6% Test Set Leakage):**
   - Out of the 36 variants in `research/manifest/frozen_test.json`, **11 variants (30.6%)** were previously exposed to the developers during Phase 2A engineering.
   - Four variants (`c.9del`, `c.92+1G>T`, `c.118del`, `c.117_118insA`) exist in production code (`backend/app/variants.py`, `backend/app/clinvar.py`, `backend/app/main.py`) or packaged example FASTAs (`data/examples/`).
   - Eight variants (`c.9del`, `c.93-1G>A`, `c.-5A>G`, `c.*10C>T`, `c.129_126del`, `c.25_28insG`, `c.999del`, `c.9delA`) were explicitly exercised in regression unit tests in `backend/tests/test_hgvs_precision_phase2a.py`.
   - While the engine passed the 25 un-leaked variants ($25/25 = 100\%$), the Phase 2B frozen test set cannot be presented as a blind evaluation.
2. **Severe Sample Sparsity ($N=140 \to N=65$):**
   - The original benchmark design in `docs/PHASE_2B_BENCHMARK_PLAN.md` proposed $N=140$ variants ($N=70$ in the test set). The implemented manifest contained only $N=65$ ($N=36$ in the test set).
   - In the test set, **7 out of 8 biological classes have $n < 5$**, and **every biological class has $n < 10$**. Duplications ($n=1$) and insertions ($n=1$) are represented by a single instance each.
3. **Statistical Uncertainty Obscured by 100% Point Estimates:**
   - For classes with $n=1$ (`c.363dup`, `c.117_118insA`), the Wilson 95% Confidence Interval is **$[20.65\%, 100.0\%]$**. Claiming "100% accuracy on insertions and duplications" based on $n=1$ is scientifically invalid.
   - For negative control rejection ($n=12$), the 95% CI is $[75.75\%, 100.0\%]$, leaving an empirical uncertainty margin of up to 24.25%.
4. **Internal Ground Truth Circularity (Class C Annotations):**
   - Five positive test variants (20.8%) had expected consequences derived solely by the authors walking the codons of RefSeq `NM_000518.5` *in silico* without external clinical registry backing. This measures internal code consistency, not external biological validation.
5. **Nominal Offline Mode Dependent on Live Network Calls:**
   - In `run_benchmark.py`, running `--mode offline` does not bypass HTTP calls in `backend/app/clinvar.py`. Live requests are executed to NCBI E-utilities.
   - `data/fixtures/clinvar_fixtures.json` contains only 7 development variants. **Zero frozen test variants exist in offline fixtures.** Disconnecting network access drops ClinVar Hit@1 from 100% to 0%.

Phase 2C establishes the architectural foundation to resolve every one of these deficits.

---

## 2. PHASE 2C THREE-LAYER VALIDATION ARCHITECTURE

To establish clear methodological boundaries, Phase 2C decomposes the evaluation framework into three strictly decoupled validation layers. Each layer addresses a distinct scientific question and reports separate, non-aggregated performance metrics.

```
                    ┌────────────────────────────────────────────────────────┐
                    │      HBB MUTATION ANALYZER VALIDATION SUITE            │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────────────┬───────┴───────────────────────────────┐
         ▼                               ▼                                       ▼
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│        LAYER A          │   │        LAYER B          │   │        LAYER C          │
│ ALGORITHMIC VALIDATION  │   │  BIOLOGICAL VALIDATION  │   │   CLINVAR RETRIEVAL     │
├─────────────────────────┤   ├─────────────────────────┤   ├─────────────────────────┤
│ Core Rule Transformation│   │ External Registry Truth │   │ Evidence Query & Rank   │
│ cDNA to Codon Mapping   │   │ ClinVar & IthaGenes     │   │ Hit@1, Hit@3, MRR       │
│ Frameshift / Splice Calc│   │ Tiers A & B ONLY        │   │ Offline vs Live Split   │
│ Adversarial Rejection   │   │ (Tiers C & D Excluded)  │   │ Network Latency Bench   │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
```

### 2.1 Layer A: Algorithmic Validation
- **Primary Scientific Question:** *Does the implementation correctly transform HGVS input strings against the reference sequence and deterministically compute the mathematically expected molecular consequence according to standard biochemical rules?*
- **Scope & Evaluated Capabilities:**
  - Standard cDNA coordinate parsing against RefSeq `NM_000518.5` (1..628 bp).
  - Intronic coordinate parsing against RefSeqGene `NG_000007.3` (Intron 1: 130 bp; Intron 2: 850 bp).
  - Immutable reference allele validation (rejection of mismatches).
  - Codon triplet translation via NCBI Translation Table 1.
  - SNV consequences: Synonymous (`p.(=)`), Missense, Nonsense (Stop-Gain).
  - Frameshift downstream codon walking: Correct downstream premature termination codon (PTC) identification and canonical HGVS format generation (e.g. `p.Gln40ArgfsTer21`).
  - In-frame deletions (e.g. `p.Lys18del`).
  - In-frame insertions and duplications.
  - Splice boundary consequence assignment: Invariant donor ($+1, +2$) and acceptor ($-1, -2$) coordinates mapped to `p.?` without speculative protein invention.
  - Regulatory 5' UTR ($-1$ to $-50$) and 3' UTR ($*1$ to $*134$) consequence assignment.
  - Adversarial negative control rejection: Reversed ranges (`c.129_126del`), non-consecutive insertion coordinates (`c.25_28insG`), out-of-bounds positions (`c.999C>T`), invalid IUPAC alphabets (`c.118C>Z`), and deprecated legacy syntax.
- **Mandatory Reporting Boundary:** **This layer must NEVER be termed "clinical validation."** It evaluates deterministic computational rule execution and string manipulation against sequence mathematics.

### 2.2 Layer B: Independent Biological Validation
- **Primary Scientific Question:** *Does the implementation reproduce independently sourced biological consequences and clinical annotations published by authoritative external registries and reference consortia?*
- **Authoritative Provenance Sources:**
  - NCBI ClinVar (Variation IDs with $\ge 1$ star review status, VCV accessions).
  - IthaGenes (Hemoglobin Variants and Thalassaemias Database, with verified PMIDs).
  - NCBI RefSeq / MANE Select (`NM_000518.5`, `NP_000509.1`).
- **Strict Five-Tier Provenance Classification Scheme:**
  - **Tier A (Independent Authoritative Standard):** Universal standards established by international bodies (RefSeq MANE, HGVS nomenclature guidelines, IUPAC nucleotide specifications).
  - **Tier B (Independent Database Evidence):** Clinical assertions from external registries (ClinVar consensus records, IthaGenes curated entries) published independently of this software.
  - **Tier C (Internally Calculated Sequence Consequence):** Expected consequences calculated by project authors walking reference transcripts *in silico*.
  - **Tier D (Implementation-Derived Expectation):** Expected values generated by recording internal software outputs (regex capture groups, internal error strings).
  - **Tier E (Synthetic / Adversarial Control):** Artificially engineered malformed inputs designed to test error handling.
- **Mandatory Reporting Boundary:** **ONLY Tier A and Tier B records qualify as independent biological validation.** Tier C, D, and E must be explicitly segregated in all reports and tables. Tier C and D must NEVER be aggregated into biological accuracy claims.

### 2.3 Layer C: ClinVar Retrieval Validation
- **Primary Scientific Question:** *Can the system accurately query NCBI ClinVar, disambiguate paralogous globin genes, and rank the authentic ClinVar Variation ID as the primary result (Hit@1)?*
- **Scope & Evaluated Capabilities:**
  - Gene-scoped query formulation (`HBB[Gene Name] AND <term>`).
  - Equivalent nomenclature alias expansion (e.g., standardizing historical literature terms to canonical cDNA).
  - Paralog filtering: Rejecting false positive hits from delta-globin (*HBD*) or gamma-globins (*HBG1*, *HBG2*).
  - Match scoring and ranking: Ensuring exact variant matches receive 100/100 score and occupy Rank 0.
- **Mandatory Reporting Boundary:** **ClinVar retrieval accuracy must be reported strictly independently from molecular consequence accuracy.** Consequence prediction assesses sequence logic; ClinVar retrieval assesses external bibliographic and database querying. Combining them into a single composite accuracy metric is scientifically misleading and prohibited.

---

## 3. DESIGN SPECIFICATION FOR THE NEW BLIND TEST SET ($D_{blind}$)

To achieve true scientific independence, Phase 2C specifies the construction of a new primary test set: **`blind_test_v1.json`**. 

*(Note: In accordance with discovery-only constraints, this dataset is designed here in specification only; it will not be populated or evaluated until Phase 2C implementation begins).*

### 3.1 Strict Exclusion Registry (Contamination Quarantine)
A candidate variant is disqualified from $D_{blind}$ if it matches any pattern in the **Exclusion Registry**:
1. **Production Code Exposure:** Any variant appearing in `backend/app/variants.py`, `backend/app/clinvar.py`, `backend/app/consequences.py`, `backend/app/reference.py`, or `backend/app/main.py`.
2. **Preset & Example Exposure:** Any variant appearing in `data/examples/*.fasta`, `backend/app/main.py:EXAMPLE_PRESETS`, or frontend preset components.
3. **Test Suite Exposure:** Any variant present in `backend/tests/*.py`, including Phase 1 smoke tests and Phase 2A regression tests (`test_hgvs_precision_phase2a.py`).
4. **Phase 2B Development & Validation Splits:** Any variant in `research/manifest/development.json` or `research/manifest/validation.json`.
5. **Phase 2B Frozen Test Leaks:** The 11 tainted variants identified in the audit (`c.9del`, `c.92+1G>T`, `c.118del`, `c.117_118insA`, `c.93-1G>A`, `c.-5A>G`, `c.*10C>T`, `c.129_126del`, `c.25_28insG`, `c.999del`, `c.9delA`).

### 3.2 Candidate Variant Schema
Every record admitted to the candidate pool must conform to the following schema:

```json
{
  "id": "HBB-BLIND-001",
  "name": "Hb D-Los Angeles / Hb D-Punjab",
  "hgvs_c_input": "c.364G>C",
  "hgvs_c_canonical": "NM_000518.5:c.364G>C",
  "reference_accession": "NM_000518.5",
  "variant_class": "substitution",
  "molecular_consequence": "Missense",
  "region": "Exon 3",
  "coordinate_cdna": "364",
  "ref_allele": "G",
  "alt_allele": "C",
  "expected_hgvs_p": "p.Glu122Gln",
  "expected_clinvar_id": "15424",
  "expected_clinvar_significance": "Pathogenic",
  "provenance": {
    "ground_truth_source": "NCBI ClinVar (VCV000015424 / VarID 15424)",
    "provenance_tier": "Tier B (Independent Database Evidence)",
    "discovery_source": "NCBI ClinVar Entrez Gene 3043 Query",
    "review_status": "criteria provided, multiple submitters, no conflicts",
    "pmid_citations": ["15598818", "21415222"],
    "notes": "Historical literature designates Codon 121 (Glu121Gln); HGVS designates Codon 122 (p.Glu122Gln)."
  },
  "blinding_audit": {
    "in_production_code": false,
    "in_unit_tests": false,
    "in_examples_or_presets": false,
    "in_phase2b_dev_or_val": false,
    "in_phase2b_leaked_test": false,
    "blinding_status": "STRICTLY_BLIND"
  }
}
```

---

## 4. AUTOMATED DATA LEAKAGE DETECTOR ARCHITECTURE

To prevent unintentional contamination, Phase 2C introduces an automated, hard-gating integrity tool: **`research/validation/leakage_checks/leakage_audit_gate.py`**.

```
┌────────────────────────────────────────────────────────┐
│     CANDIDATE TEST VARIANT POOL (D_blind candidates)   │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│        AUTOMATED LEAKAGE AUDIT GATE (AST & REGEX)      │
├────────────────────────────────────────────────────────┤
│ 1. Exact cDNA String Match (e.g. "c.118C>T")           │
│ 2. Stripped Coordinate Match (e.g. "118C>T", "c.118")  │
│ 3. ClinVar Variation ID Match (e.g. "15402")           │
│ 4. Protein Consequence Match (e.g. "p.Gln40Ter")       │
│ 5. Alias & Historical Name Match (e.g. "IVS-I-1")      │
│ 6. Production AST String Literal Scan                  │
└────────────────────────────────────────────────────────┘
         │                                      │
     MATCH FOUND                             ZERO MATCHES
         │                                      │
         ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐
│   GATE FAILS (EXIT 1)   │            │   GATE PASSES (EXIT 0)  │
│ Variant Quarantined     │            │ Variant Certified Blind │
│ Build Aborted           │            │ Admitted to D_blind     │
└─────────────────────────┘            └─────────────────────────┘
```

### 4.1 Detector Methodology & Scan Target Directory Map
The leakage detector performs automated AST parsing and regex pattern matching across:
- `backend/app/` — Scans for string literals, dictionary keys, regex pattern comments, and conditionals.
- `backend/tests/` — Scans all pytest test assertions, fixture parameters, and test docstrings.
- `frontend/src/` — Scans TypeScript components, default input forms, and preset dictionaries.
- `data/examples/` — Scans FASTA sequence headers, FASTA nucleotide sequences, and metadata.
- `data/fixtures/` — Scans cached JSON payloads for development fixture bleed.
- `research/manifest/` — Cross-references candidates against `development.json` and `validation.json`.
- `docs/` & `reports/` — Scans release reports and documentation for published test cases.

### 4.2 Hard Gating CI Enforcement
The benchmark execution harness will invoke the leakage gate as a **pre-flight verification step**:
- If `leakage_audit_gate.py` detects even a single match for any candidate variant in $D_{blind}$, the harness will refuse to execute, emitting a fatal `LeakageContaminationError` and a detailed `leakage_report.json`.

---

## 5. OFFLINE BENCHMARK ARCHITECTURE & REPRODUCIBILITY HARNESS

### 5.1 The Root Cause of Phase 2B Offline Failure
In Phase 2B, `run_benchmark.py` accepted `--mode offline`, but `backend/app/clinvar.py:fetch_clinvar_records` never received the flag. It issued live asynchronous HTTP requests to NCBI E-utilities, and none of the 13 frozen test ClinVar variants were present in `data/fixtures/clinvar_fixtures.json`.

### 5.2 Phase 2C Strict Offline Design
Phase 2C enforces an absolute design invariant:
> **OFFLINE EVALUATION MUST MAKE ZERO NETWORK REQUESTS.**

```
                                 EVALUATION MODE SELECTOR
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         ┌─────────────────────┐                         ┌─────────────────────┐
         │    OFFLINE MODE     │                         │      LIVE MODE      │
         ├─────────────────────┤                         ├─────────────────────┤
         │ httpx Blocked / Mock│                         │ Live NCBI Entrez API│
         │ Read Immutable JSON │                         │ Network Latency Rec │
         │ Local Fixture DB    │                         │ API Resilience Test │
         │ Deterministic Hash  │                         │ Dynamic Ingestion   │
         └─────────────────────┘                         └─────────────────────┘
```

1. **Pre-Cached Versioned Fixture Database (`offline_clinvar_fixtures.json`):**
   - A dedicated research fixture database will store the complete, unedited NCBI JSON/XML responses for every variant in $D_{blind}$ requiring ClinVar evaluation.
   - This file will reside at `research/validation/fixtures/offline_clinvar_fixtures.json` and be cryptographically hashed (`offline_clinvar_fixtures.sha256`).
2. **Network Interceptor Gate:**
   - In offline mode, the benchmark harness will monkeypatch or mock `httpx.AsyncClient` to raise an `UnexpectedNetworkCallError` if any outbound network connection is attempted.
   - `fetch_clinvar_records` will read exclusively from the versioned offline fixture database.
3. **Reproducibility Test Protocol:**
   - A dedicated verification script (`verify_offline_reproducibility.py`) will execute the benchmark in offline mode on an isolated, network-blocked interface.
   - It will execute the benchmark 10 consecutive times and assert:
     $$	ext{SHA-256}(	ext{Run}_1) == 	ext{SHA-256}(	ext{Run}_2) == \dots == 	ext{SHA-256}(	ext{Run}_{10})$$
   - Any variation in output, metric calculation, or ranking will cause the reproducibility test to fail.

---

## 6. PROTOCOL AMENDMENT: DOCUMENTING $N=140 	o N=65$

### 6.1 Proposed Formal Protocol Amendment
In accordance with scientific integrity standards, the reduction in dataset size between planning and implementation must be formally documented as an official protocol amendment:

> **PROTOCOL AMENDMENT NOTICE: AMEND-2026-01**  
> **Original Target:** $N = 140$ variants ($N = 120$ positive across 12 balanced classes + $N = 20$ negative controls), specified in `docs/PHASE_2B_BENCHMARK_PLAN.md`.  
> **Implemented Baseline:** $N = 65$ variants ($N = 45$ positive + $N = 20$ negative controls), instantiated in `research/manifest/hbb_benchmark_manifest.json`.  
> **Observed Reduction:** $-53.6\%$ overall reduction ($-62.5\%$ in positive variants).  
> **Evidence from Repository:**  
> In `research/build_manifest.py`, an intermediate docstring contemplated an 85-variant dataset before settling on 65. Each instantiated variant contains exhaustive manual transcript coordinates, ClinVar VCV accessions, and literature notes. However, no commit message, issue ticket, or written design amendment document exists to explain why curation ceased at 65 instead of 85 or 140.  
> **Definitive Explanation:**  
> *The formal reason cannot be established from repository evidence.*  
> **Excluded Categories:**  
> 1. Large structural deletions (>100 bp, such as the Southeast Asian / Indian 619 bp deletion `NG_000007.3:g.71609_72227del619` and Sicilian $eta^0$-thalassemia deletion).  
> 2. Complex insertion-deletion combinations (`delins` syntax).  
> 3. Globin gene fusions and cross-over alleles (Hb Lepore, Hb Kenya).  
> 4. Deep intronic cryptic splice activating alleles (>50 bp into introns, e.g. `c.252-16C>T`).  
> **Scientific Implications:**  
> The implemented Phase 2B benchmark is restricted in scope to single-nucleotide variants, short indels ($\le 4$ bp), and consensus splice site variants within canonical transcript boundaries. Claims of diagnostic generalization to broad thalassemia screening panels are invalidated by these exclusions.

---

## 7. CLASS IMBALANCE AUDIT & EXPANSION TARGETS

### 7.1 Empirical Audit of Current Phase 2B Test Set ($N = 36$)

| Variant Class | Test Count ($n$) | Current Representation Status | Empirical Deficiency Analysis |
| :--- | :---: | :---: | :--- |
| **Duplications** | **1** | **CRITICAL DEFICIENCY ($n < 5$)** | Single test case (`c.363dup`); 95% CI is $[20.7\%, 100\%]$. Zero statistical power. |
| **Insertions** | **1** | **CRITICAL DEFICIENCY ($n < 5$)** | Single test case (`c.117_118insA`); 95% CI is $[20.7\%, 100\%]$. Zero statistical power. |
| **Splice Acceptor** | **2** | **CRITICAL DEFICIENCY ($n < 5$)** | Only `c.93-1G>A` and `c.316-1G>A`; 95% CI is $[34.2\%, 100\%]$. |
| **5' UTR** | **2** | **CRITICAL DEFICIENCY ($n < 5$)** | Only `c.-50A>C` and `c.-5A>G`; 95% CI is $[34.2\%, 100\%]$. |
| **Splice Donor** | **3** | **CRITICAL DEFICIENCY ($n < 5$)** | Three variants (`c.92+1`, `c.92+2`, `c.315+2`); 95% CI is $[43.9\%, 100\%]$. |
| **Coding Deletions** | **4** | **CRITICAL DEFICIENCY ($n < 5$)** | Four variants; in-frame deletions underrepresented ($n=1$). |
| **3' UTR** | **4** | **CRITICAL DEFICIENCY ($n < 5$)** | Four variants; underpowered for polyadenylation signal disruption. |
| **Substitutions** | **7** | **SUB-OPTIMAL ($n < 10$)** | Nonsense ($n=2$), Missense ($n=2$), Synonymous ($n=3$). |
| **Negative Controls** | **12** | **ACCEPTABLE ($n \ge 10$)** | Rejection testing is moderately powered (95% CI: $[75.8\%, 100\%]$). |

### 7.2 Phase 2C Target Sample Sizes for New Blind Test Set ($D_{blind}$)
To ensure every structural class carries meaningful statistical weight, Phase 2C establishes minimum practical sample size targets:

| Structural Variant Class | Minimum Target ($n$) | Recommended Target ($n$) | Sourcing Strategy & Candidate Criteria |
| :--- | :---: | :---: | :--- |
| **Missense (Pathogenic & Benign)** | 8 | 10 | ClinVar VCV consensus (Hb C, Hb E, Hb S, plus non-pathogenic polymorphisms). |
| **Nonsense (Stop-Gain)** | 6 | 8 | ClinVar confirmed stop codons across Exons 1, 2, and 3. |
| **Synonymous (Silent)** | 6 | 8 | ClinVar benign/likely benign coding silent variants (e.g. `c.9T>C`, `c.108C>T`, `c.177T>C`). |
| **Frameshift Deletions** | 6 | 8 | Authenticated 1-bp, 2-bp, 4-bp deletions with downstream PTCs documented in ClinVar/IthaGenes. |
| **In-Frame Deletions** | 4 | 6 | 3-bp and 6-bp non-frameshifting deletions (e.g. `c.135_137del`, `c.28_30del`). |
| **Frameshift Duplications / Ins** | 6 | 8 | 1-bp duplications (`c.27dup`, `c.363dup`) and non-duplication insertions. |
| **In-Frame Insertions** | 4 | 5 | 3-bp in-frame insertions. |
| **Splice Donor ($+1, +2, +5$)** | 6 | 8 | Invariant donor sites for Intron 1 and Intron 2 from ClinVar. |
| **Splice Acceptor ($-1, -2$)** | 6 | 8 | Invariant acceptor sites for Intron 1 and Intron 2 from ClinVar. |
| **5' UTR Regulatory** | 5 | 8 | Promoter/TATA box variants (`c.-78`, `c.-79`, `c.-80`, `c.-138`) from ClinVar. |
| **3' UTR Regulatory** | 5 | 8 | Polyadenylation signal variants (`c.*110`, `c.*111`, `c.*112`, `c.*113`) from ClinVar. |
| **Adversarial Negative Controls** | 15 | 20 | Structured battery: Range inversions, insertion range errors, ref mismatches, out-of-bounds. |
| **TOTAL BLIND TEST SET ($D_{blind}$)** | **$\ge 75$** | **$\ge 105$** | **Balanced across all 12 classes; all $n \ge 5$, primary classes $n \ge 8$.** |

---

## 8. STATISTICAL METHODOLOGY & EVALUATION PLAN

### 8.1 Metric Definitions & Formulation
The validation framework will calculate the following formal statistical metrics:

1. **Binary Diagnostic Performance (Valid Variants vs Adversarial Controls):**
   - Sensitivity (True Positive Rate): $	ext{TPR} = rac{	ext{TP}}{	ext{TP} + 	ext{FN}}$
   - Specificity (True Negative Rate): $	ext{TNR} = rac{	ext{TN}}{	ext{TN} + 	ext{FP}}$
   - Precision (Positive Predictive Value): $	ext{PPV} = rac{	ext{TP}}{	ext{TP} + 	ext{FP}}$
   - F1-Score: $	ext{F1} = 2 \cdot rac{	ext{PPV} \cdot 	ext{TPR}}{	ext{PPV} + 	ext{TPR}}$
   - Overall Diagnostic Accuracy: $	ext{ACC} = rac{	ext{TP} + 	ext{TN}}{	ext{TP} + 	ext{TN} + 	ext{FP} + 	ext{FN}}$
2. **Multi-Class Consequence Concordance:**
   - Evaluated across 9 discrete consequence categories: `Nonsense`, `Missense`, `Synonymous`, `Frameshift`, `In-frame Indel`, `Splice Site`, `5' UTR`, `3' UTR`, `Invalid / Rejected`.
   - Per-class Precision, Recall, and F1.
   - Macro-averaged F1 and Weighted F1.
3. **Information Retrieval (ClinVar Evidence):**
   - Hit@1: Proportion of queries where the authentic Variation ID is ranked at Position 0.
   - Hit@3: Proportion where the authentic ID appears in the top 3 returned candidates.
   - Mean Reciprocal Rank: $	ext{MRR} = rac{1}{|Q|} \sum_{i=1}^{|Q|} rac{1}{	ext{rank}_i}$.

### 8.2 Wilson Score 95% Confidence Intervals
For all binomial proportions (concordance, sensitivity, specificity, Hit@1), 95% confidence intervals will be computed using the **Wilson score interval with continuity correction**:

$$	ilde{p} = rac{k + rac{z^2}{2}}{n + z^2}, \quad w = rac{z}{1 + rac{z^2}{n}} \sqrt{rac{p(1-p)}{n} + rac{z^2}{4n^2}}$$
$$	ext{CI}_{95\%} = \left[ \max\left(0, 	ilde{p} - wight), \; \min\left(1, 	ilde{p} + wight) ight]$$
where $z = 1.95996$, $n$ is the class sample size, and $k$ is the number of concordant predictions.

### 8.3 Strict Statistical Reporting Rules
- **Rule 1:** No accuracy score may be presented without its corresponding sample size $n$ and Wilson 95% confidence interval.
- **Rule 2:** "100% accuracy" must never be claimed in prose for any class where $n < 10$. For such classes, the text must state: *"The tool achieved $k/n$ concordance (95% CI: [low%, high%])."*
- **Rule 3:** No class-level accuracy claim is permitted for any class where $n \le 2$.

---

## 9. HISTORICAL BENCHMARK PRESERVATION STRATEGY

To preserve research provenance and maintain an auditable paper trail, Phase 2B artifacts will remain permanently preserved and immutable:

```
research/
├── manifest/
│   ├── hbb_benchmark_manifest.json    [HISTORICAL BASELINE - IMMUTABLE]
│   ├── development.json               [HISTORICAL BASELINE - IMMUTABLE]
│   ├── validation.json                [HISTORICAL BASELINE - IMMUTABLE]
│   ├── frozen_test.json               [HISTORICAL BASELINE - IMMUTABLE]
│   └── frozen_test.sha256             [HISTORICAL BASELINE - IMMUTABLE]
└── results/
    ├── benchmark_results.json         [HISTORICAL BASELINE - IMMUTABLE]
    └── BENCHMARK_REPORT.md            [HISTORICAL BASELINE - IMMUTABLE]
```

### Protocol for Historical Labeling:
In all future documentation and comparative analysis, the Phase 2B benchmark will be explicitly designated:
> **`HISTORICAL / PARTIALLY CONTAMINATED VALIDATION BASELINE (PHASE 2B)`**  
> Characterized by: $N = 36$ test cases, $30.6\%$ prior development exposure, and nominal offline execution.

The new Phase 2C validation artifacts will reside in a completely separate, dedicated namespace: `research/validation/`.

---

## 10. PROPOSED PHASE 2C ARTIFACT DIRECTORY STRUCTURE

The Phase 2C architecture introduces a clean, modular validation workspace under `research/validation/`:

```
research/validation/
├── candidate_pool/
│   ├── candidate_hbb_variants.json      # Raw candidate pool extracted from ClinVar/IthaGenes
│   └── candidate_screening_log.md       # Audit trail of candidate acceptance/rejection
├── manifests/
│   ├── exclusion_registry.json          # Machine-readable hashes of all exposed variants
│   ├── blind_test_v1.json               # Final frozen blind test manifest (N >= 75)
│   └── blind_test_v1.sha256             # Cryptographic signature of blind_test_v1.json
├── provenance/
│   ├── blind_test_provenance.json       # Exhaustive per-variant evidence & citation database
│   └── SOURCES.md                       # Human-readable bibliography and registry accessions
├── fixtures/
│   ├── offline_clinvar_fixtures.json    # Complete offline cached NCBI responses for D_blind
│   └── offline_clinvar_fixtures.sha256  # Cryptographic signature of fixture database
├── leakage_checks/
│   ├── leakage_audit_gate.py            # Automated pre-flight AST/regex scanner
│   └── leakage_report.json              # Automated audit certificate (asserts 0 leakage)
├── harness/
│   ├── run_validation.py                # Three-layer validation runner (offline & live)
│   ├── verify_offline_reproducibility.py# Hash stability test with network disabled
│   └── statistical_engine.py            # Wilson CI and multiclass metrics calculator
└── results/
    ├── validation_results_offline.json  # Bit-for-bit reproducible offline results
    ├── validation_results_live.json     # Live NCBI network results with latency metrics
    ├── metrics_summary.json             # Structured metric tables with 95% CIs
    └── VALIDATION_REPORT.md             # Formal scientific validation report
```

### Justification for Key Proposed Artifacts:
- **`exclusion_registry.json`:** Encodes every variant previously exposed in development, tests, or presets to ensure programmatic rejection during candidate sampling.
- **`blind_test_v1.json` & `.sha256`:** The primary immutable validation set. Cryptographically locked to guarantee zero post-hoc modifications.
- **`offline_clinvar_fixtures.json`:** Decouples ClinVar evidence verification from NCBI server uptime and rate limits, enabling genuine air-gapped reproducibility.
- **`leakage_report.json`:** Serves as formal proof for journal peer reviewers that the test set has zero overlap with production code or regression tests.

---

## 11. PAPER CLAIMS: SCIENTIFICALLY ACCEPTABLE VS STRICTLY PROHIBITED

| Feature / Dimension | Scientifically Acceptable Claim | Strictly Prohibited Claim |
| :--- | :--- | :--- |
| **Algorithmic Transformation** | "The software deterministically transforms canonical *HBB* HGVS cDNA notations into genomic and codon coordinates according to standard genetic code and transcript specifications." | "The software provides 100% accurate variant interpretation for all clinical beta-globin mutations." |
| **Biological Concordance** | "Across an independently curated blind evaluation panel of $N = 75$ variants, the system demonstrated $X\%$ concordance (95% CI: $[Y\%, Z\%]$) with published ClinVar/IthaGenes consequences." | "The system has zero false positives and perfectly predicts variant pathogenicity." |
| **Class-Level Performance** | "For single-nucleotide substitutions ($n = 24$), concordance was $X\%$ (95% CI: $[Y\%, Z\%]$)." | "The system achieves 100% accuracy on duplications and insertions" (when $n \le 5$). |
| **Negative Control Handling** | "The syntax and reference validation engine successfully rejected $K/M$ malformed or reference-mismatched inputs (specificity: $X\%$, 95% CI: $[Y\%, Z\%]$)." | "The system is impervious to erroneous user input in clinical environments." |
| **Evidence Retrieval** | "When evaluated against pre-cached ClinVar records in offline mode, the query engine achieved Hit@1 retrieval of $X\%$ (95% CI: $[Y\%, Z\%]$)." | "The software autonomously discovers novel clinical variants in real time." |
| **Clinical Scope** | "The tool is an open-source, local-first research aid designed strictly for exploratory analysis of short *HBB* sequence variants." | "The tool is a validated diagnostic device ready for direct clinical decision support." |

---

## 12. FINAL DECISION, ROADMAP & ACCEPTANCE CRITERIA

### Current Scientific Status: **`NOT PAPER READY`**
The current Phase 2B baseline is disqualified from academic submission due to documented test set leakage (30.6%), severe sample sparsity in key classes ($n=1$), and nominal offline execution.

### Prioritized Remediation Requirements for Phase 2C:

#### Priority 0 (P0) — Mandatory Blockers:
1. **Implement Automated Leakage Detector (`leakage_audit_gate.py`):** Must verify zero presence of candidate test variants in production code, tests, presets, and Phase 2B manifests.
2. **Curate Genuine Blind Test Set ($D_{blind}, N \ge 75$):** Assemble a completely un-leaked panel where every positive variant is classified as Tier A or Tier B with published accessions.
3. **Achieve Sample Size Minimums ($n \ge 5$ across all classes):** Expand duplications, insertions, splice donors, splice acceptors, 5' UTR, and 3' UTR so no evaluated class has $n < 5$.
4. **Implement True Offline Fixture Architecture (`offline_clinvar_fixtures.json`):** Pre-cache verified ClinVar responses for all test variants and enforce zero network calls in offline mode.
5. **Decouple Three Validation Layers:** Ensure Layer A, Layer B, and Layer C are executed and reported independently with separate metrics.

#### Priority 1 (P1) — High Priority:
6. **Implement Offline Reproducibility Verifier:** Script asserting 10 consecutive offline runs produce bit-for-bit identical JSON output and hash.
7. **Compute Wilson 95% Confidence Intervals:** Integrate exact Wilson score interval calculations for every metric in summary tables.
8. **Segregate Tier C and Tier D Annotations:** Exclude internal in silico sequence walking from external biological concordance calculations.

#### Priority 2 (P2) — Desirable Improvements:
9. **Integrate External Oracle Validation:** Benchmark against Ensembl VEP REST API on a subset of variants.
10. **Add Latency & Memory Profiling:** Formally measure runtime latency (ms) per variant across offline and live modes.

---

### Phase 2C Minimum Acceptance Criteria:
Phase 2C can be certified as complete and **`PAPER READY`** if and only if all the following empirical criteria are satisfied:

- [ ] **Zero Data Leakage:** `leakage_audit_gate.py` runs across the entire repository and returns 0 violations (`EXIT CODE 0`).
- [ ] **Blind Dataset Breadth:** $D_{blind}$ contains $N \ge 75$ authenticated variants across all 12 structural classes.
- [ ] **Class Balance:** Every single evaluated structural class contains $n \ge 5$ test instances.
- [ ] **Provenance Purity:** 100% of positive variants in $D_{blind}$ are verified Tier A or Tier B with independent external registry citations.
- [ ] **Air-Gapped Offline Execution:** The benchmark runs with network completely disabled and achieves 100% fixture coverage without issuing a single HTTP request.
- [ ] **Bit-for-Bit Reproducibility:** 10 consecutive offline runs yield identical SHA-256 hashes for `validation_results_offline.json`.
- [ ] **Rigorous Statistical Reporting:** Every accuracy, concordance, and retrieval score is accompanied by its sample size $n$ and Wilson 95% confidence interval.
- [ ] **Layer Decoupling:** Algorithmic correctness (Layer A), biological consequence agreement (Layer B), and ClinVar retrieval (Layer C) are reported in separate, non-conflated report sections.

---

**Plan Approved for Phase 2C Execution:**  
*Lead Computational Biology & Scientific Validation Architecture Team*  
*October 2026*
