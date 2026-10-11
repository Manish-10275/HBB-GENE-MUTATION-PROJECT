# Phase 2C Experiment D — Robustness & Adversarial Report

> **Document Status:** SEPARATE EXPERIMENT EVALUATION REPORT  
> **Cohort:** 18 Synthetic Negative Controls (`HBB-CP2-297` through `HBB-CP2-314`)  
> **Protocol:** Standalone Robustness Evaluation (Never Merged with Biological Primary Denominator)

---

## 1. Robustness Evaluation Summary
- **Total Adversarial Inputs Tested:** 18
- **Graceful Rejections (`AnalysisError`):** **18**
- **Unhandled Crashes / Silent Mispredictions:** **0**
- **Robustness Rejection Rate:** **100.0%** [95% Exact Clopper-Pearson CI: 81.47%, 100.00%]

---

## 2. Test Battery Breakdown

| Candidate ID | Input HGVS | Error Subtype | Error Code Returned | Engine Message | Result |
|---|---|---|---|---|:---:|
| HBB-CP2-297 | `c.150_145del` | Designed to verify INVALID_COORDINATE rejection without silent guessing. | `INVALID_COORDINATE` | `Invalid coordinate range in 'c.150_145del': start coordinate (mRNA 200) must precede end coordinate (mRNA 195).` | **PASS** |
| HBB-CP2-298 | `c.400_350del` | Designed to verify INVALID_COORDINATE rejection without silent guessing. | `INVALID_COORDINATE` | `Invalid coordinate range in 'c.400_350del': start coordinate (mRNA 450) must precede end coordinate (mRNA 400).` | **PASS** |
| HBB-CP2-299 | `c.250_240dup` | Designed to verify INVALID_COORDINATE rejection without silent guessing. | `INVALID_COORDINATE` | `Invalid coordinate range in 'c.250_240dup': start coordinate must precede or equal end coordinate.` | **PASS** |
| HBB-CP2-300 | `c.50_53insA` | Designed to verify SYNTAX_ERROR rejection without silent guessing. | `INVALID_COORDINATE` | `Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 100 and 103 given).` | **PASS** |
| HBB-CP2-301 | `c.100_104insGCC` | Designed to verify SYNTAX_ERROR rejection without silent guessing. | `INVALID_COORDINATE` | `Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 150 and 154 given).` | **PASS** |
| HBB-CP2-302 | `c.200_205insTT` | Designed to verify SYNTAX_ERROR rejection without silent guessing. | `INVALID_COORDINATE` | `Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 250 and 255 given).` | **PASS** |
| HBB-CP2-303 | `c.650A>G` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Coordinate '650' (mRNA 700) exceeds reference transcript length (628 bp).` | **PASS** |
| HBB-CP2-304 | `c.750del` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Coordinate '750' (mRNA 800) exceeds reference transcript length (628 bp).` | **PASS** |
| HBB-CP2-305 | `c.800dup` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Coordinate '800' (mRNA 850) exceeds reference transcript length (628 bp).` | **PASS** |
| HBB-CP2-306 | `c.92+250G>A` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Intronic coordinate 'c.92+250' exceeds Intron 1 physical length (130 bp).` | **PASS** |
| HBB-CP2-307 | `c.93-200G>A` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Intronic coordinate 'c.93-200' exceeds Intron 1 physical length (130 bp).` | **PASS** |
| HBB-CP2-308 | `c.315+950G>A` | Designed to verify OUT_OF_BOUNDS rejection without silent guessing. | `OUT_OF_BOUNDS` | `Intronic coordinate 'c.315+950' exceeds Intron 2 physical length (850 bp).` | **PASS** |
| HBB-CP2-309 | `c.0A>G` | Designed to verify INVALID_COORDINATE rejection without silent guessing. | `INVALID_COORDINATE` | `HGVS nomenclature does not recognize base zero (c.0). Nucleotide preceding c.1 is c.-1.` | **PASS** |
| HBB-CP2-310 | `c.*0A>G` | Designed to verify INVALID_COORDINATE rejection without silent guessing. | `INVALID_COORDINATE` | `Invalid 3' UTR offset '*0'.` | **PASS** |
| HBB-CP2-311 | `c.50A>Z` | Designed to verify SYNTAX_ERROR rejection without silent guessing. | `SYNTAX_ERROR` | `Invalid nucleotide 'Z' in alternate allele. Must be standard DNA bases (A, C, G, T).` | **PASS** |
| HBB-CP2-312 | `c.delA` | Designed to verify SYNTAX_ERROR rejection without silent guessing. | `SYNTAX_ERROR` | `Unrecognized or malformed HGVS variant syntax 'c.delA'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').` | **PASS** |
| HBB-CP2-313 | `c.70T>A` | Designed to verify REFERENCE_MISMATCH rejection without silent guessing. | `REFERENCE_MISMATCH` | `Reference base mismatch at c.70: query states 'T', but reference sequence NM_000518.5 has 'G'.` | **PASS** |
| HBB-CP2-314 | `c.92+1A>G` | Designed to verify REFERENCE_MISMATCH rejection without silent guessing. | `REFERENCE_MISMATCH` | `Reference base mismatch at c.92+1: query states 'A', but genomic reference NG_000007.3 has 'G'.` | **PASS** |

---

## 3. Robustness Conclusion
All 18 synthetic negative controls were rejected gracefully with explicit typed `AnalysisError` codes. Zero runtime exceptions escaped unhandled.