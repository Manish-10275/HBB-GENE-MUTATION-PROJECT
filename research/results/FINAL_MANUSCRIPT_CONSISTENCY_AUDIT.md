# Final Scientific Manuscript Consistency and Artifact Integrity Audit Report

> **Project:** HBB Gene Mutation Analyzer Research Project  
> **Document Title:** FINAL MANUSCRIPT CONSISTENCY AND REPRODUCIBLE ARTIFACT AUDIT  
> **Target Manuscript:** `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` (Version: 2026-10-11)  
> **Audited Evidence Artifacts:**  
> - `research/results/REFERENCE_SEQUENCE_AUTHORITY_AUDIT_FOLLOWUP.md`  
> - `research/results/REFERENCE_SEQUENCE_AUTHORITY_AUDIT.md`  
> - `research/results/CP4_3_FINAL_CONSISTENCY_CHECK.md`  
> - `research/results/CP4_3_RESULT_ARTIFACT_FORENSIC_AUDIT_FOLLOWUP.md`  
> - `research/manifest/phase2c_primary.json` & `.sha256`  
> - `research/manifest/frozen_test.json` & `.sha256`  
> - `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`  
> - `research/protocol/CP4_1_DECISION_MATRIX.md`  
> - `research/results/phase2c_benchmark_candidate_results.json`  
> - `research/results/phase2c_benchmark_summary.json`  
> - `data/reference/NM_000518.5.fasta` & `.json`  
> - `data/reference/NG_000007.3.fasta` & `.json`  
> - `backend/app/core/reference.py` & `hgvs.py`  
> **Audit Date:** 2026-10-11  
> **Execution Constraint:** Strictly Read-Only Investigation; Zero Modifications to Existing Files, Manifests, Protocol, Code, or Manuscript Text  

---

## 1. Executive Summary & Final Verdict

This audit represents the final comprehensive consistency and provenance evaluation of the *HBB* Gene Mutation Analyzer research manuscript (`research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`) against its underlying frozen research artifacts, protocol specifications, reference files, and cryptographic hashes.

### Core Audit Outcomes:
1. **Reference Sequence Integrity & Splicing Geometry:**  
   The manuscript's canonical transcript model (`NM_000518.5`, 628 nt) and genomic reference segment (`NG_000007.3:70545..72152`, 1608 nt) are verified bit-for-bit against official NCBI RefSeq records (pure sequence SHA256: `9e811fb1...` and `6de4b387...`, respectively). Exon lengths (142, 223, 263 bp), coding sequence boundaries (51–494, 444 bp), 3′ UTR boundaries (495–628, 134 bp), and intron spans (130 bp Intron 1, 850 bp Intron 2) are 100% verified against both local reference data and authoritative NCBI annotations.
2. **Mathematical Precision of Categorical Counts:**  
   The distinction between **30 exact molecular agreements** and **28 exact protein nomenclature matches** is rigorously verified. In accordance with the locked CP4.1 Decision Matrix, the 30 variants assigned to `EXACT_MOLECULAR_AGREEMENT` comprise exactly 28 coding variants with exact protein matches (`MATCH`) and 2 non-coding 3′ UTR variants (`NOT_APPLICABLE`). The remaining 25 primary candidates comprise 20 frameshift variants with format divergence (`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` / `DISCREPANCY`) and 5 canonical splice acceptor variants lacking external protein strings (`EXTERNAL_ANNOTATION_INCOMPLETE` / `INCOMPLETE`). Across all 55 candidates, primary molecular concordance is 100.00% (55/55; exact 95% Clopper-Pearson CI: [93.51%, 100.00%]).
3. **Scientific Claims & Protocol Disclosures:**  
   All six mandatory scientific boundaries are explicitly, repeatedly, and unambiguously disclosed across the Abstract, Introduction, Methods, Results, Discussion, Limitations, and Conclusion. These include:
   - Severe curation incorporation (verification) bias (`comparison_status == "EXACT_AGREEMENT"`).
   - Single-database ClinVar provenance without independent non-ClinVar corroboration (`independent_non_clinvar_corroboration == "NONE"`).
   - Complete unrepresentation ($n = 0$) of biological classes C05, C07, C08, and C10.
   - Strict operational decoupling of Experiment D (18 synthetic controls) and software regression ($A$ vs $B$) from the primary evaluation endpoint ($A$ vs $C$).
   - Explicit distinction between molecular consequence derivation and clinical pathogenicity prediction / diagnostic validation.
   - Explicit recognition that Clopper-Pearson confidence intervals quantify only Bernoulli sampling error and do not rectify retrospective selection bias.
4. **Cryptographic Immutability:**  
   All on-disk manifests, protocols, and result records match their recorded SHA256 hashes bit-for-bit with zero drift.

