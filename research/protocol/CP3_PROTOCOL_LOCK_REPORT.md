# Phase 2C — CP3 Protocol Lock Report

> **Document Status:** FORMAL BENCHMARK PROTOCOL LOCK  
> **Stage:** Phase 2C — CP3  
> **Date:** 2026-10-08  
> **Target Protocol:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`

---

## 1. Executive Summary
The Phase 2C benchmark evaluation protocol has been formally locked prior to any benchmark execution. This guarantees that all research questions, primary and secondary endpoints, error taxonomies, comparison rules, and statistical analysis plans are immutably established in advance, preventing any post-hoc bias or cherry-picking.

---

## 2. Key Protocol Commitments
1. **Research Question Formulated Prior to Execution:** Strictly restricted to deterministic molecular consequence transformation under `NM_000518.5`. Clinical diagnosis, pathogenicity prediction, and patient outcomes are explicitly out of scope.
2. **Error Taxonomy Fixed:** 10 predefined error categories locked. No new error categories may be invented in response to benchmark failures.
3. **Zero-Count Policy:** Classes with $N = 0$ (C05, C07, C08, C10) will be reported as `NOT REPRESENTED IN PRIMARY COHORT`, not 0%.
4. **Exact Statistics:** Primary endpoint will report $k/n$, %, and exact 95% Clopper-Pearson binomial confidence intervals.
5. **Complete Cohort Segregation:** Robustness controls (C12, N = 18) and Conditional variants (N = 64) are strictly excluded from the primary benchmark.
6. **Prohibited Post-Hoc Actions:** 8 specific post-hoc adjustments are strictly forbidden.

---

## 3. Mandatory Governance Status Block

```
CP3 STATUS:
READY FOR BENCHMARK

PRIMARY DATASET:
FROZEN

PRIMARY N:
55

CONDITIONAL:
64

ROBUSTNESS:
18

DATASET HASH:
39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96

ENGINE COMMIT:
845f595cc039e006d74237945450c7b4a9569ee6

BENCHMARK EXECUTED:
NO

PERFORMANCE METRICS:
NONE

POST HOC CHANGES:
NONE

HISTORICAL CONTAMINATION:
0

PRODUCTION CODE CHANGES:
0
```

---

## 4. Authorization Boundary
**CRITICAL STOP CONDITION:** Checkpoint CP3 is complete. The benchmark has NOT been executed. Zero performance metrics have been calculated. Work is stopped pending human reviewer authorization.