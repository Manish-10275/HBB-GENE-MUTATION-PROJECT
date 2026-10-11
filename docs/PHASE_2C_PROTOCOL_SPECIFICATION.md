# PHASE 2C SCIENTIFIC VALIDATION PROTOCOL SPECIFICATION
## Comprehensive Pre-Registration Protocol for Independent Blind Evaluation of the HBB Gene Mutation Analyzer

**Document ID:** HBB-PROTO-2026-2C  
**Version:** 2.0.0-DRAFT  
**Date:** October 8, 2026  
**Status:** DRAFT FOR HUMAN REVIEW & SCIENTIFIC OVERSIGHT (CP-1 CORRECTION PASS)  
**Target Gene & Transcripts:** Human *HBB* (RefSeq `NM_000518.5`, RefSeqGene `NG_000007.3`, Protein `NP_000509.1`)  
**Scope:** Research Use Only (RUO) Exploratory Bioinformatics Tool — Non-Clinical Sequence Variant Interpretation  

---

## 1. PURPOSE, REGULATORY BOUNDARIES & NON-CLINICAL DISCLAIMER

### 1.1 Purpose
This protocol specifies the methodology, candidate stratification strategy, data exclusion registry, blinding mechanisms, statistical framework, and execution controls for the independent Phase 2C scientific evaluation of the HBB Gene Mutation Analyzer.

### 1.2 Research Boundaries & Non-Clinical Disclaimer
1. **Research Aid Only:** The software is designed and evaluated strictly as a deterministic research tool for exploratory analysis of sequence alterations in the human beta-globin (*HBB*) gene.
2. **Explicit Prohibition of Diagnostic Claims:** The tool is **NOT** a clinical decision support system, is **NOT** an *in vitro* diagnostic (IVD) medical device, and must **NEVER** be presented in scientific literature or documentation as a replacement for certified clinical molecular geneticist review or accredited clinical laboratory diagnostic workflows.
3. **Deterministic Scope:** The primary evaluation measures deterministic algorithmic rule conformance to HGVS v20.05 sequence nomenclature and NCBI Translation Table 1, comparing computed molecular consequences against independently established molecular interpretations. It does not measure clinical utility, pathogenicity prediction, or patient health outcomes.

---

## 2. EVALUATION TARGET SEPARATION (NON-CONFLATION PRINCIPLE)

A foundational architectural requirement of this protocol is the absolute separation of evaluation targets. Four distinct evaluation dimensions are defined:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       EVALUATION TARGET SEPARATION                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
┌────────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│       TARGET A         │   │       TARGET B         │   │       TARGET C         │
│ MOLECULAR CONSEQUENCE  │   │   EVIDENCE RETRIEVAL   │   │  CLINICAL SIGNIFICANCE │
├────────────────────────┤   ├────────────────────────┤   ├────────────────────────┤
│ • HGVS c. Normalization│   │ • Query Formulation    │   │ • ClinVar Pathogenicity│
│ • Codon Translation    │   │ • Variation ID Ranking │   │ • ACMG / ClinGen Class │
│ • Variant Class        │   │ • Hit@1, Hit@3, MRR    │   │ • Penetrance / Trait   │
│ • Protein Consequence  │   │ • Offline vs Live      │   │ • Secondary Context    │
│ • PTC Coordinate       │   │ • Provider Resilience  │   │   ONLY (Not Ground     │
│ [PRIMARY EXPERIMENT]   │   │ [SECONDARY EXPERIMENT] │   │   Truth for Target A)  │
└────────────────────────┘   └────────────────────────┘   └────────────────────────┘
                                       │
                                       ▼
                         ┌────────────────────────┐
                         │       TARGET D         │
                         │  AI SYNTHESIS QUALITY  │
                         ├────────────────────────┤
                         │ • Fact Preservation   │
                         │ • Provenance Fidelity  │
                         │ • Zero Hallucination   │
                         │ • Discrepancy Clarity  │
                         │ [SECONDARY EXPERIMENT] │
                         └────────────────────────┘
