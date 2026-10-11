# Phase 5.5.2 — Final Reference Identifier and Ethics Statement Audit Report

> **Document Type:** FINAL EDITORIAL QUALITY AUDIT, BIBLIOGRAPHIC RECONCILIATION, AND REGULATORY STATEMENT AUDIT  
> **Evaluation Subjects:**  
> - `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` (Assembled Final Manuscript)  
> - `research/manuscript/PHASE5_5_SUBMISSION_READINESS_AUDIT.md` (Readiness Audit Report)  
> - `research/manuscript/PHASE5_5_1_CITATION_TRACEABILITY.md` (Citation Traceability Audit)  
> **Auditor Role:** Critical Scientific Editor, Research Integrity Officer & Bibliometric Auditor  
> **Audit Date:** 2026-10-11  
> **Governing Baselines (Bit-for-Bit Verified):**  
> - `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> - `research/manifest/frozen_test.json` (SHA256: `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994`)  
> - `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (SHA256: `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`)  
> **Final Editorial Verdict:** **`READY FOR AUTHOR FINALIZATION`**  
> *(Strictly bounded: The manuscript is scientifically complete and internally reconciled, but is **NOT cleared for journal submission** until human authors complete mandatory institutional declarations, affiliations, and repository accessions).*

---

## 1. Executive Summary

This Phase 5.5.2 audit was conducted to resolve outstanding bibliographic discrepancies, establish a clear tripartite distinction among bibliographic identity verification, full-text access, and substantive claim support, rigorously re-examine the study's ethics and human research statements without presuming an institutional review board (IRB) exemption, preserve the verified ClinVar review tier counts, and confirm the cryptographic integrity of all frozen benchmark artifacts.

```
================================================================================
PHASE 5.5.2 EDITORIAL AUDIT DETERMINATION:
READY FOR AUTHOR FINALIZATION
================================================================================
- Bibliographic Discrepancies: Resolved across all 17 citations against Crossref,
                              PubMed, and Europe PMC. Corrected mismatched DOIs,
                              PMIDs, and PMCIDs (including Morales et al., Rehm
                              et al., Krusche et al., Weatherall, and Giardine et al.).
- Epistemic Tripartite Model: Explicitly separated:
                              (1) Bibliographic Metadata Verification
                              (2) Primary Source Inspection Scope
                              (3) Actual Substantive Claim Support in Prose
- Claim Proportionality:      Downgraded 3 citations (Clopper & Pearson 1934,
                              Giardine et al. 2007, and Taher et al. 2018) to
                              PARTIALLY SUPPORTED due to subscription text access
                              limits or brief announcement note format. Zero claims
                              unresolved or unsupported.
- Ethics & Regulatory Audit:  Eliminated presumption of automatic IRB exemption.
                              Factually established that the study is a secondary
                              computational analysis of public de-identified data.
                              Designated formal IRB/HREC determination letters and
                              journal-specific wording as mandatory author actions.
- ClinVar Review Tiers:       Preserved exact mutually exclusive counts:
                              54 exactly 2-star (98.18%), 1 exactly 3-star (1.82%,
                              candidate HBB-CP2-245), 0 0/1-star, 0 missing.
- Frozen Hash Invariance:     Bit-for-bit identity confirmed for all 3 artifacts.
- Production Code / Pipeline: Zero modifications to production code, frozen manifests,
                              benchmark scripts, or stored results.
================================================================================
```

---

## 2. Bibliographic Discrepancy Reconciliation Table

Every reference cited in the manuscript was verified directly against authoritative records indexed by Crossref, the National Library of Medicine (PubMed / NCBI Entrez), and Europe PMC. Discrepancies and transcription errors identified in earlier working drafts or interim reports were corrected:

