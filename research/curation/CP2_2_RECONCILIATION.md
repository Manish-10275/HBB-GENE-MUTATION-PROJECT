# Phase 2C — CP-2.2 Reconciliation Dossier: Count Definitions & Quality Tier Taxonomy

**Status:** Research Curation Document (Provisional)  
**Date:** October 2026  
**Gene:** *HBB* (Hemoglobin Subunit Beta) | Reference Transcript: `NM_000518.5`

---

## 1. Executive Reconciliation Summary

During the Phase 2C Checkpoint CP-2.1 audit, two distinct candidate tallies were referenced in different analytical contexts:
1. **107 Biological Candidates** with multi-submitter consensus or expert panel review in NCBI ClinVar ($\ge 2$ stars).
2. **97 Total Candidates** categorized into the top tier (`A_STRONG`).

This document provides the mathematical reconciliation between these numbers, documents the exact filtration funnel, and formally establishes the revised, scientifically rigorous terminology for CP-2.2 and beyond.

---

## 2. Mathematical Reconciliation Funnel

The discrepancy between 107 multi-submitter biological records and 97 top-tier candidates is resolved by the following filtration steps:

```
Total Curated Candidate Pool (N = 314)
   │
   ├── Synthetic Adversarial Controls (Class E / C12) ............ n = 18
   └── Biological ClinVar Candidates (Class B / C01-C11) ......... n = 296
          │
          ├── 0-Star ClinVar Records (no assertion criteria) ..... n = 60
          ├── 1-Star ClinVar Records (single submitter) .......... n = 101
          ├── 1-Star ClinVar Records (conflicting assertions) .... n = 28
          └── Multi-Submitter / Expert Panel Records (≥ 2 stars) . n = 107
                 │
                 ├── Disqualified by Exclusion Registry .......... - 3
                 │     (c.316-2A>G, c.93-1G>A, c.316-1G>A)
                 ├── Deep Intronic (> +5 / < -3 bp) (Out of Scope) - 11
                 │     (e.g. c.316-197C>T, c.316-106C>G, c.93-21G>A)
                 ├── Intronic Indels / Duplications (Out of Scope) - 2
                 │     (c.316-171_316-156dup, c.93-22_95del)
                 ├── Conflicting Clinical Pathogenicity Flags .... - 9
                 ├── Non-Standard Bracketed Repeat Syntax ........ - 2
                 │     (c.99GGT[1], c.19GAG[1])
                 └── Complex Indel / Boundary Ambiguity .......... - 1
                 │
                 ▼
          In-Scope, Unconflicted Multi-Submitter Biological Candidates = 79
                 │
                 ▼
          + Synthetic Adversarial Controls (C12) ..................... + 18
                 │
                 ▼
          Total Top-Tier Evaluated Candidates in CP-2.1 ............... = 97
```

### Exact Categorical Arithmetic:
- **107 Multi-Submitter Biological Candidates**
  - **- 3** Excluded by historical Phase 2B manifests
  - **- 11** Quarantined as Deep Intronic ($> +5 / < -3$)
  - **- 2** Quarantined as Complex Intronic Indels
  - **- 9** Quarantined due to Conflicting Classifications
  - **- 2** Quarantined due to Non-Standard Repeat Syntax (`[1]`)
  - **- 1** Quarantined due to Complex Indel Boundary
  - **= 79 Biological High-Confidence Candidates**
- **79 Biological Candidates + 18 Synthetic Robustness Controls = 97 Top-Tier Candidates (`A_STRONG`).**

---

## 3. Revised Quality Tier Taxonomy for CP-2.2

In accordance with Section 3 of the CP-2.2 protocol instructions, the candidate quality tiers are renamed to eliminate the implication that ClinVar consensus represents "independently validated ground truth":

| Old Terminology (CP-2.1) | Revised Terminology (CP-2.2) | Scientific Definition |
|---|---|---|
| `A_STRONG` | **`A_HIGH_CONFIDENCE_DATABASE`** | High-concordance external database record with multiple independent submitters without conflict ($\ge 2$ stars) or expert panel review (3 stars). Unambiguous coding/splicing consequence. |
| `B_MODERATE` | **`B_MODERATE_DATABASE`** | Single-submitter record with assertion criteria provided (1 star) and standard codon-level translation. |
| `C_WEAK` | **`C_LOW_CONFIDENCE_DATABASE`** | Record with no assertion criteria provided (0 stars); provisional annotation requiring secondary literature validation. |
| `D_REVIEW_REQUIRED` | **`D_REVIEW_REQUIRED`** | Conflicting classifications, deep intronic coordinates, complex indels/delins, missing protein consequences, or excluded variants. |
| *(Reserved)* | **`INDEPENDENTLY_CORROBORATED`** | Reserved strictly for variants whose molecular consequence is corroborated by evidence **outside** the ClinVar database ecosystem (e.g. primary peer-reviewed literature or laboratory molecular sequencing dossiers). |

---

## 4. Key Takeaways for Human Review

1. **ClinVar Consensus $\ne$ Primary Literature Ground Truth:** Multiple submitters in ClinVar often cite the same historical paper or secondary database. ClinVar star ratings reflect submitter documentation, not independent biological replication.
2. **Deterministic Engine Scope Invariant:** The deterministic engine models transcript consequences on `NM_000518.5` and invariant splice donor ($+1, +2, +5$) / acceptor ($-1, -2$) positions on `NG_000007.3`. Deep intronic and upstream promoter positions exceeding transcript limits ($> -50$ bp) cannot be evaluated by this engine and must not contaminate the primary benchmark.
3. **Robustness Controls Separation:** Synthetic controls (Class E / C12) test parser error handling and bounds checks; they must never contribute to biological consequence accuracy metrics.