```

### 2.1 Explicit Non-Conflation Rules:
1. **Clinical Significance vs. Molecular Consequence:**
   > *"Clinical significance and molecular consequence are distinct evaluation targets and must not be conflated."*
   ClinVar pathogenicity classifications (e.g. "Pathogenic", "Benign", "Uncertain significance") are **NEVER** used as the ground truth for deterministic molecular consequences. Pathogenicity reflects clinical evidence and disease association; molecular consequence reflects sequence biology (missense, nonsense, frameshift, synonymous, splice site). Pathogenicity annotations are retained strictly as secondary contextual evidence.
2. **Evidence Retrieval vs. Molecular Consequence:**
   Failure of ClinVar or PubMed evidence retrieval (due to missing fixture, network timeout, rate limit, or NCBI service disruption) is **NOT** a failure of the deterministic molecular consequence engine.
3. **AI Synthesis vs. Primary Biological Consequence:**
   AI synthesis performance (language fluency, citation formatting, summary quality) is evaluated separately and must **NEVER** be aggregated into the primary biological accuracy metric.
4. **Target Isolation Rule:**
   > *"These are separate evaluation targets. Success or failure in one layer must not be silently converted into success or failure in another."*

---

## 3. EXPERIMENT HIERARCHY: PRIMARY & SECONDARY EXPERIMENTS

### 3.1 PRIMARY EXPERIMENT: Deterministic Molecular Consequence Validation
- **Objective:** Evaluate whether the deterministic engine correctly parses previously unseen *HBB* variants and accurately computes their molecular consequences against independently established molecular interpretations.
- **Input:** Previously unseen, un-leaked *HBB* variant representations (cDNA strings conforming to HGVS syntax).
- **Computed Outputs:**
  - Normalized canonical HGVS c. string
  - Reference transcript accession (`NM_000518.5`) and coordinate mapping
  - Structural variant class (`substitution`, `deletion`, `insertion`, `duplication`, `splice`, `regulatory_utr`)
  - Molecular consequence (`Missense`, `Nonsense`, `Synonymous`, `Frameshift`, `In-frame Indel`, `Splice Site Disruption`, `5' UTR Regulatory`, `3' UTR Regulatory`)
  - Protein consequence in standard HGVS p. notation (e.g. `p.Glu7Val`, `p.Gln40Ter`, `p.Lys18del`, `p.Lys18_Val19delinsMet`, `p.Phe42LeufsTer19`)
  - Premature termination codon (PTC) coordinate where applicable
- **Primary Comparison:** Independently established molecular interpretation from Class A, Class B, or Class C provenance sources.
- **Primary Evaluated Metrics:**
  - Canonical HGVS cDNA normalization agreement
  - Structural variant class assignment accuracy
  - Molecular consequence concordance
  - Protein consequence HGVS p. concordance
  - Adversarial negative control rejection specificity

### 3.2 SECONDARY EXPERIMENT B1: Deterministic Offline Evidence Retrieval
- **Objective:** Evaluate whether the offline evidence layer deterministically retrieves pre-cached evidence records without network reliance.
- **Requirements:**
  - Dedicated Phase 2C evidence fixtures (`research/validation/fixtures/offline_clinvar_fixtures.json`), physically separated from development fixtures.
  - Frozen with cryptographic provenance and hash verification.
  - Sockets blocked to guarantee zero network access.
  - A missing fixture entry must yield an explicit `OFFLINE_DATA_UNAVAILABLE` status, not an unhandled exception or synthetic fallback.
  - Fixture retrieval failure must **NOT** be scored as a molecular consequence failure.

### 3.3 SECONDARY EXPERIMENT B2: Live ClinVar External Retrieval
- **Objective:** Evaluate external NCBI E-utilities query formulation, alias expansion, candidate ranking, and paralog filtering under live network conditions.
- **Metrics Evaluated:**
  - Retrieval success rate (valid response returned)
  - Hit@1: Authentic Variation ID occupies Rank 0
  - Hit@3: Authentic Variation ID occupies Rank $\le 2$
  - Recall@5: Authentic Variation ID in top 5 returned candidates
  - Mean Reciprocal Rank (MRR)
  - Failure categorization: `Not Found`, `Timeout`, `Rate Limited (HTTP 429)`, `Network / Upstream 5xx`
- **Rule:** Failure of live evidence retrieval is evaluated strictly as an infrastructure/service metric and is **NEVER** scored as an algorithmic failure of the core bioinformatics engine.

### 3.4 SECONDARY EXPERIMENT C: AI Synthesis Integrity & Authority Boundary
- **Objective:** Evaluate whether the AI Copilot strictly honors the deterministic boundary and accurately synthesizes external evidence.
- **Evaluated Dimensions:**
  - **Zero Override:** AI must never contradict or alter the deterministic molecular consequence, HGVS p., or variant class.
  - **Factual Preservation:** Verbatim preservation of computed coordinates, PTC positions, and gene structures.
  - **Provenance Integrity:** AI must cite only authentically retrieved ClinVar Variation IDs and PMIDs; zero hallucinated accessions permitted.
  - **Discrepancy Transparency:** Clear explanation when external databases report conflicting interpretations.
  - **Deterministic Fallback:** Clean degradation to structured deterministic summary when LLM inference is disabled or unavailable.

---

## 4. FORMALIZED GROUND TRUTH INDEPENDENCE & PROVENANCE TAXONOMY

### 4.1 Five-Tier Provenance Classification
Every variant admitted into the Phase 2C validation manifest must be assigned an explicit ground truth provenance class:

| Provenance Class | Classification Name | Definition & Accepted Sources | Admissibility Status |
|:---:|---|---|:---:|
| **Class A** | **Independent Authoritative Reference / Nomenclature** | Universal standards established by international biological authorities: RefSeq MANE Select (`NM_000518.5`), HGVS Sequence Variant Nomenclature guidelines (v20.05), IUPAC nucleotide specifications. | **Primary Validation Ground Truth** |
| **Class B** | **Independent Curated Database Interpretation** | External curated registry records containing an independently established molecular interpretation: NCBI ClinVar (Variation IDs with $\ge 1$-star review), IthaGenes curated entries, LOVD *HBB* database. | **Primary Validation Ground Truth** |
| **Class C** | **Peer-Reviewed Primary Literature Evidence** | Published peer-reviewed scientific studies providing molecular, biochemical, or sequencing evidence for the variant's consequence (with valid PubMed ID / DOI). | **Primary Validation Ground Truth** |
| **Class D** | **Author-Derived Computational Interpretation** | *In silico* sequence walking or computational derivations generated by the project authors without external registry or literature backing. | **EXCLUDED FROM INDEPENDENT VALIDATION** (Internal sanity check only) |
| **Class E** | **Synthetic Adversarial Control** | Artificially engineered malformed inputs (inverted ranges, reference mismatches, non-consecutive insertion coordinates, invalid alphabets) designed to test error handling. | **Separately Reported Negative Controls** |

### 4.2 Provenance Independence Rules:
1. **Primary Ground Truth Restrictions:** Primary molecular consequence accuracy must rely exclusively on **Class A, Class B, or Class C** ground truth. Class D records must **NOT** be counted as independent biological validation.
2. **ClinVar Review Status Caveat:**
   > *"A ClinVar review status or star rating alone does not automatically establish independence of the molecular consequence annotation."*
   The annotation must be cross-referenced against the submitted HGVS expression and primary literature citations to ensure the molecular consequence is independently established rather than an automated pipeline artifact.
3. **Disagreement Preservation Rule:**
   If multiple independent sources disagree on a variant's nomenclature or consequence (e.g. historical literature codon numbering vs. canonical HGVS numbering, or differing transcript annotations), **the disagreement must be explicitly recorded in the provenance metadata rather than silently selecting the preferred interpretation**.
4. **Mandatory Metadata Fields:** Every record in the evaluation manifest must retain:
   - `provenance_class`: `Class A`, `Class B`, `Class C`, or `Class E`
   - `ground_truth_source`: e.g. `NCBI ClinVar (VCV000015424 / VarID 15424)`
   - `pmid_citations`: list of PubMed IDs supporting the consequence
   - `external_consequence`: external registry molecular consequence string
   - `discrepancy_notes`: explicit notation of historical or nomenclature discrepancies

---

## 5. CANDIDATE STRATIFICATION: TARGET DISTRIBUTION & EVALUABLE REPRESENTATION

### 5.1 Stratification Philosophy: Quality Over Quotas
> *"Variant quality, independent provenance, and biological interpretability take precedence over numerical class quotas."*

The target class counts specified below represent **planning targets**, not rigid mathematical quotas. If a specific class cannot achieve its target count using genuinely independent, un-leaked, verifiable variants:
1. Retain only the highest-quality eligible variants that satisfy all blinding and provenance criteria.
2. Report the achieved sample size $n$ transparently.
3. Document the biological or data availability limitation in the validation report.
4. **Strictly prohibit** manufacturing, loosening inclusion criteria, or substituting questionable variants merely to satisfy a numerical quota.
5. The final evaluation panel size may therefore be smaller or differently distributed than the planning targets.

### 5.2 Target Class Distribution (12 Stratified Variant Classes)

| Class ID | Stratified Variant Class | Planning Target ($n$) | Minimum Evaluable ($n$) | Scope & Biological Verification Criteria |
|:---:|---|:---:|:---:|---|
| **C01** | Missense SNVs | 8–10 | 5 | Pathogenic hemoglobins (Hb S, Hb C, Hb E) and benign exonic polymorphisms across Exons 1, 2, 3. |
| **C02** | Nonsense (Stop-Gain) | 6–8 | 5 | Premature termination codons across Exons 1, 2, 3. |
| **C03** | Synonymous (Silent) | 6–8 | 5 | Benign coding silent substitutions with verified lack of splice site activation. |
| **C04** | Frameshift Deletions | 6–8 | 5 | Authenticated 1-bp, 2-bp, 4-bp deletions with verified downstream termination distance (`fsTerX`). |
| **C05** | In-Frame Deletions | 5–8 | 5 | 3-bp and 6-bp non-frameshifting deletions; must include both codon-aligned and codon-splitting cases. |
| **C06** | Frameshift Duplications / Insertions | 6–8 | 5 | 1-bp, 2-bp duplications and insertions resulting in altered reading frames. |
| **C07** | In-Frame Insertions / Duplications | 5–8 | 5 | 3-bp in-frame insertions and duplications; must test codon junction translation. |
| **C08** | Splice Donor Disruptions | 6–8 | 5 | Invariant donor positions ($+1, +2, +5$) in Intron 1 and Intron 2. |
| **C09** | Splice Acceptor Disruptions | 6–8 | 5 | Invariant acceptor positions ($-1, -2$) in Intron 1 and Intron 2. |
| **C10** | 5' UTR Regulatory Variants | 5–8 | 5 | Promoter, CACCC, and TATA box mutations ($c.-88$ to $c.-28$). |
| **C11** | 3' UTR Regulatory Variants | 5–8 | 5 | Polyadenylation signal mutations (AATAAA alterations, $c.*110$ to $c.*113$). |
| **C12** | Adversarial Negative Controls | 16–20 | 10 | Structured battery: inverted ranges, non-consecutive insertion coords, reference mismatches, out-of-bounds, invalid syntax. |
| **TOTAL** | **Full Stratified Panel ($D_{blind}$)** | **~80–105** | **$\ge 65$** | **12 stratified classes; every evaluated class $n \ge 5$.** |

---

## 6. STRICT EXCLUSION REGISTRY & AUTOMATED LEAKAGE AUDIT GATE

### 6.1 Exclusion Registry (`exclusion_registry.json`)
A candidate variant is permanently disqualified from $D_{blind}$ if it matches any pattern in the **Exclusion Registry**:
1. **Production Code String Literal:** Any variant appearing in `backend/app/` (core, services, api, copilot, or legacy modules).
2. **Regression Test Suite:** Any variant present in `backend/tests/` (unit, integration, or historical tests).
3. **Preset & Example Exposure:** Any variant in `data/examples/`, `backend/app/config.py`, or frontend preset components.
4. **Phase 2A / 2B Development Splits:** Any variant in `research/manifest/development.json` or `research/manifest/validation.json`.
5. **Phase 2B Frozen Test Set:** Any of the 36 variants present in `research/manifest/frozen_test.json` (both the 11 historically tainted variants and the 25 un-leaked variants).

### 6.2 Pre-Flight Automated Leakage Audit Gate (`leakage_audit_gate.py`)
Prior to running the validation harness, an automated AST parser and regex scanner will cross-reference candidate variants against the entire repository:
- Scans for exact cDNA strings (e.g. `c.118C>T`), stripped coordinates (`118C>T`), ClinVar Variation IDs, and protein consequences.
- **Hard Gate Rule:** If even a single match is detected, the script terminates with `EXIT CODE 1`, generates a `leakage_report.json`, and halts execution.

---

## 7. DETERMINISTIC REPRODUCIBILITY HASHING & CANONICAL ARTIFACT

### 7.1 Canonical Result Artifact (`canonical_results.json`)
To eliminate ambiguity in reproducibility verification, the validation harness must generate a strictly normalized canonical result artifact: **`canonical_results.json`**.

### 7.2 Invariants for Canonical Serialization:
The canonical artifact must:
1. Use deterministic JSON serialization (`sort_keys=True`, `indent=2`, UTF-8 encoding).
2. Enforce deterministic key ordering at all dictionary levels.
3. Enforce deterministic numeric formatting (fixed decimal places for floats).
4. **Contain NO timestamps** (execution start, end, duration).
5. **Contain NO random UUIDs** or run identifiers.
6. **Contain NO machine-specific values** (hostname, OS, CPU architecture, process IDs).
7. **Contain NO environment-dependent metadata** (file paths, Python version, memory stats).
8. **Exclude variable network latency and HTTP headers** from the deterministic hash artifact.
9. Contain the complete deterministic molecular consequence result for every evaluated variant.

### 7.3 Reproducibility Verification Rule:
The offline validation harness must be executed 10 consecutive times on the frozen dataset:
$$\text{SHA256}(\text{canonical\_results\_run\_1.json}) == \text{SHA256}(\text{canonical\_results\_run\_2.json}) == \dots == \text{SHA256}(\text{canonical\_results\_run\_10.json})$$
Any non-deterministic operational metadata (such as latency measurements or provider availability) must be evaluated and recorded in a separate operational log (`operational_telemetry.json`) and must **NEVER** form part of the canonical reproducibility hash.

---

## 8. HARD ENGINE FREEZE RULE

### 8.1 Engine Immutability Invariant:
> *"Once the Phase 2C dataset and ground truth manifest are frozen, the production analysis engine MUST NOT be modified before or during execution of the primary validation experiment."*

### 8.2 Execution & Failure Protocol:
When a validation test case fails:
```
           Variant Execution
                  │
                  ▼
          Failure Observed
                  │
                  ▼
       Failure Recorded in Report
                  │
                  ▼
       Validation Run Continues
                  │
                  ▼
    Failures Analyzed After Run
                  │
                  ▼