```
================================================================================
FINAL AUDIT VERDICT:
• PASS FOR AUTHOR CORRECTIONS
================================================================================
```
The manuscript is scientifically sound, mathematically verified, and fully synchronized with frozen research artifacts. The audit has identified two minor editorial precision enhancements and outlined required author front-matter/back-matter declarations (author metadata, institutional ethics exemption, funding, competing interests, and data availability) necessary prior to journal submission.

---

## 2. Reference Sequence & Coordinate Consistency Audit

Every statement in the manuscript concerning transcript accessions, genomic models, exon/intron spans, and coordinate boundaries was audited against the authoritative findings of `research/results/REFERENCE_SEQUENCE_AUTHORITY_AUDIT_FOLLOWUP.md`.

### 2.1 Statement-by-Statement Verification Matrix

| Parameter / Feature | Authoritative NCBI RefSeq (`NM_000518.5` / `NG_000007.3`) | Manuscript Description & Location | Verification Status | Severity |
|---|---|---|:---:|:---:|
| **Canonical Transcript Accession** | `NM_000518.5` (MANE Select) | Abstract (L8, L14), Intro (L42, L65), Methods (L84, L86, L95, L101, L104, L108), Results (L218, L275, L305), Discussion (L330, L349, L354), Limitations (L382, L395), Conclusion (L401) | **VERIFIED** | VERIFIED |
| **Transcript Total Length** | 628 nucleotides | Methods Section 2.2 (L86, L95) | **VERIFIED** | VERIFIED |
| **Exon 1 Length & Coordinates** | 142 bp (1..142; genomic 70545..70686) | Methods Section 2.2 (L87) | **VERIFIED** | VERIFIED |
| **5′ UTR Length & Coordinates** | 50 bp ($c.-50$ to $c.-1$; transcript 1..50) | Methods Section 2.2 (L87) | **VERIFIED** | VERIFIED |
| **Exon 1 Coding Segment** | 92 bp ($c.1$ to $c.92$; transcript 51..142) | Methods Section 2.2 (L87) | **VERIFIED** | VERIFIED |
| **Exon 2 Length & Coordinates** | 223 bp (143..365; genomic 70817..71039) | Methods Section 2.2 (L88) | **VERIFIED** | VERIFIED |
| **Exon 2 Coding Segment** | 223 bp ($c.93$ to $c.315$; transcript 143..365) | Methods Section 2.2 (L88) | **VERIFIED** | VERIFIED |
| **Exon 3 Length & Coordinates** | 263 bp (366..628; genomic 71890..72152) | Methods Section 2.2 (L89) | **VERIFIED** | VERIFIED |
| **Exon 3 Coding Segment** | 129 bp ($c.316$ to $c.444$; transcript 366..494) | Methods Section 2.2 (L89) | **VERIFIED** | VERIFIED |
| **Coding Sequence (CDS) Total** | 444 bp ($c.1$ to $c.444$; transcript 51..494) | Methods Section 2.2 (L97), Methods Section 2.4 (L114) | **VERIFIED** | VERIFIED |
| **Translated Protein Product** | `NP_000509.1` (147 aa pre-protein; 146 aa mature) | Methods Section 2.2 (L97) | **VERIFIED** | VERIFIED |
| **3′ UTR Length & Coordinates** | 134 bp ($c.*1$ to $c.*134$; transcript 495..628) | Methods Section 2.2 (L89, L95), Methods Section 2.4 (L117) | **VERIFIED** | VERIFIED |
| **Genomic Reference Accession** | `NG_000007.3` (locus 70545..72152, 1608 bp) | Methods Section 2.2 (L84, L91), Methods Section 2.3 (L101, L104) | **VERIFIED** | VERIFIED |
| **Intron 1 (IVS-1) Length** | 130 bp (genomic 70687..70816) | Methods Section 2.2 (L92), Results Section 3.5 (L284) | **VERIFIED** | VERIFIED |
| **Intron 2 (IVS-2) Length** | 850 bp (genomic 71040..71889) | Methods Section 2.2 (L93), Results Section 3.5 (L284) | **VERIFIED** | VERIFIED |
| **Historical 626 bp / 132 bp UTR Model** | Predecessor NCBI RefSeq `NM_000518.4` (2003–2018) | Methods Section 2.2 (L95) | **UNDERSPECIFIED PROVENANCE** | MINOR |

### 2.2 Detailed Finding on Historical Transcript Model (Section 2.2, Line 95)
- **Exact Manuscript Sentence:**  
  > *"In certain historical annotations and literature summaries, Exon 3 is described as spanning 261 bp with a 132 bp 3' UTR (yielding a 626 bp spliced transcript, $c.*1..c.*132$); the project implementation and versioned RefSeq reference files (`NM_000518.5.json` and `NM_000518.5.fasta`) explicitly incorporate the 628 bp reference model ($c.*1..c.*134$)."* (Section 2.2, Line 95)
