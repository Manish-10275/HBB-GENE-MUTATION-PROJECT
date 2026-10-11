# CP4 Comparison Mapping Specification

**Document Status:** DESIGN SPECIFICATION ONLY  
**Stage:** Phase 2C — CP4  
**Scope:** Protein Normalization and Molecular Consequence Ontology Mapping for External Concordance Evaluation  
**Target Reference:** RefSeq `NM_000518.5` / `NG_000007.3`  

---

## 1. Overview and Purpose

This specification establishes the formal, deterministic mapping rules required to evaluate concordance between:
1. **Engine Runtime Predictions ($A$):** Standard IUPAC 3-letter HGVS syntax (`p.Asn109Lys`, `p.(=)`, `p.Glu7ArgfsTer13`).
2. **External ClinVar Annotations ($C$):** Heterogeneous representations including 1-letter IUPAC codes (`N109K`), truncated frameshift syntax (`E7fs`), asterisk stop notation (`Q128*`), codon-specific synonymous notation (`p.Leu69=`), and blank fields (`""`).

These rules are strictly deterministic and mathematically bounded. No heuristics or fuzzy matching are permitted.

---

## 2. Amino Acid IUPAC Translation Table

The bidirectional translation between IUPAC 1-letter and 3-letter amino acid representations is fixed as follows:

| Amino Acid Name | 3-Letter Code | 1-Letter Code | RegExp Pattern |
|---|:---:|:---:|:---:|
| Alanine | `Ala` | `A` | `Ala\|A` |
| Arginine | `Arg` | `R` | `Arg\|R` |
| Asparagine | `Asn` | `N` | `Asn\|N` |
| Aspartate / Aspartic Acid | `Asp` | `D` | `Asp\|D` |
| Cysteine | `Cys` | `C` | `Cys\|C` |
| Glutamine | `Gln` | `Q` | `Gln\|Q` |
| Glutamate / Glutamic Acid | `Glu` | `E` | `Glu\|E` |
| Glycine | `Gly` | `G` | `Gly\|G` |
| Histidine | `His` | `H` | `His\|H` |
| Isoleucine | `Ile` | `I` | `Ile\|I` |
| Leucine | `Leu` | `L` | `Leu\|L` |
| Lysine | `Lys` | `K` | `Lys\|K` |
| Methionine | `Met` | `M` | `Met\|M` |
| Phenylalanine | `Phe` | `F` | `Phe\|F` |
| Proline | `Pro` | `P` | `Pro\|P` |
| Serine | `Ser` | `S` | `Ser\|S` |
| Threonine | `Thr` | `T` | `Thr\|T` |
| Tryptophan | `Trp` | `W` | `Trp\|W` |
| Tyrosine | `Tyr` | `Y` | `Tyr\|Y` |
| Valine | `Val` | `V` | `Val\|V` |
| Termination / Translation Stop | `Ter` | `*` or `X` | `Ter\|\*\|X` |

---

## 3. Canonical Protein Consequence Representation

To eliminate formatting differences between 1-letter, 3-letter, and prefix variations, both engine outputs and external annotations must be parsed into an intermediate **Canonical Protein Consequence (`CanonicalProtein`)** data structure before comparison:

```python
class ProteinVariantType(Enum):
    MISSENSE = "MISSENSE"
    NONSENSE = "NONSENSE"
    SYNONYMOUS = "SYNONYMOUS"
    FRAMESHIFT = "FRAMESHIFT"
    IN_FRAME_INDEL = "IN_FRAME_INDEL"
    SPLICE_UNKNOWN = "SPLICE_UNKNOWN"
    NON_CODING_ABSENT = "NON_CODING_ABSENT"
    UNPARSED = "UNPARSED"

class CanonicalProtein:
    variant_type: ProteinVariantType
    codon_start: Optional[int]          # 1-based codon coordinate under NM_000518.5
    codon_end: Optional[int]            # For multi-codon events
    ref_aa: Optional[str]               # 3-letter standard IUPAC
    alt_aa: Optional[str]               # 3-letter standard IUPAC (or 'Ter')
    frameshift_offset: Optional[int]    # Ter offset codon if available
    raw_string: str                     # Original input string
```

