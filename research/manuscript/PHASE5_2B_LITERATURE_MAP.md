# Phase 5.2B — Introduction Literature Evidence Map

> **Document Type:** PRE-DRAFTING LITERATURE EVIDENCE MAPPING ARTIFACT  
> **Target Manuscript:** HBB Gene Mutation Analyzer Research Manuscript  
> **Stage:** Phase 5.2B — Stage A (Literature Evidence Lock)  
> **Governing Documents:** `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md`, `research/manuscript/PHASE5_2A_TITLE_ABSTRACT.md`, `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md`  
> **Governing Dataset Hash:** `research/manifest/phase2c_primary.sha256` (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Quality Standard:** Peer-reviewed primary literature, official international standards, and authoritative database publications only. Zero fabricated or unverified sources.

---

## 1. HBB Biology and Hemoglobinopathies

### Topic Overview
The human beta-globin gene (*HBB*) encodes the beta-globin subunit ($\beta$-globin) of adult hemoglobin ($HbA$, $\alpha_2\beta_2$). Pathogenic sequence alterations in *HBB* result in autosomal recessive hemoglobinopathies, predominantly $\beta$-thalassemia (characterized by deficient or absent $\beta$-chain synthesis) and structural hemoglobin variants such as sickle cell hemoglobin ($HbS$, $\beta^S$). The molecular spectrum of *HBB* is exceptionally diverse, encompassing single-nucleotide substitutions, small insertions and deletions, canonical and non-canonical splicing disruptions, regulatory promoter and polyadenylation variants, and large gene cluster deletions.

### Evaluated Sources

#### Source LIT-01 (Approved)
- **Citation:** Thein SL. The molecular basis of $\beta$-thalassemia. *Cold Spring Harbor Perspectives in Medicine*. 2013;3(5):a011700.
- **Identifiers:** DOI: [10.1101/cshperspect.a011700](https://doi.org/10.1101/cshperspect.a011700) | PMID: 23637309 | PMCID: PMC3633182
- **Topic:** *HBB* molecular spectrum and pathogenesis of $\beta$-thalassemia.
- **Specific Claims Supported:**
  1. *HBB* encodes the 146-amino-acid mature $\beta$-globin polypeptide that forms adult hemoglobin $HbA$ ($\alpha_2\beta_2$).
  2. Point mutations, small insertions, and deletions across the three exons, two introns, and regulatory regions of *HBB* lead to $\beta^0$ (absent $\beta$-globin) or $\beta^+$ (reduced $\beta$-globin) phenotypes.
  3. Over 300 distinct pathogenic variants have been characterized, displaying remarkable molecular heterogeneity across different geographic populations.
  4. Splicing mutations include both canonical dinucleotide disruptions (donor GT, acceptor AG) and cryptic/consensus splice site alterations.
- **Authoritative Status:** Foundational, peer-reviewed comprehensive review authored by an international leader in hemoglobin genetics (Senior Investigator at NIH/NHLBI).

#### Source LIT-02 (Approved)
- **Citation:** Taher AT, Weatherall DJ, Cappellini MD. Thalassaemia. *The Lancet*. 2018;391(10116):155–167.
- **Identifiers:** DOI: [10.1016/S0140-6736(17)31822-6](https://doi.org/10.1016/S0140-6736(17)31822-6) | PMID: 28774421
- **Topic:** Clinical relevance, epidemiology, and pathophysiological mechanisms of thalassemia.
- **Specific Claims Supported:**
  1. Hemoglobinopathies represent the most prevalent monogenic disorders globally.
  2. Imbalance of globin chain synthesis leads to ineffective erythropoiesis and peripheral hemolysis.
  3. Precise molecular diagnosis is essential for clinical management, prenatal screening, and genetic counseling.
- **Authoritative Status:** Authoritative seminar in *The Lancet* authored by leading pioneers in hemoglobinopathy medicine (including the late Sir David Weatherall).

#### Source LIT-03 (Approved)
- **Citation:** Weatherall DJ. The inherited diseases of hemoglobin are an emerging global health burden. *Blood*. 2010;115(22):4331–4336.
- **Identifiers:** DOI: [10.1182/blood-2010-01-251348](https://doi.org/10.1182/blood-2010-01-251348) | PMID: 20237318
- **Topic:** Global health burden and demographic distribution of hemoglobin disorders.
- **Specific Claims Supported:**
  1. Genetic disorders of hemoglobin constitute a substantial global public health burden, historically concentrated in malaria-endemic belts and increasingly distributed globally through international migration.
  2. Molecular categorization is foundational to understanding phenotypic severity.
- **Authoritative Status:** Seminal plenary paper in *Blood* from the Medical Research Council Molecular Haematology Unit, University of Oxford.

#### Source LIT-04 (Approved)
- **Citation:** Giardine B, van Baal S, Kaimakis P, et al. HbVar database of human hemoglobin variants and thalassemia mutations: 2007 update. *Human Mutation*. 2007;28(2):206.
- **Identifiers:** DOI: [10.1002/humu.9479](https://doi.org/10.1002/humu.9479) | PMID: 17221867
- **Topic:** Locus-specific mutation repository for hemoglobin variants.
- **Specific Claims Supported:**
  1. Systematic catalogs of hemoglobin variants demonstrate the continuous discovery and wide spectrum of non-deletional and deletional *HBB* mutations.
  2. Highlights historical nomenclature complexities where mature protein numbering omits the initiator methionine.
- **Authoritative Status:** Official primary publication for the HbVar locus-specific mutation database.

---

## 2. HGVS Nomenclature

### Topic Overview
The Human Genome Variation Society (HGVS) nomenclature guidelines represent the international consensus standard for reporting sequence variants. Clear communication of genetic variants requires strict adherence to standardized syntax anchored to defined reference sequences, separating cDNA-level descriptions ($c.$) from predicted or observed protein consequences ($p.$) and genomic coordinates ($g.$).

### Evaluated Sources

#### Source LIT-05 (Approved)
- **Citation:** den Dunnen JT, Dalgleish R, Maglott DR, Hart RK, Greenblatt MS, McGowan-Jordan J, Roux AF, Smith T, Antonarakis SE, Taschner PE. HGVS Recommendations for the Description of Sequence Variants: 2016 Update. *Human Mutation*. 2016;37(6):564–569.
- **Identifiers:** DOI: [10.1002/humu.22981](https://doi.org/10.1002/humu.22981) | PMID: 26931183 | PMCID: PMC5089531
- **Topic:** International standards for sequence variant nomenclature.
- **Specific Claims Supported:**
  1. Standardized nomenclature is vital to prevent ambiguity in clinical reporting, scientific literature, and genomic databases.
  2. Descriptions must be unequivocally anchored to a specified, versioned public reference sequence.
  3. Coding DNA descriptions ($c.$) use position $+1$ as the A of the ATG translation initiation codon and $-1$ as the nucleotide immediately $5'$ of ATG.
  4. Explicit formatting rules define substitutions, insertions, deletions, duplications, frameshifts, and splicing junction variants.
  5. Protein descriptions ($p.$) should distinguish between three-letter amino acid codes and describe consequences such as missense substitutions, terminations, and reading frame shifts ($fs$).
- **Authoritative Status:** Official international standard published by the HGVS Variant Nomenclature Committee (HVNC), universally cited across clinical genetics and bioinformatics.

---

## 3. Reference Sequence Dependence

### Topic Overview
Variant descriptions are fundamentally relative to the reference sequence model employed. Changes in transcript versions, choice between alternative isoforms, and differences between genomic coordinates (e.g., GRCh37 vs GRCh38) and transcript cDNA coordinates can alter variant notation, coordinate offsets, and consequence interpretation.

### Evaluated Sources

#### Source LIT-06 (Approved)
- **Citation:** O'Leary NA, Wright MW, Brister JR, et al. Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. *Nucleic Acids Research*. 2016;44(D1):D733–D745.
- **Identifiers:** DOI: [10.1093/nar/gkv1189](https://doi.org/10.1093/nar/gkv1189) | PMID: 26553804 | PMCID: PMC4702849
- **Topic:** NCBI RefSeq reference sequence standard and curation.
- **Specific Claims Supported:**
  1. The NCBI Reference Sequence (RefSeq) database provides curated, non-redundant, explicitly versioned genomic, transcript, and protein sequence records.
  2. Versioned RefSeq accessions (such as `NM_000518.5` for *HBB*) provide the invariant sequence foundation required for reproducible coordinate mapping and annotation.
- **Authoritative Status:** Standard official publication for NCBI RefSeq.

#### Source LIT-07 (Approved)
- **Citation:** Morales J, Pujar S, Loveland JE, Astashyn A, Bennett R, Berry A, Cox E, Davidson C, Fatumo S, Haggerty L, et al. A joint NCBI and EMBL-EBI transcript set for clinical genomics and research. *Nature*. 2022;604(7905):310–315.
- **Identifiers:** DOI: [10.1038/s41586-022-04558-8](https://doi.org/10.1038/s41586-022-04558-8) | PMID: 35418685 | PMCID: PMC9020964
- **Topic:** Matched Annotation from NCBI and EMBL-EBI (MANE) transcript standards.
- **Specific Claims Supported:**
  1. Discrepancies between transcript models historically contributed to conflicting clinical variant interpretations and reporting errors across diagnostic laboratories.
  2. MANE establishes a single high-confidence representative transcript per protein-coding gene (MANE Select) to harmonize clinical variant reporting between RefSeq and Ensembl/GENCODE.
  3. `NM_000518.5` represents the canonical MANE Select transcript for human *HBB*.
- **Authoritative Status:** Landmark collaborative paper in *Nature* establishing the current global standard for clinical transcript selection.

---

## 4. Computational Molecular Consequence Prediction

### Topic Overview
Computational variant effect annotators map sequence variants onto gene transcript structures to infer the immediate molecular consequence (e.g., synonymous, missense, stop-gained, frameshift, canonical splice donor/acceptor disruption). Deterministic rule-based engines rely on the universal genetic code and transcript coordinate geometry, operating distinctly from machine-learning pathogenicity scoring algorithms.

### Evaluated Sources

#### Source LIT-08 (Approved)
- **Citation:** McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GRS, Thormann A, Flicek P, Cunningham F. The Ensembl Variant Effect Predictor. *Genome Biology*. 2016;17(1):122.
- **Identifiers:** DOI: [10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4) | PMID: 27268795 | PMCID: PMC4893625
- **Topic:** Principles of sequence-based variant consequence annotation.
- **Specific Claims Supported:**
  1. Sequence-based consequence annotators deterministically classify the biochemical impact of variants on transcripts using standardized Sequence Ontology terms.
  2. Consequence classification utilizes transcript annotations to evaluate coding sequence alterations, reading frames, and splice junctions.
- **Authoritative Status:** Standard reference for Ensembl VEP, the global standard toolset for variant consequence prediction.

#### Source LIT-09 (Approved)
- **Citation:** Wang K, Li M, Hakonarson H. ANNOVAR: functional annotation of genetic variants from high-throughput sequencing data. *Nucleic Acids Research*. 2010;38(16):e164.
- **Identifiers:** DOI: [10.1093/nar/gkq603](https://doi.org/10.1093/nar/gkq603) | PMID: 20601685 | PMCID: PMC2952850
- **Topic:** Rule-based gene-based variant consequence calculation.
- **Specific Claims Supported:**
  1. Gene-based annotation pipelines execute deterministic lookup and translation algorithms to categorize variants into discrete molecular classes.
  2. Distinguishes deterministic sequence impact annotation from statistical or evolutionary conservation scoring.
- **Authoritative Status:** Foundational bioinformatics tool with over 10,000 citations, establishing standard computational methods for gene-based variant annotation.

---

## 5. Molecular Consequence vs. Clinical Significance

### Topic Overview
A critical conceptual boundary exists between *molecular consequence* and *clinical significance*. Molecular consequence is a deterministic biochemical descriptor of how a sequence alteration impacts the transcript or protein. Clinical significance (pathogenicity) is an evaluative judgment regarding whether that consequence causes human disease in a patient, requiring multi-layered clinical, population, and segregation evidence.

### Evaluated Sources

#### Source LIT-10 (Approved)
- **Citation:** Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, Grody WW, Hegde M, Lyon E, Spector E, Voelkerding K, Rehm HL; ACMG Laboratory Quality Assurance Committee. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genetics in Medicine*. 2015;17(5):405–424.
- **Identifiers:** DOI: [10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30) | PMID: 25741868 | PMCID: PMC4544753
- **Topic:** Professional standards for classifying sequence variants into clinical pathogenicity categories.
- **Specific Claims Supported:**
  1. Establishes a five-tier classification for sequence variants: Pathogenic, Likely Pathogenic, Uncertain Significance (VUS), Likely Benign, and Benign.
  2. Molecular consequence (such as a null variant or missense alteration) serves as an initial component of evidence (e.g., PVS1 criterion for null variants) but is not alone sufficient to define clinical pathogenicity without context regarding gene disease mechanism, population frequency, and clinical evidence.
  3. Demonstrates that computational consequence annotation must remain conceptually and operationally distinct from clinical diagnostic classification.
- **Authoritative Status:** The global gold standard for clinical variant interpretation, endorsed by ACMG, AMP, and CAP.

#### Source LIT-11 (Approved)
- **Citation:** Rehm HL, Berg JS, Brooks LD, et al. ClinGen — the Clinical Genome Resource. *New England Journal of Medicine*. 2015;372(23):2235–2242.
- **Identifiers:** DOI: [10.1056/NEJMp1503109](https://doi.org/10.1056/NEJMp1503109) | PMID: 26014582 | PMCID: PMC4474187
- **Topic:** Framework for authoritative variant curation and knowledge curation.
- **Specific Claims Supported:**
  1. Variant curation requires standardizing evidence curation across clinical and molecular domains.
  2. Distinguishes raw variant annotation from consensus expert-panel clinical curation.
- **Authoritative Status:** Definitive publication from the NIH-funded Clinical Genome Resource.

---

## 6. External Annotation Resources and ClinVar

### Topic Overview
NCBI ClinVar serves as the central public archive connecting human genomic variants with clinical interpretations and supporting evidence submitted by clinical laboratories, research centers, and expert panels. While indispensable as an external annotation resource, ClinVar aggregate records reflect submitter consensus and historical curation rather than primary in vitro experiments, and records contain varying review statuses and occasional nomenclature differences.

### Evaluated Sources

#### Source LIT-12 (Approved)
- **Citation:** Landrum MJ, Lee JM, Benson M, Brown GR, Chao C, Chitipothu S, Falx B, Foster J, Gu B, He J, et al. ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Research*. 2018;46(D1):D1062–D1067.
- **Identifiers:** DOI: [10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153) | PMID: 29165669 | PMCID: PMC5753237
- **Topic:** Architecture, submitter data model, and review status of NCBI ClinVar.
- **Specific Claims Supported:**
  1. ClinVar aggregates variant interpretations submitted by external laboratories and curates them into consensus records (Variation IDs and VCV records).
  2. Submissions include variant identifiers, HGVS expressions, asserted molecular consequences, and clinical significance classifications.
  3. A four-star review system grades the strength of assertion evidence, from zero stars (single submitter, criteria not provided) up to four stars (practice guideline).
  4. ClinVar does not independently perform experimental validation; its entries represent submitter assertions.
- **Authoritative Status:** Standard NCBI publication documenting ClinVar database structure and curation workflow.

#### Source LIT-13 (Approved)
- **Citation:** Harrison SM, Dolinsky JS, Knight Johnson AE, Pesaran T, Azzariti DR, Bale S, Cecchi AC, Faucett WA, Landrum MJ, Mao R, Moyer K, Rehm HL. Clinical laboratories collaborate to resolve differences in variant interpretations submitted to ClinVar. *Genetics in Medicine*. 2017;19(10):1096–1104.
- **Identifiers:** DOI: [10.1038/gim.2017.14](https://doi.org/10.1038/gim.2017.14) | PMID: 28301460 | PMCID: PMC5599322
- **Topic:** Discrepancies and conflict resolution in ClinVar submitter interpretations.
- **Specific Claims Supported:**
  1. Differences in interpretation and variant representation occur across submitting laboratories due to differing criteria, historical annotations, and transcript references.
  2. Submitter consensus represents an aggregated comparative reference, not an error-free biological absolute.
- **Authoritative Status:** High-impact empirical study investigating ClinVar concordance and conflict resolution across major clinical diagnostic laboratories.

#### Source LIT-17 (Approved)
- **Citation:** Landrum MJ, Chitipiralla S, Brown GR, Chen C, Gu B, Hart J, Hoffman D, Jang W, Kaur K, Liu C, Lyoshin V, Maddipatla Z, Maiti R, Mitchell J, O'Leary N, Riley GR, Shi W, Zhou G, Schneider V, Maglott D, Holmes JB, Kattman BL. ClinVar: improvements to accessing data. *Nucleic Acids Research*. 2020;48(D1):D835–D844.
- **Identifiers:** DOI: [10.1093/nar/gkz972](https://doi.org/10.1093/nar/gkz972) | PMID: 31777943 | PMCID: PMC6943040
- **Topic:** NCBI ClinVar data access improvements, Variation page redesign, public archive expansion, and submitter consensus models.
- **Specific Claims Supported:**
  1. ClinVar serves as a freely available public archive of human genetic variants and interpretations of their relationships to diseases, aggregating submitter data from clinical laboratories, research centers, and expert panels.
  2. Documents improvements to accessing ClinVar data, programmatic access via E-utilities and FTP, and standardized variation reporting.
  3. Reaffirms that ClinVar archives submitter assertions and diagnostic laboratory consensus rather than primary in vitro experimental data.
- **Authoritative Status:** Official NCBI 2020 update publication for ClinVar.

---

## 7. Reproducible Computational Evaluation

### Topic Overview
Evaluating bioinformatics software requires transparent, reproducible benchmarking practices. Established standards emphasize frozen candidate manifests, locked and pre-specified comparison protocols, rigorous isolation of software regression baselines from external comparisons, exact statistical confidence intervals, and explicit disclosure of selection bias and unrepresented classes.

### Evaluated Sources

#### Source LIT-14 (Approved)
- **Citation:** Krusche P, Trigg L, Boutros PC, et al. Best practices for benchmarking germline small-variant calls in human genomes. *Nature Biotechnology*. 2019;37(5):555–560.
- **Identifiers:** DOI: [10.1038/s41587-019-0054-x](https://doi.org/10.1038/s41587-019-0054-x) | PMID: 30858583
- **Topic:** GA4GH international guidelines for reproducible genomic variant benchmarking.
- **Specific Claims Supported:**
  1. Standardized benchmarking requires defining high-confidence comparison regions/cohorts, explicitly pre-specifying evaluation metrics, and harmonizing representation differences.
  2. Emphasizes that discrepancies often arise from alternative representations of identical biological events rather than true algorithmic failure.
  3. Recommends class-stratified reporting and transparent disclosure of evaluation boundaries.
- **Authoritative Status:** Landmark community standard formulated by the Global Alliance for Genomics and Health (GA4GH) Benchmarking Team.

#### Source LIT-15 (Approved)
- **Citation:** Stodden V, McNutt M, Bailey DH, Deelman E, Gil Y, Hanson B, Heroux MA, Ioannidis JPA, Taufer M. Enhancing reproducibility for computational methods. *Science*. 2016;354(6317):1240–1241.
- **Identifiers:** DOI: [10.1126/science.aah6168](https://doi.org/10.1126/science.aah6168) | PMID: 27940837
- **Topic:** Standards for computational scientific reproducibility.
- **Specific Claims Supported:**
  1. Computational scientific findings require complete transparency of code, frozen datasets, execution environments, and evaluation workflows to enable independent audit.
  2. Predefined evaluation protocols and version control integrity prevent retrospective parameter tuning and outcome inflation.
- **Authoritative Status:** Influential policy perspective in *Science* addressing computational reproducibility across disciplines.

#### Source LIT-16 (Approved)
- **Citation:** Clopper CJ, Pearson ES. The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika*. 1934;26(4):404–413.
- **Identifiers:** DOI: [10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404)
- **Topic:** Exact binomial confidence intervals for proportional success metrics.
- **Specific Claims Supported:**
  1. When binomial sample proportions equal 100% ($k = n$), standard normal asymptotic approximations (Wald intervals) fail due to zero standard error; exact Clopper-Pearson confidence limits must be computed based on the incomplete beta distribution.
- **Authoritative Status:** Classical statistical foundation for exact binomial interval estimation.

---

## 8. Citation Quality Assessment Summary

| Source ID | Citation Short Form | Topic Domain | Verification Status | Reason for Approval |
|:---:|---|---|:---:|---|
| **LIT-01** | Thein (2013) *CSH Perspect Med* | *HBB* Molecular Biology & $\beta$-Thal | **APPROVED** | Primary authoritative review on *HBB* mutation spectrum. |
| **LIT-02** | Taher et al. (2018) *Lancet* | Hemoglobinopathy Clinical Context | **APPROVED** | Definitive clinical seminar in *The Lancet*. |
| **LIT-03** | Weatherall (2010) *Blood* | Hemoglobinopathy Global Burden | **APPROVED** | Classic plenary perspective on global burden. |
| **LIT-04** | Giardine et al. (2007) *Hum Mutat* | HbVar Locus-Specific Database | **APPROVED** | Official publication of the HbVar mutation repository. |
| **LIT-05** | den Dunnen et al. (2016) *Hum Mutat* | HGVS Nomenclature Standards | **APPROVED** | Official international HGVS recommendation standard. |
| **LIT-06** | O'Leary et al. (2016) *Nucleic Acids Res* | NCBI RefSeq Standard | **APPROVED** | Official publication for RefSeq curated reference models. |
| **LIT-07** | Morales et al. (2022) *Nature* | MANE Select Transcript Standard | **APPROVED** | Definitive *Nature* paper establishing MANE Select (`NM_000518.5`). |
| **LIT-08** | McLaren et al. (2016) *Genome Biol* | Variant Effect Prediction (VEP) | **APPROVED** | Definitive methodology paper for computational consequence annotation. |
| **LIT-09** | Wang et al. (2010) *Nucleic Acids Res* | ANNOVAR Gene-Based Annotation | **APPROVED** | Foundational paper on rule-based variant consequence derivation. |
| **LIT-10** | Richards et al. (2015) *Genet Med* | ACMG/AMP Clinical Variant Guidelines | **APPROVED** | Global standard establishing separation of consequence from clinical classification. |
| **LIT-11** | Rehm et al. (2015) *N Engl J Med* | ClinGen Curation Framework | **APPROVED** | Landmark paper on clinical genomics curation. |
| **LIT-12** | Landrum et al. (2018) *Nucleic Acids Res* | NCBI ClinVar Architecture | **APPROVED** | Standard reference for ClinVar data model and review tiers. |
| **LIT-13** | Harrison et al. (2017) *Genet Med* | ClinVar Inter-Laboratory Concordance | **APPROVED** | Empirical demonstration that ClinVar represents consensus, not absolute truth. |
| **LIT-14** | Krusche et al. (2019) *Nat Biotechnol* | GA4GH Benchmarking Best Practices | **APPROVED** | Community standard for genomic variant benchmarking and representation handling. |
| **LIT-15** | Stodden et al. (2016) *Science* | Computational Reproducibility | **APPROVED** | Foundational *Science* policy paper on reproducible computational workflows. |
| **LIT-16** | Clopper & Pearson (1934) *Biometrika* | Exact Binomial Confidence Limits | **APPROVED** | Standard mathematical derivation of exact Clopper-Pearson confidence intervals. |
| **LIT-17** | Landrum et al. (2020) *Nucleic Acids Res* | NCBI ClinVar Access Improvements & Public Archive | **APPROVED** | Authoritative NCBI update publication for ClinVar. |

**Total Sources Evaluated:** 17  
**Total Approved for Manuscript:** 17  
**Total Rejected / Unverified:** 0  

---

## 9. Synthesis of Sources Approved for Manuscript

All 17 evaluated sources are formally approved for citation in the manuscript. Each source directly addresses a specific thematic requirement established in the literature protocol and satisfies the zero-fabrication criteria:

1. **HBB Biology:** Thein (2013) [LIT-01], Taher et al. (2018) [LIT-02], Weatherall (2010) [LIT-03], Giardine et al. (2007) [LIT-04].
2. **HGVS Nomenclature:** den Dunnen et al. (2016) [LIT-05].
3. **Reference Sequence Dependence:** O'Leary et al. (2016) [LIT-06], Morales et al. (2022) [LIT-07].
4. **Computational Molecular Consequence:** McLaren et al. (2016) [LIT-08], Wang et al. (2010) [LIT-09].
5. **Molecular Consequence vs Clinical Significance:** Richards et al. (2015) [LIT-10], Rehm et al. (2015) [LIT-11].
6. **ClinVar Reference Characterization:** Landrum et al. (2018) [LIT-12], Landrum et al. (2020) [LIT-17], Harrison et al. (2017) [LIT-13].
7. **Reproducible Evaluation & Statistics:** Krusche et al. (2019) [LIT-14], Stodden et al. (2016) [LIT-15], Clopper & Pearson (1934) [LIT-16].

*Literature mapping reconciled and verified. Total approved sources: 17.*
