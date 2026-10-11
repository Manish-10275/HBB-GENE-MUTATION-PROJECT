# Final Pre-Submission Audit: HBB Gene Mutation Analyzer Manuscript

> **Project:** HBB Gene Mutation Analyzer Research Project  
> **Document Title:** FINAL PRE-SUBMISSION AUDIT REPORT  
> **Target Manuscript:** `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`  
> **Supporting Artifact:** `research/results/CONTROLLED_AUTHOR_CORRECTIONS_REPORT.md`  
> **Execution Mode:** Read-Only Forensic Verification & Artifact Authority Audit  
> **Audit Date:** 2026-10-11  
> **Auditor:** Automated Forensic Audit System  
> **Status:** COMPLETED — Strictly Read-Only  

---

## 1. Executive Summary & Audit Mandate

This final pre-submission audit was conducted under strict read-only protocols to independently verify the scientific accuracy, textual consistency, reference authority, and administrative integrity of the complete *HBB* Gene Mutation Analyzer research manuscript (`research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`) following controlled author corrections.

### Mandatory Audit Protocols:
1. **Zero Modifications to Project Assets:** No source code, reference FASTA/JSON files, frozen manifests, benchmark results, decision matrices, or manuscript files were modified or deleted.
2. **Zero Benchmark Reruns:** No computational benchmarks were executed.
3. **Independent Sequence Authority:** Reference sequence `NM_000518.5` and predecessor `NM_000518.4` were audited directly against authoritative live NCBI Entrez E-utilities endpoints, strictly avoiding circular validation against local checksums.
4. **Explicit Separation of Evidence from Assertion:** Every verified finding is accompanied by cryptographic digests, terminal sequence coordinates, endpoint URLs, or line-numbered manuscript citations.

---

## 2. Independent Verification of Reference Sequence NM_000518.5

### 2.1 Retrieval Provenance & Official NCBI Record
The transcript reference sequence was queried directly from the official NCBI Entrez sequence retrieval service:
- **Retrieval URL / Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.5&rettype=fasta&retmode=text`
- **GenBank Flatfile Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.5&rettype=gb&retmode=text`
- **Official Accession Version:** `NM_000518.5`
- **Official FASTA Header:** `>NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA`
- **GenBank LOCUS Line:** `LOCUS NM_000518 628 bp mRNA linear PRI 06-SEP-2026`
- **Official RefSeq Status:** `RefSeq; MANE Select` (Matched Annotation from NCBI and EMBL-EBI)

### 2.2 Sequence Metrics & Cryptographic Digest
- **Authoritative Sequence Length:** Exactly **628 nucleotides**
- **Terminal 30 Nucleotides (599–628):** `5'-CCTAATAAAAAACATTTATTTTCATTGCAA-3'`
- **Pure Nucleotide Sequence SHA256 Checksum:**  
  `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3`

### 2.3 Pairwise Character-by-Character Alignment (Local vs. Official NCBI)
The local reference file `data/reference/NM_000518.5.fasta` was extracted and aligned character-by-character against the live NCBI download:
- **Alignment Length:** 628 characters
- **Total Mismatches:** **0 (Zero)**
- **Gaps / Insertions / Deletions:** **0 (Zero)**
- **First Differing Position:** None (Identical across positions 1..628)
- **Local FASTA Header:** `>NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA`
- **Verification Verdict:** **EXACT 100% BIT-FOR-BIT MATCH**

### 2.4 Official GenBank Feature Annotations
Inspection of the official GenBank feature table for `NM_000518.5` establishes the authoritative structural coordinates:
- **5' UTR:** Positions 1..50 (50 nt)
- **Coding Sequence (CDS):** Positions 51..494 (444 nt; 147 amino acid codons + stop codon)
- **Exon 1:** Positions 1..142 (142 bp)
- **Exon 2:** Positions 143..365 (223 bp)
- **Exon 3:** Positions 366..628 (263 bp)
- **3' UTR:** Positions 495..628 (134 nt)
- **Polyadenylation Signal:** Positions 604..609 (`AATAAA`)
- **Polyadenylation Site:** Position 628

---

## 3. Verification of Historical Predecessor NM_000518.4 & Terminal Adenines

