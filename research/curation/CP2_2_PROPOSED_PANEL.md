# Phase 2C — CP-2.2 Proposed Final Evaluation Panel

> **Document Status:** PROVISIONAL RESEARCH CURATION PANEL PROPOSAL  
> **Review State:** PENDING HUMAN REVIEW & APPROVAL  
> **Immutability Guarantee:** ZERO PRODUCTION CODE CHANGES — NO DATASET FROZEN — NO SHA256 GENERATED

---

## 1. Executive Summary & Panel Construction Strategy

In accordance with the principle that **scientific quality and independent molecular verifiability take precedence over rigid quotas**, this panel proposal establishes the maximum scientifically defensible cohort for Phase 2C validation.

Class balance was not artificially forced. Classes with genuine biological data availability limitations (such as C07 in-frame duplications, C08 splice donors, and C10 promoter variants exceeding transcript boundaries) are reported with complete transparency rather than filled with questionable or manufactured variants.

### Summary Panel Distribution:

- **Proposed Primary Biological Panel (C01–C11):** **119 candidates**

- **Proposed Primary Robustness Battery (C12 / Experiment D):** **18 controls**

- **Proposed Secondary Panel:** **42 candidates**

- **Quarantined for Expert Human Review:** **82 candidates**

- **Excluded / Out of Scope (Do Not Use):** **53 candidates**


---

## 2. Class Availability & Panel Balance Summary

| Class | Stratified Variant Class | Total Curated | Proposed Primary | Proposed Secondary | Quarantined Review | Out of Scope / Excluded | Scientific Availability Assessment / Shortage Rationale |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | 64 | **42** | 3 | 15 | 4 | Robustly populated; high-confidence coding missense SNVs across Exons 1, 2, 3. |
| **C02** | Nonsense (Stop-Gain) | 10 | **5** | 2 | 0 | 3 | Adequately populated (n=5); all 5 stop-gain premature termination codons verified. |
| **C03** | Synonymous (Silent) | 22 | **14** | 0 | 6 | 2 | Robustly populated (n=14); silent coding substitutions verified. |
| **C04** | Frameshift Deletions | 32 | **22** | 4 | 5 | 1 | Robustly populated (n=22); 1-bp/2-bp frameshifting deletions verified with termination distance. |
| **C05** | In-Frame Indel | 14 | **1** | 1 | 11 | 1 | Data-limited primary (n=1 primary, n=1 sec); complex delins quarantined in review. |
| **C06** | Frameshift Duplications / Insertions | 61 | **24** | 30 | 5 | 2 | Robustly populated (n=24 primary, n=30 secondary); 1-bp/2-bp coding duplications verified. |
| **C07** | In-Frame Insertions / Duplications | 5 | **0** | 2 | 3 | 0 | Data-availability shortage (n=0 primary, n=2 secondary); only 2 pure duplications, both 0-star ClinVar. |
| **C08** | Splice Disruptions | 18 | **0** | 0 | 0 | 18 | Data-availability limitation (n=0 primary); zero canonical +1, +2, +5 donors present in queried pool. |
| **C09** | Splice Acceptor Disruptions | 24 | **6** | 0 | 0 | 18 | Robustly populated (n=6 primary); canonical invariant acceptor dinucleotides (-1, -2) verified. |
| **C10** | 5' UTR Regulatory Variants | 36 | **0** | 0 | 33 | 3 | Transcript modeling boundary (n=0 primary); promoter variants (> -50 bp) exceed NM_000518.5 transcript. |
| **C11** | 3' UTR Regulatory Variants | 10 | **5** | 0 | 4 | 1 | Adequately populated (n=5 primary); polyadenylation signal regulatory SNVs verified. |
| **C12** | Adversarial Negative Controls | 18 | **18** | 0 | 0 | 0 | Fully populated (n=18); reserved exclusively for Experiment D (Robustness Negative Controls). |

---

## 3. Proposed Primary Evaluation Panel

Candidates qualifying for the primary deterministic molecular-consequence validation cohort:


