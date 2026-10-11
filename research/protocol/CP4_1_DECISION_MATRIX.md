# CP4.1 Comparison Semantics Decision Matrix

**Document Status:** LOCKED GOVERNANCE SPECIFICATION  
**Stage:** Phase 2C — CP4.1  
**Target Reference:** RefSeq `NM_000518.5` / `NG_000007.3`  
**Lock Date:** 2026-10-08  

---

## 1. Overview

This document defines the authoritative, deterministic decision matrix governing all candidate evaluations in Phase 2C. Every possible state combination across:
- **Field $A$:** Runtime Deterministic Engine Output
- **Field $C$:** External ClinVar Annotation
- **Field $B$:** Frozen Expected Reference (Software Regression Check Only)

is mapped to exactly one predefined comparison category, primary endpoint status, and secondary protein endpoint status.

---

## 2. Definitive Decision Matrix

| # | Execution / Clinical State | $A_{\text{mol}}$ vs $C_{\text{mol}}$ | $A_{\text{prot}}$ vs $C_{\text{prot}}$ | Comparison Category | Primary Molecular Endpoint | Secondary Protein Endpoint | Software Regression ($A == B$) | Denominator Status ($N=55$) |
|:---:|---|:---:|:---:|---|:---:|:---:|:---:|:---:|
| **1** | Runtime Crash / Unhandled Exception | N/A | N/A | **`ENGINE_ERROR`** | `DISCREPANCY` | `DISCREPANCY` | `FALSE` | Included |
| **2** | Non-standard HGVS / Ambiguous syntax | N/A | N/A | **`HGVS_AMBIGUITY`** | `DISCREPANCY` | `DISCREPANCY` | Evaluated independently | Included |
| **3** | Reference base != `NM_000518.5` | N/A | N/A | **`REFERENCE_MISMATCH`** | `DISCREPANCY` | `DISCREPANCY` | Evaluated independently | Included |
| **4** | Out-of-bounds ($> -50$ bp promoter, etc.) | N/A | N/A | **`ENGINE_UNSUPPORTED`** | `DISCREPANCY` | `DISCREPANCY` | Evaluated independently | Included |
| **5** | Contradictory external submissions | `CONFLICT` | `CONFLICT` | **`EXTERNAL_CONFLICT`** | `DISCREPANCY` | `DISCREPANCY` | Evaluated independently | Included |
| **6** | Coding variant lacking external protein | `MATCH` | `MISSING` | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | **`MATCH`** | **`INCOMPLETE`** | Evaluated independently | Included |
| **7** | Missing external molecular annotation | `MISSING` | Any | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | `DISCREPANCY` | `INCOMPLETE` | Evaluated independently | Included |
| **8** | Concordant molecular & exact protein | `MATCH` | `MATCH` | **`EXACT_MOLECULAR_AGREEMENT`** | **`MATCH`** | **`MATCH`** | Evaluated independently | Included |
| **9** | Concordant 3' UTR non-coding variant | `MATCH` | `ABSENT (NON_CODING)` | **`EXACT_MOLECULAR_AGREEMENT`** | **`MATCH`** | **`NOT_APPLICABLE`** | Evaluated independently | Included |
| **10** | Concordant synonymous semantic translation | `MATCH` | `MATCH (SEMANTIC)` | **`EXACT_MOLECULAR_AGREEMENT`** | **`MATCH`** | **`MATCH`** | Evaluated independently | Included |
| **11** | Concordant molecular, truncated protein (`E7fs`) | `MATCH` | `FORMAT_DIFFERENCE` | **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | **`MATCH`** | **`DISCREPANCY`** | Evaluated independently | Included |
| **12** | Divergent ontology, concordant protein | `DIFFERENCE` | `MATCH` | **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | `DISCREPANCY` | **`MATCH`** | Evaluated independently | Included |
| **13** | Pure biological disagreement ($A \neq C$) | `DIFFERENCE` | `DIFFERENCE` | **`UNRESOLVED`** | `DISCREPANCY` | `DISCREPANCY` | Evaluated independently | Included |

---

## 3. Detailed Endpoint Semantics

### 3.1 Primary Endpoint: Deterministic Molecular Consequence Concordance
- **Evaluation:** $A_{\text{mol}} == C_{\text{mol}}$ (normalized via `CP4_COMPARISON_MAPPING.md`).
- **Valid States:**
  - **`MATCH`**: The engine's predicted molecular consequence category matches the external ClinVar annotation.
  - **`DISCREPANCY`**: The engine's predicted molecular consequence differs from external annotation, engine raises an error, or external annotation is absent/conflicting.
- **Independence Guarantee:** The primary endpoint status is **independent of protein annotation availability** for Class C09 (Splice Site Disruption).

### 3.2 Secondary Endpoint: Protein Consequence Concordance
- **Evaluation:** $A_{\text{prot}}$ vs $C_{\text{prot}}$ (normalized via `CP4_COMPARISON_MAPPING.md`).
- **Valid States:**
  - **`MATCH`**: Both representations denote identical amino acid alteration under `NM_000518.5` coordinates (including normalized 1-letter $\leftrightarrow$ 3-letter, stop notations, and synonymous semantic equivalence).
  - **`DISCREPANCY`**: Both representations exist but differ in residue, codon position, or syntax detail (e.g. truncated `E7fs` vs full `p.Glu7ArgfsTer13`).
  - **`INCOMPLETE`**: External ClinVar record omits protein annotation for a coding or splice-altering variant (`""` or `null`).
  - **`NOT_APPLICABLE`**: The variant resides in a non-coding region (e.g. Class C11 3' UTR) where no translated protein product exists.

### 3.3 Clinical Significance Status
- **Evaluation:** Inspection of ClinVar submitter assertions.
- **Valid States:**
  - **`NO_CONFLICT`**: Single or unanimous clinical assertion (e.g., `Pathogenic`, `Likely pathogenic`, `VUS`).
  - **`CLINICAL_SIGNIFICANCE_CONFLICT`**: Divergent clinical assertions across submitters (e.g., `Pathogenic` vs `VUS`).
  - **`NOT_ASSESSED`**: No clinical interpretation recorded.
- **Boundary Rule:** `clinical_significance_status` is purely an orthogonal audit attribute. It **never alters** the primary molecular endpoint or secondary protein endpoint.

### 3.4 Software Regression Status
- **Evaluation:** $A == B$ ($A_{\text{mol}} == B_{\text{mol}} \land A_{\text{prot}} == B_{\text{prot}}$).
- **Valid States:**
  - **`True`**: The runtime engine reproduces 100% of its previously frozen expected outputs.
  - **`False`**: A software divergence or regression has occurred in the engine runtime.
- **Isolation Guarantee:** Stored in `software_regression_check.regression_concordant`. Has **zero input** into the external biological concordance decision tree.