Potential Remediation Assigned to
     FUTURE Software Version
                  │
                  ▼
Future Version Requires SEPARATE
      Validation Experiment
```

### 8.3 Absolute Prohibition:
```
[PROHIBITED WORKFLOW]
Failure Observed ──→ Code Change in Engine ──→ Re-Run Benchmark ──→ Overwrite Result (FRAUDULENT)
```
Phase 2C test failures are empirical observations that document current algorithmic boundaries. They are **never** reasons to alter the frozen production engine during validation.

---

## 9. STATISTICAL METHODOLOGY & REPORTING STANDARDS

### 9.1 Point Estimates and Confidence Intervals Rule
> *"All point estimates must be accompanied by numerator, denominator, and confidence interval."*  
> *"Observed 100% concordance in a small sample must not be interpreted as evidence of general population-level 100% accuracy."*

- **Example of Correct Scientific Reporting:**
  For a class with $5/5$ concordant predictions:
  > *"The tool achieved $5/5$ ($100.0\%$) observed concordance (Wilson 95% CI: $[56.6\%, 100.0\%]$)."*
- **Example of Prohibited Reporting:**
  > *"The tool demonstrates 100% accuracy on in-frame insertions."* (PROHIBITED)

### 9.2 Wilson Score 95% Confidence Intervals
For all binomial proportions $p = k/n$, 95% confidence intervals will be computed using the **Wilson score interval with continuity correction**:

$$\tilde{p} = \frac{k + \frac{z^2}{2}}{n + z^2}, \quad w = \frac{z}{1 + \frac{z^2}{n}} \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}$$
$$\text{CI}_{95\%} = \left[ \max\left(0, \tilde{p} - w\right), \; \min\left(1, \tilde{p} + w\right) \right]$$
where $z = 1.95996$.

### 9.3 Performance Metrics Formulation:
1. **Binary Diagnostic Performance (Valid Variants vs Adversarial Controls):**
   $$\text{Sensitivity (TPR)} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{Specificity (TNR)} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$
   $$\text{Precision (PPV)} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Overall Accuracy (ACC)} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$
   $$\text{F1-Score} = 2 \cdot \frac{\text{PPV} \cdot \text{TPR}}{\text{PPV} + \text{TPR}}$$
2. **Multi-Class Consequence Concordance:**
   - Evaluated across 9 discrete consequence categories: `Nonsense`, `Missense`, `Synonymous`, `Frameshift`, `In-frame Indel`, `Splice Site`, `5' UTR`, `3' UTR`, `Invalid / Rejected`.
   - Per-class Precision, Recall, and F1. Macro-averaged and Weighted F1.
3. **Information Retrieval (ClinVar Evidence):**
   - Hit@1: Proportion where authentic Variation ID is at Rank 0.
   - Hit@3: Proportion where authentic Variation ID is at Rank $\le 2$.
   - Recall@5: Proportion where authentic Variation ID is in top 5.
   - Mean Reciprocal Rank (MRR): $\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$.

---

## 10. PRE-REGISTRATION WORKFLOW & HUMAN OVERSIGHT CHECKPOINTS

```
[Phase 2C Protocol Approved (CP-1)]
                 │
                 ▼