### 3.1 Historical NCBI RefSeq Record NM_000518.4
To resolve the conflict between the modern 628 nt model and historical literature describing a 626 bp spliced transcript with a 132 bp 3' UTR, the versioned predecessor record was retrieved directly from NCBI:
- **Retrieval URL / Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.4&rettype=fasta&retmode=text`
- **GenBank Flatfile Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.4&rettype=gb&retmode=text`
- **Official Accession Version:** `NM_000518.4`
- **Official FASTA Header:** `>NM_000518.4 Homo sapiens hemoglobin subunit beta (HBB), mRNA`
- **GenBank LOCUS Line:** `LOCUS NM_000518 626 bp mRNA linear PRI 01-MAY-2018`
- **Historical Effective Dates:** February 11, 2003 through June 13, 2018
- **Historical Sequence Length:** Exactly **626 nucleotides**
- **Terminal 30 Nucleotides (597–626):** `5'-TGCCTAATAAAAAACATTTATTTTCATTGC-3'`
- **Pure Nucleotide Sequence SHA256 Checksum:**  
  `ac038be3f141f8e792f00c32497408615a5204d0654f3aa0ff39e07c4be588f9`

### 3.2 Pairwise Comparison: NM_000518.5 vs. NM_000518.4
Pairwise character alignment between version 4 and version 5 reveals:
- **Positions 1..626:** Exactly 100% identical (0 substitutions across all 626 bases).
- **Positions 627..628 in NM_000518.5:** Exactly two terminal adenines (`5'-AA-3'`).
- **Terminal Sequence Alignment:**
  ```text
  NM_000518.4 (597..626): TGCCTAATAAAAAACATTTATTTTCATTGC--
  NM_000518.5 (599..628): TGCCTAATAAAAAACATTTATTTTCATTGCAA
  ```
- **Historical Structural Annotations under NM_000518.4:**
  - Exon 3: Positions 366..626 (261 bp)
  - 3' UTR: Positions 495..626 (132 nt, spanning $c.*1..c.*132$)
- **Biological Basis of Update:**  
  The official NCBI GenBank comment for `NM_000518.5` explicitly records:  
  *"On Jun 13, 2018 this sequence version replaced NM_000518.4."*  
  The PRIMARY table cites experimental evidence from full-length human cDNA clone `BU661647.1` (bases 507–640 aligned to transcript span 495–628), which experimentally verified the two terminal adenines prior to polyadenylation.
- **Verification Verdict:** **VERIFIED AND SUPPORTED BY VERSIONED NCBI RECORDS**. The manuscript's distinction in Methods Section 2.2 accurately reflects NCBI RefSeq evolution.

---

## 4. Manuscript Numerical Consistency Audit

Every numerical claim, cohort denominator, statistical confidence interval, and biological classification was audited across the entire manuscript draft (`PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`):

### 4.1 Harmonization of Categorization and Protein Counts
The audit verified that the manuscript strictly and consistently distinguishes between primary molecular consequence categories and secondary protein nomenclature matching:

| Entity / Metric | Exact Manuscript Count | Percentage | 95% Clopper-Pearson CI | Primary Manuscript Locations |
|---|:---:|:---:|:---:|---|
| **Primary Cohort Denominator** | **55** | 100.00% | — | Abstract (L14), Methods (L129), Results (L209), Discussion (L325) |
| **Primary Molecular Concordance ($A == C$)** | **55** | **100.00%** | **[93.51%, 100.00%]** | Abstract (L17), Results (L209, Table 1), Discussion (L325), Conclusion (L406) |
| **`EXACT_MOLECULAR_AGREEMENT` Category** | **30** | **54.55%** | **[40.57%, 68.01%]** | Abstract (L17), Results (L221), Table 2 (L238), Discussion (L328) |
| ↳ *Coding Variants with Exact Protein Match* | **28** | **50.91%** | **[37.07%, 64.65%]** | Abstract (L17), Results (L221, L234), Table 2 (L238), Discussion (L328), Lim. (L392) |
| ↳ *Non-Coding 3' UTR (Protein Not Applicable)* | **2** | **3.64%** | **[0.44%, 12.53%]** | Abstract (L17), Results (L221, L237), Table 2 (L238), Discussion (L328) |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | **20** | **36.36%** | **[23.78%, 50.45%]** | Abstract (L17), Results (L222, L235), Table 2 (L238), Discussion (L329), Lim. (L392) |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | **5** | **9.09%** | **[3.01%, 20.01%]** | Abstract (L17), Results (L223, L236), Table 2 (L238), Discussion (L330), Lim. (L392) |
| **Synthetic Negative Controls (Exp. D)** | **18 / 18** | **100.00%** | **[81.47%, 100.00%]** | Abstract (L17), Results (L295, Table 5), Discussion (L332), Conclusion (L406) |
| **Software Regression Reproduction ($A == B$)** | **55 / 55** | **100.00%** | **[93.51%, 100.00%]** | Abstract (L17), Results (L307, Table 5), Discussion (L332) |

