# CP4.1 — Comparison Semantics Resolution and Protocol Lock

**Project:** HBB Gene Mutation Analyzer  
**Stage:** Phase 2C — CP4.1  
**Document Status:** LOCKED GOVERNANCE SPECIFICATION — NO BENCHMARK EXECUTION  
**Scope:** Final Resolution and Semantic Lock of All Evaluation Endpoints and Comparison Categories  
**Target References:** RefSeq `NM_000518.5` (cDNA), `NG_000007.3` (Genomic)  
**Evaluated Cohort:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`, $N = 55$)  
**Engine Commit Lock:** `845f595cc039e006d74237945450c7b4a9569ee6`  
**Lock Date:** 2026-10-08  

---

## 1. Primary Endpoint Specification

The primary evaluation endpoint of Phase 2C is formally locked as:
$$\textbf{Deterministic Molecular Consequence Concordance}$$

### Governing Definition:
The primary endpoint evaluates the proportion of candidates where the runtime deterministic engine output ($A_{\text{molecular}}$) achieves an exact category match with the normalized external ClinVar molecular annotation ($C_{\text{molecular}}$):
$$\text{Primary Comparison: } \mathbf{A_{\text{molecular}} \text{ versus } C_{\text{molecular}}}$$

### Absolute Prohibition:
The comparison must **NEVER** evaluate $A_{\text{molecular}}$ against $B_{\text{molecular}}$ (`deterministic_molecular_consequence`). Field $B$ is restricted strictly to software regression and self-consistency checking. It is completely excluded from the primary biological concordance metric.

---

## 2. Secondary Protein Endpoint Specification

The protein consequence evaluation is formally locked as a **Secondary Endpoint**:
- **$A_{\text{protein}}$:** Runtime deterministic engine protein consequence in standard IUPAC 3-letter HGVS syntax (e.g. `p.Asn109Lys`, `p.Gln128Ter`, `p.(=)`).
- **$C_{\text{protein}}$:** External ClinVar protein annotation after deterministic normalization (e.g. `N109K` $\rightarrow$ `p.Asn109Lys`, `Q128*` $\rightarrow$ `p.Gln128Ter`).

### Core Hierarchy Rule:
Secondary protein consequence evaluation **must never override a valid primary molecular consequence match**.
- If $A_{\text{molecular}} == C_{\text{molecular}}$ and $A_{\text{protein}} == C_{\text{protein}}$ after deterministic normalization:
  - `primary_endpoint_status`: **`MATCH`**
  - `protein_endpoint_status`: **`MATCH`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**

---

## 3. Missing External Protein Annotation Handling

A missing external protein annotation **must NOT automatically invalidate a valid molecular consequence comparison**.

### Clinical and Database Reality:
External databases (ClinVar) frequently record molecular consequence categories (e.g., `Splice Site Disruption`, `splice_acceptor_variant`) without recording predicted translated protein strings, because predicting translated protein alterations for non-coding or splice-altering variants requires functional RNA sequencing.

### Formal Evaluation Rules:
When molecular consequences agree ($A_{\text{molecular}} == C_{\text{molecular}}$), but external protein annotation is absent ($C_{\text{protein}} \in \{\text{""}, \text{None}\}$):
1. **Primary Molecular Endpoint Status:** **`MATCH`** (The molecular prediction is validated against the external record).
2. **Secondary Protein Endpoint Status:** **`INCOMPLETE`** (The external record lacks protein detail).
3. **Comparison Category:** **`EXTERNAL_ANNOTATION_INCOMPLETE`** (Cataloged transparently as an external annotation limitation).
4. **Negative Guardrails:**
   - **DO NOT** report this as `EXACT_MOLECULAR_AGREEMENT` (because protein annotation is missing).
   - **DO NOT** report this as a primary molecular `DISCREPANCY` (merely because protein annotation is absent).

---

## 4. Class C09 (Splice Site Disruption) Resolution

For the five (5) candidates in Class C09 (`HBB-CP2-241`, `HBB-CP2-253`, `HBB-CP2-254`, `HBB-CP2-256`, `HBB-CP2-257`):
- Runtime Engine Output: `A_mol = "Splice Site Disruption"`, `A_prot = "p.?"`
- External ClinVar Evidence: `C_mol = "Splice Site Disruption"`, `C_prot = ""`

### Locked Resolution:
- $A_{\text{mol}}$ and $C_{\text{mol}}$ agree exactly on the molecular consequence class.
- ClinVar provides no predicted protein consequence.
- **Primary Endpoint Status:** **`MATCH`**
- **Secondary Protein Endpoint:** **`INCOMPLETE`**
- **Comparison Category:** **`EXTERNAL_ANNOTATION_INCOMPLETE`**
- **Scientific Impact:** C09 candidates contribute **5 of 5 matches** to the primary molecular consequence numerator, while being transparently documented under `EXTERNAL_ANNOTATION_INCOMPLETE` to reflect ClinVar's omission of protein strings.

---

## 5. Class C11 (3' UTR Regulatory Variants) Resolution

For the two (2) candidates in Class C11 (`HBB-CP2-265`, `HBB-CP2-268`):
- Runtime Engine Output: `A_mol = "3' UTR Regulatory"`, `A_prot = None`
- External ClinVar Evidence: `C_mol = "3' UTR Regulatory"`, `C_prot = ""`

### Biological and Structural Reality:
3' UTR variants reside downstream of the translation termination codon (`Ter147`). Biologically, non-coding transcript positions have no translated protein product. ClinVar's empty string reflects the genuine biological absence of a protein product, not an omission of data.

### Locked Resolution:
- The implementation must explicitly distinguish **`MISSING_BUT_EXPECTED_NONCODING`** from **`MISSING_REQUIRED_ANNOTATION`**.
- For non-coding classes (C10, C11), when `A_prot is None` and `C_prot in ("", None)`:
  - **Primary Endpoint Status:** **`MATCH`**
  - **Secondary Protein Endpoint:** **`NOT_APPLICABLE`**
  - **Comparison Category:** **`EXACT_MOLECULAR_AGREEMENT`**
- **Negative Guardrail:** Non-coding variants **must NOT** be classified as `EXTERNAL_ANNOTATION_INCOMPLETE`.

---

## 6. Clinical Significance Conflict Separation

Clinical significance assertions (`Pathogenic`, `Likely pathogenic`, `VUS`, `Likely benign`, `Benign`) are orthogonal to molecular consequence evaluation.

### Locked Rules:
1. Disagreement or conflict in clinical significance **never constitutes a molecular consequence conflict**.
2. If ClinVar submitters disagree (e.g. Submitter 1 asserts `Pathogenic`, Submitter 2 asserts `VUS`), but both assert a `Missense` alteration matching the engine's `Missense` prediction:
   - `primary_endpoint_status`: **`MATCH`**
   - `protein_endpoint_status`: **`MATCH`**
   - `clinical_significance_status`: **`CLINICAL_SIGNIFICANCE_CONFLICT`**
   - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
3. `clinical_significance_status` is locked with three mutually exclusive values:
   - `NO_CONFLICT`: Single submission or concordant submissions.
   - `CLINICAL_SIGNIFICANCE_CONFLICT`: Divergent classifications across submitters.
   - `NOT_ASSESSED`: No clinical assertion available.

---

## 7. External Molecular Consequence Conflict Resolution

An external molecular conflict occurs when external repositories assert contradictory molecular consequence categories for the same variant (e.g., Submitter 1 asserts `missense_variant` and Submitter 2 asserts `stop_gained` / Nonsense).

### Locked Rules:
1. **No Arbitrary Selection:** If external evidence contains conflicting molecular classifications without an authoritative consensus, the engine must **NOT** arbitrarily pick one.
2. **No Engine Bias:** The comparison engine must **NOT** select the external assertion that matches the engine.
3. **No Field B Arbitration:** Field $B$ must **NOT** be used to break ties.
4. **Classification:** The variant is classified as:
   - `comparison_category`: **`EXTERNAL_CONFLICT`**
   - `primary_endpoint_status`: **`DISCREPANCY`**
   - Both conflicting external assertions are preserved verbatim in the candidate audit log.

---

## 8. Protein Normalization Rules

Protein normalization must be strictly deterministic, rule-based, and mathematically bounded.

### Prohibited Techniques:
❌ Fuzzy matching  
❌ Substring searching  
❌ Approximate sequence alignment  
❌ Machine learning / LLM interpretation  
❌ Heuristic guessing  

### Locked Normalization Transformations:
1. **Amino Acid Vocabulary:** Bidirectional translation across all 20 standard IUPAC amino acids between 1-letter and 3-letter representations (`CP4_COMPARISON_MAPPING.md`).
2. **Termination Notation:** `*`, `Ter`, `X` resolve to canonical `Ter`.
3. **Missense:** Single amino acid substitutions translate to canonical `(MISSENSE, Codon, RefAA, AltAA)`.
4. **Nonsense:** Premature stops translate to canonical `(NONSENSE, Codon, RefAA, Ter)`.
5. **Synonymous:** Coding silent mutations resolve to canonical `(SYNONYMOUS, Codon, RefAA, =)`. Both CDS-level `p.(=)` and codon-level `p.Leu69=` assert zero translated alteration and are evaluated as concordant.
6. **Frameshift:** Evaluated as described in Section 9.
7. **Splice / Unknown:** `p.?` translates to canonical `(SPLICE_UNKNOWN, None, None, ?)`.
8. **Non-coding:** `None` translates to canonical `(NON_CODING_ABSENT, None, None, None)`.

---

## 9. Frameshift Protein Notation Handling

ClinVar frequently records truncated frameshift syntax (e.g. `E7fs`) indicating only the initial altered codon, whereas the deterministic engine outputs full HGVS nomenclature including the downstream terminal offset codon (e.g. `p.Glu7ArgfsTer13`).

### Locked Resolution:
- When molecular consequences agree independently (`Frameshift == Frameshift`):
  - **Primary Molecular Endpoint Status:** **`MATCH`**
  - **Secondary Protein Endpoint Status:** **`DISCREPANCY`** (or `LIMITED_EXTERNAL_DETAIL`)
  - **Comparison Category:** **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`**