---

## 4. Protein Pattern Normalization Grammar

### 4.1 Missense Single Amino Acid Substitutions
- **Engine Syntax Pattern:** `^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$`  
  *Example:* `p.Asn109Lys` $\rightarrow$ `ref_aa: Asn, codon: 109, alt_aa: Lys`
- **ClinVar 1-Letter Syntax Pattern:** `^([A-Z])(\d+)([A-Z])$`  
  *Example:* `N109K` $\rightarrow$ `ref_aa: Asn, codon: 109, alt_aa: Lys`
- **ClinVar 3-Letter Syntax Pattern:** `^p?\.?([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$`  
  *Example:* `p.Asn109Lys` or `Asn109Lys` $\rightarrow$ `ref_aa: Asn, codon: 109, alt_aa: Lys`
- **Concordance Criterion:**
  $$\text{ref\_aa}_A == \text{ref\_aa}_C \land \text{codon}_A == \text{codon}_C \land \text{alt\_aa}_A == \text{alt\_aa}_C$$

### 4.2 Nonsense (Premature Termination)
- **Engine Syntax Pattern:** `^p\.([A-Z][a-z]{2})(\d+)(?:Ter|\*)$`  
  *Example:* `p.Gln128Ter` $\rightarrow$ `ref_aa: Gln, codon: 128, alt_aa: Ter`
- **ClinVar Asterisk Syntax Pattern:** `^([A-Z])(\d+)\*$`  
  *Example:* `Q128*` $\rightarrow$ `ref_aa: Gln, codon: 128, alt_aa: Ter`
- **ClinVar Ter Syntax Pattern:** `^p?\.?([A-Z][a-z]{2})(\d+)Ter$`  
  *Example:* `p.Gln128Ter` $\rightarrow$ `ref_aa: Gln, codon: 128, alt_aa: Ter`
- **Concordance Criterion:**
  $$\text{ref\_aa}_A == \text{ref\_aa}_C \land \text{codon}_A == \text{codon}_C \land \text{alt\_aa}_A == \text{Ter} \land \text{alt\_aa}_C == \text{Ter}$$

### 4.3 Synonymous (Silent) Variants
- **Engine CDS Syntax Pattern:** `^p\.\(=\)$` or `^p\.=$`  
  *Definition:* Transcript coding sequence unaltered.
- **ClinVar Codon Syntax Pattern:** `^p?\.?([A-Z][a-z]{2})(\d+)=$` or `^([A-Z])(\d+)=$`  
  *Example:* `p.Leu69=` or `L69=` $\rightarrow$ `ref_aa: Leu, codon: 69, alt_aa: =`
- **Concordance Handling:**
  - **Semantic Protein Concordance:** Both assert zero amino acid change across the translated product. If the variant nucleotide change lies within codon 69, semantic protein concordance is **`MATCH`**.
  - **Syntax Concordance:** String representations differ (`p.(=)` vs `p.Leu69=`). If strict literal HGVS string matching is required without semantic synonymous equivalence, this is classified as `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`.
  - **CP4 Decision:** Semantic synonymous equivalence is mapped to `EXACT_MOLECULAR_AGREEMENT` because both assert identical biological translation.

### 4.4 Frameshift Insertions and Deletions
- **Engine Full HGVS Pattern:** `^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})fs(?:Ter|\*)(\d+|\?)$`  
  *Example:* `p.Glu7ArgfsTer13` $\rightarrow$ `ref_aa: Glu, codon: 7, alt_aa: Arg, offset: 13`
- **ClinVar Truncated Syntax Pattern:** `^([A-Z])(\d+)fs$` or `^p?\.?([A-Z][a-z]{2})(\d+)fs$`  
  *Example:* `E7fs` $\rightarrow$ `ref_aa: Glu, codon: 7, alt_aa: None, offset: None`