### 4.2 Mathematical Integrity Checks:
- Category sum check: $30 + 20 + 5 = 55$ (**100.00%**)
- Protein match hierarchy check: $28\text{ (MATCH)} + 2\text{ (NOT\_APPLICABLE)} = 30\text{ (`EXACT_MOLECULAR_AGREEMENT`)}$
- Total protein status check: $28\text{ (MATCH)} + 20\text{ (FORMAT\_DIFF)} + 5\text{ (OMITTED)} + 2\text{ (NOT\_APPLICABLE)} = 55$
- **Audit Finding:** Zero conflation exists in the manuscript between the 30 molecular agreement variants and the 28 exact protein nomenclature matches. All percentage calculations and Clopper-Pearson intervals are mathematically verified.

---

## 5. Methodological and Epidemiological Disclosures Audit

The manuscript was scrutinized to verify that scientific limitations, selection biases, and evidence boundaries are clearly and prominently articulated:

### 5.1 Incorporation and Verification Bias
- **Section 1 (Introduction, L67–72):** Highlights that evaluating algorithms against pre-screened concordant sets introduces incorporation bias.
- **Section 2.4 (Methods, L150–158):** Explicitly documents that Checkpoint CP2.2 admission required `comparison_status == "EXACT_AGREEMENT"`, formalizing incorporation bias.
- **Section 5.1 (Limitations, L372–376):** Devotes an entire subsection to incorporation bias, noting that cryptographic immutability of manifests guarantees reproducible execution but does not rectify retrospective curation selection bias.

### 5.2 External Reference Dependence & Absence of Non-ClinVar Corroboration
- **Section 2.3 (Methods, L129–134):** Records that 100% (55/55) of candidates originate from ClinVar, and exactly zero candidates have independent non-ClinVar corroboration (`independent_non_clinvar_corroboration == "NONE"`).
- **Section 5.2 (Limitations, L377–381):** Highlights that public archives reflect diagnostic laboratory consensus rather than biological ground truth, emphasizing the lack of orthogonal data from HbVar, IthaGenes, LOVD, or direct sequencing.

### 5.3 Bounded Scope of Inference
- **Section 4.2 (Discussion, L334–343):** Defines three evidentiary tiers, emphasizing that the empirical artifacts support Tier 1 (computational rule fidelity) and Tier 2 (concordance on clean submissions), but **explicitly do not establish Tier 3 (generalization to novel or unselected clinical sequencing callsets)**.
- **Section 4.5 (Discussion, L361):** Strictly separates objective molecular consequence derivation from computational pathogenicity scoring (ACMG/AMP criteria).
- **Section 5.3 (Limitations, L382–390):** Explicitly enumerates the four unrepresented biological mutation classes ($n = 0$: C05, C07, C08, C10), stating that algorithmic performance for these classes remains completely unmeasured.
- **Section 6 (Conclusion, L408):** Reasserts that findings establish computational rule execution fidelity rather than biological ground truth or clinical validity.

---

## 6. Administrative and Integrity Declarations Audit

The manuscript was audited for compliance with publication ethics and anti-fabrication guidelines:

### 6.1 Status of Administrative Placeholders (Section 8 & Header)
- **Author Names & Affiliations:** Formatted as `[AUTHOR PLACEHOLDER]` (Lines 41–44, 437). Zero fictitious author identities or affiliations exist.
- **Corresponding Author:** Formatted as `[CORRESPONDING AUTHOR PLACEHOLDER]` (Line 438). Zero dummy email addresses exist.
- **Ethics Approval & Consent:** Formatted as `[ETHICS PLACEHOLDER]` (Line 441). Explicitly warns authors: *"Do not assert exemption without institutional or journal confirmation."*
- **Consent for Publication:** Formatted as `[CONSENT PLACEHOLDER]` (Line 444).
- **Competing Interests:** Formatted as `[COMPETING INTERESTS PLACEHOLDER]` (Line 447).
- **Funding:** Formatted as `[FUNDING PLACEHOLDER]` (Line 450).
- **Author Contributions:** Formatted as `[CONTRIBUTIONS PLACEHOLDER]` (Line 453).
- **Acknowledgements:** Formatted as `[ACKNOWLEDGEMENTS PLACEHOLDER]` (Line 456).
- **Data & Code Availability:** Formatted as `[DATA/CODE AVAILABILITY PLACEHOLDER]` (Line 459).