- **Evaluation:**  
  While the sentence accurately describes the historical 626 bp spliced length, 261 bp Exon 3, and 132 bp 3′ UTR, it attributes these figures generally to *"certain historical annotations and literature summaries"*. As conclusively demonstrated in the follow-up authority audit (`REFERENCE_SEQUENCE_AUTHORITY_AUDIT_FOLLOWUP.md`), this 626 bp model is not an informal summary but the **exact official NCBI RefSeq specification of predecessor accession `NM_000518.4`** (curated from February 11, 2003 to June 13, 2018).
- **Severity:** **MINOR**
- **Recommended Author Correction:**  
  Revise line 95 to cite RefSeq `NM_000518.4` directly:  
  *Proposed Text:* *"Under historical RefSeq accession `NM_000518.4` (in effect 2003–2018) and associated literature summaries, Exon 3 was annotated as spanning 261 bp with a 132 bp 3' UTR (yielding a 626 bp spliced transcript, $c.*1..c.*132$ terminating at `...TTCATTGC`); the updated RefSeq `NM_000518.5` standard and project reference files (`NM_000518.5.json` and `NM_000518.5.fasta`) incorporate two additional terminal adenines (`AA` at positions 627–628 derived from cDNA BU661647.1), establishing the current 628 bp reference model ($c.*1..c.*134$)."*

---

## 3. Molecular and Protein Agreement Counts Audit

A central requirement of this audit is verifying that the manuscript does not conflate the **30 variants in `EXACT_MOLECULAR_AGREEMENT`** with the **28 variants exhibiting exact protein nomenclature matches (`MATCH`)**.

### 3.1 Mapping of Frozen Candidate Results to Locked Decision Matrix

Cross-tabulation of the 55 primary candidates in `research/results/phase2c_benchmark_candidate_results.json` against the locked `research/protocol/CP4_1_DECISION_MATRIX.md` demonstrates exact mathematical consistency:

```
+----------------------------------------+-------------------------+-------+
| Comparison Category (Ten-Tier Rule)   | Protein Endpoint Status | Count |
+----------------------------------------+-------------------------+-------+
| EXACT_MOLECULAR_AGREEMENT              | MATCH                   |    28 |
| EXACT_MOLECULAR_AGREEMENT              | NOT_APPLICABLE          |     2 |
| MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE | DISCREPANCY (Format)    |    20 |
| EXTERNAL_ANNOTATION_INCOMPLETE         | INCOMPLETE              |     5 |
+----------------------------------------+-------------------------+-------+
| TOTAL PRIMARY EVALUATION COHORT        |                         |    55 |
+----------------------------------------+-------------------------+-------+
```

### 3.2 Biological Explanation of the 30 vs. 28 Discrepancy
- **The 30 `EXACT_MOLECULAR_AGREEMENT` Candidates:**  
  Under the CP4.1 Decision Matrix, assignment to `EXACT_MOLECULAR_AGREEMENT` requires that the runtime molecular consequence matches the external ClinVar annotation ($A_{\text{mol}} == C_{\text{mol}}$) and that no protein nomenclature discrepancy exists.  
  - For 28 coding variants (Classes C01, C02, C03, and one C06 stop insertion `p.Glu44Ter`), both molecular and protein strings match identically ($A_{\text{prot}} == C_{\text{prot}}$).  
  - For 2 non-coding 3′ UTR regulatory variants (Class C11: candidates `HBB-CP2-265` [$c.*110T>C$] and `HBB-CP2-268` [$c.*113A>G$]), molecular consequences match identically (`3' UTR Regulatory`), while protein translation is physically absent (`runtime_protein: None`, `external_protein: None`). Under CP4.1 Decision Matrix Rule 9, these non-coding records are assigned comparison category `EXACT_MOLECULAR_AGREEMENT` with secondary protein status `NOT_APPLICABLE`.  
  - Therefore: $\text{Category } 30 = 28\text{ (Protein MATCH)} + 2\text{ (Protein NOT\_APPLICABLE)}$.
- **The 20 `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` Candidates:**  
  All 20 are frameshift alterations (9 deletions in C04, 11 duplications in C06). The molecular consequence matches 100% (`Frameshift`), but ClinVar records shorthand notation (`E7fs`, `V127fs`, etc.) while the engine outputs full HGVS translation syntax (`p.Glu7ArgfsTer13`).
- **The 5 `EXTERNAL_ANNOTATION_INCOMPLETE` Candidates:**  
  All 5 are canonical splice acceptor variants (Class C09: `c.93-1G>C`, `c.93-2A>C`, `c.93-2A>G`, `c.316-1G>T`, `c.316-2A>C`). The molecular consequence matches 100% (`Splice Site Disruption`), but ClinVar records omit protein strings entirely (`p.?`).

