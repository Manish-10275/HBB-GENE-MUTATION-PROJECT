# CP4.3A — Independent Candidate Level Result Audit

> **Audit Document:** INDEPENDENT SCIENTIFIC INTEGRITY AUDIT  
> **Target Artifact:** `research/results/phase2c_benchmark_candidate_results.json` ($N = 55$)  
> **Source Manifest:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de...`)  
> **Locked Protocol:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`  
> **Audit Scope:** Candidate-by-Candidate Micro-Audit of All 55 Records

---

## Verdict

```
CP4.3A AUDIT VERDICT: PASS
PRIMARY COHORT INTEGRITY: VERIFIED (55 / 55)
DATASET IMMUTABILITY: VERIFIED (BYTE-FOR-BYTE IDENTICAL)
ANTI-ORACLE ISOLATION: VERIFIED (FIELD B STRICTLY ISOLATED)
CATEGORY ASSIGNMENTS: VERIFIED (100% CONCORDANT WITH CP4.1 DECISION MATRIX)
```

The candidate-level benchmark records in `research/results/phase2c_benchmark_candidate_results.json` were audited individually against `research/manifest/phase2c_primary.json` and the locked comparison semantics in `research/protocol/CP4_1_DECISION_MATRIX.md`. All 55 candidate records exhibit 100% internal and external consistency without leakage, heuristic arbitration, or post-hoc alteration.

---

## Independent aggregate reconstruction

Recalculated directly from the individual 55 candidate records (independent of any stored summary metadata):

- **$N$ (Total Primary Cohort):** `55`
- **Molecular Matches ($k$):** `55`
- **Molecular Discrepancies:** `0`
- **Execution Failures / Errors:** `0`
- **Observed Molecular Concordance:** **100.00%** (`55 / 55`)
- **Exact Clopper-Pearson 95% Confidence Interval:** **[93.51%, 100.0%]**

---

## Category reconstruction

Independent tally across all ten predefined comparison categories:

| Predefined Category | Count | Proportion | Impact on Primary Endpoint | Primary Evaluation Rule |
|---|:---:|:---:|:---:|---|
| **`EXACT_MOLECULAR_AGREEMENT`** | **30** | 54.55% | MATCH | A_mol == C_mol and A_prot == C_prot |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | **20** | 36.36% | MATCH | A_mol == C_mol but A_prot != C_prot |
| **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | **5** | 9.09% | MATCH | A_mol == C_mol but C_prot incomplete |
| **`EXTERNAL_CONFLICT`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`REFERENCE_MISMATCH`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`HGVS_AMBIGUITY`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`ENGINE_UNSUPPORTED`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`ENGINE_ERROR`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **`UNRESOLVED`** | **0** | 0.00% | DISCREPANCY | Defined error/discrepancy state |
| **TOTAL** | **55** | **100.00%** | | |

---

## Class reconstruction

Independent class stratification audit across all 11 biological classes:

| Class ID | Variant Class Name | Represented ($n$) | Matches ($k$) | Discrepancies | Concordance (%) | Exact 95% Clopper-Pearson CI | Scientific Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | **14** | **14** | 0 | **100.0%** | [76.84%, 100.0%] | Adequately represented cohort ($n=14$) |
| **C02** | Nonsense (Stop-Gain) | **3** | **3** | 0 | **100.0%** | [29.24%, 100.0%] | Small sample size ($n < 5$); wide CI |
| **C03** | Synonymous (Silent) | **10** | **10** | 0 | **100.0%** | [69.15%, 100.0%] | Adequately represented cohort ($n=10$) |
| **C04** | Frameshift Deletions | **9** | **9** | 0 | **100.0%** | [66.37%, 100.0%] | Adequately represented cohort ($n=9$) |
| **C05** | In-Frame Indels / Deletions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C06** | Frameshift Duplications / Insertions | **12** | **12** | 0 | **100.0%** | [73.54%, 100.0%] | Adequately represented cohort ($n=12$) |
| **C07** | In-Frame Insertions / Duplications | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C08** | Splice Donor Disruptions | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C09** | Splice Acceptor Disruptions | **5** | **5** | 0 | **100.0%** | [47.82%, 100.0%] | Adequately represented cohort ($n=5$) |
| **C10** | 5' UTR Regulatory Variants | **0** | — | — | — | — | **NOT REPRESENTED IN PRIMARY COHORT** |
| **C11** | 3' UTR Regulatory Variants | **2** | **2** | 0 | **100.0%** | [15.81%, 100.0%] | Small sample size ($n < 5$); wide CI |
| **TOTAL** | **All 11 Biological Classes** | **55** | **55** | **0** | **100.0%** | **[93.51%, 100.0%]** | **Primary Evaluation Cohort** |

