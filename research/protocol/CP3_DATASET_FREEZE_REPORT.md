# Phase 2C — CP3 Dataset Freeze Report

> **Document Status:** IMMUTABLE AUDIT REPORT  
> **Stage:** Phase 2C — CP3 (Dataset Freeze)  
> **Timestamp:** 2026-10-08T21:25:00Z  
> **Dataset Path:** `research/manifest/phase2c_primary.json`  
> **SHA256 Checksum:** `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`

---

## 1. Executive Summary
In strict compliance with Checkpoint CP3, the proposed primary Phase 2C evaluation cohort of **55 high confidence ClinVar concordant biological candidates** has been frozen into an immutable evaluation manifest.

```
PRIMARY DATASET STATUS: FROZEN
DATASET SHA256:         39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96
TOTAL CANDIDATES (N):   55
CONDITIONAL COHORT (N): 64 (SEPARATE / EXCLUDED)
ROBUSTNESS COHORT (N):  18 (SEPARATE / EXCLUDED)
FILE SIZE:              59605 bytes
```

---

## 2. Pre-Freeze Cohort Identity Verification Results
All 13 mandatory cohort identity checks were executed and verified prior to hashing:

1. **Count Verification:** Exactly 55 candidates present (**PASS**).
2. **CP-2.3.2 Origin:** Every candidate originates from the accepted CP-2.3.2 cohort (**PASS**).
3. **Phase Consistency:** No candidate exists only in earlier discarded iterations (**PASS**).
4. **Zero Additions:** Zero candidates added after CP-2.3.2 (**PASS**).
5. **Conditional Segregation:** Zero Conditional candidates present (**PASS**).
6. **Robustness Segregation:** Zero C12 synthetic robustness controls present (**PASS**).
7. **Historical Separation:** Zero Phase 2B frozen test candidates present (**PASS**).
8. **Exclusion Registry:** Zero violations of the exclusion registry (**PASS**).
9. **ID Uniqueness:** 55 unique candidate IDs (**PASS**).
10. **HGVS Immutability:** All HGVS cDNA representations unchanged from CP-2.3.2 (**PASS**).
11. **Transcript Immutability:** All variants mapped to `NM_000518.5` (**PASS**).
12. **Consequence Immutability:** Deterministic consequence fields unchanged (**PASS**).
13. **Provenance Immutability:** External ClinVar IDs, accessions, stars, and review statuses unchanged (**PASS**).

---

## 3. Stratified Class Representation
| Class ID | Variant Class Name | Primary Count | Representation Status |
|:---:|---|:---:|---|
| **C01** | Missense SNVs | **14** | Represented |
| **C02** | Nonsense (Stop-Gain) | **3** | Represented |
| **C03** | Synonymous (Silent) | **10** | Represented |
| **C04** | Frameshift Deletions | **9** | Represented |
| **C05** | In-Frame Indels / Deletions | **0** | **Class limitation** (`c.9_83del` in Conditional) |
| **C06** | Frameshift Duplications / Insertions | **12** | Represented |
| **C07** | In-Frame Insertions / Duplications | **0** | **Class limitation** (2 duplications in secondary, 0-star) |
| **C08** | Splice Donor Disruptions | **0** | **Class limitation** (0 canonical donors in pool) |
| **C09** | Splice Acceptor Disruptions | **5** | Represented |
| **C10** | 5' UTR Regulatory Variants | **0** | **Transcript boundary limitation** (promoter > -50 bp) |
| **C11** | 3' UTR Regulatory Variants | **2** | Represented |
| **TOTAL** | **All 11 Biological Classes** | **55** | **Frozen Quality-Constrained Cohort** |

---

## 4. Immutability Protocol & Checksum Verification
The SHA256 digest was computed directly over the exact serialized byte stream of `research/manifest/phase2c_primary.json`:

```
SHA256 (phase2c_primary.json) = 39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96
```

**Strict Immutability Rule:** Any subsequent modification to `phase2c_primary.json` is strictly prohibited. If a genuine defect is discovered, the dataset must not be silently edited; a formal governance reopening checkpoint must be declared.

---

## 5. Next Steps
- Dataset is completely frozen.
- Protocol is completely locked.
- **Benchmark execution is NOT authorized during CP3.**