### 3.3 Manuscript Text Audit on Counts
Every occurrence in `PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` was inspected:
1. **Abstract Results (Line 17):**  
   > *"...across seven represented biological mutation classes (30 exact molecular agreements, 20 molecular agreements with protein representation differences, and 5 external annotations lacking protein strings). Secondary exact protein nomenclature concordance was 50.91% (28/55; exact 95% CI: [37.07%, 64.65%]), reflecting 20 shorthand truncated frameshift representations, 5 omitted splice protein strings in ClinVar records, and 2 non-coding 3' UTR variants for which protein consequence matching was not applicable."*  
   **Verdict: VERIFIED.** Completely accurate and mathematically partitioned.
2. **Results Section 3.2 (Line 221):**  
   > *"1. `EXACT_MOLECULAR_AGREEMENT`: 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies. This category encompasses 28 coding variants with exact protein nomenclature agreement (`MATCH`) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (`NOT_APPLICABLE`)."*  
   **Verdict: VERIFIED.** Explicitly distinguishes the 28 from the 2.
3. **Results Section 3.3 Table 2 (Lines 231–238):**  
   > Breakdown lists: `MATCH` = 28 (50.91%), `DISCREPANCY (Format)` = 20 (36.36%), `INCOMPLETE` = 5 (9.09%), `NOT_APPLICABLE` = 2 (3.64%), Total = 55 (100.00%).  
   **Verdict: VERIFIED.** Fully detailed with class distributions.
4. **Discussion Section 4.1 (Line 323):**  
   > *"1. `EXACT_MOLECULAR_AGREEMENT`: Exactly 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies, comprising 28 coding variants with exact protein nomenclature agreement (`MATCH`) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (`NOT_APPLICABLE`)."*  
   **Verdict: VERIFIED.** Fully synchronized with Results.

**Audit Finding:** Zero instances of conflating the 30 molecular agreements with exact protein matches exist in the manuscript. All statements are verified.

---

## 4. Scientific Claims, Protocol Boundaries & Disclosures Audit

The manuscript was audited to confirm that all required methodological limitations, selection biases, and boundaries are rigorously and consistently stated.

### 4.1 Disclosure 1: Curation Incorporation (Verification) Bias
- **Requirement:** Disclose that primary cohort variants were selected using engine agreement with external annotations (`comparison_status == "EXACT_AGREEMENT"`), creating incorporation/verification bias.
- **Manuscript Evidence:**
  - *Abstract (Line 20):* *"Candidate qualification during curation required deterministic engine agreement (`comparison_status == "EXACT_AGREEMENT"`), introducing substantial incorporation (verification) bias that restricts generalizability to unselected or novel clinical variants."*
  - *Introduction 1.7 (Line 67):* *"Crucially, during CP2.2 curation, admission to the proposed primary cohort required deterministic engine agreement (`comparison_status == "EXACT_AGREEMENT"`)... creating incorporation or verification bias."*
  - *Methods 2.6 (Lines 143–145):* Cites exact script lines (`run_independent_verification.py`, lines 231–246) and details the diversion of discordant variants into secondary registries.
  - *Discussion 4.2 (Line 337) & Limitations 5.1 (Lines 367–370):* Entire dedicated limitation subsection.
- **Audit Verdict: VERIFIED.**

### 4.2 Disclosure 2: Single-Database ClinVar Origin Without Non-ClinVar Corroboration
- **Requirement:** Disclose that all 55 primary variants are ClinVar-derived with zero independent non-ClinVar biological corroboration dossiers.
- **Manuscript Evidence:**
  - *Abstract (Line 20):* *"`independent_non_clinvar_corroboration == "NONE"`"*
  - *Introduction 1.7 (Line 67):* *"All 55 primary variants were derived exclusively from ClinVar records, and zero finalized independent non-ClinVar biological corroboration dossiers were available..."*
  - *Methods 2.5 (Line 126):* *"Exactly 0 of the 55 primary candidates possessed independent biological corroboration dossiers outside of ClinVar..."*
  - *Results 3.1 (Line 206) & Limitations 5.2 (Lines 372–376):* Dedicated limitation subsection on external reference dependence.
- **Audit Verdict: VERIFIED.**

### 4.3 Disclosure 3: Unrepresented Biological Classes ($n = 0$)
- **Requirement:** Disclose that biological mutation classes C05, C07, C08, and C10 have zero primary cohort candidates.
- **Manuscript Evidence:**
  - *Abstract (Line 20), Intro 1.7 (Line 67), Results 3.4 Table 3 & Subsection (Lines 261, 263, 264, 266, 270–277), Limitations 5.3 (Lines 377–385), Conclusion (Line 403).*
  - Itemized reasons documented: C05 (25-codon deletion relegated to conditional); C07 (0-star evidence relegated to secondary); C08 (zero clean donor variants available); C10 (promoter variants $> -50$ bp exceeded transcript boundary).
- **Audit Verdict: VERIFIED.**