- **Scientific Rationale:** This credits the engine's validated prediction of reading frame disruption, while transparently documenting the difference in descriptive protein formatting.

---

## 10. Legacy Protein Numbering Resolution

Classical literature frequently employs mature protein numbering (-1 amino acid offset, omitting the initiator Met-1 residue, e.g. Hb Vancouver as codon 30 vs standard codon 31).

### Locked Resolution:
1. **Never Assume Equivalence by Appearance:** Identical coordinate strings from different reference models (e.g. `p.Ala130del` vs `p.Leu130del`) must never be assumed equal without formal translation.
2. **ClinVar Manifest Verification:** An exhaustive audit of the 33 legacy candidates in `phase2c_primary.json` confirms that ClinVar's `external_protein_annotation` fields are already indexed to standard RefSeq `NM_000518.5` codon coordinates ($31=31, 64=64, 122=122$).
3. **Rule:** For candidates in `phase2c_primary.json`, no coordinate subtraction is applied. Normalization is strictly limited to 1-letter $\rightarrow$ 3-letter IUPAC translation.
4. **Metadata Preservation:** Legacy nomenclature flags and historical aliases remain recorded in candidate metadata for auditability.

---

## 11. Comparison Category Definitions and Precedence

The ten (10) categories predefined in Protocol Section 15 are formally locked with explicit definitions and attributes:

