# Phase 2C — CP-2.3.2 Primary Cohort Acceptance Dossier

> **Document Status:** FORMAL GOVERNANCE ACCEPTANCE RECORD  
> **Stage:** Checkpoint CP-2.3.2 (Primary Cohort Acceptance Decision)  
> **Project:** HBB Gene Mutation Analyzer  
> **Decision:** **ACCEPTED (N = 55)**

---

## 1. Formal Decision Statement

> **DECISION STATEMENT:**  

> *The 55 high confidence ClinVar concordant biological candidates are accepted as the proposed primary 
Phase 2C evaluation cohort. Acceptance is based on predefined provenance, deterministic molecular evaluation, 
concordance, and historical separation criteria. The cohort is not considered independently validated ground truth 
and contains known class representation limitations. These limitations are retained transparently rather than addressed 
through artificial candidate substitution or class balancing.*


---

## 2. Mandatory Scientific Status & Disclaimers

- **Scientific Classification:** The cohort comprises **55 high confidence ClinVar concordant biological candidates proposed for the primary Phase 2C evaluation cohort**.

- **Explicitly Excluded Claims:** The candidates are **NOT** described as:

  - *ground truth variants*

  - *independently validated variants*

  - *biologically validated variants*

  - *clinically validated variants*

  - *gold standard variants*

- **Independent Non-ClinVar Corroboration:** Exactly **0 finalized candidates**. External database concordance (ClinVar 2-star/3-star) provides external repository consensus, not independent biological corroboration.


---

## 3. Formal Acceptance Rationale (10 Pillars)

    1. **Exact Set Identity:** The accepted cohort is exactly the 55 candidates approved and locked by CP-2.3.1 without additions, substitutions, or deletions.

2. **Zero Molecular Conflicts:** CP-2.3.1 verified that all 55 candidates exhibit zero molecular consequence category conflicts between external annotation and deterministic engine calculation.

3. **Zero HGVS/Reference Conflicts:** All 55 variants map strictly and consistently to RefSeq transcript `NM_000518.5` (Coding Sequence 1..444 nt).

4. **Zero Protein Consequence Conflicts:** Deterministic protein consequences match external annotations across all coding variants.

5. **Zero Clinical Significance Conflicts Within Cohort:** All 55 accepted variants carry non-conflicting ClinVar pathogenicity assertions (54 multiple submitters consensus 2-star; 1 expert panel 3-star). All 27 conflicting variants remain excluded in Conditional/Quarantine.

6. **Deterministic Engine Reproducibility:** All 55 candidates were deterministically evaluated using the current engine AS IS with 100% internal reproducibility.

7. **Historical Phase 2B Separation:** 100% clean against the Phase 2B exclusion registry and frozen test manifest; zero historical contamination.

8. **Strict Boundary Preservation:** No new candidates were discovered; no Conditional candidates were promoted; no candidates were relaxed.

9. **Predefined High-Confidence Inclusion:** Every candidate meets the predefined $\ge 2$-star consensus or 3-star expert panel inclusion threshold.

10. **Refusal of Artificial Balancing:** The cohort adheres strictly to 'Quality over Quotas' by rejecting manufactured substitutions or relaxed filters.


---

## 4. Methodological Boundaries

The primary evaluation cohort is designed strictly to evaluate **deterministic molecular consequence transformation** (cDNA coordinate mapping, coding frame translation, codon boundary determination, and splice junction identification).


It is **NOT** designed or intended to establish:

- Clinical pathogenicity accuracy

- Diagnostic accuracy

- Clinical validity

- Population-level biological prevalence

- Generalized HBB mutation performance across all 11 variant classes


ClinVar is utilized strictly as an **external evidence source**, not as an infallible biological oracle.


---

## 5. Class Representation Limitations (Quality-Constrained Policy)

In accordance with the project governance, class shortages are **not** interpreted as evidence that HBB lacks such variants biologically. They are formally documented as:


> *Class representation limitations under the current reference, curation, and evidence criteria.*


| Class | Variant Category | Accepted Primary | Curation Limitation & Status Assessment |

|:---:|---|:---:|---|

| **C01** | Missense SNVs | **14** | Adequately populated across Exons 1, 2, 3. |

