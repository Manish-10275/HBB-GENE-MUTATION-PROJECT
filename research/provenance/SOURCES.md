# Ground Truth Evidence Provenance — HBB Mutation Analyzer

This document catalogs every authoritative source and classification tier employed in the **HBB Gene Mutation Analyzer Phase 2B Benchmark Dataset**.

---

## 1. Provenance Classification Hierarchy

To eliminate circular reasoning and uphold scientific validity, every benchmark entry is tagged with its formal evidence provenance:

- **Class A (Authoritative Standards & Universal Reference):**
  - RefSeq Transcript: `NM_000518.5` (NCBI Reference Sequence, MANE Select, CCDS7753.1).
  - RefSeq Genomic Gene Locus: `NG_000007.3:70545..72152` (Exons 1–3, Introns 1–2).
  - Standard Genetic Code: NCBI Translation Table 1.
  - HGVS Nomenclature Recommendations (Human Genome Variation Society).
- **Class B (External Clinical Registry Evidence):**
  - NCBI ClinVar database assertions, Variation IDs, and VCV accessions retrieved via Entrez E-utilities.
  - Review statuses: Criteria provided, Multiple submitters, or Reviewed by expert panel.
- **Class C (Curated Registry & Literature Cross-References):**
  - IthaGenes (Hemoglobin Variants and Thalassaemias Database).
  - Primary peer-reviewed medical publications with verified PMIDs.
- **Class D (In Silico Computed):**
  - Derived solely from algorithmic execution (e.g. downstream codon walking without external database annotation).
  - *Explicitly segregated from external validation claims.*

---

## 2. Authoritative Database Ground Truth Inventory

| Variation ID | Accession | HGVS cDNA | Protein Consequence | Clinical Significance | Review Status | Source Authority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **15402** | `VCV000015402` | `c.118C>T` | `p.Gln40Ter` | Pathogenic | multiple submitters | NCBI ClinVar |
| **15333** | `VCV000015333` | `c.20A>T` | `p.Glu7Val` | Pathogenic | multiple submitters | NCBI ClinVar |
| **15126** | `VCV000015126` | `c.19G>A` | `p.Glu7Lys` | Pathogenic/Likely pathogenic | multiple submitters | NCBI ClinVar |
| **15161** | `VCV000015161` | `c.79G>A` | `p.Glu27Lys` | Pathogenic | multiple submitters | NCBI ClinVar |
| **15447** | `VCV000015447` | `c.92+5G>C` | `p.?` | Pathogenic | reviewed by expert panel | NCBI ClinVar |
| **15437** | `VCV000015437` | `c.92+1G>T` | `p.?` | Pathogenic | criteria provided | NCBI ClinVar |
| **36334** | `VCV000036334` | `c.92+2T>C` | `p.?` | Pathogenic | criteria provided | NCBI ClinVar |
| **15438** | `VCV000015438` | `c.315+1G>A` | `p.?` | Pathogenic | multiple submitters | NCBI ClinVar |
| **869355**| `VCV000869355` | `c.315+2T>C` | `p.?` | Pathogenic | criteria provided | NCBI ClinVar |
| **15446** | `VCV000015446` | `c.93-1G>A` | `p.?` | Pathogenic | criteria provided | NCBI ClinVar |
| **552712** | `VCV000552712` | `c.316-1G>A` | `p.?` | Pathogenic/Likely pathogenic | criteria provided | NCBI ClinVar |
| **21191**  | `VCV000021191` | `c.316-2A>G` | `p.?` | Pathogenic | criteria provided | NCBI ClinVar |
| **15417** | `VCV000015417` | `c.126_129del` | `p.Phe42fs` | Pathogenic/Likely pathogenic | multiple submitters | NCBI ClinVar |
| **36308** | `VCV000036308` | `c.27dup` | `p.Ser10fs` | Pathogenic | multiple submitters | NCBI ClinVar |
| **869321** | `VCV000869321` | `c.93G>C` | `p.Arg31Ser` | Pathogenic | no assertion criteria | NCBI ClinVar |
| **193106** | `VCV000193106` | `c.9T>C` | `p.His3=` | Benign | criteria provided | NCBI ClinVar |
| **3572117**| `VCV003572117` | `c.15T>A` | `p.Thr5=` | Likely benign | criteria provided | NCBI ClinVar |
| **1544548**| `VCV001544548` | `c.108C>T` | `p.Tyr36=` | Conflicting classifications | multiple submitters | NCBI ClinVar |
| **15405** | `VCV000015405` | `c.114G>A` | `p.Trp38Ter` | Pathogenic | criteria provided | NCBI ClinVar |
| **15406** | `VCV000015406` | `c.130G>T` | `p.Glu44Ter` | Pathogenic | criteria provided | NCBI ClinVar |
| **15470** | `VCV000015470` | `c.-78A>C` | None | Pathogenic | reviewed by expert panel | NCBI ClinVar |
| **869290** | `VCV000869290` | `c.-80T>C` | None | Pathogenic | criteria provided | NCBI ClinVar |
| **15488** | `VCV000015488` | `c.*111A>G` | None | Pathogenic | reviewed by expert panel | NCBI ClinVar |
| **15476** | `VCV000015476` | `c.*112A>G` | None | Pathogenic/Likely pathogenic | criteria provided | NCBI ClinVar |
| **393707** | `VCV000393707` | `c.*6C>G` | None | Pathogenic/Likely pathogenic | criteria provided | NCBI ClinVar |
| **495966** | `VCV000495966` | `c.*102C>T` | None | Likely benign | criteria provided | NCBI ClinVar |
| **495970** | `VCV000495970` | `c.*67G>T` | None | Benign | criteria provided | NCBI ClinVar |
| **3599779**| `VCV003599779` | `c.*129T>C` | None | Likely benign | criteria provided | NCBI ClinVar |
| **3572119**| `VCV003572119` | `c.363dup` | `p.Glu122fs` | Pathogenic | criteria provided | NCBI ClinVar |

---

## 3. Negative Control Ground Truth Rationale

Negative controls ($N = 20$) are formulated according to formal HGVS sequence variant specifications:
- **Range Inversions (`c.129_126del`):** Violation of HGVS rule stating start position must precede end position.
- **Non-consecutive Insertions (`c.25_28insG`):** Violation of HGVS rule stating inserted sequence must be flanked by consecutive nucleotides.
- **Reference Base Mismatches (`c.9delA`, `c.118A>T`, `c.20G>T`, `c.92+5A>C`):** User-supplied reference allele conflicts with the immutable RefSeq `NM_000518.5` or `NG_000007.3` standard.
- **Transcript Out-of-Bounds (`c.999C>T`):** Coordinate 999 exceeds total transcript length (628 bp).
- **Intron Out-of-Bounds (`c.92+999G>A`, `c.315+999G>A`):** Coordinate exceeds physical intron lengths (Intron 1: 130 bp, Intron 2: 850 bp).
- **Invalid Alphabets & Syntaxes:** Rejection of non-IUPAC bases, missing operators, and legacy numeric syntax.