| candidate_id | HGVS | Class | Engine Consequence | Engine Protein | External Consequence | Comparison | Evidence Source | Quality Tier | Review Priority | Reason for Inclusion |
|---|---|:---:|---|---|---|:---:|---|:---:|:---:|---|
| HBB-CP2-001 | `c.11T>G` | C01 | Missense | `p.Leu4Arg` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-002 | `c.358G>A` | C01 | Missense | `p.Gly120Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-003 | `c.235C>A` | C01 | Missense | `p.Leu79Met` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-004 | `c.103G>C` | C01 | Missense | `p.Val35Leu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-005 | `c.163G>A` | C01 | Missense | `p.Val55Ile` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-006 | `c.327C>A` | C01 | Missense | `p.Asn109Lys` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-007 | `c.325A>C` | C01 | Missense | `p.Asn109His` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-008 | `c.94C>A` | C01 | Missense | `p.Leu32Met` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-009 | `c.240C>A` | C01 | Missense | `p.Asp80Glu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-010 | `c.61G>C` | C01 | Missense | `p.Val21Leu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-011 | `c.9T>G` | C01 | Missense | `p.His3Gln` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-012 | `c.396G>T` | C01 | Missense | `p.Gln132His` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-013 | `c.73G>A` | C01 | Missense | `p.Gly25Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-014 | `c.347C>T` | C01 | Missense | `p.Ala116Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-015 | `c.161C>T` | C01 | Missense | `p.Ala54Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-016 | `c.327C>G` | C01 | Missense | `p.Asn109Lys` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-017 | `c.400G>T` | C01 | Missense | `p.Val134Leu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-018 | `c.385G>A` | C01 | Missense | `p.Ala129Thr` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-019 | `c.323G>A` | C01 | Missense | `p.Gly108Asp` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-020 | `c.116C>G` | C01 | Missense | `p.Thr39Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-021 | `c.407C>T` | C01 | Missense | `p.Ala136Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-022 | `c.40G>A` | C01 | Missense | `p.Ala14Thr` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-023 | `c.91A>G` | C01 | Missense | `p.Arg31Gly` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-026 | `c.294C>G` | C01 | Missense | `p.His98Gln` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-027 | `c.190C>A` | C01 | Missense | `p.His64Asn` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-028 | `c.41C>T` | C01 | Missense | `p.Ala14Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-029 | `c.70G>C` | C01 | Missense | `p.Val24Leu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-031 | `c.151A>T` | C01 | Missense | `p.Thr51Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-033 | `c.98T>A` | C01 | Missense | `p.Leu33Gln` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-036 | `c.11T>A` | C01 | Missense | `p.Leu4Gln` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-038 | `c.92G>A` | C01 | Missense | `p.Arg31Lys` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-039 | `c.212C>T` | C01 | Missense | `p.Ala71Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-043 | `c.386C>T` | C01 | Missense | `p.Ala129Val` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-045 | `c.116C>A` | C01 | Missense | `p.Thr39Asn` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-046 | `c.62T>A` | C01 | Missense | `p.Val21Glu` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-049 | `c.125T>C` | C01 | Missense | `p.Phe42Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-050 | `c.203T>G` | C01 | Missense | `p.Val68Gly` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-051 | `c.55del` | C04 | Frameshift | `p.Val19Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-052 | `c.36dup` | C06 | Frameshift | `p.Thr13TyrfsTer11` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-053 | `c.327del` | C04 | Frameshift | `p.Asn109LysfsTer50` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-054 | `c.275del` | C04 | Frameshift | `p.Leu92ArgfsTer67` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-056 | `c.20_21del` | C04 | Frameshift | `p.Glu7GlyfsTer16` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-057 | `c.126_129dup` | C06 | Frameshift | `p.Glu44LeufsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-058 | `c.19del` | C04 | Frameshift | `p.Glu7ArgfsTer13` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-059 | `c.263_267dup` | C06 | Frameshift | `p.Ser90HisfsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-060 | `c.114del` | C04 | Frameshift | `p.Trp38Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-061 | `c.118_121dup` | C06 | Frameshift | `p.Arg41ThrfsTer5` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-063 | `c.382C>T` | C02 | Nonsense | `p.Gln128Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-064 | `c.380_396del` | C04 | Frameshift | `p.Val127GlufsTer8` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-065 | `c.126dup` | C06 | Frameshift | `p.Phe43LeufsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-066 | `c.196A>T` | C02 | Nonsense | `p.Lys66Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-067 | `c.233_234del` | C04 | Frameshift | `p.His78ProfsTer13` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-069 | `c.396_397del` | C04 | Frameshift | `p.Lys133SerfsTer7` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-070 | `c.78dup` | C06 | Frameshift | `p.Glu27Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-071 | `c.68_74del` | C04 | Frameshift | `p.Glu23ValfsTer37` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-072 | `c.67G>T` | C02 | Nonsense | `p.Glu23Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-073 | `c.30dup` | C06 | Frameshift | `p.Ala11CysfsTer13` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-074 | `c.138del` | C04 | Frameshift | `p.Phe46LeufsTer16` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-078 | `c.394C>T` | C02 | Nonsense | `p.Gln132Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-079 | `c.253_260del` | C04 | Frameshift | `p.Thr85HisfsTer4` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-080 | `c.129dup` | C06 | Frameshift | `p.Glu44Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-081 | `c.375dup` | C06 | Frameshift | `p.Pro126ThrfsTer15` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-084 | `c.189T>C` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-085 | `c.207C>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-088 | `c.276G>T` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-089 | `c.12G>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-090 | `c.372C>G` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-091 | `c.27G>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-092 | `c.21G>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-093 | `c.351T>C` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-095 | `c.51C>T` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-096 | `c.91A>C` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-097 | `c.327C>T` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-098 | `c.45G>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-103 | `c.75T>A` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-104 | `c.206_216del` | C04 | Frameshift | `p.Leu69GlnfsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-105 | `c.9_83del` | C05 | In-frame Indel | `p.Thr5_Leu29del` | In-frame Indel | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-106 | `c.331del` | C04 | Frameshift | `p.Leu111TrpfsTer48` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-107 | `c.84_90del` | C04 | Frameshift | `p.Leu29GlyfsTer31` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-108 | `c.199_202del` | C04 | Frameshift | `p.Lys67CysfsTer22` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-109 | `c.346del` | C04 | Frameshift | `p.Ala116ProfsTer43` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-123 | `c.389_401del` | C04 | Frameshift | `p.Ala130GlyfsTer25` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-124 | `c.269del` | C04 | Frameshift | `p.Ser90MetfsTer69` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-129 | `c.345_348dup` | C06 | Frameshift | `p.His117GlyfsTer25` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-130 | `c.342dup` | C06 | Frameshift | `p.Leu115AlafsTer26` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-159 | `c.221_224dup` | C06 | Frameshift | `p.Leu76TrpfsTer17` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-160 | `c.292_295dup` | C06 | Frameshift | `p.Val99AlafsTer5` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-161 | `c.64dup` | C06 | Frameshift | `p.Asp22GlyfsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-163 | `c.33dup` | C06 | Frameshift | `p.Val12ArgfsTer12` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-164 | `c.323dup` | C06 | Frameshift | `p.Asn109GlnfsTer32` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-165 | `c.143_146dup` | C06 | Frameshift | `p.Thr51ValfsTer4` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-168 | `c.432C>T` | C03 | Synonymous | `p.(=)` | Synonymous | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-170 | `c.287dup` | C06 | Frameshift | `p.Leu97AlafsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-175 | `c.143dup` | C06 | Frameshift | `p.Asp48GlufsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-182 | `c.85dup` | C06 | Frameshift | `p.Leu29ProfsTer16` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-183 | `c.45dup` | C06 | Frameshift | `p.Trp16ValfsTer8` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-184 | `c.217dup` | C06 | Frameshift | `p.Ser73LysfsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-185 | `c.20del` | C04 | Frameshift | `p.Glu7GlyfsTer13` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-187 | `c.51del` | C04 | Frameshift | `p.Lys18ArgfsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-188 | `c.25_26del` | C04 | Frameshift | `p.Lys9ValfsTer14` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-199 | `c.224_225insTCCAG` | C06 | Frameshift | `p.Leu76ProfsTer16` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-205 | `c.279_280insGTGG` | C06 | Frameshift | `p.Cys94ValfsTer3` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-208 | `c.*110T>A` | C11 | 3' UTR Regulatory | *none* | 3' UTR Regulatory | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-214 | `c.364G>T` | C02 | Nonsense | `p.Glu122Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-237 | `c.92G>T` | C01 | Missense | `p.Arg31Met` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-239 | `c.*47C>G` | C11 | 3' UTR Regulatory | *none* | 3' UTR Regulatory | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-241 | `c.93-1G>C` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-244 | `c.315G>C` | C01 | Missense | `p.Arg105Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-245 | `c.380T>G` | C01 | Missense | `p.Val127Gly` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-253 | `c.93-2A>C` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-254 | `c.316-1G>T` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-256 | `c.316-2A>C` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-257 | `c.93-2A>G` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-258 | `c.316-1G>C` | C09 | Splice Site Disruption | `p.?` | Splice Site Disruption | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-262 | `c.93G>T` | C01 | Missense | `p.Arg31Ser` | Missense | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-264 | `c.*115A>C` | C11 | 3' UTR Regulatory | *none* | 3' UTR Regulatory | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-265 | `c.*110T>C` | C11 | 3' UTR Regulatory | *none* | 3' UTR Regulatory | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-268 | `c.*113A>G` | C11 | 3' UTR Regulatory | *none* | 3' UTR Regulatory | EXACT_AGREEMENT | NCBI ClinVar | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-296 | `c.169G>C` | C01 | Missense | `p.Gly57Arg` | Missense | EXACT_AGREEMENT | NCBI ClinVar | B_MODERATE_DATABASE | **HIGH** | Deterministic engine result agrees with external record. |
| HBB-CP2-297 | `c.150_145del` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Invalid coordinate range in 'c.150_145del': start coordinate (mRNA 200) must precede end coordinate (mRNA 195).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-298 | `c.400_350del` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Invalid coordinate range in 'c.400_350del': start coordinate (mRNA 450) must precede end coordinate (mRNA 400).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-299 | `c.250_240dup` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Invalid coordinate range in 'c.250_240dup': start coordinate must precede or equal end coordinate.; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-300 | `c.50_53insA` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 100 and 103 given).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-301 | `c.100_104insGCC` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 150 and 154 given).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-302 | `c.200_205insTT` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Insertion coordinates must designate two consecutive flanking nucleotides (mRNA 250 and 255 given).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-303 | `c.650A>G` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Coordinate '650' (mRNA 700) exceeds reference transcript length (628 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-304 | `c.750del` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Coordinate '750' (mRNA 800) exceeds reference transcript length (628 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-305 | `c.800dup` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Coordinate '800' (mRNA 850) exceeds reference transcript length (628 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-306 | `c.92+250G>A` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Intronic coordinate 'c.92+250' exceeds Intron 1 physical length (130 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-307 | `c.93-200G>A` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Intronic coordinate 'c.93-200' exceeds Intron 1 physical length (130 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-308 | `c.315+950G>A` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: OUT_OF_BOUNDS - Intronic coordinate 'c.315+950' exceeds Intron 2 physical length (850 bp).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-309 | `c.0A>G` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - HGVS nomenclature does not recognize base zero (c.0). Nucleotide preceding c.1 is c.-1.; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-310 | `c.*0A>G` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: INVALID_COORDINATE - Invalid 3' UTR offset '*0'.; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-311 | `c.50A>Z` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: SYNTAX_ERROR - Invalid nucleotide 'Z' in alternate allele. Must be standard DNA bases (A, C, G, T).; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-312 | `c.delA` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: SYNTAX_ERROR - Unrecognized or malformed HGVS variant syntax 'c.delA'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-313 | `c.70T>A` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: REFERENCE_MISMATCH - Reference base mismatch at c.70: query states 'T', but reference sequence NM_000518.5 has 'G'.; Reserved for Experiment D (Robustness Negative Controls). |
| HBB-CP2-314 | `c.92+1A>G` | C12 | N/A | *none* | Invalid / Rejected | EXACT_AGREEMENT | Synthetic Adversarial Control | A_HIGH_CONFIDENCE_DATABASE | **HIGH** | Engine rejected invalid input as expected: REFERENCE_MISMATCH - Reference base mismatch at c.92+1: query states 'A', but genomic reference NG_000007.3 has 'G'.; Reserved for Experiment D (Robustness Negative Controls). |

---

## 4. Proposed Secondary Evaluation Panel

Candidates suitable for exploratory or secondary evaluation cohorts (e.g. 0-star ClinVar evidence with verified biological plausibility):


| candidate_id | HGVS | Class | Engine Consequence | Engine Protein | External Consequence | Comparison | Evidence Source | Quality Tier | Reason for Secondary Status |
|---|---|:---:|---|---|---|:---:|---|:---:|---|
| HBB-CP2-040 | `c.184A>C` | C01 | Missense | `p.Lys62Gln` | Missense | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-041 | `c.385G>C` | C01 | Missense | `p.Ala129Pro` | Missense | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-047 | `c.383A>G` | C01 | Missense | `p.Gln128Arg` | Missense | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-055 | `c.268_281del` | C04 | Frameshift | `p.Ser90Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-075 | `c.417dup` | C06 | Frameshift | `p.Asn140Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-077 | `c.397A>T` | C02 | Nonsense | `p.Lys133Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-082 | `c.339T>A` | C02 | Nonsense | `p.Cys113Ter` | Nonsense | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-083 | `c.244_265del` | C04 | Frameshift | `p.Leu82Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-111 | `c.43del` | C04 | Frameshift | `p.Leu15CysfsTer5` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-112 | `c.155_167del` | C04 | Frameshift | `p.Pro52ArgfsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-125 | `c.299_315dup` | C06 | Frameshift | `p.Leu106IlefsTer59` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-133 | `c.9dup` | C06 | Frameshift | `p.Leu4SerfsTer4` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-134 | `c.50dup` | C06 | Frameshift | `p.Lys18GlnfsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-135 | `c.166dup` | C06 | Frameshift | `p.Met56AsnfsTer5` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-136 | `c.163dup` | C06 | Frameshift | `p.Val55GlyfsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-137 | `c.142dup` | C06 | Frameshift | `p.Asp48GlyfsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-138 | `c.138dup` | C06 | Frameshift | `p.Gly47TrpfsTer7` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-140 | `c.92_94dup` | C07 | In-frame Indel | `p.Arg31dup` | In-frame Indel | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-141 | `c.44dup` | C06 | Frameshift | `p.Trp16ValfsTer8` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-142 | `c.395dup` | C06 | Frameshift | `p.Lys133GlufsTer8` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-143 | `c.275dup` | C06 | Frameshift | `p.His93AlafsTer3` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-144 | `c.272_295dup` | C07 | In-frame Indel | `p.Glu91_His98dup` | In-frame Indel | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-145 | `c.266dup` | C06 | Frameshift | `p.Ser90GlufsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-146 | `c.258dup` | C06 | Frameshift | `p.Ala87CysfsTer5` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-147 | `c.255dup` | C06 | Frameshift | `p.Phe86LeufsTer6` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-148 | `c.24dup` | C06 | Frameshift | `p.Lys9GlufsTer15` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-149 | `c.130dup` | C06 | Frameshift | `p.Glu44GlyfsTer10` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-150 | `c.125dup` | C06 | Frameshift | `p.Phe43LeufsTer2` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-151 | `c.11dup` | C06 | Frameshift | `p.Thr5AspfsTer3` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-152 | `c.339_345dup` | C06 | Frameshift | `p.Ala116CysfsTer27` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-154 | `c.235dup` | C06 | Frameshift | `p.Leu79ProfsTer13` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-155 | `c.219dup` | C06 | Frameshift | `p.Asp74Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-157 | `c.187_251dup` | C06 | Frameshift | `p.Thr85LeufsTer27` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-158 | `c.176dup` | C06 | Frameshift | `p.Lys60Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-181 | `c.216dup` | C06 | Frameshift | `p.Ser73Ter` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-194 | `c.105_106insCTAC` | C06 | Frameshift | `p.Tyr36LeufsTer10` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-200 | `c.28_29insTA` | C06 | Frameshift | `p.Ser10LeufsTer11` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-202 | `c.27_28insAGAA` | C06 | Frameshift | `p.Ser10ArgfsTer15` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-203 | `c.349_350insTGAT` | C06 | Frameshift | `p.His117LeufsTer25` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-209 | `c.415_417del` | C05 | In-frame Indel | `p.Ala139del` | In-frame Indel | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-210 | `c.79_80insT` | C06 | Frameshift | `p.Glu27ValfsTer18` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |
| HBB-CP2-215 | `c.436_437insCT` | C06 | Frameshift | `p.Tyr146SerfsTer14` | Frameshift | EXACT_AGREEMENT | NCBI ClinVar | C_LOW_CONFIDENCE_DATABASE | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |

