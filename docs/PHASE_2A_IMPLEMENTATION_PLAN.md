# PHASE 2A IMPLEMENTATION PLAN
## Structured HGVS Precision Upgrade & Indel Consequence Engine
**Project:** HBB Gene Mutation Analyzer  
**Component:** Variant Interpretation, Direct HGVS Parser, & Protein Consequence Subsystem  
**Baseline Status:** Phase 1 Frozen Baseline (78/78 Tests Passing, 18/18 Doctor Checks Passed)  
**Document Classification:** Engineering Architecture & Implementation Blueprint (Pre-Implementation)  
**Date:** 2026-10-06  

---

## 1. EXECUTIVE SUMMARY

The **HBB Gene Mutation Analyzer** Phase 1 baseline established a robust, local-first bioinformatics engine capable of deterministic sequence alignment against `NM_000518.5` and `NG_000007.3`, automated ClinVar retrieval with candidate scoring, and strictly grounded AI narrative synthesis.

However, an exhaustive audit of the Phase 1 variant interpretation engine reveals a significant architectural bottleneck:
- **The Direct Variant Search subsystem ([`parse_hgvs_input`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L343)) is strictly hardcoded to single-nucleotide substitutions (`c.[pos][Ref]>[Alt]`).** Entering any deletion, insertion, duplication, range variant, or splice-site coordinate (such as the high-prevalence Indian thalassemia mutations `c.126_129del`, `c.27dup`, or `c.315+1G>A`) results in immediate parsing rejection (`Unsupported HGVS syntax`).
- **Downstream Term Reconstruction Defect:** In [`backend/app/main.py#L394`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/main.py#L394), the API layer reconstructs the database query term using `f"c.{variant_model.c_position}{variant_model.ref_allele}>{variant_model.alt_allele}"`, an expression that fundamentally assumes substitutions and corrupts non-substitution variant representations.
- **Consequence Engine Placeholders:** While the sequence-based pairwise aligner ([`detect_variants`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L134)) detects indels from raw FASTA input, its protein consequence evaluation assigns static placeholder strings (e.g., `p.({c_pos}del_fs)` or `p.({c_pos}del)`), completely lacking dynamic reading frame tracking, altered amino acid identification, and downstream premature termination codon (PTC) calculations.

**Phase 2A Objective:** Upgrade the variant interpretation engine from an SNV-oriented parser into a comprehensive, structured HGVS interpretation engine supporting substitutions, deletions, duplications, insertions, splice-site donor SNVs, dynamic downstream frameshift translation, and in-frame indel residue deltas, while maintaining 100% backward compatibility with all Phase 1 baseline tests and benchmarks.

---

## 2. CURRENT HGVS PARSER ARCHITECTURE

### 2.1 Function Specification
- **Function Name:** `parse_hgvs_input(raw_query: str, ref_data: ReferenceData) -> Tuple[Optional[DetectedVariant], Optional[str]]`
- **Location:** [`backend/app/variants.py#L343-L421`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L343-L421)

### 2.2 Accepted vs Rejected Syntax
```
Current Parser Syntax Filter
├── Step 1: Strip optional accession prefix (e.g., "NM_000518.5:c.118C>T" -> "c.118C>T")
├── Step 2: Auto-prefix check: r"^(\*?-?\d+)[A-Z]>[A-Z]$" -> prepends "c."
└── Step 3: Strict substitution regex:
            r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$"
```

| Variant Representation | Query Example | Current Parser Behavior | Classification |
| :--- | :--- | :--- | :--- |
| **Canonical Coding SNV** | `c.118C>T` | Accepted $\to$ `p.Gln40Ter` | **SUPPORTED** |
| **5' UTR SNV** | `c.-5A>G` | Accepted $\to$ `Non-coding` | **SUPPORTED** |
| **3' UTR SNV** | `c.*10T>C` | Accepted $\to$ `Non-coding` | **SUPPORTED** |
| **Single Base Deletion** | `c.9delT` / `c.9del` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |
| **Multi-Base Range Deletion** | `c.126_129del` / `c.126_129delCTTT` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |
| **Duplication** | `c.27dup` / `c.27dupG` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |
| **Flanked Insertion** | `c.27_28insG` / `c.117_118insA` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |
| **Splice Donor SNV** | `c.315+1G>A` / `c.92+5G>C` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |
| **Delins** | `c.118_119delinsTT` | Rejected $\to$ `Unsupported HGVS syntax` | **UNSUPPORTED** |

### 2.3 End-to-End Execution Flow
```
User Input (DirectVariantSearch.tsx)
  │
  ▼
GET /variant/search?query=... (main.py:375)
  │
  ▼
parse_hgvs_input(query, ref_data) (variants.py:343)
  ├── Parses regex r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$"
  ├── Validates reference base: ref_data.sequence[mrna_pos - 1] == ref_base
  └── Computes consequence via evaluate_substitution_codon_consequence()
  │
  ▼
clean_term Reconstruction (main.py:394)
  │ [CRITICAL SNV ASSUMPTION: clean_term = f"c.{c_pos}{ref}>{alt}"]
  ▼
NCBI Query Dispatch
  ├── fetch_clinvar_records(clean_term, transcript, aliases, protein) (clinvar.py:261)
  └── fetch_pubmed_records(clean_term, aliases) (pubmed.py)
  │
  ▼
VariantSearchResponse JSON (main.py:408)
  │
  ▼
Frontend Display (DirectVariantSearch.tsx)
```

### 2.4 Hardcoded SNV Assumptions in Downstream Code
1. [`backend/app/variants.py#L366`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L366): Regex requires single character Ref `[A-Za-z]` and Alt `[A-Za-z]`.
2. [`backend/app/variants.py#L400`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L400): Standard HGVS formatted strictly as `{ref_data.accession}:c.{c_pos_str}{ref_base}>{alt_base}`.
3. [`backend/app/variants.py#L405`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L405): Hardcodes `variant_type="substitution"`.
4. [`backend/app/main.py#L394`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/main.py#L394): Reconstructs search term assuming `ref_allele>alt_allele`. If an indel variant enters, it creates corrupted queries like `c.126_129CTTT>-` or `c.27dupG>-`.
5. [`backend/app/consequences.py`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/consequences.py): Only implements `evaluate_substitution_codon_consequence`; zero indel consequence evaluation logic exists.

---

## 3. CURRENT VARIANT REPRESENTATION

Variants are represented across the platform by the `DetectedVariant` Pydantic model:
```python
# backend/app/models.py
class DetectedVariant(BaseModel):
    id: str
    variant_type: str  # "substitution", "insertion", "deletion", "duplication"
    ref_position_mrna: int  # 1-based mRNA index
    c_position: str  # e.g., "118", "-5", "*12", "126_129", "27"
    ref_allele: str
    alt_allele: str
    hgvs_c: str
    hgvs_p: Optional[str] = None
    codon_change: Optional[CodonChange] = None
    functional_impact: str
    confidence: str = "Deterministic"
    equivalent_nomenclature: List[str] = Field(default_factory=list)
    nomenclature_notes: Optional[str] = None
```

### Limitations of `DetectedVariant` for Non-SNV Classes
- **Scalar mRNA Position:** `ref_position_mrna: int` represents a single point coordinate. For a range deletion (e.g., `c.126_129del`), it captures only the start coordinate.
- **Intronic Coordinate Incompatibility:** For splice variants (e.g., `c.315+1G>A`), there is NO corresponding nucleotide in mRNA transcript `NM_000518.5`. Assigning `ref_position_mrna` for an intronic variant is bioinformatically invalid.
- **CodonChange Model Rigidity:** `CodonChange` is strictly designed for a single codon replacement (`ref_codon: str` [3 nt], `sample_codon: str` [3 nt], `codon_number: int`). It cannot represent a frameshift walk or multi-codon deletion.

---

## 4. CURRENT CONSEQUENCE ENGINE

### 4.1 Substitutions
Evaluated by `evaluate_substitution_codon_consequence()` in [`backend/app/consequences.py#L41-L124`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/consequences.py#L41-L124):
- Accurately identifies codon number, wildtype triplet, mutated triplet, amino acid transformation, stop gain (`is_stop_gain`), stop loss (`is_stop_loss`), and synonymous status.
- Generates standard HGVS protein notation (e.g., `p.Gln40Ter`, `p.Glu7Val`, `p.(=)`).

### 4.2 Sequence-Based Indels
In [`backend/app/variants.py`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py):
- **Deletions (Lines 248-250):**
  ```python
  impact = "In-frame Deletion" if del_len % 3 == 0 else "Frameshift Deletion"
  hgvs_p = f"p.({c_start_str}del_fs)" if del_len % 3 != 0 else f"p.({c_start_str}del)"
  ```
- **Insertions & Duplications (Lines 314-316):**
  ```python
  impact = "Frameshift Insertion" if ins_len % 3 != 0 else "In-frame Insertion"
  hgvs_p = f"p.({c_left_str}ins_fs)" if ins_len % 3 != 0 else f"p.({c_left_str}ins)"
  ```
- **Origin of Placeholders:** Both `hgvs_p` constructions are literal placeholder strings (`p.(126del_fs)`, `p.(27ins_fs)`). Neither dynamic codon translation nor downstream termination codon searching is performed.

---

## 5. CURRENT COORDINATE SYSTEM

### 5.1 Dual-Reference Specification
1. **cDNA Transcript `NM_000518.5` (628 bp):**
   - 5' UTR: mRNA 1..50 $\to$ `c.-50` .. `c.-1`
   - CDS: mRNA 51..494 $\to$ `c.1` .. `c.444` (Codons 1..148, including `TAA` stop)
   - 3' UTR: mRNA 495..628 $\to$ `c.*1` .. `c.*134`
   - *Introns: Zero intronic bases present in mRNA sequence.*
2. **Genomic RefSeqGene Segment `NG_000007.3` (1,608 bp):**
   - Spans genomic coordinates `70545..72152`.
   - Exon 1: Relative 1..142 (Genomic 70545..70686) $\to$ `c.-50` .. `c.92`
   - Intron 1: Relative 143..272 (Genomic 70687..70816, 130 bp) $\to$ `c.92+1` .. `c.92+130`
   - Exon 2: Relative 273..495 (Genomic 70817..71039, 223 bp) $\to$ `c.93` .. `c.315`
   - Intron 2: Relative 496..1345 (Genomic 71040..71889, 850 bp) $\to$ `c.315+1` .. `c.315+850`
   - Exon 3: Relative 1346..1608 (Genomic 71890..72152, 263 bp) $\to$ `c.316` .. `c.*134`

### 5.2 Splicing & Coordinate Gaps
- `ReferenceData.c_pos_to_mrna_pos()` in [`backend/app/reference.py#L62`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/reference.py#L62) calls `int(c_str)`. Passing `"315+1"` or `"92+5"` raises `ValueError` and returns `None`.
- Forward genomic-to-cDNA intronic mapping exists in `_map_genomic_to_cdna_pos()` ([`variants.py#L10`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/variants.py#L10)), but **the inverse mapping (cDNA intronic coordinate $\to$ genomic sequence base) is completely missing.**

---

## 6. CURRENT CLINVAR INTEGRATION

The ClinVar retrieval subsystem in [`backend/app/clinvar.py`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/clinvar.py) already includes robust foundational support for indel queries:
- **Canonical Equivalents Mapping:** Lines 59–65 map `c.126_129del` $\leftrightarrow$ `c.124_127del` and `c.27dup` $\leftrightarrow$ `c.26_27insG`.
- **Indel Title Pattern Matching:** Line 209 uses regex `(?::|\b){escaped}(?:[A-Za-z]+)?(?:\s|\(|$)` specifically to match deletions and duplications with or without trailing nucleotide strings.
- **Hardened Progressive Search:** Tiers 1–5 retrieve up to 50 candidates and verify coordinates, alleles, and protein consequences without candidate window truncation.

**Why Indel Direct Search Fails Today:** The failure is purely in the pre-retrieval layer:
1. `parse_hgvs_input` rejects the syntax before ClinVar is ever called.
2. If `parse_hgvs_input` is bypassed, `main.py#L394` mangles the query term into `c.126_129CTTT>-`, which fails ClinVar Entrez search.

---

## 7. PHASE 2A REQUIREMENTS

```
Phase 2A Scope Hierarchy
├── 1. Direct HGVS Parser Expansion
│   ├── Substitutions: c.118C>T, c.20A>T, c.-5A>G, c.*10T>C
│   ├── Deletions: c.9delT, c.9del, c.126_129del, c.126_129delCTTT
│   ├── Duplications: c.27dup, c.27dupG, c.20_23dup
│   ├── Flanked Insertions: c.27_28insG, c.117_118insA
│   └── Splice Donor SNVs: c.315+1G>A, c.92+5G>C
├── 2. Consequence Engine Precision Upgrade
│   ├── Dynamic Frameshift Translation (downstream reading frame walk to PTC)
│   ├── In-frame Indel Translation (amino acid deltas and reconstituted codons)
│   └── Splice Variant Phenotypic Safety (explicit p.? unverified annotation)
└── 3. API & Coordinate Hardening
    ├── Fix main.py:394 query term reconstruction
    └── Bidirectional genomic coordinate mapping for intronic splice sites
```

---

## 8. PROPOSED NORMALIZED VARIANT MODEL

To eliminate the assumption that all variants are single-base substitutions, Phase 2A introduces a typed, intermediate representation:

```python
# Proposed: backend/app/hgvs_parser.py
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class VariantOperation(str, Enum):
    SUBSTITUTION = "substitution"
    DELETION = "deletion"
    DUPLICATION = "duplication"
    INSERTION = "insertion"
    DELINS = "delins"
    SPLICE_SUBSTITUTION = "splice_substitution"

class CoordinateSystem(str, Enum):
    CDNA_CODING = "cDNA_coding"
    CDNA_5_UTR = "cDNA_5_utr"
    CDNA_3_UTR = "cDNA_3_utr"
    CDNA_INTRONIC = "cDNA_intronic"
    GENOMIC = "genomic"

class ValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNSUPPORTED = "UNSUPPORTED"
    AMBIGUOUS = "AMBIGUOUS"

class ParsedHGVSVariant(BaseModel):
    raw_query: str
    transcript_accession: str = "NM_000518.5"
    operation: VariantOperation
    coordinate_system: CoordinateSystem
    start_pos: int
    end_pos: int
    intronic_offset: Optional[int] = None      # e.g., +1, +5, -2
    intronic_anchor_exon: Optional[int] = None # Exon boundary coordinate
    ref_allele: Optional[str] = None           # Expected sequence from reference
    alt_allele: Optional[str] = None           # Inserted / alternate sequence
    standard_hgvs_c: str                       # Canonical 3'-shifted HGVS string
    validation_status: ValidationStatus
    validation_error: Optional[str] = None
```

### Backward Compatibility Mapping to `DetectedVariant`
When adapting `ParsedHGVSVariant` into `DetectedVariant`:
- `variant_type`: Maps directly from `operation.value`.
- `c_position`: String representation (`"118"`, `"126_129"`, `"27"`, `"315+1"`).
- `ref_position_mrna`: For coding/UTR variants, the 1-based mRNA coordinate of `start_pos`. For intronic variants, set to relative genomic locus coordinate on `NG_000007.3`.
- `ref_allele`: Deleted string or reference nucleotide (or `"-"` for insertions).
- `alt_allele`: Inserted string or alternate nucleotide (or `"-"` for deletions).

---

## 9. PROPOSED HGVS PARSER ARCHITECTURE

### 9.1 Syntax Dispatch Grammar
```
HGVS Parsing Dispatch Pipeline
├── Normalize: Strip whitespace, extract accession prefix (NM_000518.5 / NG_000007.3)
├── Dispatch Table:
│   ├── Pattern 1: Substitution
│   │   r"^c\.(\*?-?\d+)([A-Za-z])>([A-Za-z])$"
│   ├── Pattern 2: Splice Substitution
│   │   r"^c\.(\d+)([+-]\d+)([A-Za-z])>([A-Za-z])$"
│   ├── Pattern 3: Single Deletion
│   │   r"^c\.(\*?-?\d+)del([A-Za-z]+)?$"
│   ├── Pattern 4: Range Deletion
│   │   r"^c\.(\*?-?\d+)_(\*?-?\d+)del([A-Za-z]+)?$"
│   ├── Pattern 5: Duplication
│   │   r"^c\.(\*?-?\d+)(?:_(\*?-?\d+))?dup([A-Za-z]+)?$"
│   ├── Pattern 6: Flanked Insertion
│   │   r"^c\.(\*?-?\d+)_(\*?-?\d+)ins([A-Za-z]+)$"
│   └── Pattern 7: Delins
│       r"^c\.(\*?-?\d+)(?:_(\*?-?\d+))?delins([A-Za-z]+)$"
└── Fallback: Return UNSUPPORTED with clear grammar diagnostic
```

### 9.2 Validation & State Determination Rules
1. **Coordinate Verification:**
   - Single coordinates must be valid within reference transcript boundaries ($c.-50$ to $c.*134$).
   - Ranges ($c.A\_B$) must satisfy $A < B$. If $A \ge B$, status is `INVALID` (`"Invalid coordinate range: start coordinate must precede end coordinate"`).
   - Insertions ($c.A\_BinsSEQ$) must satisfy $B = A + 1$. If $B \ne A + 1$, status is `INVALID` (`"HGVS insertion coordinates must be consecutive flanking nucleotides"`).
2. **Reference Sequence Conformance:**
   - **For Substitutions:** Compare reference base at coordinate $c.A$. If mismatch, return `INVALID` (`"Reference base mismatch at c.118: query states 'A', but reference has 'C'"`).
   - **For Deletions with Explicit Bases (e.g., `c.9delT`):** Compare reference base. In `NM_000518.5`, base $c.9$ is `T`.
     - `c.9delT` $\to$ `VALID`.
     - `c.9delA` $\to$ `INVALID` (`"Reference sequence at c.9 is 'T', but query specified deletion of 'A'"`).
   - **For Deletions without Explicit Bases (e.g., `c.9del`, `c.126_129del`):**
     - Automatically extract reference bases from `ref_data.cds_sequence` ($c.126..129$ is `CTTT`).
     - Populate `ref_allele = "CTTT"`.
     - Normalize to canonical HGVS string: `NM_000518.5:c.126_129del`.
3. **HGVS 3'-Shifting Canonicalization:**
   - In repetitive/tandem sequences, shift the deletion or duplication to the 3'-most position in accordance with HGVS guidelines.
   - Example: In codons 41–43 (`TTCTTTGAG`), deleting `TTCT` (124–127), `TCTT` (125–128), or `CTTT` (126–129) leaves the identical sequence `TTGAG`. The 3'-most representation is canonical `c.126_129del`. If a user enters `c.124_127del`, the parser accepts it, links it via `CANONICAL_EQUIVALENTS`, and normalizes it to `c.126_129del`.

---

## 10. FRAMESHIFT TRANSLATION ALGORITHM

### 10.1 Mathematical & Biological Algorithm
```
Input:
  - ref_cds: Complete 444 bp coding sequence (NM_000518.5 CDS)
  - ref_3utr: Complete 134 bp 3' UTR sequence (mRNA 495..628)
  - c_start: 1-based start coordinate in CDS
  - c_end: 1-based end coordinate in CDS
  - op: VariantOperation (DELETION, INSERTION, DUPLICATION)
  - inserted_bases: str

Algorithm:
1. Construct Mutated In Silico Transcript:
   full_ref = ref_cds + ref_3utr (total 578 bp)
   if op == DELETION:
       mut_seq = full_ref[:c_start - 1] + full_ref[c_end:]
   elif op == INSERTION:
       mut_seq = full_ref[:c_start] + inserted_bases + full_ref[c_start:]
   elif op == DUPLICATION:
       dup_len = c_end - c_start + 1
       mut_seq = full_ref[:c_end] + full_ref[c_start - 1 : c_end] + full_ref[c_end:]

2. Verify Reading Frame Disruption:
   net_delta = len(mut_seq) - len(full_ref)
   if net_delta % 3 == 0:
       return RouteToInFrameIndelEngine()

3. Identify First Affected Codon:
   initial_codon_num = ((c_start - 1) // 3) + 1

4. Identify First Altered Amino Acid:
   Walk from initial_codon_num:
   wt_triplet = ref_cds[(codon_idx - 1)*3 : codon_idx*3]
   mut_triplet = mut_seq[(codon_idx - 1)*3 : codon_idx*3]
   wt_aa = translate(wt_triplet)
   mut_aa = translate(mut_triplet)
   if wt_aa == mut_aa:
       codon_idx += 1  # e.g., c.9delT preserves His3 (CAT->CAC), altering codon 4
   first_altered_codon = codon_idx
   first_wt_aa = wt_aa
   first_mut_aa = mut_aa

5. Downstream Walk to Termination Codon:
   if first_mut_aa == "Ter":
       # Immediate stop codon created
       hgvs_p = f"p.{first_wt_aa}{first_altered_codon}Ter"
       impact = "Nonsense (Frameshift Immediate Termination)"
       return hgvs_p, impact

   walk_idx = first_altered_codon + 1
   stop_found = False
   while (walk_idx * 3) <= len(mut_seq):
       triplet = mut_seq[(walk_idx - 1)*3 : walk_idx*3]
       aa = translate(triplet)
       if aa == "Ter":
           stop_codon_num = walk_idx
           stop_found = True
           break
       walk_idx += 1

6. Formulate HGVS Protein Nomenclature:
   k = (stop_codon_num - first_altered_codon) + 1
   # Canonical full: p.Phe42LeufsTer19
   # Canonical short: p.Phe42fs
   hgvs_p_full = f"p.{first_wt_aa}{first_altered_codon}{first_mut_aa}fsTer{k}"
   hgvs_p_short = f"p.{first_wt_aa}{first_altered_codon}fs"
   impact = "Frameshift Deletion" (or Insertion)
```

### 10.2 Empirical Validation of Key Indel Benchmark Cases
- **Case 1: `c.126_129del` (Cd41/42 -TCTT):**
  - Deleted bases: `CTTT` at $c.126..129$.
  - Wildtype Codon 42: `TTC` ($\text{Phe}$). Mutated Codon 42: `TTG` ($\text{Leu}$).
  - Termination codon encountered at codon 60 (`TGA`).
  - Distance: $60 - 42 + 1 = 19$.
  - **Result:** `p.Phe42LeufsTer19` (short: `p.Phe42fs`). Matches ClinVar VarID 15417.
- **Case 2: `c.27dup` (Cd8/9 +G):**
  - Inserted base: `G` after $c.27$.
  - Wildtype Codon 9: `AAG` ($\text{Lys}$). Codon 9 remains `AAG` ($\text{Lys}$).
  - Wildtype Codon 10: `TCT` ($\text{Ser}$). Mutated Codon 10: `GTC` ($\text{Val}$).
  - Termination codon encountered at codon 23 (`TGA`).
  - Distance: $23 - 10 + 1 = 14$.
  - **Result:** `p.Ser10ValfsTer14` (short: `p.Ser10fs`). Matches ClinVar VarID 36308.
- **Case 3: `c.9del` ($c.9delT$):**
  - Deleted base: `T` at $c.9$.
  - Codon 3: Wildtype `CAT` ($\text{His}$), Mutated `CAC` ($\text{His}$) $\to$ residue 3 is unchanged!
  - Codon 4: Wildtype `CTG` ($\text{Leu}$), Mutated `TGA` ($\text{Ter}$) $\to$ immediate stop!
  - **Result:** `p.Leu4Ter` (or `p.Leu4fsTer1`).

---

## 11. IN-FRAME INDEL DESIGN

When $\text{net\_delta} \pmod 3 == 0$:
1. **Single Amino Acid Deletion (3 bp deleted within one codon):**
   - Example: Deletion of $c.127\_129delTTT$ (Codon 43 `TTT`, Phe43).
   - HGVS consequence: `p.Phe43del`.
2. **Multi Amino Acid Deletion (Multiple of 3 bp across codons):**
   - Example: Deletion of $c.19\_24delGAGGTG$ (Codons 7 and 8).
   - HGVS consequence: `p.Glu7_Glu8del`.
3. **Split-Codon Deletion (3 bp deleted across codon boundaries):**
   - When a 3 bp deletion straddles two codons, the flanking bases fuse to form a reconstituted codon.
   - If the reconstituted codon translates to the wildtype amino acid, one amino acid is cleanly deleted: `p.Xaa#del`.
   - If the reconstituted codon codes for a novel amino acid, it represents an in-frame deletion-insertion: `p.Xaa#_Yaa#delinsZaa`.
4. **In-frame Duplication / Insertion:**
   - Single codon duplication: `p.Ala12dup`.
   - Multi codon insertion: `p.Lys9_Ser10insGly`.

---

## 12. SPLICE VARIANT HANDLING

### 12.1 Canonical Splice Variants Analyzed
- **`c.315+1G>A` (Intron 2 Donor Invariant Dinucleotide):**
  - Exon 2 ends at $c.315$. Intron 2 donor site invariant dinucleotide is `GT` at $c.315+1$ and $c.315+2$.
  - In `NG_000007.3`, this resides at relative position 496 (Genomic 71040).
  - Reference base is `G`, Alternate base is `A`.
- **`c.92+5G>C` (IVS1-5 G>C Indian Panel Variant):**
  - Exon 1 ends at $c.92$. Intron 1 +5 consensus nucleotide.
  - In `NG_000007.3`, this resides at relative position 147 (Genomic 70691).
  - Reference base is `G`, Alternate base is `C`.

### 12.2 Scientific Boundary: Zero Speculative Protein Consequences
> [!CAUTION]
> **Scientific Integrity Rule:** Splicing mutations cannot be translated into in silico protein sequences without experimental RNA sequencing data. A splice donor mutation may cause exon skipping, intron retention, cryptic splice site activation, or complete nonsense-mediated decay (NMD).
> 
> The system **MUST NOT** fabricate a protein sequence for `c.315+1G>A` or `c.92+5G>C`.

**Mandatory Scientific Annotation:**
- `functional_impact`:
  - `c.315+1G>A` $\to$ `"Splice Site Disruption (Intron 2 donor invariant GT dinucleotide)"`
  - `c.92+5G>C` $\to$ `"Splice Site Defect (Intron 1 donor +5 consensus site)"`
- `hgvs_p`: `None` (or `"p.?"`)
- `nomenclature_notes`: `"Splice site variant in non-coding intronic region. Exact transcript splicing defect (exon skipping vs cryptic splice activation) requires experimental RNA analysis; in silico protein translation is unresolved (p.?)."`

---

## 13. CLINVAR COMPATIBILITY PLAN

### 13.1 Root Cause Fix in `backend/app/main.py#L394`
**Current Implementation:**
```python
clean_term = f"c.{variant_model.c_position}{variant_model.ref_allele}>{variant_model.alt_allele}"
```
**Phase 2A Solution:**
```python
if variant_model.variant_type == "substitution":
    clean_term = f"c.{variant_model.c_position}{variant_model.ref_allele}>{variant_model.alt_allele}"
elif variant_model.variant_type in ("deletion", "duplication", "insertion"):
    # Strip transcript prefix if present: "NM_000518.5:c.126_129del" -> "c.126_129del"
    clean_term = variant_model.hgvs_c.split(":")[-1] if ":" in variant_model.hgvs_c else variant_model.hgvs_c
else:
    clean_term = variant_model.hgvs_c
```

### 13.2 ClinVar Search Verification
With `clean_term` accurately populated:
1. `c.126_129del` enters Tier 1: `"c.126_129del"[Variant Name] AND HBB[Gene Name]`.
2. Tier 4 canonical equivalence maps `c.126_129del` $\leftrightarrow$ `c.124_127del`.
3. Candidate classification scoring ([`clinvar.py#L209`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/clinvar.py#L209)) recognizes the deletion title and assigns Priority Score 100 (`EXACT VARIANT MATCH`).
4. **Zero regression for `c.118C>T`:** The substitution path remains identical.

---

## 14. API COMPATIBILITY PLAN

### 14.1 Endpoint Contracts
- `GET /variant/search` & `POST /variant/search`:
  - Request Model: `VariantSearchRequest(query: str)` $\to$ **100% UNCHANGED**.
  - Response Model: `VariantSearchResponse` $\to$ **100% UNCHANGED**.
- Existing consumers sending `{ "query": "c.118C>T" }` receive the identical JSON payload.
- Consumers sending `{ "query": "c.126_129del" }` or `{ "query": "c.27dup" }` will now receive HTTP 200 with `error: null` and populated `clinvar_records`, instead of an error message.

---

## 15. FRONTEND IMPACT

### 15.1 Component Audit
- **Files Inspected:**
  - [`frontend/lib/api.ts`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/frontend/lib/api.ts): Encapsulates API calls via `searchVariantDirect`. Requires zero changes.
  - [`frontend/lib/types.ts`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/frontend/lib/types.ts): TypeScript interfaces already define `variant_type: string`, `hgvs_p?: string | null`. Requires zero changes.
  - [`frontend/components/DirectVariantSearch.tsx`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/frontend/components/DirectVariantSearch.tsx):
    - Update input placeholder to: `e.g. c.118C>T, c.126_129del, c.27dup, c.315+1G>A`.
    - Expand `presetChips` to include indel and splice examples:
      ```typescript
      const presetChips = [
        { label: "c.118C>T (p.Gln40Ter)", query: "c.118C>T" },
        { label: "c.20A>T (HbS)", query: "c.20A>T" },
        { label: "c.126_129del (Cd41/42)", query: "c.126_129del" },
        { label: "c.27dup (Cd8/9)", query: "c.27dup" },
        { label: "c.315+1G>A (IVS2-1)", query: "c.315+1G>A" },
      ];
      ```

---

## 16. TEST MATRIX

| Test ID | Test Category | Target Query / Variant | Expected Consequence / Result | Validation Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **REG-01** | Regression | `c.118C>T` | `p.Gln40Ter` (Nonsense) | VarID 15402, Score 100 |
| **REG-02** | Regression | `c.20A>T` | `p.Glu7Val` (Missense) | VarID 15333, Score 100 |
| **PAR-01** | Parser: Deletion | `c.9delT` | `p.Leu4Ter` (Frameshift) | Valid single deletion |
| **PAR-02** | Parser: Deletion | `c.9del` | `p.Leu4Ter` (Ref inferred) | Auto-extracts `T` |
| **PAR-03** | Parser: Range Del | `c.126_129delCTTT` | `p.Phe42LeufsTer19` | Canonical 3'-shifted |
| **PAR-04** | Parser: Range Del | `c.126_129del` | `p.Phe42LeufsTer19` | Inferred `CTTT` |
| **PAR-05** | Parser: Duplication | `c.27dup` | `p.Ser10ValfsTer14` | Canonical duplication |
| **PAR-06** | Parser: Insertion | `c.27_28insG` | `p.Ser10ValfsTer14` | Flanked insertion |
| **PAR-07** | Parser: Splice SNV | `c.315+1G>A` | `p.?` (Splice Disruption) | Non-coding donor GT |
| **PAR-08** | Parser: Splice SNV | `c.92+5G>C` | `p.?` (Splice Defect) | Non-coding +5 consensus |
| **ERR-01** | Error: Mismatch | `c.9delA` | `INVALID: ref mismatch` | Reference at $c.9$ is T |
| **ERR-02** | Error: Inverted | `c.129_126del` | `INVALID: range order` | Start must be < End |
| **ERR-03** | Error: Non-flank Ins| `c.25_28insG` | `INVALID: non-consecutive` | Ins must be $B = A + 1$ |
| **ERR-04** | Error: Out of Bounds| `c.999del` | `INVALID: out of bounds` | CDS length is 444 bp |
| **FS-01** | Translation Engine | CDS $c.126\_129del$ | Stop codon at residue 60 | PTC distance = 19 |
| **FS-02** | Translation Engine | CDS $c.27dup$ | Stop codon at residue 23 | PTC distance = 14 |
| **IF-01** | Translation Engine | CDS $c.127\_129del$ | `p.Phe43del` (In-frame) | Single residue loss |
| **CV-01** | ClinVar Integration| Direct search `c.126_129del` | VarID 15417 returned | Tier 1 exact match |
| **CV-02** | ClinVar Integration| Direct search `c.27dup` | VarID 36308 returned | Tier 1 exact match |

---

## 17. REGRESSION PROTECTION STRATEGY

To safeguard the frozen Phase 1 release baseline:
1. **Zero Modification to Baseline Test Suites:** The existing 78 tests across `test_pipeline.py`, `test_clinvar_retrieval_hardening.py`, `test_copilot_hardening_audit.py`, `test_groq_ai.py`, `test_indian_mutations_and_screening.py`, and `test_provenance_and_hallucination.py` will not be altered.
2. **Dedicated Phase 2A Test Suite:** All new tests will be authored in a new test file: `backend/tests/test_hgvs_precision_phase2a.py`.
3. **Doctor Invariance:** The 18 system diagnostics in `tools/doctor.py` must maintain an uncompromised 18/18 PASS rate.
4. **Pre-commit Audit Execution:** Full release audit (`python tools/release_audit.py`) will be executed at every milestone.

---

## 18. DOCUMENTATION CHANGES

Upon implementation approval, the following documentation files will be updated:
- [`README.md`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/README.md): Document expanded direct search syntax support for indels and splice variants.
- [`docs/API.md`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/docs/API.md): Document indel query examples and updated `VariantSearchResponse` behavior.
- [`docs/ARCHITECTURE.md`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/docs/ARCHITECTURE.md): Diagram the updated `hgvs_parser.py` intermediate representation.
- [`docs/SCIENTIFIC_METHOD.md`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/docs/SCIENTIFIC_METHOD.md): Detail the frameshift codon translation mathematics and splice safety policies.

---

## 19. PERFORMANCE CONSIDERATIONS

- **Zero Heavy Dependencies:** The entire parser and frameshift translation engine will be authored in standard Python using string slicing and lookup tables.
- **Latency Impact:** Codon translation of a 147-amino acid sequence requires < 0.2 ms on standard CPU hardware. Total API response time will remain dominated by external network I/O to NCBI E-utilities.
- **Memory Footprint:** In-memory sequence manipulation adds < 1 KB per request.

---

## 20. SCIENTIFIC RISKS

1. **Risk:** Over-predicting protein consequences for splice variants.  
   *Mitigation:* Strict enforcement of `p.?` for all intronic variants.
2. **Risk:** 3'-shifting discrepancies in homopolymer runs.  
   *Mitigation:* Implement standard HGVS 3'-most rule and maintain bidirectional canonical equivalence tables (`c.126_129del` $\leftrightarrow$ `c.124_127del`).
3. **Risk:** Frameshifts extending past canonical codon 147 (`TAA` stop).  
   *Mitigation:* The translation engine must append the 134 bp 3' UTR to the CDS when searching for downstream cryptic termination codons.

---

## 21. IMPLEMENTATION SEQUENCE

```
Recommended Implementation Flow
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Author Normalized Model & Parser (backend/app/hgvs_parser.py)  │
│         - ParsedHGVSVariant model & regex dispatch grammar             │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Author Consequence Engine (backend/app/indel_consequences.py)  │
│         - Dynamic frameshift downstream codon walk & in-frame deltas   │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Implement Splicing Coordinate Adapter                          │
│         - Dual-mode coordinate resolution (mRNA vs NG_000007.3)        │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Integrate into backend/app/variants.py & Fix main.py:394       │
│         - Upgrade parse_hgvs_input & fix clean_term reconstruction     │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Author Dedicated Test Suite (tests/test_hgvs_precision_phase2a)│
│         - Implement the 20 test cases from Section 16 Matrix           │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 6: Execute Regression Verification                                │
│         - Verify 78/78 baseline tests + 20 Phase 2A tests (98 passed)  │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 7: Update Frontend Preset Chips (DirectVariantSearch.tsx)         │
│         - Non-breaking UI polish with indel examples                   │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 8: Run Full Release Audit (tools/release_audit.py)                │
│         - Doctor 18/18, TypeScript 0 errors, Build Clean               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 22. EXPLICIT OUT-OF-SCOPE ITEMS

The following features are strictly **EXCLUDED** from Phase 2A:
1. **Whole-Genome Structural Rearrangements:** Large deletions (> 500 bp, such as the 619 bp Indian deletion) remain out of scope for the point-coordinate parser.
2. **Machine Learning Splicing Models:** Complex deep-learning splice predictors (e.g., SpliceAI) are excluded to maintain lightweight zero-dependency execution.
3. **Compound Heterozygote Multi-Allele Parsing:** Inputting multi-variant genotypes (e.g., `[c.118C>T];[c.20A>T]`) in a single query is excluded; variants must be queried individually.
4. **Autonomous Medical Decision Support:** Clinical treatment advice remains strictly forbidden.

---

## 23. ACCEPTANCE CRITERIA

1. **Parser Acceptance:** Queries for `c.118C>T`, `c.9del`, `c.9delT`, `c.126_129del`, `c.27dup`, `c.27_28insG`, `c.315+1G>A`, and `c.92+5G>C` return HTTP 200 with `error: null`.
2. **Deterministic Protein Precision:**
   - `c.126_129del` computes `p.Phe42LeufsTer19` (short: `p.Phe42fs`).
   - `c.27dup` computes `p.Ser10ValfsTer14` (short: `p.Ser10fs`).
   - `c.315+1G>A` and `c.92+5G>C` strictly output `p.?` with splice disruption annotations.
3. **ClinVar Interoperability:** Direct search for `c.126_129del` retrieves ClinVar Variation ID `15417` as an Exact Variant Match. Direct search for `c.27dup` retrieves Variation ID `36308` as an Exact Variant Match.
4. **Test Suite Expansion:** All 78 Phase 1 tests pass + 100% of new Phase 2A tests pass (0 failures).
5. **System Invariants:** `tools/doctor.py` passes 18/18 checks, frontend TypeScript passes with 0 errors, and `tools/benchmark_c118.py` confirms VarID 15402 at Match Score 100.

---

# PHASE 2A READINESS VERDICT

### **VERDICT: READY WITH CONDITIONS**

**Decision Rationale:**
The codebase architecture, reference sequences, and ClinVar integration layers are fully understood, verified, and exceptionally well-suited for this precision upgrade. However, implementation must satisfy **three strict technical pre-conditions**:

1. **Condition 1 (Query Term Fix):** Line 394 of [`backend/app/main.py`](file:///e:/HBB%20GENE%20MUTATION%20PROJECT/backend/app/main.py#L394) must be refactored to prevent mangling non-substitution variant terms before external NCBI dispatch.
2. **Condition 2 (Dual Coordinate Resolution):** Splice-site intronic variants (`c.315+1G>A`, `c.92+5G>C`) must resolve their reference nucleotides against the genomic locus reference `NG_000007.3` rather than attempting an invalid lookup in the spliced mRNA `NM_000518.5`.
3. **Condition 3 (3' UTR Extension for Frameshifts):** The dynamic frameshift translation walk must include the 134 bp 3' UTR to handle variants near the C-terminus that shift the reading frame past canonical codon 147.

*Phase 2A discovery is complete. The repository baseline remains frozen and untouched. Awaiting user authorization to proceed to implementation.*