| Ref # | Cited Reference & Authoritative Identifiers | Discrepancy / Error Detected in Prior Reports or Drafts | Authoritative Primary Verification Basis | Corrected Metadata Status |
|:---:|---|---|---|:---:|
| **1** | **Clopper CJ, Pearson ES (1934)**<br>*Biometrika* 26(4):404–413.<br>DOI: [10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404)<br>PMID: *None (Pre-1946 / Pre-MEDLINE)*<br>PMCID: *None* | Previously unindexed in MEDLINE. No identifier errors; historic paper lacks PMID/PMCID. | Verified via Crossref metadata and Oxford Academic archives. | **VERIFIED & ACCURATE** |
| **2** | **den Dunnen JT et al. (2016)**<br>*Hum Mutat* 37(6):564–569.<br>DOI: [10.1002/humu.22981](https://doi.org/10.1002/humu.22981)<br>PMID: [26931183](https://pubmed.ncbi.nlm.nih.gov/26931183/)<br>PMCID: *None (Closed-access Wiley)* | Earlier readiness audit note mistakenly associated `PMC5089531` with this reference. | `PMC5089531` belongs to an unrelated neurology article (*Neurology* 2016;87:1770–1776). den Dunnen et al. was published under standard subscription in *Hum Mutat* and has no PMCID. Sequence guidelines verified via official HGVS SVD-WG web standard (`varnomen.hgvs.org`). | **CORRECTED**<br>(Bogus PMCID removed; closed-access status noted) |
| **3** | **Giardine B et al. (2007)**<br>*Hum Mutat* 28(2):206.<br>DOI: [10.1002/humu.9479](https://doi.org/10.1002/humu.9479)<br>PMID: [17221864](https://pubmed.ncbi.nlm.nih.gov/17221864/)<br>PMCID: *None* | Prior audit reports recorded `PMID: 17221867`. | `PMID: 17221867` corresponds to de Brouwer et al. (*Hum Mutat* 28(2):207). The authoritative PMID for Giardine et al. is **17221864**. | **CORRECTED**<br>(PMID updated: 17221867 $\to$ 17221864) |
| **4** | **Harrison SM et al. (2017)**<br>*Genet Med* 19(10):1096–1104.<br>DOI: [10.1038/gim.2017.14](https://doi.org/10.1038/gim.2017.14)<br>PMID: [28301460](https://pubmed.ncbi.nlm.nih.gov/28301460/)<br>PMCID: [PMC5600649](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5600649/) | Interim audit report line 86 cited `PMC5599322`. | `PMC5599322` corresponds to Zhao et al. (*Biol Psychiatry* 2018). The authoritative open-access PMCID for Harrison et al. is **PMC5600649**. | **CORRECTED**<br>(PMCID updated: PMC5599322 $\to$ PMC5600649) |
| **5** | **Krusche P et al. (2019)**<br>*Nat Biotechnol* 37(5):555–560.<br>DOI: [10.1038/s41587-019-0054-x](https://doi.org/10.1038/s41587-019-0054-x)<br>PMID: [30858580](https://pubmed.ncbi.nlm.nih.gov/30858580/)<br>PMCID: [PMC6699627](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6699627/) | Prior reports recorded `PMID: 30858583` and described the source as unretrieved subscription text. | `PMID: 30858583` was a typographical error (unindexed). The authoritative PMID is **30858580**. The article is open-access in PubMed Central under **PMC6699627**. | **CORRECTED**<br>(PMID: 30858583 $\to$ 30858580; PMCID PMC6699627 confirmed) |
| **6** | **Landrum MJ et al. (2018)**<br>*Nucleic Acids Res* 46(D1):D1062–D1067.<br>DOI: [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153)<br>PMID: [29165669](https://pubmed.ncbi.nlm.nih.gov/29165669/)<br>PMCID: [PMC5753237](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5753237/) | None. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **7** | **Landrum MJ et al. (2020)**<br>*Nucleic Acids Res* 48(D1):D835–D844.<br>DOI: [10.1093/nar/gkz972](https://doi.org/10.1093/nar/gkz972)<br>PMID: [31777943](https://pubmed.ncbi.nlm.nih.gov/31777943/)<br>PMCID: [PMC6943040](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6943040/) | Earlier Phase 5.3.3 reconciliation had confused title/author metadata with another paper. Resolved in Phase 5.3.4. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **8** | **McLaren W et al. (2016)**<br>*Genome Biol* 17(1):122.<br>DOI: [10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4)<br>PMID: [27268795](https://pubmed.ncbi.nlm.nih.gov/27268795/)<br>PMCID: [PMC4893825](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4893825/) | Typographical error in readiness report line 90 (`PMC4893625`). | Authoritative open-access PMCID is **PMC4893825**. | **CORRECTED**<br>(PMCID typo resolved: PMC4893625 $\to$ PMC4893825) |
| **9** | **Morales J et al. (2022)**<br>*Nature* 604(7905):310–315.<br>DOI: [10.1038/s41586-022-04558-8](https://doi.org/10.1038/s41586-022-04558-8)<br>PMID: [35388217](https://pubmed.ncbi.nlm.nih.gov/35388217/)<br>PMCID: [PMC9007741](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9007741/) | Prior reports recorded `PMID: 35418685` and `PMCID: PMC9645817`. | Programmatic check against DOI `10.1038/s41586-022-04558-8` confirmed that `35418685` / `PMC9645817` belongs to an adjacent Nature paper (Calvanese et al., "Mapping human haematopoietic stem cells..."). Authoritative identifiers for Morales et al. MANE paper are **PMID: 35388217** and **PMCID: PMC9007741**. | **CORRECTED**<br>(PMID: 35418685 $\to$ 35388217; PMCID: PMC9645817 $\to$ PMC9007741) |
| **10** | **O'Leary NA et al. (2016)**<br>*Nucleic Acids Res* 44(D1):D733–D745.<br>DOI: [10.1093/nar/gkv1189](https://doi.org/10.1093/nar/gkv1189)<br>PMID: [26553804](https://pubmed.ncbi.nlm.nih.gov/26553804/)<br>PMCID: [PMC4702849](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4702849/) | None. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **11** | **Rehm HL et al. (2015)**<br>*N Engl J Med* 372(23):2235–2242.<br>DOI: [10.1056/NEJMsr1406261](https://doi.org/10.1056/NEJMsr1406261)<br>PMID: [26014595](https://pubmed.ncbi.nlm.nih.gov/26014595/)<br>PMCID: [PMC4474187](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4474187/) | Manuscript draft and prior reports listed invalid DOI `10.1056/NEJMp1503109`, invalid PMID `26014582`, and invalid PMCID `PMC4744716`. | `10.1056/NEJMp1503109` returns 404 on Crossref. `PMID: 26014582` / `PMC4744716` belongs to Kofler et al. (*Mol Ecol Resour* 2016). Authoritative NEJM Special Report DOI is **10.1056/NEJMsr1406261**, authoritative PMID is **26014595**, and authoritative PMCID is **PMC4474187**. | **CORRECTED**<br>(DOI, PMID, and PMCID updated in manuscript draft L415) |
| **12** | **Richards S et al. (2015)**<br>*Genet Med* 17(5):405–424.<br>DOI: [10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30)<br>PMID: [25741868](https://pubmed.ncbi.nlm.nih.gov/25741868/)<br>PMCID: [PMC4544753](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4544753/) | None. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **13** | **Stodden V et al. (2016)**<br>*Science* 354(6317):1240–1241.<br>DOI: [10.1126/science.aah6168](https://doi.org/10.1126/science.aah6168)<br>PMID: [27940837](https://pubmed.ncbi.nlm.nih.gov/27940837/)<br>PMCID: *None (Closed-access Science)* | None. | Verified via PubMed and Science policy statement indexing. | **VERIFIED & ACCURATE** |
| **14** | **Taher AT et al. (2018)**<br>*Lancet* 391(10116):155–167.<br>DOI: [10.1016/S0140-6736(17)31822-6](https://doi.org/10.1016/S0140-6736(17)31822-6)<br>PMID: [28774421](https://pubmed.ncbi.nlm.nih.gov/28774421/)<br>PMCID: *None (Subscription Lancet)* | None. | Verified via PubMed core record. Subscription journal PDF uninspected locally. | **VERIFIED & ACCURATE** |
| **15** | **Thein SL (2013)**<br>*Cold Spring Harb Perspect Med* 3(5):a011700.<br>DOI: [10.1101/cshperspect.a011700](https://doi.org/10.1101/cshperspect.a011700)<br>PMID: [23637309](https://pubmed.ncbi.nlm.nih.gov/23637309/)<br>PMCID: [PMC3633182](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3633182/) | None. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **16** | **Wang K et al. (2010)**<br>*Nucleic Acids Res* 38(16):e164.<br>DOI: [10.1093/nar/gkq603](https://doi.org/10.1093/nar/gkq603)<br>PMID: [20601685](https://pubmed.ncbi.nlm.nih.gov/20601685/)<br>PMCID: [PMC2938201](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2938201/) | None. | Verified via PubMed Central open-access repository. | **VERIFIED & ACCURATE** |
| **17** | **Weatherall DJ (2010)**<br>*Blood* 115(22):4331–4336.<br>DOI: [10.1182/blood-2010-01-251348](https://doi.org/10.1182/blood-2010-01-251348)<br>PMID: [20233970](https://pubmed.ncbi.nlm.nih.gov/20233970/)<br>PMCID: [PMC2881491](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2881491/) | Prior reports recorded `PMID: 20237318` and omitted PMCID. | `PMID: 20237318` corresponds to Beekman & Touw (*Blood* 2010;115:5131). The authoritative PMID for Weatherall is **20233970**, and the open-access PMCID is **PMC2881491**. | **CORRECTED**<br>(PMID: 20237318 $\to$ 20233970; PMCID PMC2881491 confirmed) |

---

## 3. Epistemic Tripartite Differentiation Matrix

In compliance with Requirement 2, this audit explicitly decouples:
1. **Level A (Bibliographic Metadata Verification):** Author, title, year, journal, volume, pages, and persistent identifiers (DOI/PMID/PMCID) verified against bibliographic databases.
2. **Level B (Primary Source Inspection Scope):** Direct inspection of full primary text, official consensus standard guidelines, or core abstracts/reference implementations.
3. **Level C (Substantive Claim Support in Manuscript Prose):** Degree to which the cited source actually substantiates the specific empirical, computational, or clinical assertions made in the text.

```
+-------------------------------------------------------------------------------+
|                      TRIPARTITE VERIFICATION FRAMEWORK                       |
+-------------------------------------------------------------------------------+
| Level A: Bibliographic Identity  | Confirmed against Crossref, PubMed, PMC    |
| Level B: Source Inspection Scope | Full Text vs Consensus Standard vs Abstract|
| Level C: Manuscript Claim Support| Supported vs Partially Supported vs Unres. |
+-------------------------------------------------------------------------------+
```

### Tripartite Evaluation Summary Table

| Ref # | Cited Source | Level A: Bibliographic Metadata Status | Level B: Primary Source Inspection Scope | Specific Manuscript Claim Evaluated | Level C: Substantive Claim Support Verdict |
|:---:|---|:---:|---|---|:---:|
| **1** | **Clopper & Pearson (1934)** | **VERIFIED** | Statistical reference implementation & incomplete beta derivation (`run_phase2c_benchmark.py`). Historic 1934 printed journal unretrieved. | Exact two-sided binomial CI using incomplete beta distribution; failure of Wald approximation when $k = n$ (§2.9, §4.1). | **PARTIALLY SUPPORTED**<br>*(Formula verified; 1934 print text uninspected)* |
| **2** | **den Dunnen et al. (2016)** | **VERIFIED** | Official international HGVS consensus guidelines & SVD-WG specifications (`varnomen.hgvs.org`). Wiley subscription journal uninspected. | Distinction among $c.$, $p.$, $g.$; codon 1 = initiator Met; modern Met-1 vs legacy Val-1; full frameshift syntax (`p.Glu7GlyfsTer13`) (§1.2, §2.3, §4.3). | **SUPPORTED**<br>*(via official HGVS standard specifications)* |
| **3** | **Giardine et al. (2007)** | **VERIFIED** | Official HbVar live repository documentation (`globin.bx.psu.edu/hbvar/`) & PubMed abstract (PMID: 17221864). | HbVar locus-specific mutation database; allelic heterogeneity of *HBB*; mature protein amino-terminal numbering conventions (-1 codon offset) (§1.1, §2.3, §4.4, §5.2). | **PARTIALLY SUPPORTED**<br>*(Supported via live database & abstract; print note is 1-page update)* |
| **4** | **Harrison et al. (2017)** | **VERIFIED** | Complete primary article inspected via PMC5600649 (*Genet Med* 19:1096–1104). | ClinVar submissions represent submitter assertions and clinical consensus rather than primary in vitro experimental data; inter-laboratory discordance exists (§1.5, §2.5, §5.2). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **5** | **Krusche et al. (2019)** | **VERIFIED** | Complete primary article inspected via PMC6699627 (*Nat Biotechnol* 37:555–560) and GA4GH repository guidelines. | GA4GH benchmarking best practices; pre-defining metrics, defining high-confidence cohorts, and isolating representation differences from algorithmic failure (§1.6, §2.1, §4.6). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **6** | **Landrum et al. (2018)** | **VERIFIED** | Complete primary article inspected via PMC5753237 (*Nucleic Acids Res* 46:D1062–D1067). | ClinVar architecture; 4-star review status system; submitter data model; shorthand truncated frameshifts; omitted protein strings (§1.5, §2.5, §4.3, §5.2). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **7** | **Landrum et al. (2020)** | **VERIFIED** | Complete primary article inspected via PMC6943040 (*Nucleic Acids Res* 48:D835–D844). | ClinVar public archive expansion, programmatic access via E-utilities/FTP, variation page redesign, aggregation of laboratory and expert panel interpretations (§1.5, §2.5, §5.2). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **8** | **McLaren et al. (2016)** | **VERIFIED** | Complete primary article inspected via PMC4893825 (*Genome Biol* 17:122). | Principles of deterministic sequence-based variant consequence annotation; mapping alterations onto transcripts using Sequence Ontology terms; codon translation (§1.3, §4.5). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **9** | **Morales et al. (2022)** | **VERIFIED** | Complete primary author manuscript inspected via PMC9007741 (*Nature* 604:310–315). | MANE initiative establishing canonical MANE Select transcript standard per protein-coding gene; `NM_000518.5` as canonical MANE Select transcript for human *HBB* (§1.2, §2.2, §4.4). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **10** | **O'Leary et al. (2016)** | **VERIFIED** | Complete primary article inspected via PMC4702849 (*Nucleic Acids Res* 44:D733–D745). | NCBI RefSeq curated, non-redundant, explicitly versioned reference sequences; versioned accessions (`NM_000518.5`, `NG_000007.3`) as invariant coordinate foundation (§1.2, §2.2, §4.4). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **11** | **Rehm et al. (2015)** | **VERIFIED** | Complete primary author manuscript inspected via PMC4474187 (*N Engl J Med* 372:2235–2242). | ClinGen Clinical Genome Resource; standardized clinical variant curation framework; distinguishing raw sequence annotation from consensus expert-panel clinical curation (§1.4, §5.2). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **12** | **Richards et al. (2015)** | **VERIFIED** | Complete primary article inspected via PMC4544753 (*Genet Med* 17:405–424). | ACMG/AMP variant interpretation guidelines; 5-tier pathogenicity classification; operational orthogonality between objective consequence and clinical pathogenicity (§1.4, §4.5). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **13** | **Stodden et al. (2016)** | **VERIFIED** | Published policy text and PubMed indexing record inspected (*Science* 354:1240–1241). | Principles of computational scientific reproducibility; transparency of source code, frozen data manifests, execution environments, and pre-specified evaluation protocols (§1.6, §2.1, §4.6). | **SUPPORTED**<br>*(Policy text directly supports general principles)* |
| **14** | **Taher et al. (2018)** | **VERIFIED** | PubMed core abstract and indexing record inspected (*Lancet* 391:155–167). Full publisher PDF uninspected locally. | Thalassemia clinical seminar; global epidemiology and monogenic disease burden; pathophysiological mechanisms of globin chain imbalance; necessity of molecular diagnosis (§1.1, §4.4). | **PARTIALLY SUPPORTED**<br>*(Epidemiological overview supported; full text unretrieved)* |
| **15** | **Thein SL (2013)** | **VERIFIED** | Complete primary article inspected via PMC3633182 (*Cold Spring Harb Perspect Med* 3:a011700). | Molecular biology and pathology of $\beta$-thalassemia; *HBB* gene structure (3 exons, 2 introns, 146-aa mature polypeptide, 147-aa pre-protein); spectrum of $>300$ mutations; legacy numbering (§1.1, §1.2, §2.2, §4.4). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **16** | **Wang et al. (2010)** | **VERIFIED** | Complete primary article inspected via PMC2938201 (*Nucleic Acids Res* 38:e164). | ANNOVAR gene-based variant annotation algorithms; rule-based sequence translation and lookup vs statistical pathogenicity scoring (§1.3, §4.5). | **SUPPORTED**<br>*(Full primary text inspected)* |
| **17** | **Weatherall DJ (2010)** | **VERIFIED** | Complete primary article inspected via PMC2881491 (*Blood* 115:4331–4336). | Inherited diseases of hemoglobin as an emerging global health burden; demographic distribution; public health significance across populations (§1.1, §4.4). | **SUPPORTED**<br>*(Full primary text inspected)* |

---

## 4. Re-examination of Broad Manuscript Claims and Downward Adjustments

To ensure scientific defensibility and avoid overclaiming source authority:

### 4.1 Downward Adjustments Applied
1. **Clopper & Pearson (1934):**
   - *Status:* Maintained as **`PARTIALLY SUPPORTED`**.
   - *Rationale:* The mathematical formulation ($\theta_L, \theta_U$ calculated via the incomplete beta integral) and the failure of normal approximations at $k = n$ are mathematically verified and implemented in `run_phase2c_benchmark.py`. However, because the original 1934 printed volume of *Biometrika* was not directly inspected in physical or scanned facsimile form, the citation cannot be designated as fully supported via primary source inspection.
2. **Giardine et al. (2007):**
   - *Status:* Formally adjusted from Supported to **`PARTIALLY SUPPORTED`**.
   - *Rationale:* The 2007 article in *Human Mutation* (28:206) is a brief one-page database update notice announcing improvements to the HbVar web portal. While the live database itself and its online documentation fully substantiate the continuous cataloging of $>300$ *HBB* variants and traditional mature protein numbering offsets, the one-page 2007 print notice does not itself present the comprehensive variant catalog or formal legacy conversion tables in print.
3. **Taher et al. (2018):**
   - *Status:* Maintained as **`PARTIALLY SUPPORTED`**.
   - *Rationale:* The citation supports broad epidemiological and clinical statements regarding thalassemia burden and globin chain imbalance. These assertions are substantiated at the abstract and indexing record level; however, because the full subscription text of *The Lancet* was not retrieved locally, epistemic transparency requires maintaining this source as partially supported.

### 4.2 Proportionality of Remaining Citations
All remaining 14 citations (den Dunnen, Harrison, Krusche, Landrum 2018, Landrum 2020, McLaren, Morales, O'Leary, Rehm, Richards, Stodden, Thein, Wang, Weatherall) are **`SUPPORTED`** either through complete open-access full text in PubMed Central (PMC), official ASH archives, or direct international consensus standard specifications (HGVS and GA4GH). Zero citations in the manuscript are unverified, ghost, or unsupported.

---

## 5. Critical Audit of Ethics and Human Research Regulatory Statements

### 5.1 Defect in Prior Audit Presumption
Previous audit reports (e.g., `PHASE5_5_SUBMISSION_READINESS_AUDIT.md` §6.6) recommended stating:
> *"State that the study evaluated publicly accessible, de-identified genomic repository records from NCBI ClinVar and did not involve direct human subjects, patient biological specimens, or private clinical health records, qualifying for institutional review board exemption."*

**Audit Critique:** Claiming that a study *"qualifies for institutional review board exemption"* without an institutional determination letter from an authorized Institutional Review Board (IRB) or Human Research Ethics Committee (HREC) commits an unauthorized presumption of regulatory status. In academic research, investigators cannot independently certify or declare their own official IRB exemption if local institutional policy mandates formal administrative review.

### 5.2 Factually Established Realities of the Study
The manuscript and repository artifacts factually establish the following objective parameters:
1. **In Silico Computational Scope:** The investigation was conducted exclusively as a computational benchmark evaluating pure-Python sequence-transformation software algorithms.
2. **Public Data Provenance:** All genomic variant records were harvested from the publicly accessible, open-access, de-identified National Center for Biotechnology Information (NCBI) ClinVar database (`research/manifest/phase2c_primary.json`), alongside synthetically constructed test sequences.
3. **Absence of Human Subject Interaction:** Zero living human participants were recruited, consented, contacted, or subjected to intervention.
4. **Absence of Biological Specimen Handling:** Zero human biological tissues, cell lines, genomic DNA extracts, or clinical diagnostic specimens were collected, handled, stored, or sequenced.
5. **Absence of Protected Health Information:** No private, individual-level health records, identifiable clinical patient histories, or Protected Health Information (PHI) were accessed or processed.

### 5.3 Mandatory Human Author Regulatory Actions
The author team must complete the following regulatory compliance steps prior to journal submission:
1. **Institutional Determination Check:** Authors must review their home academic or medical institution's Human Research Protection Program (HRPP) guidelines to determine whether secondary research using public, de-identified repository data:
   - Does not meet the statutory definition of human subjects research under 45 CFR 46.102 (non-human subjects research determination);
   - Requires a formal administrative exemption application and written determination letter; or
   - Is exempt from institutional submission entirely under institutional blanket policies.
2. **Journal-Specific Human Research Declaration:** Authors must format the ethics disclosure in accordance with the specific author guidelines of their chosen target journal (e.g., *Bioinformatics*, *Human Mutation*, or *JMD*), stating factually that the study evaluated public, de-identified genomic data and including the specific institutional protocol or waiver identifier if issued by the authors' institution.

---

## 6. ClinVar Review Status Stratification Verification

Direct programmatic re-verification of the frozen primary evaluation dataset manifest (`research/manifest/phase2c_primary.json`, $N = 55$) confirmed the **mutually exclusive** stratification:

| Review Status Tier | Exact Criteria / Filter | Count ($k$) | Proportion (%) | Verification Details |
|---|---|:---:|:---:|---|
| **Exactly 2 Stars** | `clinvar_star_rating == 2` | **54** | **98.18%** | Criteria provided, multiple submitters, no conflicts |
| **Exactly 3 Stars** | `clinvar_star_rating == 3` | **1** | **1.82%** | **Candidate `HBB-CP2-245`** (`VCV000015483`, $c.380T>G$, $p.Val127Gly$, "reviewed by expert panel") |
| **0 or 1 Star** | `clinvar_star_rating in (0, 1)` | **0** | **0.00%** | Zero records in primary cohort |
| **Unknown or Missing** | `clinvar_star_rating is None` | **0** | **0.00%** | Zero records with missing rating |
| **Total Cohort ($N$)** | Sum of mutually exclusive tiers | **55** | **100.00%** | Primary evaluation denominator |

### Resolution of Candidate Association:
- Candidate **`HBB-CP2-245`** ($c.380T>G$, $p.Val127Gly$) is verified as the sole 3-star expert-panel record (`clinvar_star_rating: 3`).
- Candidate **`HBB-CP2-072`** ($c.67G>T$, $p.Glu23Ter$) is verified as an exactly 2-star record (`clinvar_star_rating: 2`).
- The final manuscript draft ([PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md), lines 121 and 202) correctly cites `HBB-CP2-245`.

---

## 7. Cryptographic Artifact Integrity Verification

Bit-for-bit SHA256 checksums were re-verified across all frozen evaluation artifacts:

```
================================================================================
FROZEN REPOSITORY ARTIFACT SHA256 VERIFICATION
================================================================================
1. Primary Dataset Manifest:
   Path:     research/manifest/phase2c_primary.json
   Expected: 39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96
   Actual:   39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96
   Match:    TRUE (Bit-for-bit identical)

2. Historical Development Test Manifest:
   Path:     research/manifest/frozen_test.json
   Expected: 2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994
   Actual:   2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994
   Match:    TRUE (Bit-for-bit identical)

3. Benchmark Protocol Specification:
   Path:     research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md
   Expected: e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969
   Actual:   e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969
   Match:    TRUE (Bit-for-bit identical)
================================================================================
```

---

## 8. Actionable Checklist for Human Authors Prior to Journal Upload

The research manuscript draft ([PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md)) is complete, verified, and reconciled. The human author team must execute the following administrative actions prior to formal submission:

- [ ] **Author Bylines & Affiliations:** Insert full legal names, academic departments, institutions, and verified ORCID identifiers for all authors.
- [ ] **Corresponding Author Designation:** Provide corresponding author contact details (institutional email and physical postal address).
- [ ] **CRediT Contributor Roles:** Complete author contribution statements across CRediT taxonomy categories.
- [ ] **Funding & Competing Interests:** State specific grant numbers or declare the standard absence of external funding; sign competing interests statements.
- [ ] **Public Code/Data Repository DOI:** Mint a persistent DOI (via Zenodo / Figshare / GitHub release) for benchmark code, manifests, and engine commit `845f595cc039e006d74237945450c7b4a9569ee6`.
- [ ] **Ethics & Regulatory Statement:** Verify home institutional requirements for secondary research with public de-identified genomic data and include formal IRB determination/waiver reference if required by the target journal.

---

## 9. Final Pre-Submission Verdict and Editorial Rationale

```
================================================================================
EDITORIAL AUDIT VERDICT:
READY FOR AUTHOR FINALIZATION
================================================================================
```

### Editorial Rationale:
1. **Bibliographic Identity & Claim Concordance:** Mismatched DOIs, PMIDs, and PMCIDs across all 17 citations have been fully reconciled against primary databases. The distinction among metadata verification, inspection scope, and claim support has been established. Citations with limited access or brief notice formats have been downgraded to `PARTIALLY SUPPORTED`, ensuring defensible claims.
2. **Regulatory Objectivity:** The ethics statement strictly reports factually established realities without presuming or declaring an unverified IRB exemption, designating institutional determination as an author action.
3. **Data & Code Immobility:** The primary evaluation denominator ($N = 55$), review tier counts (54 exactly 2-star, 1 exactly 3-star), primary concordance (100.00% [93.51%, 100.00%]), secondary protein concordance (50.91% [37.07%, 64.65%]), synthetic controls (18/18 [81.47%, 100.00%]), and regression invariance (55/55) remain 100% verified.
4. **Submission Boundary:** The work is designated **`READY FOR AUTHOR FINALIZATION`**. It is **not** cleared for journal submission until human authors supply their administrative declarations.
