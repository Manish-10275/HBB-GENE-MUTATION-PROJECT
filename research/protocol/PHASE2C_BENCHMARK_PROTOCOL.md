# Phase 2C Benchmark Protocol Specification

> **Document Status:** IMMUTABLE PRE-BENCHMARK PROTOCOL LOCK  
> **Stage:** Phase 2C — CP3  
> **Lock State:** LOCKED PRIOR TO BENCHMARK EXECUTION  
> **Primary Evaluation Dataset:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)

---

## 1. Primary Research Question
The primary research question for Phase 2C is formulated as:

> *How consistently does the deterministic HBB molecular consequence engine transform predefined HGVS variants into the expected molecular consequence representation under the fixed NM_000518.5 reference model?*

**Strict Boundary:** This experiment does **NOT** evaluate:
- Clinical disease diagnosis or pathogenicity prediction.
- Clinical validity, actionability, or patient risk.
- Therapeutic efficacy or treatment selection.

---

## 2. Input Dataset Specification
- **Primary Evaluation Dataset:** `research/manifest/phase2c_primary.json`
- **Cohort Size:** Exactly **N = 55** biological candidates.
- **Dataset Integrity:** Verified by SHA256 digest `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`.
- **Immutability Policy:** Dataset is frozen. No post-hoc additions, deletions, or substitutions are permitted.

---

## 3. Reference Transcript Specification
- **Primary Transcript:** RefSeq `NM_000518.5` (Coding Sequence: 1..444 nt, 147 amino acids).
- **Genomic Locus:** RefSeq `NG_000007.3` (HBB region: 70545..72152, 1608 bp).
- **Genome Build:** GRCh38.

---

## 4. Reference Sequence Policy
- The reference sequences are loaded from production reference files without modification.
- Any candidate requiring transcript versions other than `NM_000518.5` is outside the evaluation scope.

---

## 5. Deterministic Engine Software Lock
- **Engine Commit SHA:** `845f595cc039e006d74237945450c7b4a9569ee6`
- **Core Modules:** `backend/app/core/hgvs.py`, `backend/app/core/consequences.py`, `backend/app/core/reference.py`
- **Execution Mode:** Engine executed strictly **AS IS**; zero heuristic overrides, benchmark aliases, or runtime tuning permitted.

---

## 6. HGVS Parsing Rules
- Input strings must follow HGVS Sequence Variant Nomenclature (HGVS v20.05).
- Formats supported: cDNA substitutions (`c.327C>G`), deletions (`c.19del`), duplications (`c.30dup`), insertions (`c.143_146dup`), indels, and canonical splice offsets (`c.93-1G>C`).
- Coordinates outside transcript boundaries or non-canonical syntax will trigger predefined `AnalysisError` exceptions.

---

## 7. Consequence Comparison Rules
Deterministic consequence comparison evaluates category concordance:
- **Missense:** Non-synonymous single amino acid substitution.
- **Nonsense (Stop-Gain):** Introduction of premature termination codon (`Ter`).
- **Synonymous (Silent):** Coding substitution without amino acid alteration (`p.(=)`).
- **Frameshift:** Insertion or deletion where length is not divisible by 3 ($L \pmod 3 \neq 0$).
- **In-Frame Indel:** Insertion or deletion preserving reading frame ($L \pmod 3 = 0$).
- **Splice Site Disruption:** Disruption of invariant donor (`+1, +2`) or acceptor (`-1, -2`) dinucleotides.
- **3' UTR Regulatory:** Non-coding substitution located within the 3' untranslated region (`c.*1..c.*134`).

---

## 8. Protein Comparison Rules
- Standard 3-letter IUPAC amino acid notation is required (e.g. `p.Asn109Lys`, `p.Gln128Ter`, `p.(=)`).
- Synonymous variants must be represented as `p.(=)`.
- Splice junction disruptions are evaluated as `p.?`.
- Frameshift nomenclature must report the terminal offset codon (e.g. `p.Glu7ArgfsTer13`).

---

## 9. Handling of External Annotation Differences
- External database annotations (ClinVar) may exhibit ontology differences or incomplete protein fields.
- Discrepancies where the molecular impact agrees but descriptive terminology differs are cataloged under `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` or `PROTEIN_AGREEMENT_CLASS_DIFFERENCE`.

---

## 10. Handling of Legacy Nomenclature
- Classical hemoglobinopathy literature frequently uses mature protein numbering (-1 amino acid offset, omitting Met-1) or traditional codon/IVS labels (e.g. `CD 30`, `H63N`, `V126G`, `IVS I-130`).
- The benchmark evaluation is conducted strictly against standard `NM_000518.5` coordinates. Legacy aliases are tracked for auditability but do not alter engine scoring.

---

## 11. Handling of Unsupported Variants
- Variants exceeding transcript boundaries (e.g. promoter mutations situated $> -50$ bp upstream) are classified as `ENGINE_UNSUPPORTED` (`OUT_OF_BOUNDS`).

---

## 12. Handling of Ambiguous HGVS
- Any input string with ambiguous positional notation or multiple valid interpretations will be flagged as `HGVS_AMBIGUITY`.

---

## 13. Primary Endpoint Specification
- **Primary Endpoint:** **Deterministic Molecular Consequence Concordance**.
- **Definition:** Proportion of candidates where the deterministic engine output achieves exact consequence category match with the locked expected consequence under `NM_000518.5`.
- **Metric:** Reported as $k / n$, percentage, and exact 95% binomial confidence interval (Clopper-Pearson).

---

