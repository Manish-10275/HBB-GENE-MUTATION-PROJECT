# Phase 5.2A — Title and Abstract

> **Document Type:** MANUSCRIPT PRE-DRAFTING FRAMING ARTIFACT  
> **Target Manuscript:** HBB Gene Mutation Analyzer Research Manuscript  
> **Stage:** Phase 5.2A (Title Selection and Structured Abstract Lock)  
> **Governing Documents:** `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md`, `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md`  
> **Frozen Dataset Hash:** `research/manifest/phase2c_primary.sha256` (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Immutability Status:** AUTHORING CONSTRAINED STRICTLY TO TITLE AND STRUCTURED ABSTRACT

---

## Candidate Titles

The following five candidate titles were designed and evaluated against the governing authoring guardrails and scientific risk profiles established in the Manuscript Evidence Matrix:

### Candidate 1 (Central Framing)
> **"Concordance Evaluation of Deterministic HBB Molecular Consequence Prediction Against a Curated ClinVar-Derived External Annotation Reference"**
- **Scientific Accuracy:** **Highest.** Directly reflects the primary benchmark comparison ($A$ vs $C$) without ambiguity.
- **Risk of Overclaiming:** **Lowest.** Uses "Concordance Evaluation" rather than "Validation", explicitly discloses the comparator ("Curated ClinVar-Derived External Annotation Reference"), and specifies the operational mechanism ("Deterministic").
- **Clarity:** **High.** Unambiguously specifies the target gene (*HBB*), mechanism, endpoint, and reference source.
- **Discoverability:** **High.** Indexes under *HBB*, molecular consequence, ClinVar, variant curation, and deterministic algorithms.
- **Alignment with Actual Endpoint:** **Exact.** Directly aligns with the predefined primary endpoint of molecular consequence concordance.
- **Suitability:** **Optimal.** Professional, conservative, and fully defensible for peer-reviewed computational biology / bioinformatics journals.

### Candidate 2
> **"Deterministic Molecular Consequence Prediction in the Human Beta-Globin Gene (HBB): A Computational Concordance Evaluation Against ClinVar Consensus Annotations"**
- **Scientific Accuracy:** **High.** Accurately identifies the computational mechanism, full gene name, and reference standard.
- **Risk of Overclaiming:** **Very Low.** Explicitly restricts the scope to a "Computational Concordance Evaluation".
- **Clarity:** **High.** Expanding *HBB* to "Human Beta-Globin Gene" enhances readability for multidisciplinary audiences.
- **Discoverability:** **Very High.** Strong search indexing for both gene name variants and ClinVar concordance studies.
- **Alignment with Actual Endpoint:** **High.** Accurately captures the primary comparison.
- **Suitability:** **High.** Excellent alternative, slightly longer than Candidate 1.

### Candidate 3
> **"Computational Concordance of Deterministic Molecular Consequence Modeling for Curated HBB Variants"**
- **Scientific Accuracy:** **High.** Confines claims strictly to computational modeling and curated variants.
- **Risk of Overclaiming:** **Low.** Explicitly scopes the candidate pool to "Curated *HBB* Variants".
- **Clarity:** **Moderate-High.** Concise and direct.
- **Discoverability:** **Moderate.** Omits ClinVar from the title, reducing immediate visibility for database curation queries.
- **Alignment with Actual Endpoint:** **Good.** Fully aligned with the computational consequence outcome.
- **Suitability:** **Good.** Lean and conservative, but less descriptive of the comparator source than Candidate 1.

### Candidate 4
> **"Benchmarking Deterministic Molecular Consequence Annotation for HBB Variants Against Curated Database Records"**
- **Scientific Accuracy:** **High.** Accurately frames the work as a computational benchmarking study against database records.
- **Risk of Overclaiming:** **Low.** Uses "Database Records" rather than implying biological ground truth.
- **Clarity:** **High.** Standard benchmarking terminology.
- **Discoverability:** **High.** Appeals to curators and benchmark suite developers.
- **Alignment with Actual Endpoint:** **Good.** Slightly generic ("Database Records" rather than specific ClinVar reference).
- **Suitability:** **High.** Strong computational biology focus.

### Candidate 5
> **"Transcript-Defined Deterministic Consequence Prediction for Human Beta-Globin (HBB) Variants: An Empirical Concordance Study"**
- **Scientific Accuracy:** **High.** Highlights the transcript coordinate dependence (RefSeq NM_000518.5).
- **Risk of Overclaiming:** **Low-Moderate.** "Empirical Concordance Study" is defensible but less precise regarding the external reference than Candidate 1.
- **Clarity:** **High.** Emphasizes transcript definition.
- **Discoverability:** **Moderate.** Omits ClinVar from the title.
- **Alignment with Actual Endpoint:** **Good.** Captures the transcript-defined rules and concordance nature.
- **Suitability:** **Moderate-High.** Sound title, but Candidate 1 provides clearer external comparator attribution.

---

## Recommended Title

### Selected Title:
> **"Concordance Evaluation of Deterministic HBB Molecular Consequence Prediction Against a Curated ClinVar-Derived External Annotation Reference"**

### Rationale:
Candidate 1 is the safest, most precise, and most scientifically defensible choice. It strictly adopts the locked primary title concept (**CLM-TIT-05**) authorized in `MANUSCRIPT_EVIDENCE_MATRIX.md`. It explicitly communicates the exact nature of the study:
1. It replaces value-laden words like "validation" or "accuracy" with the objective metric **"concordance evaluation"**.
2. It clarifies that the algorithm is **"deterministic"** rather than heuristic, statistical, or machine-learned.
3. It names the exact comparator: a **"curated ClinVar-derived external annotation reference"**, preventing any reader from mistaking the database consensus for wet-lab or clinical ground truth.
4. It avoids all prohibited terms (no "AI", no "clinical validation", no "pathogenicity", no "100% accuracy").

---

## Structured Abstract

## Background
Accurate interpretation of human beta-globin (*HBB*) variants requires precise, deterministic molecular consequence computation from standardized HGVS syntax mapped against defined reference transcripts (RefSeq NM_000518.5). In computational variant curation, molecular consequence categorization must remain strictly distinct from clinical significance or pathogenicity predictions.

## Objective
To evaluate whether a deterministic rule-based computational pipeline derives *HBB* molecular consequences concordant with curated external molecular annotations derived from NCBI ClinVar.

## Methods
A deterministic molecular consequence engine operating on RefSeq NM_000518.5 was evaluated against a frozen primary cohort of 55 curated *HBB* variants. External reference annotations were curated ClinVar-derived external molecular annotations. The predefined primary endpoint evaluated concordance between runtime consequence predictions and normalized external annotations, strictly isolating frozen regression baselines. Exact 95% Clopper-Pearson confidence intervals were calculated. Secondary endpoints assessed exact protein nomenclature matching. Input validation was evaluated via an isolated synthetic negative control cohort ($N = 18$).

## Results
Deterministic molecular consequence predictions achieved 55/55 concordance (100.00%; exact 95% CI: 93.51%–100.00%) across seven represented biological classes (30 exact molecular agreements, 20 molecular agreements with protein representation differences, and 5 external annotations lacking protein strings). Secondary exact protein concordance was 50.91% (28/55), reflecting 20 truncated frameshift representations in ClinVar. In a separate robustness experiment, 18/18 synthetic malformed inputs were gracefully rejected.

## Limitations
All 55 primary candidates were derived from ClinVar without independent secondary database corroboration. Cohort admission incorporated deterministic engine agreement during curation, introducing incorporation/verification bias. Four biological classes (C05, C07, C08, C10) were unrepresented ($n = 0$), and classes C02 ($n = 3$) and C11 ($n = 2$) had limited sample sizes. The evaluation measures computational consequence categorization, not clinical significance, pathogenicity, or diagnostic accuracy.

## Conclusion
The deterministic pipeline demonstrated complete molecular consequence concordance within the frozen curated cohort against curated ClinVar-derived external molecular annotations. However, these findings establish computational rule fidelity, not independent biological truth or clinical validity.

---

## Claim Safety Check

This structured abstract has been verified against the locked Prohibited Claims Register and Authoring Guardrails:

| Safety Criterion | Verification Status | Exact Phrasing / Location in Abstract |
|---|:---:|---|
| **No clinical validation claim** | **PASS** | Explicitly stated: *"not clinical significance, pathogenicity, or diagnostic accuracy"* and *"not independent biological truth or clinical validity"*. |
| **No pathogenicity claim** | **PASS** | Background and Limitations explicitly separate molecular consequence categorization from clinical pathogenicity predictions. |
| **No diagnostic accuracy claim** | **PASS** | Term "diagnostic accuracy" is explicitly disclaimed in Limitations; "accuracy" is replaced with "concordance". |
| **No biological accuracy claim** | **PASS** | Conclusion explicitly states findings reflect *"computational rule fidelity, not independent biological truth"*. |
| **Incorporation / verification bias disclosed** | **PASS** | Prominently stated in Limitations: *"Cohort admission incorporated deterministic engine agreement during curation, introducing incorporation/verification bias"*. |
| **ClinVar dependence disclosed** | **PASS** | Title, Objective, Methods, Results, Limitations, and Conclusion explicitly state that external annotations derive from ClinVar. |
| **Zero non-ClinVar corroboration disclosed** | **PASS** | Explicitly stated in Limitations: *"All 55 primary candidates were derived from ClinVar without independent secondary database corroboration"*. |
| **Absent classes disclosed** | **PASS** | Explicitly stated in Limitations: *"Four biological classes (C05, C07, C08, C10) were unrepresented (n = 0)"*. |
| **55/55 correctly scoped to frozen cohort** | **PASS** | Stated in Results: *"55/55 concordance (100.00%...)"* and Conclusion: *"within the frozen curated cohort"*; never generalized to all *HBB* variants. |
| **Confidence interval correctly scoped** | **PASS** | Stated in Results: *"exact 95% CI: 93.51%–100.00%"* via the exact Clopper-Pearson method; no population-wide claims. |
| **Secondary protein divergence reported** | **PASS** | Discloses 50.91% (28/55) exact match and 20 truncated frameshift representations. |
| **Robustness controls isolated** | **PASS** | Robustness results (18/18) reported strictly as a separate experiment, not combined with biological cohort. |
| **Word count compliance** | **PASS** | Abstract body text contains exactly **298 words**, well within the 250–300 word target. |
