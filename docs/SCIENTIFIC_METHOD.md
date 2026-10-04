# Scientific Methodology & Biological Specification

**HBB Mutation Analyzer: Understand the sequence. Follow the evidence.**

---

## 1. Biological Target: Human Beta-Globin (*HBB*)

The human *HBB* gene (hemoglobin subunit beta) is located on chromosome 11p15.4. It encodes the beta-globin polypeptide, which pairs with alpha-globin chains to assemble the adult hemoglobin heterotetramer ($\alpha_2\beta_2$). Defects in *HBB* cause hereditary hemoglobinopathies, including sickle cell disease and $\beta$-thalassemia.

### 1.1 Canonical Reference Standard: NM_000518.5
The application fixes its target transcript to the authoritative NCBI RefSeq MANE Select transcript:
* **Transcript Accession:** `NM_000518.5` (GenBank / RefSeq)
* **Protein Accession:** `NP_000509.1`
* **CCDS Identifier:** `CCDS7753.1`
* **Total mRNA Length:** 628 bp
* **Exon Boundaries:**
  * Exon 1: 1 .. 142 bp
  * Exon 2: 143 .. 365 bp
  * Exon 3: 366 .. 628 bp
* **Coding Sequence (CDS):** 51 .. 494 bp (Length: 444 bp, coding for 147 amino acids plus 1 stop codon `TAA`).

---

## 2. Genomic Coordinate Mapping Mathematics

HGVS cDNA sequence variant nomenclature ($c.$) maps positions relative to the transcription translation initiation codon (`ATG`):
* **$c.1$**: Position 51 of the mRNA sequence (Adenine of `ATG`).
* **5' Untranslated Region (5' UTR)**: Preceding base 51:
  $$\text{c.pos} = \text{mrna\_pos} - 51 \quad (\text{e.g., base 50 is } c.-1, \text{base 49 is } c.-2)$$
* **Coding Region (CDS)**: Bases 51 through 494:
  $$\text{c.pos} = \text{mrna\_pos} - 50 \quad (\text{range } c.1 \text{ to } c.444)$$
* **3' Untranslated Region (3' UTR)**: Following stop codon base 494:
  $$\text{c.pos} = *(\text{mrna\_pos} - 494) \quad (\text{e.g., base 495 is } c.*1)$$

### 2.1 Codon and Reading Frame Computation
For any coding coordinate $c \in [1, 444]$:
$$\text{Codon Number} = \left\lfloor \frac{c - 1}{3} \right\rfloor + 1 \quad \in [1, 148]$$
$$\text{Intra-codon Offset} = (c - 1) \pmod 3 \quad \in \{0, 1, 2\}$$
$$\text{Codon Start Coordinate} = (\text{Codon Number} - 1) \times 3 + 1$$
$$\text{Codon End Coordinate} = \text{Codon Number} \times 3$$

---

## 3. The Controlled Validation Case: `c.118C>T` (`p.Gln40Ter`)

### 3.1 Molecular Mechanism
* **Reference Coordinate:** $c.118$ (mRNA position 168, 0-based index 167 in mRNA).
* **Codon Number:** $\lfloor (118 - 1) / 3 \rfloor + 1 = 40$.
* **Reference Triplet:** `CAG` (Codes for Glutamine, $\text{Gln}$ / $\text{Q}$).
* **Nucleotide Substitution:** Cytosine ($C$) $\rightarrow$ Thymine ($T$) at intra-codon offset 0.
* **Sample Triplet:** `TAG` (Amber stop codon, $\text{Ter}$ / $*$).
* **Consequence:** Nonsense mutation producing a premature termination codon (PTC) at residue 40.
* **HGVS Notations:**
  * cDNA: `NM_000518.5:c.118C>T`
  * Protein: `p.Gln40Ter`

### 3.2 Historical vs Modern HGVS Numbering
In historic hemoglobin literature, globin amino acid residues were numbered starting after the post-translationally cleaved initiator Methionine (counting from Valine 1). Consequently, this classic Mediterranean $\beta^0$-thalassemia allele was traditionally termed **"Codon 39 nonsense"**. Under standard HGVS recommendations (RefSeq NP_000509.1), the initiator Methionine is residue 1, making this position **Codon 40** (`p.Gln40Ter`). The analyzer adheres to modern HGVS standards while capturing both notations in external database queries.