| **C02** | Nonsense (Stop-Gain) | **3** | Adequately populated with premature termination codons. |

| **C03** | Synonymous (Silent) | **10** | Adequately populated silent coding substitutions. |

| **C04** | Frameshift Deletions | **9** | Adequately populated frameshift deletions. |

| **C05** | In-Frame Indels / Deletions | **0** | **Class Limitation:** 0 approved candidates. Candidate `HBB-CP2-105` (`c.9_83del`, 25-codon deletion) remains `CONDITIONAL` and is **not promoted**. |

| **C06** | Frameshift Duplications / Insertions | **12** | Adequately populated frameshift duplications. |

| **C07** | In-Frame Insertions / Duplications | **0** | **Class Limitation:** 0 approved candidates. Only 2 clean duplications exist in candidate pool, both 0-star ClinVar evidence in secondary cohort. **Not promoted**. |

| **C08** | Splice Donor Disruptions | **0** | **Class Limitation:** 0 approved candidates. No canonical $+1, +2, +5$ donor candidates were present in queried ClinVar pool. **No artificial replacements created**. |

| **C09** | Splice Acceptor Disruptions | **5** | Adequately populated canonical $-1, -2$ acceptor disruptions. |

| **C10** | 5' UTR Regulatory Variants | **0** | **Class Limitation:** 0 approved candidates. Promoter variants situated $> -50$ bp upstream exceed the `NM_000518.5` transcript boundary. **No model expansion or relabeling performed**. |

| **C11** | 3' UTR Regulatory Variants | **2** | Adequately populated polyA signal regulatory SNVs. |

| **TOTAL** | **All 11 Biological Classes** | **55** | **Quality-constrained primary cohort spanning 7 biological classes.** |


---

## 6. Complete Separation of Distinct Cohorts

- **Primary Biological Evaluation Cohort:** N = 55 (Formally Accepted here).

- **Conditional / Exploratory Cohort:** N = 64 (Single-submitter 1-star ClinVar variants, large indel `c.9_83del`, and clinical conflict variants; remain segregated for exploratory analysis).

- **Synthetic Adversarial Robustness Cohort (C12):** N = 18 (Synthetic negative controls `HBB-CP2-297`..`314` reserved strictly for Experiment D; **never merged into biological accuracy metrics**).

- **Excluded / Out-of-Scope Cohort:** N = 53 (Deep intronic, complex indels, out-of-bounds variants).

- **Quarantined Discrepancies:** N = 82 (Includes `HBB-CP2-204` 14-bp frameshift vs ClinVar in-frame claim, `HBB-CP2-156`, `HBB-CP2-201`).


---

## 7. Accepted Candidate Inventory (N = 55)

| Candidate ID | Class | HGVS cDNA | Deterministic Protein | ClinVar VarID | Stars | ClinVar Review Status | Legacy Flag |

|---|:---:|---|---|:---:|:---:|---|:---:|