| # | Category Code | Trigger Condition | Molecular Endpoint | Protein Endpoint | Denominator Status ($N=55$) |
|:---:|---|---|:---:|:---:|:---:|
| 1 | **`ENGINE_ERROR`** | Runtime unhandled exception or system crash | `DISCREPANCY` | `DISCREPANCY` | Included |
| 2 | **`HGVS_AMBIGUITY`** | Non-standard or ambiguous HGVS syntax | `DISCREPANCY` | `DISCREPANCY` | Included |
| 3 | **`REFERENCE_MISMATCH`** | Input reference nucleotide != `NM_000518.5` | `DISCREPANCY` | `DISCREPANCY` | Included |
| 4 | **`ENGINE_UNSUPPORTED`** | Variant lies outside engine scope (e.g. promoter $> -50$ bp) | `DISCREPANCY` | `DISCREPANCY` | Included |
| 5 | **`EXTERNAL_CONFLICT`** | Conflicting external molecular consequence assertions | `DISCREPANCY` | `DISCREPANCY` | Included |
| 6 | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | External record lacks protein annotation for coding/splice variant | **`MATCH`** (C09) / `DISCREPANCY` | **`INCOMPLETE`** | Included |
| 7 | **`EXACT_MOLECULAR_AGREEMENT`** | Concordant on molecular and protein endpoints | **`MATCH`** | **`MATCH`** / `NOT_APPLICABLE` | Included |
| 8 | **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | Molecular agrees; protein syntax formatting differs (`E7fs`) | **`MATCH`** | **`DISCREPANCY`** | Included |
| 9 | **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | Protein agrees; classification ontology differs | `DISCREPANCY` | **`MATCH`** | Included |
| 10 | **`UNRESOLVED`** | Direct molecular and protein disagreement ($A \neq C$) | `DISCREPANCY` | `DISCREPANCY` | Included |

