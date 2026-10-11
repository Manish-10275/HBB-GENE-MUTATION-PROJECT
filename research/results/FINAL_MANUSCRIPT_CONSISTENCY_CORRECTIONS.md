# Final Scientific Manuscript Consistency Corrections Report

> **Project:** HBB Gene Mutation Analyzer Research Manuscript  
> **Document Type:** SCIENTIFIC CONSISTENCY CORRECTIONS AND AUDIT REPORT  
> **Target Manuscript:** `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`  
> **Audited Engine & Reference Files:**  
> - `backend/app/core/reference.py`  
> - `backend/app/core/hgvs.py`  
> - `data/reference/NM_000518.5.json`  
> - `data/reference/NM_000518.5.fasta`  
> - `data/reference/NG_000007.3.json`  
> - `data/reference/NG_000007.3.fasta`  
> **Audit Date:** 2026-10-11  
> **Execution Status:** COMPLETED (Strictly Evidence-Supported Edits; Zero Project Code or Benchmark Data Alterations)

---

## 1. Executive Summary

This report documents the final scientific consistency corrections applied to the manuscript draft (`research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md`). All edits were strictly evidence-supported, grounded directly in the frozen reference files (`data/reference/`) and actual backend validation code (`backend/app/core/`). 

In accordance with strict audit rules:
- Zero benchmarks were rerun.
- The frozen dataset manifest, protocols, comparison engine, and result artifacts were **not modified**.
- No numerical metrics were altered (Primary molecular concordance remains 55/55 [100.00%]; categories remain 30/20/5; protein endpoints remain 28/20/5/2; robustness controls remain 18/18 [100.00%]).
- All existing scientific disclosures regarding selection bias, incorporation bias, unrepresented mutation classes, and computational boundaries were **strictly preserved**.

---

## 2. Itemized Manuscript Changes

Every modification made to `research/manuscript/PHASE5_4_FINAL_MANUSCRIPT_DRAFT.md` is itemized below with its exact location, previous text, new text, and scientific rationale:

### Change 1: Clarification of Secondary Protein Endpoints in Abstract
- **Section:** Abstract — Results
- **Line:** Line 17
- **Previous Text:**  
  `Secondary exact protein nomenclature concordance was 50.91% (28/55; exact 95% CI: [37.07%, 64.65%]), reflecting 20 shorthand truncated frameshift representations and 5 omitted splice protein strings in ClinVar records.`
- **New Text:**  
  `Secondary exact protein nomenclature concordance was 50.91% (28/55; exact 95% CI: [37.07%, 64.65%]), reflecting 20 shorthand truncated frameshift representations, 5 omitted splice protein strings in ClinVar records, and 2 non-coding 3' UTR variants for which protein consequence matching was not applicable.`
- **Scientific Reason:** Provides complete mathematical accounting of all 27 non-matching records ($20 + 5 + 2 = 27$; $28 + 27 = 55$) in the Abstract, ensuring that the reader understands why exact protein agreement is 28 rather than 30.

---

### Change 2: Transcript Model vs. Genomic Locus Separation & 628 bp Harmonization
- **Section:** Methods — Section 2.2 ("Reference Sequence and Transcript Model")
- **Lines:** Lines 83–94
- **Previous Text:**  
  `The transcript model for NM_000518.5 spans 626 transcribed nucleotides, comprising three coding exons and two intervening introns:`  
  `- Exon 1: Transcript nucleotides 1–142, containing 50 bp of 5' untranslated region (c.-50 to c.-1) and 92 bp of coding sequence (c.1 to c.92).`  
  `- Intron 1: 130 bp intervening sequence situated between c.92 and c.93.`  
  `- Exon 2: Transcript nucleotides 143–365, containing 223 bp of coding sequence (c.93 to c.315).`  
  `- Intron 2: 850 bp intervening sequence situated between c.315 and c.316.`  
  `- Exon 3: Transcript nucleotides 366–626, containing 129 bp of coding sequence (c.316 to c.444) and 132 bp of 3' untranslated region (c.*1 to c.*132).`