- **Concordance Handling:**
  - **Molecular Concordance:** Both assert reading frame disruption $\rightarrow$ Molecular `MATCH`.
  - **Protein Concordance:** ClinVar truncated syntax specifies only the initial altered codon, whereas engine output specifies the initial substitution and downstream stop offset.
  - **Classification:** Under Section 15 of `PHASE2C_BENCHMARK_PROTOCOL.md`:
    $$\text{category} = \mathbf{MOLECULAR\_AGREEMENT\_PROTEIN\_DIFFERENCE}$$
    $$\text{primary\_endpoint\_status} = \mathbf{MATCH}$$
    $$\text{protein\_endpoint\_status} = \mathbf{DISCREPANCY}$$
  - This provides exact adherence to protocol: molecular concordance is recognized, while protein syntax variance is cataloged as a formatting difference.

### 4.5 Splice Site Disruptions (C09)
- **Engine Syntax:** `p.?`
- **ClinVar External Syntax:** `""` (Empty string) or `None`
- **Biological Context:** Canonical splice donor/acceptor disruptions affect pre-mRNA splicing and typically trigger exon skipping, intron retention, or nonsense-mediated decay; standard translated protein cannot be predicted without experimental RNA analysis.
- **Protocol Classification:**
  - In ClinVar, protein consequence is omitted (`""`).
  - The protocol defines:
    > **`EXTERNAL_ANNOTATION_INCOMPLETE`**: External reference record lacks protein or consequence details. Endpoint Impact: **`DISCREPANCY`**.
  - Therefore, candidates where external protein is absent cannot be assigned `EXACT_MOLECULAR_AGREEMENT`. They must be classified under `EXTERNAL_ANNOTATION_INCOMPLETE`.

### 4.6 3' UTR Regulatory Variants (C11)
- **Engine Syntax:** `None`
- **ClinVar External Syntax:** `""` (Empty string) or `None`
- **Biological Context:** Non-coding variants outside the coding sequence do not code for amino acids.
- **Protocol Classification:**
  - Both engine and ClinVar agree that no protein product exists.
  - Unlike coding variants where protein is missing due to incomplete database curation, for 3' UTR variants the absence of a protein string is biologically expected.
  - **Rule:** For non-coding classes (C10, C11), if `engine_protein is None` and `external_protein in ("", None)`, the protein endpoint is evaluated as **`MATCH (NON_CODING)`**, avoiding false classification as incomplete.

---

## 5. Molecular Consequence Ontology Mapping Table

To perform a valid comparison between runtime engine consequences and external database classifications, the following ontology equivalence matrix is established:

| Engine Consequence Class | Sequence Ontology (SO) Term | ClinVar Molecular Description | Expected Mapping Status |
|---|---|---|:---:|
| **`Missense`** | `SO:0001583` (`missense_variant`) | `Missense`, `missense variant` | **DIRECT MATCH** |
| **`Nonsense`** | `SO:0001587` (`stop_gained`) | `Nonsense`, `stop gained` | **DIRECT MATCH** |
| **`Synonymous`** | `SO:0001819` (`synonymous_variant`) | `Synonymous`, `synonymous variant` | **DIRECT MATCH** |
| **`Frameshift`** | `SO:0001589` (`frameshift_variant`) | `Frameshift`, `frameshift variant` | **DIRECT MATCH** |
| **`In-Frame Indel`** | `SO:0001820` (`inframe_indel`) | `In-frame deletion`, `In-frame insertion` | **DIRECT MATCH** |
| **`Splice Site Disruption`** | `SO:0001574` (`splice_acceptor_variant`), `SO:0001575` (`splice_donor_variant`) | `Splice site`, `Splice acceptor`, `Splice donor` | **DIRECT MATCH** |
| **`3' UTR Regulatory`** | `SO:0001624` (`3_prime_UTR_variant`) | `3' UTR`, `3' untranslated region` | **DIRECT MATCH** |
| **`5' UTR Regulatory`** | `SO:0001623` (`5_prime_UTR_variant`) | `5' UTR`, `5' untranslated region` | **DIRECT MATCH** |

Any annotation outside this mapping table triggers `UNRESOLVED` or `EXTERNAL_CONFLICT`.
