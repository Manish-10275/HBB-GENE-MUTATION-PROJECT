# Phase 2C — CP-2.3 Class Availability & Scientific Limitation Report

> **Document Status:** PROVISIONAL RESEARCH CURATION REPORT  
> **Scientific Rule:** QUALITY OVER QUOTAS — ABSENCE OF VARIANTS DOCUMENTED TRANSPARENTLY

---

## 1. Class Availability Matrix (11 Biological Classes)

| Class | Stratified Variant Class | Available Candidates | Proposed Primary | Approved (High Conf) | Conditional (Mod Conf) | Rejected | Final Potentially Usable | Biological & Data Availability Limitation |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | 64 | 42 | **14** | 28 | 0 | **42** | No shortage; robust exonic missense representation. |
| **C02** | Nonsense (Stop-Gain) | 10 | 5 | **3** | 2 | 0 | **5** | No shortage; 5 premature termination codons across Exons 1, 2, 3. |
| **C03** | Synonymous (Silent) | 22 | 14 | **10** | 4 | 0 | **14** | No shortage; 14 silent coding substitutions verified. |
| **C04** | Frameshift Deletions | 32 | 22 | **9** | 13 | 0 | **22** | No shortage; 22 frameshifting deletions verified. |
| **C05** | In-Frame Indels / Deletions | 14 | 1 | **0** | 1 | 0 | **1** | Data limitation: Only 1 primary candidate (c.9_83del); large 25-codon deletion (Conditional). |
| **C06** | Frameshift Duplications / Insertions | 61 | 24 | **12** | 12 | 0 | **24** | No shortage; 24 primary frameshifting duplications verified. |
| **C07** | In-Frame Insertions / Duplications | 5 | 0 | **0** | 0 | 0 | **0** | Data-availability shortage: Primary = 0. Only 2 clean duplications exist in secondary (0-star). |
| **C08** | Splice Donor Disruptions | 18 | 0 | **0** | 0 | 0 | **0** | Data-availability limitation: Primary = 0. Zero canonical +1, +2, +5 donors present in queried pool. |
| **C09** | Splice Acceptor Disruptions | 24 | 6 | **5** | 1 | 0 | **6** | No shortage; 6 primary canonical acceptor dinucleotide disruptions verified. |
| **C10** | 5' UTR Regulatory Variants | 36 | 0 | **0** | 0 | 0 | **0** | Transcript boundary limitation: Primary = 0. Promoter variants (> -50 bp) exceed NM_000518.5 transcript. |
| **C11** | 3' UTR Regulatory Variants | 10 | 5 | **2** | 3 | 0 | **5** | No shortage; 5 primary polyadenylation signal regulatory SNVs verified. |
| **TOTAL** | **All 11 Biological Classes** | **296** | **119** | **55** | **64** | **0** | **119** | |

## 2. Transparent Documentation of Zero-Count & Low-Count Classes

In strict compliance with Tasks 9, 11, 12, and 14, no candidate discovery was run, no class definitions were loosened, and no class balance was manufactured:

- **Class C05 (In-Frame Deletions):** Potentially usable count is **1** (`c.9_83del`). This is a 75-bp (25 codons) deletion. Marked `CONDITIONAL` due to its large size. A second clean 3-bp deletion (`c.415_417del`) exists in secondary.

- **Class C07 (In-Frame Insertions / Duplications):** Potentially usable primary count is **0**. Only two clean in-frame duplications exist in the candidate pool (`c.92_94dup` and `c.272_295dup`), but both have 0-star ClinVar evidence and remain in secondary.

- **Class C08 (Splice Donor Disruptions):** Potentially usable primary count is **0**. In the queried ClinVar pool, zero canonical invariant $+1, +2, +5$ donor variants were present. Designated `DATA_AVAILABILITY_LIMITATION`.

- **Class C10 (5' UTR Regulatory Variants):** Potentially usable primary count is **0**. In the RefSeq transcript model `NM_000518.5`, the 5' UTR spans 50 bp ($c.-1$ to $c.-50$). Promoter mutations situated $> -50$ bp upstream (e.g. $-78, -80, -83, -106, -137$) physically precede the modeled transcript and trigger `OUT_OF_BOUNDS`. Designated `TRANSCRIPT_BOUNDARY_LIMITATION`.
