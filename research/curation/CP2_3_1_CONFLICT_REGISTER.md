# Phase 2C — CP-2.3.1 Conflict Register

> **Document Status:** PROVISIONAL RESEARCH CURATION REGISTER  
> **Cohort Scope:** AUDIT OF 55 PROPOSED BIOLOGICAL PRIMARY CANDIDATES  
> **Reference Standard:** `NM_000518.5`

---

## 1. Molecular Consequence Conflicts (`MOLECULAR: NO_CONFLICT`)

All **55 candidates** in the locked CP-2.3.1 primary cohort demonstrate complete concordance between external ClinVar molecular annotation and deterministic consequence engine calculation:

- **HGVS Conflicts:** 0 detected.

- **Protein Consequence Conflicts:** 0 detected.

- **Reference Sequence Conflicts:** 0 detected.

- **Multiple Molecular Conflicts:** 0 detected.


> **Quarantine Reference:**  

> Candidates with genuine molecular discrepancies (`HBB-CP2-204` `c.170_171insGCAACCCTAAGGTG`, `HBB-CP2-156` `c.-22_23dup`) and protein ambiguities (`HBB-CP2-201` `c.385_388delinsCCACA`) were excluded during CP-2.2 and remain quarantined in `REVIEW_REQUIRED`. None were admitted into this cohort.


---

## 2. Clinical Significance Conflicts (`CLINICAL: NO_CONFLICT`)

All **55 candidates** in the locked CP-2.3.1 primary cohort possess non-conflicting ClinVar pathogenicity assertions (either 2-star consensus or 3-star expert panel review):

- **Clinical Significance Conflicts:** 0 detected in this 55-candidate cohort.


> **Quarantine Reference:**  

> The 27 candidates identified in CP-2.3 with conflicting clinical assertions (e.g. `c.118C>A`, `c.334G>C`, `c.394C>G`) remain in the `CONDITIONAL` / `REVIEW_REQUIRED` cohorts and were strictly excluded from the CP-2.3.1 locked primary cohort.


---

## 3. Legacy Nomenclature and Protein Numbering Analysis

A total of **33 candidates** exhibit legacy nomenclature records. These are NOT biological contradictions, but reflections of historical hemoglobinopathy nomenclature conventions:


### A. The Mature Protein Numbering Offset (-1 Codon Offset)

In classical hematology literature (Weatherall, HbVar, IthaGenes), beta-globin residues were numbered starting from the N-terminal Valine of the mature protein chain after post-translational enzymatic cleavage of the initiator Methionine (Met-1):

- **Classical / Legacy Codon 1:** Valine (`GTG`), corresponding to **HGVS Codon 2** (`p.Val2`).

- **Classical HbS:** `beta 6(A3) Glu>Val`, corresponding to **HGVS** `c.20A>T` (`p.Glu7Val`).


The following 5 candidates in the CP-2.3.1 cohort possess legacy protein notation with this exact -1 amino acid offset:


| Candidate ID | HGVS cDNA | Deterministic Protein (`NM_000518.5`) | Legacy Protein Notation | Numbering Offset Explanation |

|---|---|---|---|---|

| HBB-CP2-027 | `c.190C>A` | `p.His64Asn` | `H63N` | Residue 63 in mature protein equals HGVS codon 64 counting initiator Met-1. |
| HBB-CP2-103 | `c.75T>A` | `p.(=)` | `G24G` | Residue 24 in mature protein equals HGVS codon 25 counting initiator Met-1. |
| HBB-CP2-214 | `c.364G>T` | `p.Glu122Ter` | `E121*` | Residue 121 in mature protein equals HGVS codon 122 counting initiator Met-1. |
| HBB-CP2-244 | `c.315G>C` | `p.Arg105Ser` | `R104S` | Residue 104 in mature protein equals HGVS codon 105 counting initiator Met-1. |
| HBB-CP2-245 | `c.380T>G` | `p.Val127Gly` | `V126G` | Residue 126 in mature protein equals HGVS codon 127 counting initiator Met-1. |
| HBB-CP2-262 | `c.93G>T` | `p.Arg31Ser` | `R30S` | Residue 30 in mature protein equals HGVS codon 31 counting initiator Met-1. |

### B. Traditional Codon (CD) and Intron (IVS) Designations

Traditional thalassemic mutations were named by codon number (`CD`) or intervening sequence position (`IVS`):

- **Codon notation:** e.g. `CD 30`, `CD 22`, `CD 6`, `CD 8`, `CD 45`.

- **IVS notation:** e.g. `IVS I-130 G>C` (`c.93-1G>C`), `IVS II-850 G>T` (`c.316-1G>T`), `IVS II-849 A>C` (`c.316-2A>C`).

- **3' UTR notation:** e.g. `3-UNT, T-C, +3` (`c.*110T>C`), `3-UNT, A-G, +6` (`c.*113A>G`).


All such aliases have been verified as historically authentic and non-contradictory.


---

## 4. Conflict Register Conclusion

- **Total Candidates in Locked Cohort:** 55

- **Total Unresolved Molecular Conflicts:** 0

- **Total Unresolved Clinical Conflicts:** 0

- **Audit Verdict:** Locked CP-2.3.1 cohort is free of molecular and clinical conflicts.
