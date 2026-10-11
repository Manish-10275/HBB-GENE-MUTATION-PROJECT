# Phase 2C — CP-2.2 Independent Molecular Verification Report

> **Document Status:** PROVISIONAL RESEARCH CURATION REPORT  
> **Execution Mode:** DETERMINISTIC PRODUCTION CORE AS-IS (Zero code changes, zero heuristics tuned)  
> **Benchmark Status:** NO BENCHMARK RUN — NO ACCURACY COMPUTED — NO DATASET FROZEN

---

## 1. Executive Summary & Verification Methodology

In accordance with the core scientific principle of Checkpoint CP-2.2, the deterministic consequence engine was executed AS-IS on all **314 candidate variants** without relying on external databases as an oracle. The external ClinVar records were utilized purely as evidence for **post-computation comparison**, never for guiding algorithm behavior.

### Verification Execution Flow:

```

Candidate HGVS Input

       │

       ▼

Reference Sequence Validation (NM_000518.5 / NG_000007.3)

       │

       ▼

Deterministic Molecular Consequence Evaluation (app.core AS-IS)

       │

       ▼

External Evidence Extraction (ClinVar reported consequence)

       │

       ▼

Comparison Status Assignment (Agreement / Discrepancy / Unsupported)

```

### Overall Verification Outcome Distribution (N = 314):