### 4.4 Disclosure 4: Decoupling of Synthetic Controls & Software Regression
- **Requirement:** Ensure that Experiment D (18 synthetic controls) and software regression ($A$ vs $B$) are strictly isolated from the primary endpoint ($A$ vs $C$).
- **Manuscript Evidence:**
  - *Methods 2.1 (Lines 76–81):* Formally defines Entity $A$, Entity $B$, and Entity $C$, and isolates $B$ from primary concordance logic.
  - *Methods 2.10 (Lines 193–198):* Experiment D ($N = 18$) never pooled into primary denominator ($N = 55$).
  - *Results 3.2, 3.5, 3.6, and Table 5:* Present $A$ vs $C$, secondary protein, Experiment D ($N = 18$), and $A$ vs $B$ as four mathematically separate dimensions.
- **Audit Verdict: VERIFIED.**

### 4.5 Disclosure 5: Molecular Consequence vs. Clinical Pathogenicity & Diagnostic Validity
- **Requirement:** Do not claim clinical diagnostic validity or pathogenicity prediction from molecular consequence agreement.
- **Manuscript Evidence:**
  - *Abstract (L8, L20, L23), Intro 1.4 (L49–53), Intro 1.7 (L65), Methods 2.1 (L74), Discussion 4.2 (L332), Discussion 4.5 (L356), Limitations 5.6 (L395), Conclusion (L403).*
  - Consistently emphasizes ACMG/AMP distinction (molecular impact vs evaluative clinical determination).
- **Audit Verdict: VERIFIED.**

### 4.6 Disclosure 6: Statistical Sampling vs. Selection Bias
- **Requirement:** Disclose that confidence intervals quantify sampling error and do not rectify selection bias.
- **Manuscript Evidence:**
  - *Methods 2.9 (Line 189):* *"The Clopper-Pearson confidence interval quantifies sampling uncertainty under the mathematical assumption of independent Bernoulli trials drawn from the specified cohort distribution. This statistical interval does not correct for selection bias, incorporation bias, reference transcript dependency, or single-database provenance."*
  - *Limitations 5.5 (Lines 389–393):* Re-emphasizes statistical bounds and wide CIs for small classes.
- **Audit Verdict: VERIFIED.**

---

## 5. Cryptographic & Computational Integrity Checks

To ensure that research artifacts remain untampered and reproducible, all on-disk files were hashed using SHA256 and compared against pre-recorded values:

| Artifact Description | Local File Path | Expected SHA256 Checksum | Actual Computed SHA256 | Verification Result |
|---|---|---|---|:---:|
| **Primary Dataset Manifest** | `research/manifest/phase2c_primary.json` | `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` | `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` | **PERFECT MATCH** |
| **Historical Test Manifest** | `research/manifest/frozen_test.json` | `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994` | `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994` | **PERFECT MATCH** |
| **Benchmark Protocol Specification** | `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` | `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` | **PERFECT MATCH** |
| **Candidate Result Records** | `research/results/phase2c_benchmark_candidate_results.json` | `e0493b36b95c75b7034ff37f30aaa393dcaaa9f7252fc171ec6b20db29a766c4` | `e0493b36b95c75b7034ff37f30aaa393dcaaa9f7252fc171ec6b20db29a766c4` | **PERFECT MATCH** |
| **Benchmark Summary Record** | `research/results/phase2c_benchmark_summary.json` | `36047f0675a86ccf2032f42624ce2f48c16636ba37ca2bf15607376c533b8718` | `36047f0675a86ccf2032f42624ce2f48c16636ba37ca2bf15607376c533b8718` | **PERFECT MATCH** |
| **Pure Sequence (NM_000518.5)** | `data/reference/NM_000518.5.fasta` (seq only) | `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` | `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` | **PERFECT MATCH** |
| **Pure Sequence (NG_000007.3)** | `data/reference/NG_000007.3.fasta` (seq only) | `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18` | `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18` | **PERFECT MATCH** |

### Computational Integrity Note:
- **No Overclaiming of Software Verification:** As documented in `research/results/CP4_3_FINAL_CONSISTENCY_CHECK.md`, the initial CP2.2 curation check reused the comparison engine function rather than an independent software reimplementation. The manuscript correctly characterizes its primary result as **computational rule execution fidelity on curated records**, and does not claim independent software verification or biological ground truth.

---

## 6. Master Table of Numerical Claims & Supporting Artifacts