| HBB-CP2-016 | C01 | `c.327C>G` | `p.Asn109Lys` | [3336287](https://www.ncbi.nlm.nih.gov/clinvar/variation/3336287/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-017 | C01 | `c.400G>T` | `p.Val134Leu` | [3251803](https://www.ncbi.nlm.nih.gov/clinvar/variation/3251803/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-018 | C01 | `c.385G>A` | `p.Ala129Thr` | [3235090](https://www.ncbi.nlm.nih.gov/clinvar/variation/3235090/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-019 | C01 | `c.323G>A` | `p.Gly108Asp` | [2735520](https://www.ncbi.nlm.nih.gov/clinvar/variation/2735520/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-023 | C01 | `c.91A>G` | `p.Arg31Gly` | [869243](https://www.ncbi.nlm.nih.gov/clinvar/variation/869243/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-026 | C01 | `c.294C>G` | `p.His98Gln` | [801186](https://www.ncbi.nlm.nih.gov/clinvar/variation/801186/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-027 | C01 | `c.190C>A` | `p.His64Asn` | [694445](https://www.ncbi.nlm.nih.gov/clinvar/variation/694445/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-028 | C01 | `c.41C>T` | `p.Ala14Val` | [619858](https://www.ncbi.nlm.nih.gov/clinvar/variation/619858/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-031 | C01 | `c.151A>T` | `p.Thr51Ser` | [495980](https://www.ncbi.nlm.nih.gov/clinvar/variation/495980/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-036 | C01 | `c.11T>A` | `p.Leu4Gln` | [439132](https://www.ncbi.nlm.nih.gov/clinvar/variation/439132/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-038 | C01 | `c.92G>A` | `p.Arg31Lys` | [36337](https://www.ncbi.nlm.nih.gov/clinvar/variation/36337/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-058 | C04 | `c.19del` | `p.Glu7ArgfsTer13` | [3068889](https://www.ncbi.nlm.nih.gov/clinvar/variation/3068889/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-063 | C02 | `c.382C>T` | `p.Gln128Ter` | [1705074](https://www.ncbi.nlm.nih.gov/clinvar/variation/1705074/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-064 | C04 | `c.380_396del` | `p.Val127GlufsTer8` | [1459872](https://www.ncbi.nlm.nih.gov/clinvar/variation/1459872/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-067 | C04 | `c.233_234del` | `p.His78ProfsTer13` | [1065151](https://www.ncbi.nlm.nih.gov/clinvar/variation/1065151/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-069 | C04 | `c.396_397del` | `p.Lys133SerfsTer7` | [928758](https://www.ncbi.nlm.nih.gov/clinvar/variation/928758/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-071 | C04 | `c.68_74del` | `p.Glu23ValfsTer37` | [869360](https://www.ncbi.nlm.nih.gov/clinvar/variation/869360/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-072 | C02 | `c.67G>T` | `p.Glu23Ter` | [869359](https://www.ncbi.nlm.nih.gov/clinvar/variation/869359/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-073 | C06 | `c.30dup` | `p.Ala11CysfsTer13` | [869352](https://www.ncbi.nlm.nih.gov/clinvar/variation/869352/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-074 | C04 | `c.138del` | `p.Phe46LeufsTer16` | [869338](https://www.ncbi.nlm.nih.gov/clinvar/variation/869338/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-080 | C06 | `c.129dup` | `p.Glu44Ter` | [869297](https://www.ncbi.nlm.nih.gov/clinvar/variation/869297/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-085 | C03 | `c.207C>A` | `p.(=)` | [3627289](https://www.ncbi.nlm.nih.gov/clinvar/variation/3627289/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-090 | C03 | `c.372C>G` | `p.(=)` | [2501083](https://www.ncbi.nlm.nih.gov/clinvar/variation/2501083/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-091 | C03 | `c.27G>A` | `p.(=)` | [1568873](https://www.ncbi.nlm.nih.gov/clinvar/variation/1568873/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-092 | C03 | `c.21G>A` | `p.(=)` | [933190](https://www.ncbi.nlm.nih.gov/clinvar/variation/933190/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-095 | C03 | `c.51C>T` | `p.(=)` | [811787](https://www.ncbi.nlm.nih.gov/clinvar/variation/811787/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-096 | C03 | `c.91A>C` | `p.(=)` | [590773](https://www.ncbi.nlm.nih.gov/clinvar/variation/590773/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-097 | C03 | `c.327C>T` | `p.(=)` | [495997](https://www.ncbi.nlm.nih.gov/clinvar/variation/495997/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-098 | C03 | `c.45G>A` | `p.(=)` | [440467](https://www.ncbi.nlm.nih.gov/clinvar/variation/440467/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-103 | C03 | `c.75T>A` | `p.(=)` | [15459](https://www.ncbi.nlm.nih.gov/clinvar/variation/15459/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-159 | C06 | `c.221_224dup` | `p.Leu76TrpfsTer17` | [619856](https://www.ncbi.nlm.nih.gov/clinvar/variation/619856/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-160 | C06 | `c.292_295dup` | `p.Val99AlafsTer5` | [619685](https://www.ncbi.nlm.nih.gov/clinvar/variation/619685/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-161 | C06 | `c.64dup` | `p.Asp22GlyfsTer2` | [551389](https://www.ncbi.nlm.nih.gov/clinvar/variation/551389/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-164 | C06 | `c.323dup` | `p.Asn109GlnfsTer32` | [439153](https://www.ncbi.nlm.nih.gov/clinvar/variation/439153/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-165 | C06 | `c.143_146dup` | `p.Thr51ValfsTer4` | [439135](https://www.ncbi.nlm.nih.gov/clinvar/variation/439135/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-168 | C03 | `c.432C>T` | `p.(=)` | [36329](https://www.ncbi.nlm.nih.gov/clinvar/variation/36329/) | 2★ | criteria provided, multiple submitters, no conflicts | NO |
| HBB-CP2-170 | C06 | `c.287dup` | `p.Leu97AlafsTer6` | [36309](https://www.ncbi.nlm.nih.gov/clinvar/variation/36309/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-175 | C06 | `c.143dup` | `p.Asp48GlufsTer6` | [15485](https://www.ncbi.nlm.nih.gov/clinvar/variation/15485/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-182 | C06 | `c.85dup` | `p.Leu29ProfsTer16` | [15432](https://www.ncbi.nlm.nih.gov/clinvar/variation/15432/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-183 | C06 | `c.45dup` | `p.Trp16ValfsTer8` | [15426](https://www.ncbi.nlm.nih.gov/clinvar/variation/15426/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-184 | C06 | `c.217dup` | `p.Ser73LysfsTer2` | [15419](https://www.ncbi.nlm.nih.gov/clinvar/variation/15419/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-185 | C04 | `c.20del` | `p.Glu7GlyfsTer13` | [15418](https://www.ncbi.nlm.nih.gov/clinvar/variation/15418/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-187 | C04 | `c.51del` | `p.Lys18ArgfsTer2` | [15414](https://www.ncbi.nlm.nih.gov/clinvar/variation/15414/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-188 | C04 | `c.25_26del` | `p.Lys9ValfsTer14` | [15413](https://www.ncbi.nlm.nih.gov/clinvar/variation/15413/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-214 | C02 | `c.364G>T` | `p.Glu122Ter` | [15404](https://www.ncbi.nlm.nih.gov/clinvar/variation/15404/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-241 | C09 | `c.93-1G>C` | `p.?` | [439166](https://www.ncbi.nlm.nih.gov/clinvar/variation/439166/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-244 | C01 | `c.315G>C` | `p.Arg105Ser` | [15525](https://www.ncbi.nlm.nih.gov/clinvar/variation/15525/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-245 | C01 | `c.380T>G` | `p.Val127Gly` | [15483](https://www.ncbi.nlm.nih.gov/clinvar/variation/15483/) | 3★ | reviewed by expert panel | YES |
| HBB-CP2-253 | C09 | `c.93-2A>C` | `p.?` | [439167](https://www.ncbi.nlm.nih.gov/clinvar/variation/439167/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-254 | C09 | `c.316-1G>T` | `p.?` | [38671](https://www.ncbi.nlm.nih.gov/clinvar/variation/38671/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-256 | C09 | `c.316-2A>C` | `p.?` | [21190](https://www.ncbi.nlm.nih.gov/clinvar/variation/21190/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-257 | C09 | `c.93-2A>G` | `p.?` | [15562](https://www.ncbi.nlm.nih.gov/clinvar/variation/15562/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-262 | C01 | `c.93G>T` | `p.Arg31Ser` | [15368](https://www.ncbi.nlm.nih.gov/clinvar/variation/15368/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-265 | C11 | `c.*110T>C` | *none* | [36332](https://www.ncbi.nlm.nih.gov/clinvar/variation/36332/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |
| HBB-CP2-268 | C11 | `c.*113A>G` | *none* | [15473](https://www.ncbi.nlm.nih.gov/clinvar/variation/15473/) | 2★ | criteria provided, multiple submitters, no conflicts | YES |

---

## 8. Governance Sign-off & CP-3 Stop Boundary

- **Checkpoint Decision:** ACCEPTED

- **Primary Proposed Cohort:** N = 55

- **Conditional Cohort:** N = 64

- **Robustness Cohort:** N = 18

- **Phase 2C Dataset Frozen:** **NO** (Neither `phase2c_test.json` nor `phase2c_test.sha256` created)

- **Phase 2C Benchmark Executed:** **NO** (Zero performance metrics calculated)

- **Production Code Modified:** **NO** (Zero code changes)

- **CP-3 Status:** **NOT STARTED** (Execution strictly halted pending human reviewer authorization)
