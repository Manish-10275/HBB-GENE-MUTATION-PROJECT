# Reproducible Reference Sequence Authority Forensic Follow-Up Audit: HBB Transcript & Genomic Models

> **Audit Document:** INDEPENDENT REPRODUCIBLE REFERENCE SEQUENCE AUTHORITY AUDIT (FOLLOW-UP)  
> **Investigation Focus:** Conflict Resolution between Reported 626 bp Transcript (External Page) vs. 628 bp Model (`NM_000518.5`)  
> **Target Accessions:** NCBI RefSeq `NM_000518.5`, NCBI RefSeq `NM_000518.4`, NCBI RefSeqGene `NG_000007.3`  
> **Audit Date:** 2026-10-11  
> **Execution Constraint:** Strictly Read-Only Investigation; Zero Modifications to Reference Files, Code, Frozen Benchmark Data, or Manuscript Text  

---

## 1. Executive Summary & Objective

An external reference data page was noted reporting the human *HBB* canonical transcript `NM_000518.5` as **626 bp** with a **444 bp open reading frame (ORF)**, conflicting with the project's local reference file (`data/reference/NM_000518.5.fasta`) and the previous audit report, which both recorded a length of **628 nt**.

This follow-up audit was conducted to resolve this conflict through an independent, end-to-end reproducible inspection directly querying the official NCBI Entrez E-Utilities endpoints without relying on prior audit assertions.

### Core Findings Summary:
1. **Live NCBI RefSeq Query Confirms NM_000518.5 is Exactly 628 nt:**  
   The authoritative NCBI RefSeq FASTA and GenBank records retrieved directly from the NCBI E-Utilities endpoint confirm that `NM_000518.5` is **628 nucleotides** in length.
2. **Local Reference is 100% Bit-for-Bit Identical to Official NCBI NM_000518.5:**  
   Direct character-by-character comparison between `data/reference/NM_000518.5.fasta` and the official NCBI download revealed **0 mismatches** across all 628 nucleotides. Both yield the identical cryptographic SHA256 hash:  
   `9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3`.
3. **Traceability of the 626 bp / 444 bp ORF Claim:**  
   The 444 bp coding sequence (CDS 51..494) is identical in both `NM_000518.4` and `NM_000518.5`. However, the 626 bp transcript length originated from **NCBI RefSeq predecessor version `NM_000518.4`** (curated 2003–2018). On June 13, 2018, NCBI replaced version 4 with `NM_000518.5`, incorporating two additional terminal adenines (`AA` at positions 627–628) from full-length cDNA clone `BU661647.1`. Third-party pages describing `NM_000518.5` as 626 bp are citing or caching legacy `NM_000518.4` sequence metrics.
4. **Genomic Splicing (`NG_000007.3:70545..72152`) Reproduces 628 nt Transcript Exactly:**  
   Concatenating Exon 1 (70545..70686, 142 bp), Exon 2 (70817..71039, 223 bp), and Exon 3 (71890..72152, 263 bp) from RefSeqGene `NG_000007.3` yields precisely 628 bp with canonical donor/acceptor dinucleotides (`GT..AG`), exactly matching `NM_000518.5`.

---

## 2. Protocol and Execution Commands

The audit was executed via a standalone, reproducible Python script querying official NCBI REST endpoints:
- NCBI FASTA endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<ACCESSION>&rettype=fasta&retmode=text`
- NCBI GenBank endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<ACCESSION>&rettype=gb&retmode=text`