---

## 5. Excluded Candidates & Out-of-Scope Rationale (`DO_NOT_USE`)

Candidates permanently disqualified or quarantined outside the deterministic engine's scope:


| candidate_id | HGVS | Class | Reason for Disqualification | Evidence / Source of Exclusion |
|---|---|:---:|---|---|
| HBB-CP2-025 | `c.118C>A` | C01 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.118C>A' previously exposed in codebase or Phase 2B manifests. | VarID:811501 |
| HBB-CP2-086 | `c.15T>A` | C03 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.15T>A' previously exposed in codebase or Phase 2B manifests. | VarID:3572117 |
| HBB-CP2-101 | `c.9T>C` | C03 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.9T>C' previously exposed in codebase or Phase 2B manifests. | VarID:193106 |
| HBB-CP2-113 | `c.79G>A` | C01 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.79G>A' previously exposed in codebase or Phase 2B manifests. | VarID:3777010 |
| HBB-CP2-114 | `c.316-33del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-33del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2875907 |
| HBB-CP2-115 | `c.316-405del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-405del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2739204 |
| HBB-CP2-116 | `c.316-38del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-38del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2700062 |
| HBB-CP2-118 | `c.316-48del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-48del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2107602 |
| HBB-CP2-119 | `c.93-65_93-64del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-65_93-64del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2097478 |
| HBB-CP2-120 | `c.93-33_101del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-33_101del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2044665 |
| HBB-CP2-121 | `c.316-328del` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-328del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2025792 |
| HBB-CP2-122 | `c.93-33_96delinsACTGTCCCTTGGGCTGTTTTCCTACCCTCAGATTA` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-33_96delinsACTGTCCCTTGGGCTGTTTTCCTACCCTCAGATTA'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2024192 |
| HBB-CP2-126 | `c.363dup` | C06 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.363DUP' previously exposed in codebase or Phase 2B manifests. | VarID:3572119 |
| HBB-CP2-127 | `c.316-315dup` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-315dup'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2849928 |
| HBB-CP2-128 | `c.93-9dup` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-9dup'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:2825403 |
| HBB-CP2-131 | `c.316-171_316-156dup` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-171_316-156dup'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:1563749 |
| HBB-CP2-132 | `c.316-115dup` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-115dup'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:1136202 |
| HBB-CP2-153 | `c.316-98_316-86dup` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-98_316-86dup'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:869277 |
| HBB-CP2-171 | `c.27dup` | C06 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.27DUP' previously exposed in codebase or Phase 2B manifests. | VarID:36308 |
| HBB-CP2-174 | `c.316-2A>G` | C09 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.316-2A>G' previously exposed in codebase or Phase 2B manifests. | VarID:21191 |
| HBB-CP2-178 | `c.316-197C>T` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:15458 |
| HBB-CP2-179 | `c.316-106C>G` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:15457 |
| HBB-CP2-180 | `c.93-21G>A` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:15454 |
| HBB-CP2-186 | `c.126_129del` | C04 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.126_129DEL' previously exposed in codebase or Phase 2B manifests. | VarID:15417 |
| HBB-CP2-189 | `c.47G>A` | C02 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.47G>A' previously exposed in codebase or Phase 2B manifests. | VarID:15403 |
| HBB-CP2-190 | `c.118C>T` | C02 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.118C>T' previously exposed in codebase or Phase 2B manifests. | VarID:15402 |
| HBB-CP2-191 | `c.52A>T` | C02 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.52A>T' previously exposed in codebase or Phase 2B manifests. | VarID:15401 |
| HBB-CP2-192 | `c.20A>T` | C01 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.20A>T' previously exposed in codebase or Phase 2B manifests. | VarID:15333 |
| HBB-CP2-198 | `c.316-290_316-289insGGGCAATAATTT` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-290_316-289insGGGCAATAATTT'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:1130606 |
| HBB-CP2-206 | `c.93-30_96delinsGTCCCTTGGGCTGTTTTCCTACCCTCAGATTA` | C08 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-30_96delinsGTCCCTTGGGCTGTTTTCCTACCCTCAGATTA'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:439168 |
| HBB-CP2-218 | `c.2T>C` | C01 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.2T>C' previously exposed in codebase or Phase 2B manifests. | VarID:36310 |
| HBB-CP2-219 | `c.316-3C>A` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:15451 |
| HBB-CP2-222 | `c.127_129del` | C05 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.127_129DEL' previously exposed in codebase or Phase 2B manifests. | VarID:15121 |
| HBB-CP2-224 | `c.316-12_316-7delinsCTCCTA` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.316-12_316-7delinsCTCCTA'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:4848400 |
| HBB-CP2-238 | `c.316-79G>A` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:2199483 |
| HBB-CP2-240 | `c.316-145G>A` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:632848 |
| HBB-CP2-242 | `c.93-3T>G` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:36341 |
| HBB-CP2-243 | `c.316-146T>G` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:36312 |
| HBB-CP2-246 | `c.93-1G>A` | C09 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.93-1G>A' previously exposed in codebase or Phase 2B manifests. | VarID:15446 |
| HBB-CP2-247 | `c.316-12T>C` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:810861 |
| HBB-CP2-248 | `c.93-21_96del` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-21_96del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:632854 |
| HBB-CP2-249 | `c.316-3C>G` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:619687 |
| HBB-CP2-250 | `c.316-1G>A` | C09 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.316-1G>A' previously exposed in codebase or Phase 2B manifests. | VarID:552712 |
| HBB-CP2-251 | `c.316-7C>A` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:551906 |
| HBB-CP2-252 | `c.93-15T>G` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:550356 |
| HBB-CP2-255 | `c.316-14T>G` | C09 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:36313 |
| HBB-CP2-259 | `c.316-8T>G` | C08 | Deterministic engine result agrees with external record.; Deep intronic position outside deterministic engine scope. | VarID:15453 |
| HBB-CP2-260 | `c.93-22_95del` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-22_95del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:15442 |
| HBB-CP2-261 | `c.93-17_93-1del` | C09 | Non-standard syntax: Unrecognized or malformed HGVS variant syntax 'c.93-17_93-1del'. Supported notations: SNV ('c.118C>T'), splice ('c.92+5G>C'), deletion ('c.15del', 'c.20_22del'), duplication ('c.27dup'), and insertion ('c.27_28insG').; Deep intronic position outside deterministic engine scope. | VarID:15441 |
| HBB-CP2-266 | `c.-50A>C` | C10 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.-50A>C' previously exposed in codebase or Phase 2B manifests. | VarID:36292 |
| HBB-CP2-267 | `c.*111A>G` | C11 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.*111A>G' previously exposed in codebase or Phase 2B manifests. | VarID:15488 |
| HBB-CP2-282 | `c.-29G>A` | C10 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.-29G>A' previously exposed in codebase or Phase 2B manifests. | VarID:393702 |
| HBB-CP2-291 | `c.-78A>C` | C10 | Disqualified by Exclusion Registry: Exclusion Registry: cDNA string 'C.-78A>C' previously exposed in codebase or Phase 2B manifests. | VarID:15470 |