---

## 12. Final Precedence Hierarchy

When multiple conditions or anomalies co-occur for a single candidate, the following deterministic precedence hierarchy governs classification:

$$\begin{array}{clll}
\textbf{Priority} & \textbf{Category Code} & \textbf{State Type} & \textbf{Evaluation Logic} \\
\hline
1 & \text{ENGINE\_ERROR} & \text{Runtime Failure} & \text{Halts execution; captures traceback.} \\
2 & \text{HGVS\_AMBIGUITY} & \text{Input Syntax Error} & \text{Prevents unambiguous transcript mapping.} \\
3 & \text{REFERENCE\_MISMATCH} & \text{Model Inconsistency} & \text{Reference base mismatch invalidates variant.} \\
4 & \text{ENGINE\_UNSUPPORTED} & \text{Scope Boundary} & \text{Coordinates exceed supported boundaries.} \\
5 & \text{EXTERNAL\_CONFLICT} & \text{Evidence Contradiction} & \text{Contradictory external submissions preclude benchmark.} \\
6 & \text{EXTERNAL\_ANNOTATION\_INCOMPLETE} & \text{Evidence Incompleteness} & \text{External record lacks required protein/molecular field.} \\
7 & \text{EXACT\_MOLECULAR\_AGREEMENT} & \text{Concordant Evaluation} & \text{Full agreement on molecular and protein endpoints.} \\
8 & \text{MOLECULAR\_AGREEMENT\_PROTEIN\_DIFFERENCE} & \text{Syntax Divergence} & \text{Molecular match, syntax detail divergence.} \\
9 & \text{PROTEIN\_AGREEMENT\_CLASS\_DIFFERENCE} & \text{Ontology Divergence} & \text{Protein match, classification ontology difference.} \\
10 & \text{UNRESOLVED} & \text{Biological Disagreement} & \text{True consequence discrepancy between engine and external.}
\end{array}$$

---

## 13. Software Regression ($A == B$) Isolation Guarantees

1. **Independent Evaluation:** Software regression is evaluated in a separate, isolated code block:
   ```python
   runtime_expected_match = (
       runtime_output.molecular_consequence == expected_output.expected_molecular and
       runtime_output.protein_consequence == expected_output.expected_protein
   )
   ```
