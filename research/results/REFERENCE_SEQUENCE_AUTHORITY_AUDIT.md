# Authoritative Reference Sequence Verification Report: HBB Transcript & Genomic Reference Models

> **Audit Document:** INDEPENDENT REFERENCE SEQUENCE AUTHORITY & PROVENANCE AUDIT  
> **Target Investigation:** Authority, Traceability, and Coordinate Consistency of `NM_000518.5` and `NG_000007.3`  
> **Local Reference Files Audited:**  
> - `data/reference/NM_000518.5.fasta`  
> - `data/reference/NM_000518.5.json`  
> - `data/reference/NG_000007.3.fasta`  
> - `data/reference/NG_000007.3.json`  
> **Authoritative Remote Sources Queried (via NCBI E-Utilities API):**  
> - NCBI RefSeq `NM_000518.5` (GenBank & FASTA, Version 06-SEP-2026)  
> - NCBI RefSeq `NM_000518.4` (GenBank & FASTA, Version 01-MAY-2018)  
> - NCBI RefSeqGene `NG_000007.3` (FASTA, Coordinates 70545..72152)  
> **Audit Date:** 2026-10-11  
> **Execution Constraint:** Strictly Read-Only Investigation; Zero Modifications to Files, Manuscript Text, Code, or Datasets

---

## 1. Executive Summary

This forensic reference sequence audit was conducted to resolve the question regarding the length and coordinate boundaries of the human beta-globin (*HBB*) canonical transcript reference model. Specifically, this audit evaluated whether the local reference file (`data/reference/NM_000518.5.fasta`, length **628 nucleotides**) is valid and authentic, or whether the historical literature description of **626 nucleotides** represents the correct RefSeq specification.

### Key Audit Findings:
1. **Network Access & Authoritative RefSeq Query:**  
   Live programmatic network access to the National Center for Biotechnology Information (NCBI) Entrez E-Utilities API was established. Authoritative RefSeq GenBank and FASTA records were retrieved directly for `NM_000518.5`, historical predecessor `NM_000518.4`, and RefSeqGene `NG_000007.3`.
2. **Local `NM_000518.5` is 100% Bit-for-Bit Identical to Authoritative NCBI RefSeq:**  
   The local sequence (`data/reference/NM_000518.5.fasta`) matches the authoritative NCBI RefSeq record for `NM_000518.5` with **zero nucleotide discrepancies** across all 628 bases. Both share the exact SHA256 sequence checksum:  
   `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3`.
3. **Exon, CDS, and 3' UTR Boundaries are Identical to NCBI RefSeq:**  
   The authoritative NCBI record confirms:
   - Exon 1: bases 1–142 (142 bp)
   - Exon 2: bases 143–365 (223 bp)
   - Exon 3: bases 366–628 (263 bp)
   - Coding Sequence (CDS): bases 51–494 (444 bp, translating to `NP_000509.1`, 147 amino acids)
   - 3' UTR: bases 495–628 (134 bp, $c.*1$ to $c.*134$, terminating at major polyA site 628).
4. **Historical Origin of the 626 Nucleotide / 132 bp UTR Description:**  
   The description of a 626-nucleotide transcript with a 132 bp 3' UTR ($c.*1..c.*132$) is **fully traceable to an official NCBI RefSeq record**: predecessor version **`NM_000518.4`** (in effect until June 13, 2018). In `NM_000518.4`, the sequence terminated at base 626 (`...ttcattgc`). On June 13, 2018, NCBI updated the accession to **`NM_000518.5`**, adding two terminal adenines (`AA`) supported by full-length cDNA clone `BU661647.1`, establishing the current 628 bp / 134 bp UTR standard.
5. **Genomic Locus `NG_000007.3` is 100% Bit-for-Bit Identical:**  
   The local genomic reference segment (`data/reference/NG_000007.3.fasta`, 1608 bp) matches NCBI RefSeqGene `NG_000007.3:70545..72152` exactly (SHA256: `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18`). Splicing the three genomic exons in silico reproduces `NM_000518.5` with 100% sequence identity and canonical invariant dinucleotide splice junctions (`GT` donor, `AG` acceptor).

---

## 2. Local Reference Artifact Inventory & Cryptographic Checksums

Direct inspection of the versioned local files in `data/reference/` yielded the following metadata and cryptographic hashes:

