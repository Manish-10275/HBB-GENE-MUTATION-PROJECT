# Phase 2C Class-Stratified Benchmark Results

> **Document Status:** STRATIFIED AUDIT REPORT  
> **Benchmark Cohort:** 55 Biological Primary Candidates  
> **Protocol:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`

---

## 1. Class Stratification Table

| Class ID | Variant Class Name | Represented ($n$) | Successes ($k$) | Discrepancies | Concordance (%) | Exact 95% Clopper-Pearson CI | Uncertainty & Representation Assessment |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | **14** | **14** | 0 | **100.0%** | [76.84%, 100.0%] | Adequately represented cohort ($N=14$) |
| **C02** | Nonsense (Stop-Gain) | **3** | **3** | 0 | **100.0%** | [29.24%, 100.0%] | Small sample size ($N=3$); wide confidence interval |
| **C03** | Synonymous (Silent) | **10** | **10** | 0 | **100.0%** | [69.15%, 100.0%] | Adequately represented cohort ($N=10$) |
| **C04** | Frameshift Deletions | **9** | **9** | 0 | **100.0%** | [66.37%, 100.0%] | Adequately represented cohort ($N=9$) |
| **C05** | In-Frame Indels / Deletions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** (quality constraint) |
| **C06** | Frameshift Duplications / Insertions | **12** | **12** | 0 | **100.0%** | [73.54%, 100.0%] | Adequately represented cohort ($N=12$) |
| **C07** | In-Frame Insertions / Duplications | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** (quality constraint) |
| **C08** | Splice Donor Disruptions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** (quality constraint) |
| **C09** | Splice Acceptor Disruptions | **5** | **5** | 0 | **100.0%** | [47.82%, 100.0%] | Adequately represented cohort ($N=5$) |
| **C10** | 5' UTR Regulatory Variants | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** (quality constraint) |
| **C11** | 3' UTR Regulatory Variants | **2** | **2** | 0 | **100.0%** | [15.81%, 100.0%] | Small sample size ($N=2$); wide confidence interval |
| **TOTAL** | **All 11 Biological Classes** | **55** | **55** | **0** | **100.0%** | **[93.51%, 100.0%]** | **Locked Quality-Constrained Primary Cohort** |

---

## 2. Transparent Documentation of Unrepresented Classes
In strict compliance with the Phase 2C scientific governance guidelines, empty classes are **not** reported as 0% accuracy. They are documented as:

> *Class representation limitations under the current reference, curation, and evidence criteria.*

- **Class C05 (In-Frame Deletions):** $N = 0$. Candidate `HBB-CP2-105` (`c.9_83del`, 25 codons) was retained in Conditional due to structural size and single submitter status.
- **Class C07 (In-Frame Duplications):** $N = 0$. Only 2 clean duplications existed in the candidate pool, both having 0-star ClinVar evidence (retained in secondary).
- **Class C08 (Splice Donor Disruptions):** $N = 0$. Zero canonical $+1, +2, +5$ donor candidates were available in the queried ClinVar pool.
- **Class C10 (5' UTR Regulatory Variants):** $N = 0$. All queried promoter variants ($> -50$ bp upstream) exceed the physical transcript boundary of `NM_000518.5`.

No artificial candidates were synthesized to fill these categories.