2. **Metadata Only:** `runtime_expected_match` is written strictly to `software_regression_check.regression_concordant`.
3. **No Downstream Leakage:** It never enters `evaluate_external_concordance()`, never influences `comparison_category`, and never alters `primary_endpoint_status`.

---

## 14. Anti-Oracle Test Specifications

Two synthetic test fixtures are locked to guarantee mathematical isolation:

### Test 1: External Disagreement Detection
- $A = \text{Missense}, \quad B = \text{Missense}, \quad C = \text{Nonsense}$
- **Expected:**
  - `runtime_expected_match = True`
  - `primary_endpoint_status = "DISCREPANCY"`
  - `comparison_category = "UNRESOLVED"`
- **Assertion:** $B$ cannot override $C$.

### Test 2: Expected Disagreement Independence
- $A = \text{Missense}, \quad B = \text{Nonsense}, \quad C = \text{Missense}$
- **Expected:**
  - `runtime_expected_match = False`
  - `primary_endpoint_status = "MATCH"`
  - `comparison_category = "EXACT_MOLECULAR_AGREEMENT"`
- **Assertion:** A software regression against $B$ cannot corrupt a valid external concordance match with $C$.

---

## 15. C09 and C11 Test Specifications

### C09 Splice Test Fixture:
- $A_{\text{mol}} = \text{"Splice Site Disruption"}, \quad B_{\text{mol}} = \text{"Splice Site Disruption"}, \quad C_{\text{mol}} = \text{"Splice Site Disruption"}$
- $A_{\text{prot}} = \text{"p.?"}, \quad B_{\text{prot}} = \text{"p.?"}, \quad C_{\text{prot}} = \text{""}$
- **Expected:**
  - `primary_endpoint_status = "MATCH"`
  - `secondary_protein_endpoint = "INCOMPLETE"`
  - `comparison_category = "EXTERNAL_ANNOTATION_INCOMPLETE"`

### C11 3' UTR Test Fixture:
- $A_{\text{mol}} = \text{"3' UTR Regulatory"}, \quad B_{\text{mol}} = \text{"3' UTR Regulatory"}, \quad C_{\text{mol}} = \text{"3' UTR Regulatory"}$
- $A_{\text{prot}} = \text{None}, \quad B_{\text{prot}} = \text{None}, \quad C_{\text{prot}} = \text{""}$
- **Expected:**
  - `primary_endpoint_status = "MATCH"`
  - `secondary_protein_endpoint = "NOT_APPLICABLE"`
  - `comparison_category = "EXACT_MOLECULAR_AGREEMENT"`

---

## 16. Clinical Conflict and Molecular Conflict Test Specifications

### Clinical Conflict Test Fixture:
- $A_{\text{mol}} = \text{"Missense"}, \quad C_{\text{mol}} = \text{"Missense"}$
- Clinical assertions: `["Pathogenic", "Uncertain significance"]`
- **Expected:**
  - `primary_endpoint_status = "MATCH"`
  - `clinical_significance_status = "CLINICAL_SIGNIFICANCE_CONFLICT"`
  - `comparison_category = "EXACT_MOLECULAR_AGREEMENT"`

### External Molecular Conflict Test Fixture:
- External assertions: `["Missense", "Nonsense"]`
- **Expected:**
  - `primary_endpoint_status = "DISCREPANCY"`
  - `comparison_category = "EXTERNAL_CONFLICT"`
  - Engine does not pick the preferred assertion; Field $B$ is not consulted.

---

## 17. Scientific Terminology Lock

All documentation, reports, and code comments must strictly adhere to the locked terminology standards:

### Prohibited Phrases:
❌ *"ground truth"*  
❌ *"independently validated"*  
❌ *"biological truth"*  
❌ *"100% biological accuracy"*  
❌ *"100% biological precision"*  
❌ *"diagnostic accuracy"*  
❌ *"clinical accuracy"*  
❌ *"ClinVar oracle"*  

