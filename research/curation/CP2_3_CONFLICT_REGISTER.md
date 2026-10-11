# Phase 2C — CP-2.3 Conflict Register

> **Document Status:** PROVISIONAL RESEARCH CURATION REGISTER  
> **Scope:** Explicit Tracking of Molecular, Protein, HGVS, and Clinical Discrepancies

---

## 1. Molecular Consequence Conflicts (`MOLECULAR_CONSEQUENCE_CONFLICT`)

Discrepancies where the deterministic consequence computation and external database classification disagree on the molecular impact category:


### Case Study: Candidate `HBB-CP2-204` (`c.170_171insGCAACCCTAAGGTG`)

- **HGVS Input:** `c.170_171insGCAACCCTAAGGTG`

- **Deterministic Engine Result:** `Frameshift` (`p.Asn58GlnfsTer3`)

- **External ClinVar Result:** `In-frame insertion` (`p.Gly57_Asn58insGlnProTer`, VarID: 869222)

- **Discrepancy Cause:** The inserted nucleotide sequence `GCAACCCTAAGGTG` has a length of **14 nucleotides** ($14 \pmod 3 = 2$). A 14-bp insertion mathematically forces a reading frameshift, generating downstream premature termination at codon 60 (`fsTer3`). The ClinVar annotation claiming an in-frame insertion is mathematically and biologically discordant.

- **Human Decision:** **`REJECT`** from in-frame insertion cohort. Quarantined in `REVIEW_REQUIRED` as a documented database discordance. **Not silently corrected.**


### Other Molecular Discrepancies:

- **`HBB-CP2-156` (`c.-22_23dup`):** Classified externally as 5' UTR regulatory variant, but the 45-bp duplication extends across the start codon into Exon 1, inducing a coding frameshift (`p.Ala-7LysfsTer156`). Decision: Quarantined under `REVIEW_REQUIRED`.


---

## 2. Protein Consequence Conflicts (`PROTEIN_CONSEQUENCE_CONFLICT`)

Cases where molecular consequence category agrees, but protein nomenclature annotations exhibit conflict:


- **`HBB-CP2-201` (`c.385_388delinsCCACA`):** External ClinVar summary contains dual competing protein consequence annotations (`A129fs, K133fs`). Decision: Quarantined under `REVIEW_REQUIRED`.


---

## 3. Clinical Significance Conflicts (`CLINICAL_SIGNIFICANCE_CONFLICT`)

The primary validation experiment evaluates **deterministic molecular consequence**, NOT clinical pathogenicity. Consequently, variants with clinical significance conflicts in ClinVar were **NOT** excluded if their molecular consequences were deterministically unambiguous:


Total variants with clinical pathogenicity conflicts in ClinVar: **27 candidates**.


| candidate_id | HGVS | Class | Engine Consequence | Engine Protein | ClinVar Pathogenicity Status | Decision | Reason |
|---|---|:---:|---|---|---|:---:|---|
| HBB-CP2-025 | `c.118C>A` | C01 | Missense | `p.Gln40Lys` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-032 | `c.334G>C` | C01 | Missense | `p.Val112Leu` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-034 | `c.394C>G` | C01 | Missense | `p.Gln132Glu` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-035 | `c.31G>A` | C01 | Missense | `p.Ala11Thr` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-037 | `c.359G>A` | C01 | Missense | `p.Gly120Asp` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-042 | `c.404T>C` | C01 | Missense | `p.Val135Ala` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-044 | `c.110C>A` | C01 | Missense | `p.Pro37His` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-087 | `c.24G>A` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-094 | `c.85C>T` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-099 | `c.33C>A` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-100 | `c.274C>T` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-102 | `c.90C>T` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-162 | `c.440_441dup` | C06 | Frameshift | `p.Ter148ThrfsTer12` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-167 | `c.*96T>C` | C11 | 3' UTR Regulatory | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-169 | `c.324C>T` | C03 | Synonymous | `p.(=)` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-172 | `c.-31C>T` | C10 | 5' UTR Regulatory | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-193 | `c.286A>G` | C01 | Missense | `p.Lys96Glu` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-206 | `c.93-30_96delinsGTCCCTTGGGCTGTTTTCCTACCCTCAGATTA` | C08 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-216 | `c.208G>A` | C01 | Missense | `p.Gly70Ser` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-222 | `c.127_129del` | C05 | In-frame Indel | `p.Phe43del` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-229 | `c.289_290delinsGG` | C05 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-247 | `c.316-12T>C` | C09 | Splice Site Disruption | `p.?` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-251 | `c.316-7C>A` | C08 | Splice Site Disruption | `p.?` | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-274 | `c.-122T>A` | C10 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-277 | `c.-77_-76del` | C10 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-278 | `c.-140C>G` | C10 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |
| HBB-CP2-281 | `c.-82C>T` | C10 | N/A | *none* | Conflicting classifications of pathogenicity | **REVIEW_REQUIRED** | Pathogenicity conflict does not affect unambiguous molecular consequence. |