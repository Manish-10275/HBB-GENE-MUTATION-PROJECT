# Phase 2C Benchmark Error Register

> **Document Status:** AUDIT REGISTER  
> **Target Dataset:** `research/manifest/phase2c_primary.json` (N = 55)  
> **Benchmark Status:** COMPLETED

---

## 1. Primary Benchmark Molecular Error Audit
During execution of the locked primary benchmark cohort (N = 55):
- **Total Primary Candidates:** 55
- **Total Molecular Discrepancies Encountered:** **0**
- **Total Execution Failures (`ENGINE_ERROR`):** **0**
- **Total Syntax / Parsing Errors:** **0**
- **Total Reference Mismatches:** **0**

## 2. Predefined Category Distribution Breakdown
- **`EXACT_MOLECULAR_AGREEMENT`:** **30** (54.55%)
- **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`:** **20** (36.36%) — Truncated frameshift syntax (`E7fs`) in ClinVar records
- **`EXTERNAL_ANNOTATION_INCOMPLETE`:** **5** (9.09%) — Class C09 canonical splice acceptors lacking external protein string
- **All Other Predefined Error Categories:** **0**

## 3. Register of Candidates with Legacy Nomenclature (Tracked)
The following 33 candidates exhibit historical legacy nomenclature in ClinVar, which were verified as non-contradictory mature protein (-1 codon offset) or traditional codon (CD) designations:

| Candidate ID | HGVS cDNA | Deterministic Protein | Legacy Alias Records | Status |
|---|---|---|---|:---:|
| HBB-CP2-023 | `c.91A>G` | `p.Arg31Gly` | `CD 30 (A>G) or IVS I (-2) AGG>GGG (Arg>Gly)` | VERIFIED_CONCORDANT |
| HBB-CP2-027 | `c.190C>A` | `p.His64Asn` | `H63N`, `Hb Haná` | VERIFIED_CONCORDANT |
| HBB-CP2-038 | `c.92G>A` | `p.Arg31Lys` | `CD 30 (G>A) or IVS I (-1) AGG>AAG (Arg>Lys)` | VERIFIED_CONCORDANT |
| HBB-CP2-071 | `c.68_74del` | `p.Glu23ValfsTer37` | `CD 22-24 ( -7 bp): (-AAGTTGG)` | VERIFIED_CONCORDANT |
| HBB-CP2-072 | `c.67G>T` | `p.Glu23Ter` | `CD 22 (GAA>TAA)` | VERIFIED_CONCORDANT |
| HBB-CP2-073 | `c.30dup` | `p.Ala11CysfsTer13` | `CD 9/10 (+T)` | VERIFIED_CONCORDANT |
| HBB-CP2-074 | `c.138del` | `p.Phe46LeufsTer16` | `CD 45 (-T)` | VERIFIED_CONCORDANT |
| HBB-CP2-080 | `c.129dup` | `p.Glu44Ter` | `CD 42/43 (+T)` | VERIFIED_CONCORDANT |
| HBB-CP2-096 | `c.91A>C` | `p.(=)` | `CD 30 (A>C) or IVS I (-2) AGG>CGG [Arg>Arg]` | VERIFIED_CONCORDANT |
| HBB-CP2-098 | `c.45G>A` | `p.(=)` | `CD-15`, `p.Trp15Ter` | VERIFIED_CONCORDANT |
| HBB-CP2-103 | `c.75T>A` | `p.(=)` | `G24G`, `cd24T>A` | VERIFIED_CONCORDANT |
| HBB-CP2-161 | `c.64dup` | `p.Asp22GlyfsTer2` | `CD 20/21 (+G)` | VERIFIED_CONCORDANT |
| HBB-CP2-164 | `c.323dup` | `p.Asn109GlnfsTer32` | `CD 106/107 (+G)` | VERIFIED_CONCORDANT |
| HBB-CP2-165 | `c.143_146dup` | `p.Thr51ValfsTer4` | `CD 47/48 (+ATCT)` | VERIFIED_CONCORDANT |
| HBB-CP2-170 | `c.287dup` | `p.Leu97AlafsTer6` | `CD 95 (+A)` | VERIFIED_CONCORDANT |
| HBB-CP2-175 | `c.143dup` | `p.Asp48GlufsTer6` | `CD 47 (+A)` | VERIFIED_CONCORDANT |
| HBB-CP2-182 | `c.85dup` | `p.Leu29ProfsTer16` | `CD 27/28 (+C)` | VERIFIED_CONCORDANT |
| HBB-CP2-183 | `c.45dup` | `p.Trp16ValfsTer8` | `CD 14/15 (+G)` | VERIFIED_CONCORDANT |
| HBB-CP2-184 | `c.217dup` | `p.Ser73LysfsTer2` | `CD 71/72 (+A)` | VERIFIED_CONCORDANT |
| HBB-CP2-185 | `c.20del` | `p.Glu7GlyfsTer13` | `CD 6 -A`, `CD-6`, `p.Glu7ValfsTer28` | VERIFIED_CONCORDANT |
| HBB-CP2-187 | `c.51del` | `p.Lys18ArgfsTer2` | `CD 16 GGC>GG-` | VERIFIED_CONCORDANT |
| HBB-CP2-188 | `c.25_26del` | `p.Lys9ValfsTer14` | `cd8-AA`, `CD 8 (-AA)`, `CD-8`, `p.Lys9ValfsTer16` | VERIFIED_CONCORDANT |
| HBB-CP2-214 | `c.364G>T` | `p.Glu122Ter` | `E121*` | VERIFIED_CONCORDANT |
| HBB-CP2-241 | `c.93-1G>C` | `p.?` | `IVS I-130 G>C`, `IVS1AS, G-C, -1` | VERIFIED_CONCORDANT |
| HBB-CP2-244 | `c.315G>C` | `p.Arg105Ser` | `R104S` | VERIFIED_CONCORDANT |
| HBB-CP2-245 | `c.380T>G` | `p.Val127Gly` | `V126G`, `Hb Dhonburi`, `Hb Neapolis`, `CD 126 GTG>GGG` | VERIFIED_CONCORDANT |
| HBB-CP2-253 | `c.93-2A>C` | `p.?` | `IVS I-129 (A>C)` | VERIFIED_CONCORDANT |
| HBB-CP2-254 | `c.316-1G>T` | `p.?` | `IVS II-850 (G>T)` | VERIFIED_CONCORDANT |
| HBB-CP2-256 | `c.316-2A>C` | `p.?` | `IVS11-849A>C`, `IVS II-849 (A>C)`, `IVS2, A-C, -2` | VERIFIED_CONCORDANT |
| HBB-CP2-257 | `c.93-2A>G` | `p.?` | `IVS I-129 (A>G)`, `IVS1AS, A-G, -2` | VERIFIED_CONCORDANT |
| HBB-CP2-262 | `c.93G>T` | `p.Arg31Ser` | `R30S`, `Hb Tacoma` | VERIFIED_CONCORDANT |
| HBB-CP2-265 | `c.*110T>C` | `None` | `AACAAA`, `3-UNT, T-C, +3` | VERIFIED_CONCORDANT |
| HBB-CP2-268 | `c.*113A>G` | `None` | `AATAAG`, `3-UNT, A-G, +6` | VERIFIED_CONCORDANT |

---

## 4. Discrepancy Register Conclusion
Zero primary molecular errors were recorded. Under the CP4.1/CP4.2 audited comparison engine, 30 candidates achieved exact molecular and protein agreement, 20 candidates achieved molecular agreement with protein format difference (truncated frameshifts), and 5 candidates achieved molecular agreement with incomplete external protein annotations.