### 6.2 Anti-Fabrication Verification
- **Invented URLs / DOIs:** Scanned for dummy domains (e.g., `github.com/my-lab`, `zenodo.org/record/xxxx`). Result: **ZERO INVENTED IDENTIFIERS DETECTED**.
- **Asserted Exemptions:** Scanned for premature assertions of IRB exemption. Result: **ZERO PREMATURE EXEMPTIONS ASSERTED**.

---

## 7. Cryptographic Audit of Protected Project Artifacts

To certify that no research artifacts were touched during this or prior audit cycles, all SHA256 hashes were recomputed:

| Artifact Description | File Path | Baseline SHA256 Checksum | Verified SHA256 Checksum | Integrity Status |
|---|---|---|---|:---:|
| **Primary Dataset Manifest** | `research/manifest/phase2c_primary.json` | `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` | `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` | **INTACT (100% MATCH)** |
| **Historical Test Manifest** | `research/manifest/frozen_test.json` | `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994` | `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994` | **INTACT (100% MATCH)** |
| **Benchmark Protocol** | `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` | `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` | **INTACT (100% MATCH)** |
| **Candidate Benchmark Results** | `research/results/phase2c_benchmark_candidate_results.json` | `e0493b36b95c75b7034ff37f30aaa393dcaaa9f7252fc171ec6b20db29a766c4` | `e0493b36b95c75b7034ff37f30aaa393dcaaa9f7252fc171ec6b20db29a766c4` | **INTACT (100% MATCH)** |
| **Benchmark Summary Record** | `research/results/phase2c_benchmark_summary.json` | `36047f0675a86ccf2032f42624ce2f48c16636ba37ca2bf15607376c533b8718` | `36047f0675a86ccf2032f42624ce2f48c16636ba37ca2bf15607376c533b8718` | **INTACT (100% MATCH)** |
| **Transcript Reference FASTA** | `data/reference/NM_000518.5.fasta` (pure seq) | `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` | `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` | **INTACT (100% MATCH)** |
| **Genomic Reference FASTA** | `data/reference/NG_000007.3.fasta` (pure seq) | `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18` | `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18` | **INTACT (100% MATCH)** |

---

## 8. Summary of Unresolved Items & Author Action Items

The manuscript is scientifically sound and textually harmonized with the underlying research artifacts. However, it cannot be submitted directly to a journal until the human authors complete the following mandatory administrative actions:

1. **Author Identities and Institutional Affiliations:** Fill in the actual author names, affiliations, email addresses, and ORCIDs in the header and Section 8.
2. **Institutional Ethics Determination:** Verify with the home institution's Institutional Review Board (IRB) or human research committee whether secondary analysis of fully de-identified ClinVar public database records qualifies for formal IRB review exemption, and insert the institutional statement into Section 8.
3. **Competing Interest Disclosures:** Insert formal financial and non-financial conflict of interest disclosures for all contributing authors.
4. **Funding Sources:** Insert applicable grant numbers or specify that the project was conducted without external grant support.
5. **CRediT Author Statement:** Specify each author's exact role (Conceptualization, Methodology, Software, Formal Analysis, Writing - Original Draft, etc.).
6. **Code and Data Repository Archiving:** Deposit the frozen research codebase, dataset manifests, and benchmark logs into a public repository (e.g., GitHub) and generate a persistent citable digital object identifier (e.g., Zenodo DOI archive) to replace the Data/Code Availability placeholder.

---

## 9. Final Audit Determination

```
================================================================================
FINAL AUDIT VERDICT:
• PASS FOR AUTHOR REVIEW, WITH LIMITATIONS
================================================================================
```

### Explanatory Justification:
- **PASS:** The manuscript text is 100% mathematically, scientifically, and cryptographically consistent with all frozen research artifacts. The reference sequence models (`NM_000518.5` and `NM_000518.4`) are rigorously verified against official NCBI RefSeq records. The distinction between primary molecular concordance (55/55), category breakdown (30/20/5), and exact protein nomenclature matching (28/20/5/2) is fully harmonized throughout all sections.
- **FOR AUTHOR REVIEW:** The document contains explicit, mandatory administrative placeholders (authorship, affiliations, ethics, funding, repository DOIs) that must be completed by the human investigators before formal submission.
- **WITH LIMITATIONS:** The study's conclusions remain strictly bounded by inherent curation incorporation bias, single-database ClinVar provenance without orthogonal secondary corroboration, and zero empirical representation across four biological mutation classes (C05, C07, C08, C10).