- **New Text:**  
  `All sequence coordinates, genomic boundaries, and translation models in this study were anchored to versioned, curated RefSeq reference accessions (O'Leary et al., 2016). In accordance with the MANE initiative, RefSeq accession NM_000518.5 was selected as the canonical MANE Select transcript model (Morales et al., 2022). Genomic sequence context was defined by RefSeqGene accession NG_000007.3 on build GRCh38 (genomic locus coordinates 70545..72152, total length 1608 bp).`  
  `The canonical mature mRNA transcript NM_000518.5 comprises the three spliced coding exons concatenated without intronic sequence, spanning 628 transcribed nucleotides in the project reference sequence model:`  
  `- Exon 1: Transcript nucleotides 1–142 (142 bp; genomic 70545..70686), containing 50 bp of 5' untranslated region (c.-50 to c.-1) and 92 bp of coding sequence (c.1 to c.92).`  
  `- Exon 2: Transcript nucleotides 143–365 (223 bp; genomic 70817..71039), containing 223 bp of coding sequence (c.93 to c.315).`  
  `- Exon 3: Transcript nucleotides 366–628 (263 bp; genomic 71890..72152), containing 129 bp of coding sequence (c.316 to c.444) and 134 bp of 3' untranslated region (c.*1 to c.*134).`  
  `The two intervening introns interrupting the mature coding exons are defined within the genomic gene locus NG_000007.3:`  
  `- Intron 1 (IVS-1): 130 bp intervening sequence situated between Exon 1 and Exon 2 (c.92 and c.93; genomic nucleotides 70687..70816).`  
  `- Intron 2 (IVS-2): 850 bp intervening sequence situated between Exon 2 and Exon 3 (c.315 and c.316; genomic nucleotides 71040..71889).`  
  `In certain historical annotations and literature summaries, Exon 3 is described as spanning 261 bp with a 132 bp 3' UTR (yielding a 626 bp spliced transcript, c.*1..c.*132); the project implementation and versioned RefSeq reference files (NM_000518.5.json and NM_000518.5.fasta) explicitly incorporate the 628 bp reference model (c.*1..c.*134).`
- **Scientific Reason:**  
  1. Biological accuracy: The spliced mRNA transcript `NM_000518.5` contains only spliced exons; intervening introns do not exist within mature mRNA and reside exclusively within the genomic locus `NG_000007.3`.  
  2. Coordinate verification: The project reference files (`data/reference/NM_000518.5.fasta` and `NM_000518.5.json`) and codebase (`backend/app/core/reference.py`) define total length as 628 bp, Exon 3 as 366–628 (263 bp), and 3' UTR as 134 bp ($c.*1..c.*134$). Describing Exon 3 as 366–626 (132 bp UTR) contradicted the project's actual reference file. Both conventions are now rigorously documented.

---

### Change 3: Clarification of Reference Allele Validation & Accession Syntax
- **Section:** Methods — Section 2.3 ("Variant Representation and HGVS Parsing")
- **Lines:** Lines 97 and 100
- **Previous Text:**  
  `1. Input Sanitization & Accession Validation: Verifies HGVS syntax and matches authorized HBB reference accessions (NM_000518.5 or NG_000007.3).`  
  `...`  
  `4. Reference Allele Confirmation: Matches the asserted reference nucleotide against the actual nucleotide in NM_000518.5. Any mismatch triggers an explicit REFERENCE_MISMATCH error.`
- **New Text:**  
  `1. Input Sanitization & Accession Validation: Verifies HGVS cDNA syntax starting with c. and matches authorized HBB reference accessions (NM_000518.5 or NG_000007.3). Direct genomic coordinate syntax (g.) is not parsed.`  
  `...`  
  `4. Reference Allele Confirmation: Matches the asserted reference nucleotide against the biological reference sequence: exonic and UTR variants are validated against the spliced transcript NM_000518.5, while intronic variants are mapped and validated against the genomic sequence NG_000007.3. Any mismatch between query allele and reference base triggers an explicit REFERENCE_MISMATCH error.`