### Authoritative Approved Terminology:
✅ **`external comparison reference`**  
✅ **`external annotation`**  
✅ **`deterministic molecular consequence`**  
✅ **`molecular concordance`**  
✅ **`software regression / self-consistency`**  
✅ **`high-confidence ClinVar-concordant cohort`**  
✅ **`proposed evaluation cohort`**  
✅ **`external evidence`**  

---

## 18. Absolute Stoppage and No Implementation Rule

### Governance Boundary:
- CP4.1 is strictly a **SEMANTICS RESOLUTION AND PROTOCOL LOCK** stage.
- **DO NOT create `phase2c_comparison_engine.py` or `test_phase2c_comparison_engine.py` during CP4.1.**
- **DO NOT modify `run_phase2c_benchmark.py` during CP4.1.**
- **DO NOT execute any tests against the benchmark during CP4.1.**
- All implementation is strictly deferred to CP4.2.

---

## Final Verification and Sign-Off

### CP4.1 STATUS: **SEMANTICS LOCKED**

---

### 1. Final Primary Endpoint Definition
The primary endpoint is **Deterministic Molecular Consequence Concordance**, calculated strictly between runtime engine output ($A_{\text{molecular}}$) and normalized external ClinVar annotation ($C_{\text{molecular}}$).

### 2. Final Secondary Endpoint Definition
The secondary endpoint is **Protein Consequence Concordance**, calculated between runtime engine protein ($A_{\text{protein}}$) and normalized external ClinVar protein ($C_{\text{protein}}$). Secondary protein status never overrides a valid primary molecular match.

### 3. Final C09 Rule
For Class C09 canonical splice variants, missing external protein strings (`""`) do not invalidate primary molecular consequence concordance. Primary endpoint is **`MATCH`**, protein endpoint is **`INCOMPLETE`**, and category is **`EXTERNAL_ANNOTATION_INCOMPLETE`**.

### 4. Final C11 Rule
For Class C11 3' UTR regulatory variants, non-coding protein absence is expected. Primary endpoint is **`MATCH`**, protein endpoint is **`NOT_APPLICABLE`**, and category is **`EXACT_MOLECULAR_AGREEMENT`**.

### 5. Final Clinical Conflict Rule
Clinical pathogenicity assertions are orthogonal to molecular consequence. Discrepancies across submitters are cataloged under `clinical_significance_status = "CLINICAL_SIGNIFICANCE_CONFLICT"` without altering primary molecular concordance.

### 6. Final External Conflict Rule
Contradictory external molecular assertions trigger `comparison_category = "EXTERNAL_CONFLICT"` and `primary_endpoint_status = "DISCREPANCY"`. The engine does not arbitrate using Field $B$ or its own predictions.

### 7. Final Protein Normalization Rule
Deterministic regex-based parsing maps 1-letter IUPAC codes, asterisk stop notations, and synonymous codon notations into canonical intermediate representations without fuzzy or heuristic matching.

### 8. Final Precedence Hierarchy
Precedence order: `ENGINE_ERROR` > `HGVS_AMBIGUITY` > `REFERENCE_MISMATCH` > `ENGINE_UNSUPPORTED` > `EXTERNAL_CONFLICT` > `EXTERNAL_ANNOTATION_INCOMPLETE` > `EXACT_MOLECULAR_AGREEMENT` > `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` > `PROTEIN_AGREEMENT_CLASS_DIFFERENCE` > `UNRESOLVED`.

### 9. Final Anti-Oracle Guarantees
Field $B$ is isolated to software regression testing. Anti-oracle tests verify that $B$ cannot override $C$, and AST static analysis guarantees zero expected-field tokens inside the comparison engine.

### 10. Exact Implementation Files Permitted in CP4.2
1. `research/curation/phase2c_comparison_engine.py` *(New isolated comparison module)*
2. `research/curation/test_phase2c_comparison_engine.py` *(New unit test suite)*
3. `research/curation/test_ast_anti_leakage.py` *(AST static audit script)*
4. `research/curation/run_phase2c_benchmark.py` *(Refactored execution script)*