| Numerical Claim | Value in Manuscript | Denominator ($N$) | Percentage (%) | Exact 95% Clopper-Pearson CI | Primary Supporting Artifact | Verification Status |
|---|:---:|:---:|:---:|:---:|---|:---:|
| **Primary Cohort Size** | 55 | 55 | 100.00% | — | `phase2c_primary.json` | **VERIFIED** |
| **Primary Molecular Matches** | 55 | 55 | 100.00% | [93.51%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Primary Molecular Discrepancies** | 0 | 55 | 0.00% | [0.00%, 6.49%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Comparison Category: EXACT_MOLECULAR_AGREEMENT** | 30 | 55 | 54.55% | [40.57%, 68.01%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Comparison Category: MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE** | 20 | 55 | 36.36% | [23.83%, 50.38%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Comparison Category: EXTERNAL_ANNOTATION_INCOMPLETE** | 5 | 55 | 9.09% | [3.02%, 20.01%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Secondary Exact Protein Matches (`MATCH`)** | 28 | 55 | 50.91% | [37.07%, 64.65%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Secondary Protein Format Discrepancies (`DISCREPANCY`)** | 20 | 55 | 36.36% | [23.83%, 50.38%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Secondary Protein Omissions (`INCOMPLETE`)** | 5 | 55 | 9.09% | [3.02%, 20.01%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Secondary Protein Not Applicable (`NOT_APPLICABLE`)** | 2 | 55 | 3.64% | [0.44%, 12.53%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C01 Missense Concordance** | 14 | 14 | 100.00% | [76.84%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C02 Nonsense Concordance** | 3 | 3 | 100.00% | [29.24%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C03 Synonymous Concordance** | 10 | 10 | 100.00% | [69.15%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C04 Frameshift Deletions** | 9 | 9 | 100.00% | [66.37%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C05 In-Frame Indels/Deletions** | 0 | 0 | — | null | `phase2c_primary.json` | **VERIFIED** |
| **Class C06 Frameshift Duplications** | 12 | 12 | 100.00% | [73.54%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C07 In-Frame Insertions/Duplications** | 0 | 0 | — | null | `phase2c_primary.json` | **VERIFIED** |
| **Class C08 Splice Donor Disruptions** | 0 | 0 | — | null | `phase2c_primary.json` | **VERIFIED** |
| **Class C09 Splice Acceptor Disruptions** | 5 | 5 | 100.00% | [47.82%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Class C10 5′ UTR Regulatory Variants** | 0 | 0 | — | null | `phase2c_primary.json` | **VERIFIED** |
| **Class C11 3′ UTR Regulatory Variants** | 2 | 2 | 100.00% | [15.81%, 100.00%] | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Experiment D Robustness Rejections** | 18 | 18 | 100.00% | [81.47%, 100.00%] | `phase2c_robustness_results.json` | **VERIFIED** |
| **Software Regression Invariance ($A == B$)** | 55 | 55 | 100.00% | — | `phase2c_benchmark_candidate_results.json` | **VERIFIED** |
| **Legacy Codon Designations Tracked** | 33 | 55 | 60.00% | [45.91%, 72.98%] | `PHASE2C_ERROR_REGISTER.md` | **VERIFIED** |

---

## 7. Master Table of Reference Accession & Coordinate Claims

| Coordinate / Structural Parameter | Claimed in Manuscript | Primary Biological Source | Local Reference File | Verification Status |
|---|---|---|---|:---:|
| **Transcript Accession** | `NM_000518.5` | NCBI RefSeq / MANE Select | `NM_000518.5.fasta` / `.json` | **VERIFIED** |
| **Total Spliced Length** | 628 nt | NCBI Nuccore `NM_000518.5` | `NM_000518.5.fasta` (len: 628) | **VERIFIED** |
| **Exon 1 Boundaries** | Transcript 1..142 (142 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (exons[0]) | **VERIFIED** |
| **5′ UTR Boundaries** | $c.-50..c.-1$ (bases 1..50, 50 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (5_utr) | **VERIFIED** |
| **Exon 1 Coding Segment** | $c.1..c.92$ (bases 51..142, 92 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (cds) | **VERIFIED** |
| **Exon 2 Boundaries** | Transcript 143..365 (223 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (exons[1]) | **VERIFIED** |
| **Exon 2 Coding Segment** | $c.93..c.315$ (bases 143..365, 223 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (cds) | **VERIFIED** |
| **Exon 3 Boundaries** | Transcript 366..628 (263 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (exons[2]) | **VERIFIED** |
| **Exon 3 Coding Segment** | $c.316..c.444$ (bases 366..494, 129 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (cds) | **VERIFIED** |
| **Coding Sequence (CDS)** | $c.1..c.444$ (bases 51..494, 444 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (cds_length: 444) | **VERIFIED** |
| **3′ UTR Boundaries** | $c.*1..c.*134$ (bases 495..628, 134 bp) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (3_utr) | **VERIFIED** |
| **PolyA Cleavage Site** | Position 628 ($c.*134$) | NCBI GenBank `NM_000518.5` | `NM_000518.5.json` (polyA) | **VERIFIED** |
| **Genomic Reference Locus** | `NG_000007.3:70545..72152` (1608 bp) | NCBI RefSeqGene `NG_000007.3` | `NG_000007.3.fasta` / `.json` | **VERIFIED** |
| **Intron 1 Coordinates & Span** | Genomic 70687..70816 (130 bp) | NCBI RefSeqGene `NG_000007.3` | `NG_000007.3.json` (introns[0]) | **VERIFIED** |
| **Intron 2 Coordinates & Span** | Genomic 71040..71889 (850 bp) | NCBI RefSeqGene `NG_000007.3` | `NG_000007.3.json` (introns[1]) | **VERIFIED** |
| **Intron 1 Splice Dinucleotides** | Donor: `GT` (70687-88); Acceptor: `AG` (70815-16) | In silico genomic extraction | `backend/app/core/reference.py` | **VERIFIED** |
| **Intron 2 Splice Dinucleotides** | Donor: `GT` (71040-41); Acceptor: `AG` (71888-89) | In silico genomic extraction | `backend/app/core/reference.py` | **VERIFIED** |

---

## 8. Consolidated Findings Registry

Every finding in this audit is classified according to standard clinical and scientific editorial severity:
- **CRITICAL:** Factual error, numerical contradiction, or unsubstantiated claim that invalidates core conclusions.
- **MAJOR:** Missing required academic front-matter, structural section omission, or potential ambiguity requiring author resolution before journal submission.
- **MINOR:** Stylistic, provenance, or precision enhancement that strengthens peer-review readiness.
- **VERIFIED:** Statement or data point confirmed 100% accurate and mathematically aligned.

| ID | Category | Location | Summary of Finding | Severity | Recommended Author Action |
|:---:|---|---|---|:---:|---|
| **F-01** | Manuscript Metadata | Manuscript Header | Manuscript draft lacks author names, institutional affiliations, ORCID identifiers, and corresponding author contact email. | **MAJOR** | Insert complete author list, institutional affiliations, and corresponding author email prior to submission. |
| **F-02** | Ethical Governance | Methods / End-matter | Manuscript currently lacks an explicit Institutional Review Board (IRB) / Ethics Committee determination statement. | **MAJOR** | Add an explicit Ethics Statement (e.g., declaring exemption due to exclusive use of publicly available, fully de-identified ClinVar records). |
| **F-03** | Declarations | End-matter | Manuscript draft lacks Funding and Competing Interests disclosure sections. | **MAJOR** | Add standard declarations ("Funding: This research received no external funding", "Competing Interests: The authors declare no competing interests"). |
| **F-04** | Data Availability | End-matter | Manuscript draft lacks a formal Data and Code Availability statement. | **MAJOR** | Add Data Availability statement referencing the GitHub repository, Zenodo DOI, and NCBI ClinVar accession identifiers. |
| **F-05** | Provenance Precision | Methods Section 2.2 (L95) | Historical 626 bp / 132 bp UTR model is attributed generally to "certain historical annotations and literature summaries" rather than citing NCBI RefSeq predecessor `NM_000518.4`. | **MINOR** | Update sentence to explicitly cite RefSeq predecessor `NM_000518.4` (in effect 2003–2018) for definitive provenance. |
| **F-06** | Table Clarification | Results Table 1 (L218) | Evidentiary basis states "All 55 variants valid under NM_000518.5", whereas intronic reference bases are confirmed against `NG_000007.3`. | **MINOR** | Clarify note: "All 55 variants valid under canonical cDNA coordinates (exonic/UTR against NM_000518.5, intronic against NG_000007.3)". |
| **F-07** | Categorical Counts | Abstract, Results 3.2, Discussion 4.1 | 30 exact molecular agreements vs 28 exact protein nomenclature matches are correctly distinguished and explained. | **VERIFIED** | Maintain current phrasing; mathematical accounting is sound. |
| **F-08** | Bias Disclosures | Abstract, Intro, Methods, Discussion, Limitations | Incorporation/verification bias (`comparison_status == "EXACT_AGREEMENT"`) and ClinVar exclusivity are fully disclosed. | **VERIFIED** | Preserve all current limitation text unchanged. |
| **F-09** | Reference Models | Methods 2.2, Results 3.5 | 628 nt transcript model, 444 nt CDS, 134 nt 3′ UTR, 130/850 bp introns, and exon lengths 142/223/263 bp are verified bit-for-bit. | **VERIFIED** | Maintain current text unchanged. |
| **F-10** | Cryptographic Hashes | Manuscript 2.7, Results 3.1, Discussion 4.6 | SHA256 checksums for primary manifest, frozen baseline, and protocol specification match on-disk files exactly. | **VERIFIED** | Maintain current hashes unchanged. |

---

## 9. Statements That Are Already Correct and Must Remain Unchanged

The following core passages in `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` have been verified as scientifically accurate, mathematically sound, and methodologically rigorous. They should **NOT** be altered during author review:

1. **Abstract Results (Line 17):**  
   The complete mathematical accounting of the primary endpoint ($55/55$, $100.00\%$, CI: [93.51%, 100.00%]), secondary protein concordance ($28/55$, $50.91\%$), 20 truncated frameshifts, 5 incomplete splice strings, and 2 non-coding UTR variants ($28 + 20 + 5 + 2 = 55$).
2. **Methods Section 2.1 (Lines 76–81):**  
   The mathematical and operational decoupling of Entity $A$ (Runtime Engine), Entity $B$ (Frozen Regression Expected), and Entity $C$ (External ClinVar Annotation), establishing that $A$ is compared exclusively against $C$ for primary concordance.
3. **Methods Section 2.2 (Lines 83–94):**  
   The biological and structural separation between the spliced mature mRNA transcript (`NM_000518.5`, 628 nt) and the genomic gene locus (`NG_000007.3`, 1608 nt), properly allocating introns 1 and 2 to the genomic locus.
4. **Methods Section 2.6 (Lines 143–145):**  
   The candid, scientifically rigorous disclosure of curation incorporation (verification) bias resulting from conditioning primary cohort admission on `comparison_status == "EXACT_AGREEMENT"` in `run_independent_verification.py`.
5. **Methods Section 2.9 (Lines 181–192):**  
   The Clopper-Pearson exact binomial confidence interval formulation and the critical methodological caveat that statistical confidence intervals quantify only random Bernoulli sampling error and cannot correct for selection bias.
6. **Results Section 3.2 (Line 221) & Discussion Section 4.1 (Line 323):**  
   The precise definition of `EXACT_MOLECULAR_AGREEMENT` ($n = 30$), explicitly documenting the composition as 28 protein `MATCH` and 2 protein `NOT_APPLICABLE`.
7. **Results Section 3.4 Table 3 & Subsection (Lines 261–277):**  
   The transparent reporting of $n = 0$ for unrepresented biological mutation classes C05, C07, C08, and C10 with CI reported as `null` / unrepresented.
8. **Limitations Sections 5.1 through 5.6 (Lines 365–396):**  
   The six comprehensive limitation subsections detailing incorporation bias, single-database ClinVar dependence, mutation class gaps, protein annotation incompleteness, sample size constraints, and restricted scope of computational inference.

---

## 10. Outstanding Author Actions Prior to Journal Submission

To prepare the manuscript draft for submission to a peer-reviewed bioinformatics or human genetics journal, the following author actions are required:

1. **Author Details & Affiliations:**  
   Provide the full author name(s), institutional affiliations, institutional physical addresses, ORCID iDs, and the corresponding author's email address.
2. **Institutional Ethics & IRB Determination:**  
   Insert a formal Ethics Statement in the Methods or End-matter.  
   *Suggested Template:* *"Ethics approval was not required for this study as it involved exclusively computational analysis of publicly available, fully de-identified genetic variant records deposited in the NCBI ClinVar database. No human subjects, animals, or primary clinical specimens were recruited or analyzed."*
3. **Funding Disclosure:**  
   Insert a formal funding declaration.  
   *Suggested Template:* *"This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors."* (or insert active grant numbers if applicable).
4. **Competing Interests Statement:**  
   Insert a formal declaration of interest statement.  
   *Suggested Template:* *"The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."*
5. **Data & Code Availability:**  
   Insert a dedicated Data Availability section.  
   *Suggested Template:* *"The complete source code of the deterministic HBB mutation analyzer, benchmark evaluation suite, locked protocol specifications, and frozen dataset manifests are publicly available in the GitHub repository [insert URL] and archived on Zenodo [insert DOI]. Primary genetic variant annotations were obtained from NCBI ClinVar (https://www.ncbi.nlm.nih.gov/clinvar/)."*
6. **Minor Editorial Enhancements (F-05 & F-06):**  
   Review the minor enhancements recommended in Section 8 (explicitly citing RefSeq `NM_000518.4` in Section 2.2 line 95, and clarifying intronic reference validation in Table 1).

---

## 11. Anti-Tampering & Repository Integrity Sign-Off

We certify that throughout the execution of this forensic consistency audit:
1. **Zero files were edited, overwritten, renamed, or deleted**, with the sole exception of creating this audit report (`research/results/FINAL_MANUSCRIPT_CONSISTENCY_AUDIT.md`).
2. **No source code, reference FASTA files, JSON metadata, or frozen datasets were altered.**
3. **No benchmarks were rerun, and no numerical findings were modified.**
4. **The manuscript draft (`PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`) was inspected strictly in read-only mode.**
5. **All findings are traceable directly to versioned, cryptographic on-disk artifacts.**

---

## 12. Final Audit Sign-Off

```
================================================================================
FINAL VERDICT:
• PASS FOR AUTHOR CORRECTIONS
================================================================================
```
The HBB Gene Mutation Analyzer manuscript draft is scientifically coherent, mathematically validated, and fully synchronized with its supporting frozen research artifacts. Following the completion of the author administrative actions detailed in Section 10, the manuscript will be fully prepared for formal journal submission.