- **Scientific Reason:**  
  1. In `backend/app/core/hgvs.py` (lines 108–120), intronic variants (e.g. `c.92+1G>A`, `c.93-1G>C`) are validated against `ng_seq` (`NG_000007.3`) because `NM_000518.5` lacks intronic sequences. The previous text erroneously claimed all variants were matched against `NM_000518.5`.  
  2. In `backend/app/core/hgvs.py` (lines 74–86), queries must start with `c.`; genomic coordinate syntax (`g.`) is rejected with `SYNTAX_ERROR`. Disclosing this prevents overclaiming genomic parser capabilities.

---

### Change 4: Harmonization of 3' UTR Physical Boundary in Section 2.4
- **Section:** Methods — Section 2.4 ("Deterministic Molecular Consequence Computation")
- **Line:** Line 117
- **Previous Text:**  
  `- Untranslated Regions (UTRs): Variants at c. < 1 are classified as 5' UTR Regulatory, and variants at c. > 444 (c.*1..c.*132) are classified as 3' UTR Regulatory.`
- **New Text:**  
  `- Untranslated Regions (UTRs): Variants at c. < 1 are classified as 5' UTR Regulatory, and variants at c. > 444 (c.*1..c.*134) are classified as 3' UTR Regulatory.`
- **Scientific Reason:** Matches the 628 bp reference model where the 3' UTR spans 134 bp ($495..628$). In `backend/app/core/reference.py` line 52–57, coordinates up to `c.*134` are accepted, while `c.*135` triggers `OUT_OF_BOUNDS`.

---

### Change 5: Disambiguation of 30 vs. 28 Counts in Results Section 3.2
- **Section:** Results — Section 3.2 ("Primary Molecular Consequence Concordance")
- **Line:** Line 221
- **Previous Text:**  
  `1. EXACT_MOLECULAR_AGREEMENT: 30 variants (54.55%) exhibited simultaneous exact molecular consequence concordance and exact protein nomenclature matching.`
- **New Text:**  
  `1. EXACT_MOLECULAR_AGREEMENT: 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies. This category encompasses 28 coding variants with exact protein nomenclature agreement (MATCH) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (NOT_APPLICABLE).`
- **Scientific Reason:** Eliminates the misleading implication that all 30 variants had exact protein string matches. Clarifies that the 2 non-coding 3' UTR variants (Class C11) reside in `EXACT_MOLECULAR_AGREEMENT` at the molecular level, while their protein status is `NOT_APPLICABLE` (as they do not produce a translated polypeptide).

---

### Change 6: Disambiguation of 30 vs. 28 Counts in Discussion Section 4.1
- **Section:** Discussion — Section 4.1 ("Principal Findings")
- **Line:** Line 323
- **Previous Text:**  
  `1. EXACT_MOLECULAR_AGREEMENT: Exactly 30 variants (54.55%) exhibited simultaneous exact primary molecular consequence concordance and exact protein nomenclature matching.`
- **New Text:**  
  `1. EXACT_MOLECULAR_AGREEMENT: Exactly 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies, comprising 28 coding variants with exact protein nomenclature agreement (MATCH) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (NOT_APPLICABLE).`
- **Scientific Reason:** Aligns the discussion summary with the corrected Results Section 3.2 and Table 2.

---

## 3. Technical Statements That Could Not Be Verified

During the audit of reference files and implementation code, the following items could not be independently corroborated solely from the local repository:

1. **Origin of the Historical 626 bp Transcript Length:**  
   In older clinical publications and certain legacy NCBI web pages, human *HBB* mRNA is occasionally described as 626 bp with a 132 bp 3' UTR. The local files in the project (`NM_000518.5.fasta` and `NM_000518.5.json`) contain 628 bp with a 134 bp 3' UTR. Because no external network connection is permitted, we could not determine whether the 2-bp difference represents an earlier NCBI RefSeq assembly release or historical polyadenylation signal annotation convention. The manuscript text now explicitly documents both conventions.