## 14. Secondary Endpoints
1. **Protein Consequence Exact Concordance:** Proportion of coding variants achieving exact HGVS protein string match.
2. **Class-Stratified Concordance:** Independent evaluation across each represented biological class.
3. **Error Taxonomy Distribution:** Exact frequency distribution across all predefined error categories.

---

## 15. Predefined Error Categories
The following mutually exclusive categories are locked prior to benchmark execution:

| Category Code | Definition | Endpoint Impact |
|---|---|:---:|
| **`EXACT_MOLECULAR_AGREEMENT`** | Engine consequence and protein consequence agree exactly with expected | **MATCH** |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | Molecular consequence category agrees; protein nomenclature formatting differs | **DISCREPANCY** |
| **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | Protein consequence agrees; classification ontology differs | **DISCREPANCY** |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | External reference record lacks protein or consequence details | **DISCREPANCY** |
| **`EXTERNAL_CONFLICT`** | External repository contains conflicting assertions | **DISCREPANCY** |
| **`REFERENCE_MISMATCH`** | Reference nucleotide in HGVS does not match `NM_000518.5` | **DISCREPANCY** |
| **`HGVS_AMBIGUITY`** | HGVS syntax permits multiple divergent interpretations | **DISCREPANCY** |
| **`ENGINE_UNSUPPORTED`** | Variant lies outside deterministic engine boundary (e.g. promoter $> -50$ bp) | **DISCREPANCY** |
| **`ENGINE_ERROR`** | Engine raises unexpected exception or fails execution | **DISCREPANCY** |
| **`UNRESOLVED`** | Discrepancy cannot be classified under existing rules | **DISCREPANCY** |

---

## 16. Class Stratification Plan
Results must be reported independently for all 11 biological classes:

| Class ID | Variant Class Name | Primary Cohort Count ($N$) | Reporting Protocol |
|:---:|---|:---:|---|
| **C01** | Missense SNVs | 14 | Calculate $k/n$, %, 95% CI |
| **C02** | Nonsense (Stop-Gain) | 3 | Calculate $k/n$, %, 95% CI (note small $N$) |
| **C03** | Synonymous (Silent) | 10 | Calculate $k/n$, %, 95% CI |
| **C04** | Frameshift Deletions | 9 | Calculate $k/n$, %, 95% CI |
| **C05** | In-Frame Indels / Deletions | 0 | **NOT REPRESENTED IN PRIMARY COHORT** (do not report 0%) |
| **C06** | Frameshift Duplications / Insertions | 12 | Calculate $k/n$, %, 95% CI |
| **C07** | In-Frame Insertions / Duplications | 0 | **NOT REPRESENTED IN PRIMARY COHORT** (do not report 0%) |
| **C08** | Splice Donor Disruptions | 0 | **NOT REPRESENTED IN PRIMARY COHORT** (do not report 0%) |
| **C09** | Splice Acceptor Disruptions | 5 | Calculate $k/n$, %, 95% CI |
| **C10** | 5' UTR Regulatory Variants | 0 | **NOT REPRESENTED IN PRIMARY COHORT** (do not report 0%) |
| **C11** | 3' UTR Regulatory Variants | 2 | Calculate $k/n$, %, 95% CI (note small $N$) |

---

## 17. Missing and Invalid Output Handling
- Any crash, unhandled Python exception, or `None` output is automatically classified as `ENGINE_ERROR`.
- No manual exception handling or post-hoc output editing is permitted.

---

## 18. Robustness Experiment Protocol (Experiment D)
- **Cohort:** The 18 synthetic adversarial negative controls in `C12` (`HBB-CP2-297`..`314`).
- **Separation Guarantee:** Robustness controls are evaluated in a standalone experiment and **never mixed with the biological primary cohort**.
- **Endpoint:** Graceful error handling (appropriate `AnalysisError` rejection without crashing).

---

## 19. Statistical Analysis Plan
- **Proportions:** All metrics reported as exact ratio $k / n$ and percentage.
- **Confidence Intervals:** 95% two-sided confidence intervals computed using the exact Clopper-Pearson binomial method:
  $$\text{CI} = \left[ \text{Beta}^{-1}\left(\frac{\alpha}{2}; k, n - k + 1\right), \text{Beta}^{-1}\left(1 - \frac{\alpha}{2}; k + 1, n - k\right) \right]$$
- **Uncertainty Notice:** For small classes ($N < 5$), wide confidence intervals must be explicitly highlighted.
- **Generalization Limitation:** High concordance on this frozen cohort cannot be interpreted as universal generalization across unrepresented classes.

---

## 20. Stopping Rules
The benchmark execution must immediately **HALT** if:
1. A runtime crash or unhandled exception occurs in core deterministic engine modules.
2. A discrepancy reveals an undiscovered defect in the reference sequence model.
3. Dataset hash verification fails.
No silent patches, runtime parameter tuning, or re-runs are permitted.

---

## 21. Prohibited Post-Hoc Modifications
Once this protocol is locked, the following actions are strictly forbidden:
1. Removing difficult candidates from the dataset.
2. Adding easier candidates to boost metrics.
3. Modifying inclusion or exclusion rules.
4. Modifying consequence comparison rules or error categories.
5. Altering the deterministic engine codebase to fit test outcomes.
6. Altering the reference sequence definition.
7. Reclassifying failures post-hoc to improve concordance scores.
8. Iteratively re-running the benchmark until a preferred score is obtained.

---

## 22. Protocol Lock Sign-Off
- **Protocol Version:** 1.0.0
- **Lock Date:** 2026-10-08
- **Benchmark Execution Authorized:** **NO** (Strictly deferred until authorization)