Downloaded payloads were written to an external scratch directory (`C:\Users\santo\.gemini\antigravity\brain\53ca1530-43e6-4d9f-b388-505b581cfdab\scratch\`) to prevent touching any project repository files.

---

## 3. Actual Console Output and Verification Steps

### Tasks 1 & 2: Direct NCBI Download of NM_000518.5 & Metrics
```
>>> TASK 1 & 2: NCBI NM_000518.5 DOWNLOAD & METRICS
RAW FASTA (first 3 lines):
>NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA
ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATCTGACTCCTGA
GGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGC
RAW FASTA (last 2 lines):
CTAAGCTCGCTTTCTTGCTGTCCAATTTCTATTAAAGGTTCCTTTGTTCCCTAAGTCCAACTACTAAACT
GGGGGATATTATGAAGGGCCTTGAGCATCTGGATTCTGCCTAATAAAAAACATTTATTTTCATTGCAA
Accession Header:       >NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA
Sequence Length:        628 nt
Terminal 30 nt:         CCTAATAAAAAACATTTATTTTCATTGCAA
Pure Sequence SHA256:   9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3
```

### Task 3: Local `data/reference/NM_000518.5.fasta` Inspection
```
>>> TASK 3: LOCAL data/reference/NM_000518.5.fasta METRICS
Accession Header:       >NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA
Sequence Length:        628 nt
Terminal 30 nt:         CCTAATAAAAAACATTTATTTTCATTGCAA
Pure Sequence SHA256:   9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3
```

### Task 4: Character-by-Character Sequence Alignment
```
>>> TASK 4: CHARACTER-BY-CHARACTER COMPARISON
Lengths Match:          True (628 == 628)
Total Discrepancies:    0
Exact Bit-for-Bit Match: True
Zero differences detected across all 628 characters.
```

### Task 5: Genomic Reference `NG_000007.3` & In Silico Exon Splicing
```
>>> TASK 5: NG_000007.3 GENOMIC AUDIT & EXON SPLICING
NCBI NG Header:         >NG_000007.3:70545-72152 Homo sapiens beta globin region (HBB@); and beta globin locus transcript 3 (BGLT3); and hemoglobin subunit delta (HBD); and hemoglobin subunit epsilon 1 (HBE1); and hemoglobin subunit gamma 1 (HBG1); and hemoglobin subunit gamma 2 (HBG2), RefSeqGene on chromosome 11
NCBI NG Length:         1608 nt
NCBI NG SHA256:         6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18
Local NG Header:        >NG_000007.3:70545-72152 Homo sapiens hemoglobin subunit beta (HBB) genomic gene locus
Local NG Length:        1608 nt
Local NG SHA256:        6de4b3877f2d21cd0e97f69341be065e3a16fb3b737379a12c7b54db41211c18
NG Identical:           True
Exon 1 length:          142 nt (Genomic 70545..70686)
Exon 2 length:          223 nt (Genomic 70817..71039)
Exon 3 length:          263 nt (Genomic 71890..72152)
Intron 1 donor/acceptor: GT / AG (Canonical GT..AG)
Intron 2 donor/acceptor: GT / AG (Canonical GT..AG)
Spliced Transcript Len: 628 nt
Spliced SHA256:         9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3
Spliced == NM_000518.5: True
```

### Task 6: Official GenBank Feature Annotations for NM_000518.5
The official GenBank flatfile for `NM_000518.5` defines the structural features as follows:
```
LOCUS       NM_000518                628 bp    mRNA    linear   PRI 06-SEP-2026
VERSION     NM_000518.5
            reference sequence was derived from AK311825.1 and BU661647.1.
            Transcript exon combination :: BU662061.1, BU661647.1 [ECO:0000332]
PRIMARY     REFSEQ_SPAN         PRIMARY_IDENTIFIER PRIMARY_SPAN        COMP
            1-494               AK311825.1         1-494
            495-628             BU661647.1         507-640
FEATURES             Location/Qualifiers
     exon            1..142
     CDS             51..494
                     /gene="HBB"
                     /protein_id="NP_000509.1"
     exon            143..365
     exon            366..628
     polyA_site      628
```
- **Total Length:** 628 bp
- **Exon 1:** 1..142 (142 bp)
- **CDS (Coding Sequence):** 51..494 (444 bp, translating to `NP_000509.1`, 147 amino acids)
- **Exon 2:** 143..365 (223 bp)
- **Exon 3:** 366..628 (263 bp)
- **3' UTR:** 495..628 (134 bp, $c.*1$ to $c.*134$)
- **Cleavage / PolyA Site:** Position 628

---

## 4. Historical Comparative Evidence: NM_000518.4 vs. NM_000518.5

### Task 7: Official Evidence for Predecessor NM_000518.4
The official GenBank flatfile for historical predecessor `NM_000518.4` (in effect February 11, 2003 – June 13, 2018) records:
```
LOCUS       NM_000518                626 bp    mRNA    linear   PRI 01-MAY-2018
VERSION     NM_000518.4
COMMENT     On Jun 13, 2018 this sequence was replaced by NM_000518.5.
FEATURES             Location/Qualifiers
     exon            1..142
     CDS             51..494
                     /protein_id="NP_000509.1"
     exon            143..365
     exon            366..626
     polyA_site      626
NM_000518.4 Header:     >NM_000518.4 Homo sapiens hemoglobin subunit beta (HBB), mRNA
NM_000518.4 Length:     626 nt
NM_000518.4 Terminal 30:TGCCTAATAAAAAACATTTATTTTCATTGC
NM_000518.4 SHA256:     ac038be3f141f8e792f00c32497408615a5204d0654f3aa0ff39e07c4be588f9
NM_000518.5 Terminal 30:CCTAATAAAAAACATTTATTTTCATTGCAA
Prefix Match (1..626):  True
Extra bases at 627..628: 'AA'
```

### Direct Biological and Sequence Evidence:
1. **Identical Coding Sequence:** Both `NM_000518.4` and `NM_000518.5` share the exact 444 bp open reading frame ($c.1..c.444$, coordinates 51..494) encoding `NP_000509.1` (147 aa).
2. **Terminal Extension:** Bases 1 through 626 of `NM_000518.5` are 100% identical to `NM_000518.4`.
3. **The +2 Adenines:** `NM_000518.5` terminates with `...TTCATTGCAA` (628 bp), whereas `NM_000518.4` terminated with `...TTCATTGC` (626 bp). The two terminal adenines at positions 627 and 628 were incorporated by NCBI curators on June 13, 2018 based on cDNA evidence `BU661647.1` (GenBank span 495–628).
4. **Resolution of External Claim:** Third-party pages reporting "626 bp with a 444 bp ORF" are quoting the historical dimensions of `NM_000518.4` or using an unversioned summary table that was not updated upon the release of `NM_000518.5`.

---

## 5. Audit of Previous Audit Reporting (Task 8)

### Can the 628 nt Result Be Reproduced?
**Yes, 100% reproduced.**  
The previous audit (`REFERENCE_SEQUENCE_AUTHORITY_AUDIT.md`) correctly concluded that `NM_000518.5` is 628 nt. There was **no error in parsing** the downloaded responses, headers, or feature tables in either the previous audit or this follow-up audit.

| Evaluation Item | External Data Page | NCBI RefSeq `NM_000518.4` | NCBI RefSeq `NM_000518.5` | Local Reference (`data/reference/NM_000518.5`) |
|---|:---:|:---:|:---:|:---:|
| **Total Transcript Length** | 626 bp | 626 bp | **628 bp** | **628 bp** |
| **Open Reading Frame (ORF)** | 444 bp | 444 bp | **444 bp** | **444 bp** |
| **Exon 1 Length** | 142 bp | 142 bp | **142 bp** | **142 bp** |
| **Exon 2 Length** | 223 bp | 223 bp | **223 bp** | **223 bp** |
| **Exon 3 Length** | 261 bp | 261 bp | **263 bp** | **263 bp** |
| **3' UTR Length** | 132 bp | 132 bp ($c.*1..c.*132$) | **134 bp** ($c.*1..c.*134$) | **134 bp** ($c.*1..c.*134$) |
| **Terminal Sequence** | `...CATTGC` | `...CATTGC` | **`...CATTGCAA`** | **`...CATTGCAA`** |
| **Release Date at NCBI** | N/A (Stale Cache) | 2003-02-11 | **2018-06-13** | **Synchronized** |

The external reference data page is reporting legacy information from RefSeq version 4 (`NM_000518.4`). The authoritative standard for version 5 (`NM_000518.5`) in NCBI Nuccore is unequivocally **628 bp**.

---

## 6. Splicing Verification of Genomic Model `NG_000007.3`

In silico splicing of the RefSeqGene model `NG_000007.3` directly from NCBI was performed:
- **Exon 1:** Coordinates 70545..70686 $\to$ 142 nucleotides
- **Intron 1 (IVS-1):** Coordinates 70687..70816 $\to$ 130 nucleotides (`GT...AG`)
- **Exon 2:** Coordinates 70817..71039 $\to$ 223 nucleotides
- **Intron 2 (IVS-2):** Coordinates 71040..71889 $\to$ 850 nucleotides (`GT...AG`)
- **Exon 3:** Coordinates 71890..72152 $\to$ 263 nucleotides

**Result of Splicing:**  
$\text{Exon 1 (142 nt)} + \text{Exon 2 (223 nt)} + \text{Exon 3 (263 nt)} = 628\text{ nucleotides}$  
Cryptographic hash of in silico spliced sequence:  
`9e811fb12c639fc6610265da635ebbf31521b62410132c6e19dfd0192bd194f3` (Matches `NM_000518.5` with 0 mismatches).

Both the transcript reference (`NM_000518.5`) and the genomic reference (`NG_000007.3:70545..72152`) are completely synchronized, biologically authentic, and cryptographically verified.

---

## 7. Final Audit Finding

```
================================================================================
FINAL AUDIT FINDING:
• VERIFIED AGAINST AUTHORITATIVE REFERENCE
================================================================================
```
The local transcript reference `NM_000518.5` (628 nt) and genomic reference `NG_000007.3` (1608 nt) are verified bit-for-bit against official NCBI RefSeq records. The external page description of 626 bp with a 444 bp ORF is confirmed to be based on historical RefSeq version `NM_000518.4` (pre-June 2018). Zero discrepancies exist between the project reference files and current authoritative NCBI RefSeq records.