2. **Third-Party Clinic Origin of Historical Aliases:**  
   The primary manifest and error register record historical codon designations (e.g., `CD 6 -A` for `c.20del`, `CD 22 (GAA>TAA)` for `c.67G>T`, `CD 30 (A>G)` for `c.91A>G`). While their mathematical offsets (-1 codon) and cDNA mappings were verified against `NM_000518.5`, the primary clinic records from which these historical names originated in the 1970s–1980s cannot be independently verified from repository files alone.

---

## 4. Issues Requiring Author Decision

Before final manuscript submission, the author should decide on the following editorial choices:

1. **Spliced Transcript Length Terminology (628 bp vs. 626 bp):**  
   - *Current Implementation:* 628 bp (`NM_000518.5.fasta`, length 628; 3' UTR 134 bp, $c.*1..c.*134$).  
   - *Current Manuscript Text:* Now describes the 628 bp model while explicitly explaining the historical 626 bp / 132 bp UTR literature notation.  
   - *Author Decision:* Confirm whether to keep this dual explanation (recommended for peer-reviewer clarity) or adopt a single convention.
2. **Genomic Coordinate ($g.$) Roadmap Disclosure:**  
   - *Current Implementation:* The parser strictly requires cDNA syntax ($c.$) and does not parse direct genomic syntax ($g.$).  
   - *Author Decision:* Confirm whether future software releases will support $g.$ syntax or whether locus analysis will remain permanently cDNA-focused.

---

## 5. Cryptographic Immutability & Anti-Tampering Sign-Off

We confirm that **zero changes were made to frozen datasets, manifests, protocols, or execution results**:

| Component / Artifact | Path | SHA256 Checksum | Modification Status |
|---|---|---|:---:|
| **Primary Dataset Manifest** | `research/manifest/phase2c_primary.json` | `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` | **UNMODIFIED** |
| **Historical Test Set** | `research/manifest/frozen_test.json` | `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994` | **UNMODIFIED** |
| **Benchmark Protocol** | `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969` | **UNMODIFIED** |
| **Candidate Result Records** | `research/results/phase2c_benchmark_candidate_results.json` | `e0493b36b95c75b7034ff37f30aaa393dcaaa9f7252fc171ec6b20db29a766c4` | **UNMODIFIED** |
| **Benchmark Summary** | `research/results/phase2c_benchmark_summary.json` | `36047f0675a86ccf2032f42624ce2f48c16636ba37ca2bf15607376c533b8718` | **UNMODIFIED** |
| **Comparison Engine** | `research/curation/phase2c_comparison_engine.py` | `7c26c1d7ac3b0632366f88e25a17de5c8560c3854e3d7a0d3a854430a9b2c384` | **UNMODIFIED** |
| **Backend Core Engine** | `backend/app/core/` (all modules) | Pinned to commit `845f595cc039e006d74237945450c7b4a9569ee6` | **UNMODIFIED** |

Zero benchmarks were rerun. Zero numerical data were modified.

---

## 6. Readiness Assessment

```
================================================================================
MANUSCRIPT READINESS ASSESSMENT: READY FOR AUTHOR REVIEW
================================================================================
Scientific Consistency:            VERIFIED & CORRECTED
30 vs 28 Metric Disambiguation:    RESOLVED (28 MATCH, 2 NOT_APPLICABLE = 30)
Transcript/Intron Architecture:    RESOLVED (Spliced mRNA vs Genomic Locus separated)
Reference Validation Audit:        RESOLVED (Dual NM_000518.5 & NG_000007.3 documented)
Selection Bias & Limitations:      PRESERVED & EXPLICIT
Mathematical Integrity:            100% Traceable to On-Disk Artifacts
================================================================================
```

### Important Notice on Journal Submission Readiness:
The manuscript is **READY FOR AUTHOR REVIEW**. We explicitly do **not** declare it ready for journal submission, as journal submission requires author sign-off on:
1. Target journal formatting, word count, and reference style requirements.
2. Formal author authorship declarations and institutional affiliations.
3. Author decisions on the flagged coordinate terminology choices noted in Section 4.