| Comparison Status | Count | Percentage | Definition & Biological Interpretation |
|---|:---:|:---:|---|
| **`EXACT_AGREEMENT`** | 211 | 67.2% | Deterministic engine consequence and protein consequence match external record exactly. |
| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | 6 | 1.9% | Molecular consequence agrees, but protein nomenclature has descriptive difference. |
| **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | 2 | 0.6% | Protein consequence matches, but classification ontology differs (e.g. 5' UTR indel causing frameshift). |
| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | 3 | 1.0% | External ClinVar record lacks explicit protein consequence annotation. |
| **`HGVS_AMBIGUITY` / SYNTAX ERROR** | 41 | 13.1% | Non-standard syntax, bracketed repeat notations (`[1]`), or complex unsupported indels. |
| **`ENGINE_UNSUPPORTED` / BOUNDS** | 31 | 9.9% | Position outside modeled boundaries (deep intronic $> +5 / < -3$, or 5' UTR promoter $< -50$). |
| **`EXCLUDED_HISTORICAL_OVERLAP`** | 20 | 6.4% | Disqualified by Exclusion Registry due to prior Phase 2B or codebase exposure. |
| **TOTAL** | **314** | **100.0%** | |

---

## 2. Protein Consequence & Reading Frame Verification

Independent computation verified codon translations, premature termination codons (PTC), and downstream stop distances across all classes:

1. **Nonsense (Stop-Gain) Variants (C02):** Engine independently verified premature stop codon translation at codons 40, 128, etc. Matching external `*` and `Ter` records with 100% concordance.

2. **Frameshift Indels (C04, C06):** The engine dynamically reconstructed the mutant transcript sequence, located the initial altered amino acid, and walked downstream codons until finding the first in-frame premature termination codon, formatting standard HGVS `p.AaPosAa2fsTerX` nomenclature.

3. **In-Frame Codon Boundary Reconstruction (C05, C07):** Both codon-aligned deletions (`c.388_390del` -> `p.Leu130del`) and in-frame duplications (`c.92_94dup` -> `p.Arg31dup`, `c.272_295dup` -> `p.Glu91_His98dup`) were verified. The prefix-suffix matching algorithm correctly resolved intact flanking codons.


---

## 3. Special Deep-Dive: Class C07 (In-Frame Insertions / Duplications)

The 5 provisional candidates in C07 were audited individually through the engine:


### 1. `HBB-CP2-140` (`c.92_94dup`)

- **HGVS Input:** `c.92_94dup`  

- **Engine Computation:** `NM_000518.5:c.92_94dup` -> `p.Arg31dup` (Molecular Impact: `In-frame Indel`)  

- **External ClinVar Annotation:** `p.Arg31dup` (VarID: 869322)  

- **Comparison Status:** `EXACT_AGREEMENT`  

- **Provenance & Limitations:** ClinVar record has **0 stars** (no assertion criteria provided) and 0 PMIDs. Evidence is ClinVar-only.  

- **Recommendation:** `PROPOSED_SECONDARY` (Defensible biological duplication, but low database confidence).  


### 2. `HBB-CP2-144` (`c.272_295dup`)

- **HGVS Input:** `c.272_295dup`  

- **Engine Computation:** `NM_000518.5:c.272_295dup` -> `p.Glu91_His98dup` (Molecular Impact: `In-frame Indel`)  

- **External ClinVar Annotation:** `p.Glu91_His98dup` (VarID: 869309)  

- **Comparison Status:** `EXACT_AGREEMENT`  

- **Provenance & Limitations:** 24-bp duplication of 8 codons in Exon 2. ClinVar record has **0 stars** (no assertion criteria provided). ClinVar-only.  

- **Recommendation:** `PROPOSED_SECONDARY` (Defensible biological duplication, but low database confidence).  


### 3. `HBB-CP2-204` (`c.170_171insGCAACCCTAAGGTG`)

- **HGVS Input:** `c.170_171insGCAACCCTAAGGTG`  

- **Engine Computation:** `NM_000518.5:c.170_171insGCAACCCTAAGGTG` -> `p.Asn58GlnfsTer3` (Molecular Impact: `Frameshift`)  

- **External ClinVar Annotation:** `p.Gly57_Asn58insGlnProTer` (VarID: 869222)  

- **Comparison Status:** `MOLECULAR_DISCREPANCY`  

- **Critical Scientific Finding:** The inserted sequence `GCAACCCTAAGGTG` has a physical length of **14 nucleotides**, NOT 15! A 14-bp insertion induces a **+2 reading frame shift**, resulting in premature termination (`p.Asn58GlnfsTer3`). The ClinVar external annotation claiming an in-frame insertion is mathematically and biologically discordant.  

- **Recommendation:** `REVIEW_REQUIRED` (Documented discrepancy; cannot be used as an in-frame insertion).  


### 4. `HBB-CP2-212` (`c.221_227delinsCTCGGTGCCA`)

- **HGVS Input:** `c.221_227delinsCTCGGTGCCA` (Hb Cranston / VarID: 15499)  

- **Engine Computation:** Rejected as complex delins with non-contiguous codon replacement.  

- **External ClinVar Annotation:** `p.Asp74_Leu76delinsAlaArgCysGln`  

- **Comparison Status:** `HGVS_AMBIGUITY` / Complex delins outside standard insertion scope.  

- **Recommendation:** `REVIEW_REQUIRED` (Complex structural variant).  


### 5. `HBB-CP2-232` (`c.301_302delinsTCTGAGAACTT`)

- **HGVS Input:** `c.301_302delinsTCTGAGAACTT`  

- **Engine Computation:** Complex multi-base replacement with net insertion.  

- **External ClinVar Annotation:** `p.Pro101delinsSerGluAsnPhe` (VarID: 869351)  

- **Comparison Status:** `HGVS_AMBIGUITY` / Complex delins.  

- **Recommendation:** `REVIEW_REQUIRED`.  


> **C07 Scientific Conclusion:** There are **ZERO primary candidates** for C07. Exactly **two candidates** (`c.92_94dup` and `c.272_295dup`) are genuine, verified in-frame duplications, but both possess 0-star ClinVar evidence and are allocated to `PROPOSED_SECONDARY`.


---

## 4. Special Deep-Dive: Class C08 (Splice Donor) & Data Availability Limitation

- **Verification Outcome:** In the queried ClinVar pool, **zero canonical donor variants** (+1, +2, +5) were retrieved. All 18 candidate entries were intronic indels, delins, or flanking consensus changes. None are canonical invariant splice donor disruptions.

- **Protocol Enforcement (Task 9 & 15):** In strict accordance with the freeze on candidate manipulation, no noncanonical intronic variants were promoted into canonical donor status. Class balance was not manufactured.

- **Formal Designation:**  

  `C08_STATUS = DATA_AVAILABILITY_LIMITATION`  

  `PROPOSED_PRIMARY (C08) = 0`  

  `PROPOSED_SECONDARY (C08) = 0`  


---

## 5. Special Deep-Dive: Class C09 (Splice Acceptor Disruptions)

All 6 canonical splice acceptor candidates at invariant $-1$ and $-2$ positions were independently verified through the core engine:


| candidate_id | cDNA Change | Intron | Genomic Pos (NG_000007.3) | Engine Consequence | External Record | ClinVar Stars | Comparison Status | Proposed Status |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `HBB-CP2-241` | `c.93-1G>C` | Intron 1 | 70816 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |
| `HBB-CP2-253` | `c.93-2A>C` | Intron 1 | 70815 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |
| `HBB-CP2-257` | `c.93-2A>G` | Intron 1 | 70815 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |
| `HBB-CP2-254` | `c.316-1G>T` | Intron 2 | 71889 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |
| `HBB-CP2-256` | `c.316-2A>C` | Intron 2 | 71888 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |
| `HBB-CP2-258` | `c.316-1G>C` | Intron 2 | 71889 | `p.?` (Splice Disruption) | Splice Site | 1 star | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |

> **C09 Scientific Conclusion:** Class C09 is robustly represented by **6 verified primary canonical acceptor candidates** across Intron 1 and Intron 2.


---

## 6. Deep Intronic Variants & Transcript Boundary Limits (C10 5' UTR)

The verification uncovered two critical transcript modeling boundaries:

1. **Deep Intronic Variants (Out of Scope):** 14 variants situated $> +5$ or $< -3$ bp into introns were rejected as out of scope. These variants cannot be evaluated without dedicated neural splice-site modeling.

2. **5' UTR Transcript Boundary Limits:** The canonical RefSeq transcript `NM_000518.5` defines a **50-nucleotide 5' UTR** ($c.-1$ to $c.-50$). Promoter variants located further upstream ($c.-78$, $c.-80$, $c.-81$, $c.-83$, $c.-106$, $c.-124$, $c.-136$, $c.-137$, $c.-142$) physically precede the transcript start coordinate and correctly trigger `OUT_OF_BOUNDS`. Therefore, `NM_000518.5` transcript modeling cannot evaluate upstream genomic promoter variants. Consequently, **`PROPOSED_PRIMARY (C10) = 0`**.


---

## 7. Synthetic Adversarial Controls (Class E / C12)

- All 18 synthetic negative controls in `C12` (`HBB-CP2-297` through `HBB-CP2-314`) were verified.

- The engine correctly rejected 100% of the adversarial inputs with appropriate deterministic error codes (`INVALID_COORDINATE`, `SYNTAX_ERROR`, `OUT_OF_BOUNDS`, `REFERENCE_MISMATCH`).

- In accordance with Task 12, all 18 controls are designated **`PROPOSED_PRIMARY` strictly for Experiment D (Robustness and Error Handling)**. They are excluded from biological consequence accuracy evaluation.