| Attribute | `data/reference/NM_000518.5` | `data/reference/NG_000007.3` |
|---|---|---|
| **Accession Version** | `NM_000518.5` | `NG_000007.3` |
| **Molecule Type** | mRNA (MANE Select) | genomic DNA (RefSeqGene) |
| **Total Sequence Length** | **628 nucleotides** | **1608 nucleotides** |
| **Genomic Locus Coordinates** | N/A (Spliced mRNA) | GRCh38 chr11: 70545..72152 |
| **CDS Coordinates** | 51..494 (444 bp) | 70595..72018 (3 segments: 51..142, 273..495, 1346..1474) |
| **Protein Translation** | `NP_000509.1` (147 amino acids) | `NP_000509.1` (147 amino acids) |
| **Raw Sequence SHA256** | `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` | `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18` |
| **JSON Metadata File SHA256** | `553da0b0fe9586146fc1d5289942a44b1c2b87612f10b77da20182ddfd26d7aa` | `bb17d84fcf13d5cf2c510821e25e365e1ebaf8483fdf441fe9b78e87cc5d0342` |
| **FASTA File SHA256** | `2d3b5b63aaee21c1767d9341ea22d64539ef2a4bf7fe9155bc5dbeaf0155b1eb` | `d7a5b3a3c10efec224f8bc4ee560f47e33fe1204eaae644682054ff843a1a9e6` |

---

## 3. Comparison with Authoritative NCBI RefSeq Records

Authoritative reference sequences were retrieved directly from NCBI via the Entrez API endpoint:  
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.5`

### 3.1 Sequence-Level Bit-for-Bit Alignment

```
================================================================================
NCBI REFSEQ SEQUENCE ALIGNMENT EVALUATION:
================================================================================
Local File:           data/reference/NM_000518.5.fasta
Authoritative NCBI:   NCBI Nuccore NM_000518.5 (GI: 1403306806)
Length (Local):       628 nucleotides
Length (NCBI):        628 nucleotides
SHA256 (Local):       9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3
SHA256 (NCBI):        9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3
Pairwise Mismatches:  0 / 628 (0.00%)
Alignment Verdict:    PERFECT BIT-FOR-BIT IDENTITY
================================================================================
```

### 3.2 Coordinate & Feature Alignment Against NCBI Annotation

Inspection of the authoritative NCBI GenBank record features for `NM_000518.5`:

| Structural Feature | Local Project Reference | Authoritative NCBI RefSeq (`NM_000518.5`) | Verification Status |
|---|:---:|:---:|:---:|
| **Total Transcript Length** | 628 bp | 628 bp | **MATCH** |
| **Exon 1 Span** | 1..142 (142 bp) | 1..142 (142 bp) | **MATCH** |
| **5' UTR Span** | 1..50 ($c.-50..c.-1$, 50 bp) | 1..50 (50 bp) | **MATCH** |
| **Exon 1 Coding Segment** | 51..142 ($c.1..c.92$, 92 bp) | 51..142 (92 bp) | **MATCH** |
| **Exon 2 Span** | 143..365 ($c.93..c.315$, 223 bp) | 143..365 (223 bp) | **MATCH** |
| **Exon 3 Span** | 366..628 (263 bp) | 366..628 (263 bp) | **MATCH** |
| **Exon 3 Coding Segment** | 366..494 ($c.316..c.444$, 129 bp) | 366..494 (129 bp) | **MATCH** |
| **Coding Sequence (CDS)** | 51..494 (444 bp) | 51..494 (444 bp) | **MATCH** |
| **Protein Identifier** | `NP_000509.1` (147 aa) | `NP_000509.1` (147 aa) | **MATCH** |
| **3' UTR Span** | 495..628 ($c.*1..c.*134$, 134 bp) | 495..628 (134 bp) | **MATCH** |
| **Polyadenylation Signal** | 602..607 (`AATAAA`, $c.*108..c.*113$) | 602..607 (`regulatory_class="polyA_signal_sequence"`) | **MATCH** |
| **PolyA Cleavage Site** | 628 ($c.*134$) | 628 (`polyA_site=628`, note="major polyA site") | **MATCH** |

**Conclusion:** The local sequence and coordinate metadata in `data/reference/NM_000518.5.json` and `data/reference/NM_000518.5.fasta` are **100% authentic, correct, and authoritative**.

---

## 4. Investigation of the Historical 626 Nucleotide / 132 bp UTR Description

To determine whether the historical literature description of a 626 nucleotide transcript and 132 bp 3' UTR was supported by a traceable source, we retrieved the predecessor NCBI RefSeq record:  
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.4`

### 4.1 Traceable Origin: NCBI RefSeq Version `NM_000518.4`
The official NCBI GenBank comment in `NM_000518.5` explicitly states:
> `COMMENT: On Jun 13, 2018 this sequence version replaced NM_000518.4.`

Comparison of `NM_000518.4` vs. `NM_000518.5`:

| Annotation Attribute | Predecessor `NM_000518.4` (Until June 2018) | Current Standard `NM_000518.5` (June 2018–Present) | Difference |
|---|:---:|:---:|:---:|
| **Total Length** | **626 bp** | **628 bp** | **+2 bp** |
| **Exon 1** | 1..142 (142 bp) | 1..142 (142 bp) | Identical |
| **Exon 2** | 143..365 (223 bp) | 143..365 (223 bp) | Identical |
| **Exon 3** | **366..626 (261 bp)** | **366..628 (263 bp)** | **+2 bp** |
| **CDS Span** | 51..494 (444 bp) | 51..494 (444 bp) | Identical |
| **3' UTR Span** | **495..626 (132 bp; $c.*1..c.*132$)** | **495..628 (134 bp; $c.*1..c.*134$)** | **+2 bp** |
| **PolyA Signal** | 602..607 (`AATAAA`) | 602..607 (`AATAAA`) | Identical |
| **PolyA Cleavage Site** | **626** | **628** | **+2 bp** |
| **3' Terminal Sequence** | `...ttcattgc` (base 626) | `...ttcattgcaa` (bases 627–628) | Added `AA` |
| **Evidentiary Basis** | Sourced from `V00497.1`, `AU139015.1` | Sourced from `AK311825.1`, `BU661647.1` | Updated cDNA clone |