---

## C09 audit

Independent micro-audit of all 5 Class C09 canonical splice acceptor candidates:

| Candidate ID | HGVS Input | Runtime Mol ($A_{\text{mol}}$) | Runtime Prot ($A_{\text{prot}}$) | External Mol ($C_{\text{mol}}$) | External Prot ($C_{\text{prot}}$) | Primary Endpoint | Protein Endpoint | Category Assigned | Software Regression ($A == B$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **HBB-CP2-241** | `c.93-1G>C` | Splice Site Disruption | `p.?` | Splice Site Disruption | `''` | **MATCH** | **INCOMPLETE** | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | TRUE |
| **HBB-CP2-253** | `c.93-2A>C` | Splice Site Disruption | `p.?` | Splice Site Disruption | `''` | **MATCH** | **INCOMPLETE** | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | TRUE |
| **HBB-CP2-254** | `c.316-1G>T` | Splice Site Disruption | `p.?` | Splice Site Disruption | `''` | **MATCH** | **INCOMPLETE** | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | TRUE |
| **HBB-CP2-256** | `c.316-2A>C` | Splice Site Disruption | `p.?` | Splice Site Disruption | `''` | **MATCH** | **INCOMPLETE** | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | TRUE |
| **HBB-CP2-257** | `c.93-2A>G` | Splice Site Disruption | `p.?` | Splice Site Disruption | `''` | **MATCH** | **INCOMPLETE** | **`EXTERNAL_ANNOTATION_INCOMPLETE`** | TRUE |

### C09 Verification Findings:
1. **External Molecular Evidence Present:** All 5 C09 variants have explicit, non-empty external molecular consequence annotations: `"Splice Site Disruption"`. None are missing.
2. **Runtime Molecular Consequence Concordance:** The deterministic engine predicted `"Splice Site Disruption"` for all 5 variants. Field $A_{\text{mol}}$ matches Field $C_{\text{mol}}$ exactly.
3. **Missing Protein Annotation Isolated:** ClinVar provides an empty string (`""`) for external protein annotation across all 5 records. This is correctly evaluated as `protein_endpoint_status = INCOMPLETE`.
4. **Category Conformance:** All 5 records are classified under `EXTERNAL_ANNOTATION_INCOMPLETE` in strict adherence to Rule 6 of `CP4_1_DECISION_MATRIX.md`.
5. **Primary Endpoint Independence:** The primary molecular consequence endpoint is credited as `MATCH` and is completely unaffected by the missing protein annotation string.

---

## Exceptions

Every candidate record was checked for:
- Inconsistencies between stored fields and manifest inputs: **0 detected**
- Inconsistencies between runtime engine output and re-evaluated comparison: **0 detected**
- Missing external molecular annotations credited as MATCH: **0 detected**
- Hidden `EXTERNAL_CONFLICT` or unhandled categories: **0 detected**
- Discrepancies masked under incorrect categories: **0 detected**
- Field $B$ (expected deterministic reference) influence on biological concordance: **0 detected**

> **Explicit Exception Register:** `ZERO EXCEPTIONS FOUND`. All 55 records strictly conform to the locked protocol.

---

## Complete 55-Candidate Micro-Audit Register

| Candidate ID | Class | HGVS cDNA | Runtime $A_{\text{mol}}$ | External $C_{\text{mol}}$ | Primary Endpoint | Comparison Category | Runtime $A_{\text{prot}}$ | External $C_{\text{prot}}$ | Protein Endpoint | Regression $A == B$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| HBB-CP2-016 | C01 | `c.327C>G` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Asn109Lys` | `N109K` | MATCH | TRUE |
| HBB-CP2-017 | C01 | `c.400G>T` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Val134Leu` | `V134L` | MATCH | TRUE |
| HBB-CP2-018 | C01 | `c.385G>A` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Ala129Thr` | `A129T` | MATCH | TRUE |
| HBB-CP2-019 | C01 | `c.323G>A` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Gly108Asp` | `G108D` | MATCH | TRUE |
| HBB-CP2-023 | C01 | `c.91A>G` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Arg31Gly` | `R31G` | MATCH | TRUE |
| HBB-CP2-026 | C01 | `c.294C>G` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.His98Gln` | `H98Q` | MATCH | TRUE |
| HBB-CP2-027 | C01 | `c.190C>A` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.His64Asn` | `H64N` | MATCH | TRUE |
| HBB-CP2-028 | C01 | `c.41C>T` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Ala14Val` | `A14V` | MATCH | TRUE |
| HBB-CP2-031 | C01 | `c.151A>T` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Thr51Ser` | `T51S` | MATCH | TRUE |
| HBB-CP2-036 | C01 | `c.11T>A` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Leu4Gln` | `L4Q` | MATCH | TRUE |
| HBB-CP2-038 | C01 | `c.92G>A` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Arg31Lys` | `R31K` | MATCH | TRUE |
| HBB-CP2-058 | C04 | `c.19del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Glu7ArgfsTer13` | `E7fs` | DISCREPANCY | TRUE |
| HBB-CP2-063 | C02 | `c.382C>T` | Nonsense | Nonsense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Gln128Ter` | `Q128*` | MATCH | TRUE |
| HBB-CP2-064 | C04 | `c.380_396del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Val127GlufsTer8` | `V127fs` | DISCREPANCY | TRUE |
| HBB-CP2-067 | C04 | `c.233_234del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.His78ProfsTer13` | `H78fs` | DISCREPANCY | TRUE |
| HBB-CP2-069 | C04 | `c.396_397del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Lys133SerfsTer7` | `K133fs` | DISCREPANCY | TRUE |
| HBB-CP2-071 | C04 | `c.68_74del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Glu23ValfsTer37` | `E23fs` | DISCREPANCY | TRUE |
| HBB-CP2-072 | C02 | `c.67G>T` | Nonsense | Nonsense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Glu23Ter` | `E23*` | MATCH | TRUE |
| HBB-CP2-073 | C06 | `c.30dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Ala11CysfsTer13` | `A11fs` | DISCREPANCY | TRUE |
| HBB-CP2-074 | C04 | `c.138del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Phe46LeufsTer16` | `F46fs` | DISCREPANCY | TRUE |
| HBB-CP2-080 | C06 | `c.129dup` | Frameshift | Frameshift | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Glu44Ter` | `E44*` | MATCH | TRUE |
| HBB-CP2-085 | C03 | `c.207C>A` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Leu69=` | MATCH | TRUE |
| HBB-CP2-090 | C03 | `c.372C>G` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Thr124=` | MATCH | TRUE |
| HBB-CP2-091 | C03 | `c.27G>A` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Lys9=` | MATCH | TRUE |
| HBB-CP2-092 | C03 | `c.21G>A` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Glu7=` | MATCH | TRUE |
| HBB-CP2-095 | C03 | `c.51C>T` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Gly17=` | MATCH | TRUE |
| HBB-CP2-096 | C03 | `c.91A>C` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Arg31=` | MATCH | TRUE |
| HBB-CP2-097 | C03 | `c.327C>T` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Asn109=` | MATCH | TRUE |
| HBB-CP2-098 | C03 | `c.45G>A` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Leu15=` | MATCH | TRUE |
| HBB-CP2-103 | C03 | `c.75T>A` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.Gly25=` | MATCH | TRUE |
| HBB-CP2-159 | C06 | `c.221_224dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Leu76TrpfsTer17` | `L76fs` | DISCREPANCY | TRUE |
| HBB-CP2-160 | C06 | `c.292_295dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Val99AlafsTer5` | `V99fs` | DISCREPANCY | TRUE |
| HBB-CP2-161 | C06 | `c.64dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Asp22GlyfsTer2` | `D22fs` | DISCREPANCY | TRUE |
| HBB-CP2-164 | C06 | `c.323dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Asn109GlnfsTer32` | `N109fs` | DISCREPANCY | TRUE |
| HBB-CP2-165 | C06 | `c.143_146dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Thr51ValfsTer4` | `T51fs` | DISCREPANCY | TRUE |
| HBB-CP2-168 | C03 | `c.432C>T` | Synonymous | Synonymous | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.(=)` | `p.His144=` | MATCH | TRUE |
| HBB-CP2-170 | C06 | `c.287dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Leu97AlafsTer6` | `L97fs` | DISCREPANCY | TRUE |
| HBB-CP2-175 | C06 | `c.143dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Asp48GlufsTer6` | `D48fs` | DISCREPANCY | TRUE |
| HBB-CP2-182 | C06 | `c.85dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Leu29ProfsTer16` | `L29fs` | DISCREPANCY | TRUE |
| HBB-CP2-183 | C06 | `c.45dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Trp16ValfsTer8` | `W16fs` | DISCREPANCY | TRUE |
| HBB-CP2-184 | C06 | `c.217dup` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Ser73LysfsTer2` | `S73fs` | DISCREPANCY | TRUE |
| HBB-CP2-185 | C04 | `c.20del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Glu7GlyfsTer13` | `E7fs` | DISCREPANCY | TRUE |
| HBB-CP2-187 | C04 | `c.51del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Lys18ArgfsTer2` | `K18fs` | DISCREPANCY | TRUE |
| HBB-CP2-188 | C04 | `c.25_26del` | Frameshift | Frameshift | **MATCH** | `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` | `p.Lys9ValfsTer14` | `K9fs` | DISCREPANCY | TRUE |
| HBB-CP2-214 | C02 | `c.364G>T` | Nonsense | Nonsense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Glu122Ter` | `E122*` | MATCH | TRUE |
| HBB-CP2-241 | C09 | `c.93-1G>C` | Splice Site Disruption | Splice Site Disruption | **MATCH** | `EXTERNAL_ANNOTATION_INCOMPLETE` | `p.?` | `None` | INCOMPLETE | TRUE |
| HBB-CP2-244 | C01 | `c.315G>C` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Arg105Ser` | `R105S` | MATCH | TRUE |
| HBB-CP2-245 | C01 | `c.380T>G` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Val127Gly` | `V127G` | MATCH | TRUE |
| HBB-CP2-253 | C09 | `c.93-2A>C` | Splice Site Disruption | Splice Site Disruption | **MATCH** | `EXTERNAL_ANNOTATION_INCOMPLETE` | `p.?` | `None` | INCOMPLETE | TRUE |
| HBB-CP2-254 | C09 | `c.316-1G>T` | Splice Site Disruption | Splice Site Disruption | **MATCH** | `EXTERNAL_ANNOTATION_INCOMPLETE` | `p.?` | `None` | INCOMPLETE | TRUE |
| HBB-CP2-256 | C09 | `c.316-2A>C` | Splice Site Disruption | Splice Site Disruption | **MATCH** | `EXTERNAL_ANNOTATION_INCOMPLETE` | `p.?` | `None` | INCOMPLETE | TRUE |
| HBB-CP2-257 | C09 | `c.93-2A>G` | Splice Site Disruption | Splice Site Disruption | **MATCH** | `EXTERNAL_ANNOTATION_INCOMPLETE` | `p.?` | `None` | INCOMPLETE | TRUE |
| HBB-CP2-262 | C01 | `c.93G>T` | Missense | Missense | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `p.Arg31Ser` | `R31S` | MATCH | TRUE |
| HBB-CP2-265 | C11 | `c.*110T>C` | 3' UTR Regulatory | 3' UTR Regulatory | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `None` | `None` | NOT_APPLICABLE | TRUE |
| HBB-CP2-268 | C11 | `c.*113A>G` | 3' UTR Regulatory | 3' UTR Regulatory | **MATCH** | `EXACT_MOLECULAR_AGREEMENT` | `None` | `None` | NOT_APPLICABLE | TRUE |

---

## Final assessment

The reported **55 / 55 (100.00%)** molecular consequence concordance is **fully and independently supported** by the individual candidate-level records in `research/results/phase2c_benchmark_candidate_results.json`.

Specifically:
1. Every candidate has explicit external molecular annotation in the frozen primary manifest.
2. Every candidate achieves exact normalized molecular category equivalence between the runtime deterministic engine output ($A$) and external ClinVar evidence ($C$).
3. Secondary protein format variations (truncated `E7fs` syntax in 20 frameshift variants) and missing protein strings (in 5 C09 splice variants) are accurately segregated into secondary endpoints and transparent categories (`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` and `EXTERNAL_ANNOTATION_INCOMPLETE`), neither inflating protein agreement nor contaminating the primary molecular endpoint.
4. Stored expected consequences ($B$) are strictly isolated into regression auditing and do not participate in biological concordance.

**Audit Status:** `CP4.3A COMPLETE — AUDIT PASSED WITHOUT EXCEPTION`.