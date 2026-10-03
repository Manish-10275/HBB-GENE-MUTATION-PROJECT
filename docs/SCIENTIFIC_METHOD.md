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

## 4. Other Benchmark Variants

| Common Name | HGVS cDNA | Ref Codon | Alt Codon | Amino Acid Change | Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sickle Cell (HbS)** | `c.20A>T` | `GAG` (Codon 7) | `GTG` | `p.Glu7Val` (legacy Glu6Val) | Missense |
| **Hemoglobin C (HbC)** | `c.19G>A` | `GAG` (Codon 7) | `AAG` | `p.Glu7Lys` (legacy Glu6Lys) | Missense |
| **Synthetic Frameshift** | `c.117_118insA` | Disrupts frame | Frame shifted | Downstream PTC | Frameshift |

---

## 5. Sequence Alignment Specification

The engine executes deterministic global pairwise alignment using the Needleman-Wunsch dynamic programming algorithm via Biopython's `Bio.Align.PairwiseAligner`:
* **Alignment Mode:** Global
* **Match Score:** $+2.0$
* **Mismatch Penalty:** $-1.0$
* **Gap Open Penalty:** $-2.5$
* **Gap Extend Penalty:** $-1.0$

This configuration reliably handles substitutions as well as in-frame and frameshift indels while preserving coordinate fidelity.
