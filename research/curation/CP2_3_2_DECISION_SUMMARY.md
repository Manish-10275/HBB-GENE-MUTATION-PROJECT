# Phase 2C — CP-2.3.2 Decision Summary Report

> **Document Status:** FORMAL GOVERNANCE DECISION SUMMARY  
> **Stage:** Checkpoint CP-2.3.2  
> **Date:** 2026-10-08

---

## 1. Formal Governance Checkpoint Status


```

CP2.3.2 STATUS:

ACCEPTED


PRIMARY PHASE 2C PROPOSED COHORT:

N = 55


CONDITIONAL COHORT:

N = 64


ROBUSTNESS COHORT:

N = 18


NEW CANDIDATES:

0


INDEPENDENT NON CLINVAR CORROBORATION:

0


PHASE 2C DATASET:

NOT YET FROZEN


PHASE 2C BENCHMARK:

NOT YET EXECUTED


HISTORICAL PHASE 2B TEST HASH:

UNCHANGED


HISTORICAL CONTAMINATION:

0


PRODUCTION CODE CHANGES:

0

```


---

## 2. Cohort Decision Statement

> *The 55 high confidence ClinVar concordant biological candidates are accepted as the proposed primary 
Phase 2C evaluation cohort. Acceptance is based on predefined provenance, deterministic molecular evaluation, 
concordance, and historical separation criteria. The cohort is not considered independently validated ground truth 
and contains known class representation limitations. These limitations are retained transparently rather than addressed 
through artificial candidate substitution or class balancing.*


---

## 3. Class Distribution Summary

| Class | Variant Type | Accepted Primary Count | Curation Status |

|:---:|---|:---:|---|

| **C01** | Missense SNVs | **14** | Accepted (14 candidates) |
| **C02** | Nonsense (Stop-Gain) | **3** | Accepted (3 candidates) |
| **C03** | Synonymous (Silent) | **10** | Accepted (10 candidates) |
| **C04** | Frameshift Deletions | **9** | Accepted (9 candidates) |
| **C05** | In-Frame Indels / Deletions | **0** | Class limitation (0 accepted; c.9_83del retained in Conditional) |
| **C06** | Frameshift Duplications / Insertions | **12** | Accepted (12 candidates) |
| **C07** | In-Frame Insertions / Duplications | **0** | Class limitation (0 accepted; 2 duplications in secondary 0-star) |
| **C08** | Splice Donor Disruptions | **0** | Class limitation (0 accepted; 0 canonical donors in pool) |
| **C09** | Splice Acceptor Disruptions | **5** | Accepted (5 candidates) |
| **C10** | 5' UTR Regulatory Variants | **0** | Transcript boundary limitation (0 accepted; promoter > -50 bp) |
| **C11** | 3' UTR Regulatory Variants | **2** | Accepted (2 candidates) |
| **TOTAL** | **All 11 Biological Classes** | **55** | **Accepted quality-constrained primary cohort** |


---

## 4. Integrity and Compliance Checklist

- [x] Exactly the CP-2.3.1 approved candidate set used as input (55 candidates).

- [x] Zero new candidates added.

- [x] Zero conditional candidates promoted.

- [x] Zero historical Phase 2B candidates reintroduced.

- [x] Zero molecular consequence conflicts.

- [x] Zero HGVS or reference conflicts.

- [x] Zero clinical significance conflicts within accepted cohort.

- [x] Current deterministic engine executed AS IS with 100% reproducibility.

- [x] Historical Phase 2B hash unchanged (`2f6b8842...`).

- [x] Zero production code files modified.

- [x] Zero validation benchmarks executed.

- [x] No final Phase 2C dataset hash generated.

- [x] Phase 2C dataset remains unfrozen.

- [x] Checkpoint CP-3 has NOT started.