### 4.2 Biological Evaluation:
1. The 626-nucleotide description is **NOT an error, guessing, or rumor**; it is the **exact, official RefSeq specification of `NM_000518.4`**, which was the global standard for human *HBB* prior to June 13, 2018.
2. The current 628-nucleotide model in `NM_000518.5` reflects NCBI's 2018 refinement extending the 3' UTR by 2 adenines based on full-length cDNA clone `BU661647.1` (spanning bases 495–628).
3. The coding sequence (CDS, 444 bp, codons 1–147) and all exon splice junctions are **100% identical** between both versions. The 2-bp difference is restricted exclusively to the extreme 3' terminus of the non-coding 3' UTR.

---

## 5. Genomic Reference Audit: `NG_000007.3` (Coordinates 70545..72152)

We retrieved the corresponding genomic segment of NCBI RefSeqGene `NG_000007.3` (bases 70545 to 72152, total length 1608 bp) and evaluated its correspondence to `NM_000518.5`:

### 5.1 Bit-for-Bit Sequence Alignment
- Local `data/reference/NG_000007.3.fasta`: 1608 bp, SHA256 `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18`.
- Authoritative NCBI `NG_000007.3:70545..72152`: 1608 bp, SHA256 `6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18`.
- **Verdict:** **100% Bit-for-Bit Match.**

### 5.2 Exon Splicing & Intron Coordinate Verification
Slicing the genomic segments from `NG_000007.3`:
- **Exon 1:** Genomic 70545..70686 (142 bp) $\to$ matches `NM_000518.5` bases 1..142.
- **Intron 1 (IVS-1):** Genomic 70687..70816 (130 bp) $\to$ donor dinucleotide `GT`, acceptor dinucleotide `AG`.
- **Exon 2:** Genomic 70817..71039 (223 bp) $\to$ matches `NM_000518.5` bases 143..365.
- **Intron 2 (IVS-2):** Genomic 71040..71889 (850 bp) $\to$ donor dinucleotide `GT`, acceptor dinucleotide `AG`.
- **Exon 3:** Genomic 71890..72152 (263 bp) $\to$ matches `NM_000518.5` bases 366..628.

Concatenating Exon 1 + Exon 2 + Exon 3 from `NG_000007.3` produces exactly **628 bp**, identical to `NM_000518.5` across all bases. This confirms that `data/reference/NG_000007.3` is synchronized with `NM_000518.5`.

---

## 6. Audit Findings & Traceability Summary

1. **Local Accession & Checksum:**  
   `NM_000518.5` (628 bp), SHA256: `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3`.
2. **Authoritative Comparison Status:**  
   Completed via live NCBI E-Utilities Entrez query. Local sequence matches the authoritative NCBI RefSeq standard with zero discrepancies.
3. **Exon, CDS, and 3' UTR Verification:**  
   All boundaries (Exon 1: 142 bp; Exon 2: 223 bp; Exon 3: 263 bp; CDS: 51..494; 3' UTR: 495..628, 134 bp) match authoritative `NM_000518.5`.
4. **Additional Bases / Boundary Check:**  
   Local sequence has zero additional or missing bases relative to authoritative `NM_000518.5`. It differs from `NM_000518.4` by 2 terminal adenines added by NCBI in June 2018.
5. **Genomic `NG_000007.3` Synchronization:**  
   Genomic locus 70545..72152 (1608 bp) is bit-for-bit identical to NCBI RefSeqGene and matches `NM_000518.5` splicing with exact 130 bp Intron 1 and 850 bp Intron 2.
6. **Traceability of Historical 626 bp / 132 bp UTR Description:**  
   The historical 626 bp / 132 bp UTR description is **formally supported and verified by NCBI RefSeq predecessor `NM_000518.4`**.

---

## 7. Final Determination

```
================================================================================
FINAL AUDIT DETERMINATION:
VERIFIED AGAINST AUTHORITATIVE REFERENCE
================================================================================
```

The local reference sequence files `NM_000518.5` (628 nucleotides) and `NG_000007.3` (1608 nucleotides) are **authoritative, verified against NCBI RefSeq standards, and cryptographically sound**. The historical 626-nucleotide literature description is **fully explained and verified as RefSeq version `NM_000518.4`**. Zero discrepancies exist between the project's local reference sequences and authoritative NCBI RefSeq standards.