[Step 1: Independent Candidate Curation]
(Curate variants from ClinVar/IthaGenes satisfying Class A/B/C)
                 │
                 ▼
[Step 2: Automated Leakage Audit Gate]
(Verify 0 leakage against Exclusion Registry)
                 │
                 ▼
[Candidate Pool Human Audit (CP-2)]
(Human review of curated variants & provenance citations)
                 │
                 ▼
[Step 3: Cryptographic Freezing & Engine Freezing]
(Generate phase2c_test.json and phase2c_test.sha256; lock production code)
                 │
                 ▼
[Pre-Run Freezing Sign-Off (CP-3)]
(Human authorization of sealed validation run)
                 │
                 ▼
[Step 4: Sealed Primary & Secondary Experiment Execution]
(Execute Layer A/B offline, B1 offline, B2 live, and C AI evaluation)
                 │
                 ▼
[Step 5: 10-Run Deterministic Reproducibility Verification]
(Assert SHA256 of canonical_results.json is identical across 10 runs)
                 │
                 ▼
[Final Validation Report Certification (CP-4)]
(Audit report, Wilson CIs, and paper-readiness certification)
```

| Checkpoint # | Milestone Name | Mandatory Verification Criteria | Approver Action |
|:---:|---|---|:---:|
| **CP-1** | **Protocol Specification Approval** | Review this revised protocol (`HBB-PROTO-2026-2C v2.0`); verify target separation, provenance classes, stratification rules, canonical hashing, and engine freeze. | **Human Review & Decision (Current Step)** |
| **CP-2** | **Candidate Pool Audit** | Audit curated candidate variant list (`candidate_pool.json`); verify 100% Tier A/B/C citations and 0 matches in Exclusion Registry. | Approve candidate pool for freezing |
| **CP-3** | **Pre-Run Freezing Verification** | Execute `leakage_audit_gate.py` (0 violations); record and verify `phase2c_test.sha256` prior to any runner execution. Confirm engine code lock. | Authorize sealed validation run |
| **CP-4** | **Final Validation Report Sign-Off** | Audit `VALIDATION_REPORT.md`; verify 10-run reproducibility hash match and Wilson CIs on all tables. | Final Paper-Readiness Certification |

---

## 11. PROTOCOL STATUS SUMMARY

- [x] Protocol revised with all 10 scientific corrections.
- [x] Zero Phase 2C datasets created.
- [x] Zero external network queries executed.
- [x] Zero production code modified.
- [x] Zero Phase 2A/2B historical artifacts modified.
- [x] `frozen_test.json` SHA256 verified identical to `frozen_test.sha256`.
- [x] Zero validation executed.
- [ ] **Awaiting Human Review & Decision on Checkpoint CP-1.**