---

---

## 4. The Seven Authoritative Benchmark Variants

| Common Name | Coordinate Reference | HGVS cDNA / Genomic | Codon / Locus | Amino Acid Consequence | Functional Consequence | ClinVar ID | Phenotype |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Controlled Benchmark** | `NM_000518.5` | `c.118C>T` | Codon 40 (`CAG` $\to$ `TAG`) | `p.Gln40Ter` (legacy Codon 39) | Nonsense (Stop Gain) | **15402** | $\beta^0$ Thalassemia |
| **Sickle Cell (HbS)** | `NM_000518.5` | `c.20A>T` | Codon 7 (`GAG` $\to$ `GTG`) | `p.Glu7Val` (legacy Glu6Val) | Missense | **15333** | Sickle Cell Trait / Disease |
| **Hemoglobin C (HbC)** | `NM_000518.5` | `c.19G>A` | Codon 7 (`GAG` $\to$ `AAG`) | `p.Glu7Lys` (legacy Glu6Lys) | Missense | **15126** | Hemoglobin C Trait / Disease |
| **IVS1-5 (G>C)** | `NG_000007.3` | `c.92+5G>C`<br>`g.70691G>C` | Intron 1 +5 donor splice | None | Splice Site Defect | **15447** | $\beta^+$ Thalassemia |
| **Cd41/42 (-TCTT)** | `NM_000518.5` | `c.126_129del` | Codons 41-42 (Exon 2) | `p.Phe42fs` | Frameshift Deletion (3'-shifted) | **15417** | $\beta^0$ Thalassemia |
| **Cd8/9 (+G)** | `NM_000518.5` | `c.27dup` | Codons 8-9 (Exon 1) | `p.Ser10fs` | Frameshift Duplication | **36308** | $\beta^0$ Thalassemia |
| **Cd30 (G>C)** | `NM_000518.5` | `c.93G>C` | Codon 30 / boundary 31 | `p.Arg31Ser` | Exon 1 Splice Junction Defect | **869321** | $\beta^0$ / Severe $\beta^+$ |

---

## 5. Sequence Alignment Specification

The engine executes deterministic global pairwise alignment using the Needleman-Wunsch dynamic programming algorithm via Biopython's `Bio.Align.PairwiseAligner`:
* **Alignment Mode:** Global
* **Match Score:** $+2.0$
* **Mismatch Penalty:** $-1.0$
* **Gap Open Penalty:** $-2.5$
* **Gap Extend Penalty:** $-1.0$

This configuration reliably handles substitutions as well as in-frame and frameshift indels while preserving coordinate fidelity.


## 6. ClinVar Retrieval Hardening & Evidence Tiering

To guarantee absolute scientific provenance without false positives or candidate truncation:
1. **Progressive Search Architecture**:
   - Tier 1: Exact quoted transcript cDNA notation (`"c.118C>T"[Variant Name] AND HBB[Gene Name]`).
   - Tier 2: Quoted protein change (`"p.Gln40Ter"[Variant Name] AND HBB[Gene Name]`).
   - Tier 3: Gene-scoped cDNA variant search with expanded window (`retmax=50`).
   - Tier 4: Canonical indels and historical literature aliases (`CD39 C>T`).
   - Tier 5: Direct Variation ID / VCV accession query.
2. **Deterministic Post-Retrieval Verification**:
   - Compound heterozygotes (`c.[205C>T;20A>T]`) are strictly disqualified from single variant exact match status.
   - Alternate alleles at the same codon (e.g. `c.118C>A` vs `c.118C>T`) are segregated.
3. **Three-Tier Evidence Classification**:
   - `EXACT VARIANT MATCH`: Exact codon coordinate, alleles, and consequence match.
   - `RELATED HBB RECORD`: Variants in HBB at different positions or compound genotypes.
   - `GENERAL HBB / BETA THALASSEMIA RECORD`: Unannotated or condition-level records.
