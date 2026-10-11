# Concordance Evaluation of Deterministic HBB Molecular Consequence Prediction Against a Curated ClinVar-Derived External Annotation Reference

**[Author Name(s) Placeholder — To be determined by Authors]**  
*[Institutional Affiliation(s) Placeholder — To be determined by Authors]*  
*[Corresponding Author Contact Placeholder — To be determined by Authors]*  
*[ORCID Identifier(s) Placeholder — To be determined by Authors]*  

---

## Abstract

### Background
Accurate interpretation of sequence variants in the human beta-globin gene (*HBB*) requires precise, deterministic molecular consequence computation from standardized Human Genome Variation Society (HGVS) syntax mapped against canonical reference transcripts (RefSeq `NM_000518.5`). In computational variant curation and clinical bioinformatics pipelines, objective molecular consequence categorization must remain strictly distinct from evaluative clinical significance or pathogenicity predictions.

### Objective
To evaluate whether a dedicated, deterministic rule-based computational pipeline derives *HBB* molecular consequence categories concordant with curated external molecular annotations derived from the National Center for Biotechnology Information (NCBI) ClinVar database under a predefined, protocol-locked evaluation framework.

### Methods
A pure-Python deterministic molecular consequence engine anchored strictly to RefSeq `NM_000518.5` (MANE Select) was evaluated against a frozen primary cohort of 55 curated *HBB* sequence variants. External reference comparators were normalized ClinVar-derived external molecular annotations. The predefined primary evaluation endpoint evaluated concordance between runtime deterministic predictions (Entity $A$) and normalized external annotations (Entity $C$), with stored regression baselines (Entity $B$) strictly isolated from concordance logic. Two-sided exact 95% Clopper-Pearson binomial confidence intervals were computed. Secondary endpoints evaluated exact protein nomenclature agreement and error categorization. Input validation and error-handling architecture were assessed using an isolated cohort of 18 synthetic negative controls.

### Results
Runtime deterministic molecular consequence predictions achieved 100.00% concordance (55/55 matches, 0 discrepancies; exact 95% Clopper-Pearson CI: [93.51%, 100.00%]) with curated ClinVar-derived external molecular annotations across seven represented biological mutation classes (30 exact molecular agreements, 20 molecular agreements with protein representation differences, and 5 external annotations lacking protein strings). Secondary exact protein nomenclature concordance was 50.91% (28/55; exact 95% CI: [37.07%, 64.65%]), reflecting 20 shorthand truncated frameshift representations, 5 omitted splice protein strings in ClinVar records, and 2 non-coding 3' UTR variants for which protein consequence matching was not applicable. In an isolated negative-control experiment, 18 of 18 synthetic malformed inputs (100.00%; exact 95% CI: [81.47%, 100.00%]) were gracefully rejected with typed exceptions and zero unhandled runtime crashes. Software regression testing reproduced historical expected outputs with 100.00% invariance (55/55).

### Limitations
All 55 primary candidates were derived exclusively from ClinVar submissions without independent secondary database corroboration (`independent_non_clinvar_corroboration == "NONE"`). Candidate qualification during curation required deterministic engine agreement (`comparison_status == "EXACT_AGREEMENT"`), introducing substantial incorporation (verification) bias that restricts generalizability to unselected or novel clinical variants. Four biological classes (C05 in-frame indels / deletions, C07 in-frame insertions / duplications, C08 splice donor disruptions, and C10 5' UTR regulatory variants) had zero primary candidates ($n = 0$), and classes C02 ($n = 3$) and C11 ($n = 2$) exhibited limited sample sizes with wide confidence intervals. This study evaluates computational molecular consequence categorization only; it does not assess clinical significance, ACMG/AMP pathogenicity, diagnostic accuracy, or clinical utility.

### Conclusion
The deterministic pipeline demonstrated complete molecular consequence concordance within the pre-screened, frozen curated cohort against curated ClinVar-derived external molecular annotations. These findings establish computational rule execution fidelity and reference coordinate alignment under a locked protocol, but do not establish independent biological ground truth, clinical validity, or prospective diagnostic accuracy.

---

## Keywords
*HBB*; beta-globin; hemoglobinopathies; molecular consequence; deterministic algorithms; HGVS nomenclature; ClinVar; computational benchmarking; variant curation; reproducible bioinformatics

---

## 1. Introduction

### 1.1 HBB Biology and Molecular Variant Interpretation
The human beta-globin gene (*HBB*), located within the beta-globin cluster on chromosome 11 (11p15.4), encodes the 146-amino-acid beta-globin subunit ($\beta$-globin). In adults, two beta-globin and two alpha-globin polypeptides assemble with four heme groups into tetrameric adult hemoglobin ($HbA$, $\alpha_2\beta_2$), the primary erythrocyte oxygen carrier (Thein, 2013). Inherited sequence variants in *HBB* underlie the most prevalent monogenic disorders worldwide, causing diverse hemoglobinopathies that include the $\beta$-thalassemias and structural variants such as sickle cell hemoglobin ($HbS$) (Weatherall, 2010; Taher et al., 2018). The molecular pathology of *HBB* exhibits marked allelic heterogeneity: over 300 distinct pathogenic variants have been documented, encompassing single-nucleotide substitutions, small insertions and deletions, canonical splice-site disruptions, and regulatory alterations across the three exons, two introns, and untranslated regions (Thein, 2013; Giardine et al., 2007). Precise molecular characterization of *HBB* sequence variants is therefore fundamental to genomic research, molecular diagnostics, and sequence-based variant classification.

### 1.2 Standardized Variant Representation and Legacy Numbering
Systematic variant interpretation depends on standardized, unambiguous sequence nomenclature. The Human Genome Variation Society (HGVS) guidelines provide the international consensus framework for describing sequence variants across DNA, RNA, and protein levels (den Dunnen et al., 2016). Modern HGVS recommendations require sequence alterations to be anchored to a defined, versioned reference sequence, distinguishing coding DNA ($c.$) from predicted protein consequences ($p.$) and genomic coordinates ($g.$). 

In hemoglobin genetics, standardized representation is especially critical due to persistent legacy practices: beta-globin alterations were historically numbered from the amino-terminal valine of the mature polypeptide—omitting the initiator methionine—yielding widely recognized clinical designations such as "Glu6Val" for sickle cell hemoglobin or "Glu26Lys" for hemoglobin E (Thein, 2013). Under modern HGVS standards, which designate the initiator methionine as codon 1, these variants correspond respectively to `p.Glu7Val` ($c.20A>T$) and `p.Glu27Lys` ($c.79G>A$) (den Dunnen et al., 2016). Resolving such legacy offsets and ensuring consistent syntactic translation require rigorous computational adherence to standardized reference models.

Beyond nomenclature syntax, variant interpretation is inherently dependent on the underlying reference sequence model. Coordinates, exon boundaries, reading frames, and canonical splice junctions are defined strictly relative to a specific reference transcript (O'Leary et al., 2016). Genomic (e.g., GRCh38) and transcript cDNA systems differ in numbering, and variants in overlapping genes, alternative isoforms, or untranslated regions can yield conflicting consequence assignments if the transcript reference is unspecified. To harmonize clinical reporting across databases, the Matched Annotation from NCBI and EMBL-EBI (MANE) initiative established MANE Select transcripts (Morales et al., 2022). For the human *HBB* locus, RefSeq accession `NM_000518.5` serves as the canonical MANE Select transcript, establishing an invariant reference framework for unambiguous sequence evaluation.

### 1.3 Deterministic Molecular Consequence Computation
In contemporary bioinformatics workflows, the initial step in evaluating a sequence variant is computational molecular consequence prediction. Tools such as the Ensembl Variant Effect Predictor (VEP) (McLaren et al., 2016) and ANNOVAR (Wang et al., 2010) map alterations onto transcripts to deterministically infer biochemical impact on coding sequences—categorizing variants into synonymous, missense, nonsense, frameshift, and canonical splice disruptions. This rule-based molecular consequence determination relies on deterministic computational logic: the universal genetic code, precise coordinate geometry, and codified boundary rules governing open reading frames and canonical dinucleotide splice junctions (GT at donor sites and AG at acceptor sites). 

Crucially, deterministic consequence calculation operates independently of statistical or machine-learning pathogenicity predictors, which estimate disease likelihood from phylogenetic conservation or structural features rather than computing direct sequence translation. In the present study, computational evidence retrieval and literature summarization are architecturally decoupled from deterministic consequence determination, ensuring that algorithmic execution remains strictly rule-based and reproducible.

### 1.4 Distinguishing Molecular Consequence from Clinical Significance
A fundamental principle in clinical and computational genetics is the conceptual distinction between molecular consequence and clinical significance. As articulated in the joint consensus standards of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology (ACMG/AMP), molecular consequence describes the intrinsic biochemical or structural impact of a variant on the transcript or protein product (Richards et al., 2015). In contrast, clinical significance (pathogenicity) represents an evaluative determination of whether that molecular alteration causes human disease in a patient (Richards et al., 2015; Rehm et al., 2015). 

While molecular consequence serves as an essential input into clinical interpretation—such as establishing predicted loss of function for ACMG criterion PVS1—molecular consequence alone does not determine clinical pathogenicity. For example, a frameshift insertion is biochemically categorized as a null variant regardless of whether the affected gene causes haploinsufficiency, while missense variants with identical consequence categories can range from completely benign population polymorphisms to severe disease-causing alleles. Maintaining strict operational separation between molecular consequence derivation and clinical classification is therefore paramount to avoid overclaiming computational diagnostic capability.

### 1.5 External Annotation Resources and NCBI ClinVar
To benchmark and evaluate computational variant analysis tools, researchers frequently turn to public knowledgebases, most prominently NCBI ClinVar. ClinVar serves as the central public archive aggregating human genetic variants, associated phenotypes, and clinical significance interpretations submitted by clinical laboratories, diagnostic testing facilities, and expert panels (Landrum et al., 2018; Landrum et al., 2020). ClinVar records provide standardized HGVS syntax, molecular consequence terms, and submitter classifications graded across a four-star review status system. 

However, ClinVar entries represent aggregated submitter assertions and literature consensus rather than primary in vitro experimental data, and substantial discordance can exist among submitters regarding variant interpretations, transcript choices, and protein nomenclature conventions (Harrison et al., 2017). Furthermore, variant repositories may contain historical annotation artifacts, such as truncated protein representations for frameshift variants or omitted protein consequence strings for non-coding and splice-site variants (Landrum et al., 2018). Consequently, ClinVar consensus records serve as a valuable external comparison reference, but cannot be treated as error-free biological ground truth.

### 1.6 Motivation and Research Gap
Despite the existence of broad genome-scale variant annotation suites, dedicated locus-specific analysis of *HBB* presents unique computational requirements, including the management of persistent legacy numbering offsets, handling of historical truncated protein nomenclature in external repositories, and rigorous architectural separation between deterministic rule execution and auxiliary evidence retrieval. General-purpose variant annotators are frequently embedded within extensive monolithic pipelines, making it challenging to isolate core sequence-transformation logic for transparent, reproducible evaluation. 

Best-practice guidelines for computational benchmarking emphasize that bioinformatics pipelines should be evaluated under predefined, frozen protocols that explicitly isolate primary performance endpoints from secondary exploratory comparisons, document representation differences, and transparently disclose selection biases and unrepresented mutation classes (Krusche et al., 2019; Stodden et al., 2016). The present study addresses this need by focusing specifically on deterministic, reference-aware derivation of molecular consequences for *HBB* variants and evaluating concordance against a curated external annotation reference under a frozen, audited computational protocol.

### 1.7 Study Objective and Contribution
The primary objective of this study was to evaluate deterministic molecular consequence prediction for *HBB* variants against curated ClinVar-derived external molecular annotations using a predefined, protocol-locked computational framework. We developed a dedicated, rule-based computational engine anchored strictly to RefSeq `NM_000518.5` and executed an audited benchmark against a frozen primary cohort of 55 curated *HBB* variants spanning seven biological mutation classes. The primary evaluation endpoint was predefined as molecular consequence concordance between runtime deterministic engine output and normalized external molecular annotations, with software regression baselines strictly isolated. Secondary analyses evaluated exact protein nomenclature concordance, documenting specific representation disparities such as truncated frameshifts. In addition, an isolated synthetic negative control cohort ($N = 18$) was evaluated to assess input-validation robustness. This study explicitly evaluates computational concordance with curated external annotations; it does not evaluate clinical significance, ACMG/AMP pathogenicity classification, diagnostic accuracy, or patient clinical outcomes.

Crucially, during CP2.2 curation, admission to the proposed primary cohort required deterministic engine agreement (`comparison_status == "EXACT_AGREEMENT"`). The primary cohort was therefore not selected independently of engine agreement, creating incorporation or verification bias. This selection mechanism limits interpretation of the observed concordance and prevents treating it as an unbiased estimate of performance on unseen *HBB* variants. Furthermore, while the primary cohort represents seven biological classes, four classes (C05 in-frame indels / deletions, C07 in-frame insertions / duplications, C08 splice donor disruptions, and C10 5' UTR regulatory variants) had zero primary candidates ($n = 0$) and were not evaluated in this benchmark. All 55 primary variants were derived exclusively from ClinVar records, and zero finalized independent non-ClinVar biological corroboration dossiers were available (`independent_non_clinvar_corroboration == "NONE"`).

---

## 2. Methods

### 2.1 Study Design and Mathematical Endpoint Decoupling
This study was designed as an independent, reproducible computational concordance evaluation of a deterministic molecular consequence engine for sequence variants in human *HBB*. The evaluation protocol was predefined and formally locked prior to benchmark execution, adhering to established guidelines for reproducible computational genomics and variant benchmarking (Krusche et al., 2019; Stodden et al., 2016). The benchmark was designed exclusively as a computational concordance assessment of molecular consequence categorization (e.g., Missense, Nonsense, Frameshift, Splice Acceptor). It does not constitute an independent biological validation study (as no in vitro cell assays, cDNA sequencing, or patient tissue analyses were performed), a clinical validation study, an evaluation of clinical utility, or a test of diagnostic sensitivity.

To prevent methodological circularity and outcome bias, the benchmark evaluation framework enforces strict mathematical and operational separation among three distinct data entities:
- **Entity $A$ (Runtime Engine Output):** The molecular consequence and protein consequence strings generated de novo by the deterministic engine during benchmark execution.
- **Entity $B$ (Frozen Expected Output):** Historical deterministic outputs stored in the candidate manifest during preliminary development, preserved strictly for post-hoc software regression and internal self-consistency checks.
- **Entity $C$ (External Molecular Annotation):** Independent molecular consequence consensus assertions curated from NCBI ClinVar records and normalized through locked semantic rules.

The primary evaluation endpoint of this study compares **Entity $A$ directly against Entity $C$ ($A$ vs $C$)**. Entity $B$ was completely excluded from the primary evaluation logic and did not participate in determining concordance.

### 2.2 Reference Sequence and Transcript Model
All sequence coordinates, genomic boundaries, and translation models in this study were anchored to versioned, curated RefSeq reference accessions (O'Leary et al., 2016). In accordance with the MANE initiative, RefSeq accession `NM_000518.5` was selected as the canonical MANE Select transcript model (Morales et al., 2022). Genomic sequence context was defined by RefSeqGene accession `NG_000007.3` on build GRCh38 (genomic locus coordinates 70545..72152, total length 1608 bp).

The canonical mature mRNA transcript `NM_000518.5` comprises the three spliced coding exons concatenated without intronic sequence, spanning 628 transcribed nucleotides in the project reference sequence model:
- **Exon 1:** Transcript nucleotides 1–142 (142 bp; genomic 70545..70686), containing 50 bp of 5' untranslated region ($c.-50$ to $c.-1$) and 92 bp of coding sequence ($c.1$ to $c.92$).
- **Exon 2:** Transcript nucleotides 143–365 (223 bp; genomic 70817..71039), containing 223 bp of coding sequence ($c.93$ to $c.315$).
- **Exon 3:** Transcript nucleotides 366–628 (263 bp; genomic 71890..72152), containing 129 bp of coding sequence ($c.316$ to $c.444$) and 134 bp of 3' untranslated region ($c.*1$ to $c.*134$).

The two intervening introns interrupting the mature coding exons are defined within the genomic gene locus `NG_000007.3`:
- **Intron 1 (IVS-1):** 130 bp intervening sequence situated between Exon 1 and Exon 2 ($c.92$ and $c.93$; genomic nucleotides 70687..70816).
- **Intron 2 (IVS-2):** 850 bp intervening sequence situated between Exon 2 and Exon 3 ($c.315$ and $c.316$; genomic nucleotides 71040..71889).

Under predecessor NCBI RefSeq record `NM_000518.4` (in effect February 11, 2003 until June 13, 2018) and associated historical literature, Exon 3 was annotated as spanning 261 bp with a 132 bp 3' UTR (yielding a 626 bp spliced transcript, $c.*1..c.*132$ terminating at `...TTCATTGC`); the updated RefSeq `NM_000518.5` standard and project reference files (`NM_000518.5.json` and `NM_000518.5.fasta`) explicitly incorporate the 628 bp reference model ($c.*1..c.*134$), reflecting the addition of two terminal adenines (`AA` at positions 627–628 supported by full-length cDNA clone BU661647.1).

The complete coding sequence (CDS) comprises 444 nucleotides ($c.1$ to $c.444$, 148 codons including termination), translating to a 147-amino-acid pre-protein (`NP_000509.1`). Post-translational removal of the amino-terminal initiator methionine yields the 146-amino-acid mature $\beta$-globin polypeptide (Thein, 2013). Reference sequences, exon-intron boundaries, and codon dictionaries were stored as immutable data structures within `backend/app/core/reference.py` to ensure that coordinate arithmetic remained strictly deterministic.

### 2.3 Variant Representation and HGVS Parsing
Sequence variants were represented using HGVS sequence variant nomenclature recommendations (den Dunnen et al., 2016). Input processing was implemented in a dedicated parsing module (`backend/app/core/hgvs.py`) enforcing a five-stage validation pipeline:
1. **Input Sanitization & Accession Validation:** Verifies HGVS cDNA syntax starting with `c.` and matches authorized *HBB* reference accessions (`NM_000518.5` or `NG_000007.3`). Direct genomic coordinate syntax (`g.`) is not parsed.
2. **Grammar and Token Parsing:** Regular expression grammars decompose strings into coordinate offsets, variant types (substitutions, deletions, insertions, duplications), reference alleles, and alternate alleles.
3. **Biological Coordinate Integrity:** Validates that coordinates exist within physical boundaries. Base zero ($c.0$) is strictly rejected; the base immediately preceding the initiation codon ($c.1$) is indexed as $c.-1$.
4. **Reference Allele Confirmation:** Matches the asserted reference nucleotide against the biological reference sequence: exonic and UTR variants are validated against the spliced transcript `NM_000518.5`, while intronic variants are mapped and validated against the genomic sequence `NG_000007.3`. Any mismatch between query allele and reference base triggers an explicit `REFERENCE_MISMATCH` error.
5. **Canonical Normalization:** Standardizes indels into uppercase DNA bases and converts intronic relative coordinates into transcript offsets.

#### Resolution of Historical Codon Numbering Offsets
In hemoglobin literature, variants have historically been numbered from the mature polypeptide's amino-terminal valine (Thein, 2013; Giardine et al., 2007). This created a systematic -1 amino acid offset relative to modern HGVS guidelines, where codon 1 designates the initiator methionine. For example, sickle cell hemoglobin (historical "Glu6Val") corresponds under HGVS nomenclature to `p.Glu7Val` ($c.20A>T$), and hemoglobin E (historical "Glu26Lys") corresponds to `p.Glu27Lys` ($c.79G>A$). The parser strictly enforces modern HGVS nomenclature anchored to codon 1 of `NM_000518.5` while mapping legacy aliases during curation to maintain consistency across historical records.

### 2.4 Deterministic Molecular Consequence Computation
Molecular consequence prediction was executed by a standalone deterministic bioinformatics engine (`backend/app/core/consequences.py`). The engine executes rule-based sequence transformations implemented in pure Python, containing zero stochastic machine-learning models, zero calls to large language model (LLM) APIs, and zero external network dependencies.

The computation employs the Standard Genetic Code (NCBI Translation Table 1) across defined mutation categories:
- **Coding Single Nucleotide Variants (SNVs):** For substitutions within $c.1..c.444$, the engine calculates the affected codon index ($\lceil c\_pos / 3 \rceil$), extracts the wild-type triplet, substitutes the mutant base, and translates both triplets. The event is categorized as **Synonymous** if the amino acid is unchanged, **Missense** if an alternative amino acid is encoded, or **Nonsense** if a premature termination codon (`Ter`, `*`) is introduced.
- **Frameshift Indels (Deletions, Insertions, Duplications):** For alterations whose net length is not a multiple of 3, the engine reconstructs the mutant transcript in silico. It identifies the first altered codon, translates subsequent codons in the shifted reading frame until encountering the first in-frame termination codon (`TAA`, `TAG`, `TGA`), and constructs full HGVS protein consequence syntax (e.g., `p.Glu7GlyfsTer...`).
- **Canonical Splicing Disruptions:** Variants located within the invariant 2-bp donor dinucleotide (`GT`, e.g., $c.92+1, c.92+2, c.315+1, c.315+2$) or acceptor dinucleotide (`AG`, e.g., $c.93-2, c.93-1, c.316-2, c.316-1$) are categorized respectively as **Splice Donor** or **Splice Acceptor** disruptions.
- **Untranslated Regions (UTRs):** Variants at $c. < 1$ are classified as **5' UTR Regulatory**, and variants at $c. > 444$ ($c.*1..c.*134$) are classified as **3' UTR Regulatory**.

#### Architectural Decoupling from AI Layer
In the complete software application, generative artificial intelligence is utilized strictly within a separate literature evidence retrieval and summarization module (`backend/app/ai.py`). The core consequence engine evaluated in this benchmark is architecturally decoupled from the AI layer; no generative model participated in consequence derivation, codon translation, or benchmark evaluation.

### 2.5 External Annotation Reference and Provenance Profile
The external reference comparator (Entity $C$) was curated from NCBI ClinVar (Landrum et al., 2018; Landrum et al., 2020). ClinVar aggregates variant submissions from clinical diagnostic laboratories, academic research centers, and expert panels:
- **Database Origin:** 100% (55/55) of candidates possess valid ClinVar Variation IDs and Variation Change Version (VCV) records.
- **Evidence Review Tiers:** 54 candidates (98.18%) possessed a review status of $\ge 2$ stars (criteria provided, multiple submitters, no conflicts). One candidate (1.82%; candidate `HBB-CP2-245`, $c.380T>G$, $p.Val127Gly$) possessed a 3-star review status (reviewed by an expert panel). Zero candidates possessed 0-star or 1-star ratings in the primary cohort.
- **Independent Corroboration:** Exactly 0 of the 55 primary candidates possessed independent biological corroboration dossiers outside of ClinVar (`independent_non_clinvar_corroboration == "NONE"`).

ClinVar entries reflect submitter consensus and reference assertions rather than primary in vitro experimental data (Harrison et al., 2017). Although 98.18% of primary records represent multiple-submitter consensus, multiple laboratory submissions to a central repository do not constitute independent biological validation experiments.

To guarantee benchmark reproducibility, all ClinVar annotations, review tiers, and submitter assertion strings were harvested, verified, and frozen into the local manifest (`research/manifest/phase2c_primary.json`). At execution time, the comparison engine operated strictly against this frozen manifest with zero network socket connections.

### 2.6 Cohort Construction and Methodological Disclosure of Incorporation Bias
The primary evaluation cohort ($N = 55$) was established through a multi-stage qualification pipeline during Checkpoints CP2.1 through CP2.3:
- Initial biological candidate pool: $N = 296$ variants (harvested from ClinVar).
- Disqualified in CP2.1/CP2.2 (`DO_NOT_USE`): $N = 53$ (historical overlap, deep intronic, prior exposure).
- Relegated in CP2.2 (`REVIEW_REQUIRED`): $N = 73$ (unsupported promoter $> -50$ bp, syntax ambiguity, 0-star conflicts).
- Relegated in CP2.2 (`PROPOSED_SECONDARY`): $N = 42$ (0-star records lacking criteria).
- Relegated in CP2.2 (`CONDITIONAL`): $N = 9$ (incomplete protein annotations).
- Qualified primary pool in CP2.2 (`PROPOSED_PRIMARY`): $N = 119$.
- Relegated in CP2.3 (`CONDITIONAL`): $N = 64$ (63 1-star single-submitter records, 1 multi-codon 25-amino-acid deletion).
- Final Approved Primary Cohort: **$N = 55$ biological variants**.

A critical methodological disclosure established during scientific audit must be emphasized: **candidate admission into the primary evaluation cohort required deterministic engine agreement during curation**. In `research/curation/run_independent_verification.py` (lines 231–246), assignment of a biological candidate to `PROPOSED_PRIMARY` required that `comparison_status == "EXACT_AGREEMENT"`. Candidates where the engine diverged from external annotations were diverted into secondary or exclusion registries. Furthermore, subsequent human review sampled exclusively from `PROPOSED_PRIMARY`.

In clinical epidemiology and computational validation, this practice introduces **incorporation bias** (also termed **verification bias**). Because cohort eligibility was conditioned on initial agreement with the evaluated engine, the primary cohort ($N = 55$) represents an **artificially enriched, highly concordant subset**. The resulting benchmark evaluates **software self-consistency, deterministic rule execution fidelity, and consensus database alignment on clean records**, rather than an unbiased, unselected prospective sample of all *HBB* variants.

### 2.7 Benchmark Freeze and Cryptographic Integrity Specifications
The evaluation cohort, protocol, and software environment were formally locked prior to benchmark execution:
- **Primary Manifest:** `research/manifest/phase2c_primary.json` ($N = 55$ biological variants; SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`).
- **Historical Baseline Manifest:** `research/manifest/frozen_test.json` (SHA256: `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994`; 0 overlapping candidates).
- **Benchmark Protocol Document:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (Version 1.0.0; SHA256: `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`).
- **Target Engine Commit:** Git commit `845f595cc039e006d74237945450c7b4a9569ee6`.
- **Execution Environment:** Python 3.14.7 (AMD64) on Windows 10 (Build 10.0.19045), recorded in `research/protocol/PHASE2C_ENVIRONMENT_RECORD.json`.

Cryptographic SHA256 hashing confirms artifact identity against pre-recorded values and confirms the absence of code drift or post-hoc manifest alteration. Cryptographic immutability does not eliminate retrospective curation selection bias or guarantee biological ground truth.

### 2.8 Primary and Secondary Evaluation Endpoints

#### Primary Evaluation Endpoint ($A$ vs $C$)
The predefined primary endpoint was **Molecular Consequence Concordance**, defined as the proportion of primary cohort candidates for which the runtime deterministic engine consequence (Entity $A$) matched the normalized external ClinVar molecular annotation (Entity $C$):
$$\text{Primary Concordance} = \frac{\sum_{i=1}^{N} \mathbb{I}(A_i^{\text{mol}} = C_i^{\text{mol}})}{N}$$
Primary concordance was classified as `MATCH` (identical normalized categories) or `DISCREPANCY` (divergent categories).

#### Secondary Endpoints
1. **Protein Consequence Concordance:** Evaluates exact string and semantic matching between runtime protein predictions and normalized external protein annotations, categorized into:
   - `MATCH`: Exact semantic nomenclature agreement (e.g., `p.Glu7Val` vs `p.Glu7Val`).
   - `DISCREPANCY`: Format divergence (e.g., engine complete frameshift syntax vs ClinVar shorthand).
   - `INCOMPLETE`: External record omits protein consequence string.
   - `NOT_APPLICABLE`: Non-coding variants (e.g., UTR variants).
2. **Ten-Tier Error Category Hierarchy:** Categorizes candidates according to a fixed precedence hierarchy:
   $$\text{ENGINE\_ERROR} > \text{HGVS\_AMBIGUITY} > \text{REFERENCE\_MISMATCH} > \text{ENGINE\_UNSUPPORTED} >$$
   $$\text{EXTERNAL\_CONFLICT} > \text{EXTERNAL\_ANNOTATION\_INCOMPLETE} > \text{EXACT\_MOLECULAR\_AGREEMENT} >$$
   $$\text{MOLECULAR\_AGREEMENT\_PROTEIN\_DIFFERENCE} > \text{PROTEIN\_AGREEMENT\_CLASS\_DIFFERENCE} > \text{UNRESOLVED}$$

#### Normalization of External Annotations
To enable fair comparison without penalizing cosmetic syntax variations, external annotations were normalized through locked semantic rules (`research/curation/phase2c_comparison_engine.py`):
- **Molecular Category Normalization:** Maps Sequence Ontology synonyms to unified categories (`missense_variant` $\to$ `Missense`; `stop_gained` $\to$ `Nonsense`; `frameshift_variant` $\to$ `Frameshift`; `splice_acceptor_variant` $\to$ `Splice Acceptor`).
- **Truncated Frameshift Normalization:** ClinVar frequently stores shorthand frameshift expressions denoting only the initial affected amino acid (e.g., `p.Glu7fs` or `E7fs`) rather than full translation syntax (`p.Glu7GlyfsTer...`). The normalization module verifies concordance of the initial affected residue and codon index.
- **Incomplete Splice Records:** Canonical splice acceptor candidates lacking protein strings in ClinVar were classified as `EXTERNAL_ANNOTATION_INCOMPLETE` for protein evaluation while remaining evaluable for primary molecular consequence concordance.

### 2.9 Statistical Analysis
Proportional success metrics ($k / n$) were evaluated using exact 95% two-sided binomial confidence intervals via the Clopper-Pearson method (Clopper & Pearson, 1934). Standard normal asymptotic approximations (Wald intervals) fail when observed success equals 100% ($k = n$) due to zero standard error.

The exact Clopper-Pearson lower limit ($\theta_L$) and upper limit ($\theta_U$) were computed from the incomplete beta distribution by solving:
$$\sum_{x=k}^{n} \binom{n}{x} \theta_L^x (1 - \theta_L)^{n-x} = \frac{\alpha}{2} \quad (\text{for } k > 0)$$
$$\sum_{x=0}^{k} \binom{n}{x} \theta_U^x (1 - \theta_U)^{n-x} = \frac{\alpha}{2} \quad (\text{for } k < n)$$
with significance level $\alpha = 0.05$. When $k = n$, the upper confidence limit is exactly $1.00$ ($100.00\%$), and the lower limit simplifies to $\theta_L = (\alpha / 2)^{1/n} = (0.025)^{1/55} \approx 93.51\%$.

The Clopper-Pearson confidence interval quantifies sampling uncertainty under the mathematical assumption of independent Bernoulli trials drawn from the specified cohort distribution. This statistical interval does not correct for selection bias, incorporation bias, reference transcript dependency, or single-database provenance.

Concordance metrics were stratified across biological mutation classes. Classes with zero primary candidates ($n = 0$) were reported explicitly as `NOT REPRESENTED IN PRIMARY COHORT` (CI: `null`), prohibiting the assignment of artificial 0% or 100% values.

### 2.10 Synthetic Robustness Controls and Software Regression
- **Synthetic Robustness Controls (Experiment D):** An isolated cohort of 18 synthetic negative controls (Class C12) was constructed to evaluate error handling. These inputs represent malformed HGVS strings, inverted coordinates, boundary overflows, and reference mismatches. Robustness controls were evaluated separately and were never pooled into the primary biological denominator ($N = 55$). Success was defined as graceful rejection with a typed `AnalysisError` without unhandled exceptions or crashes.
- **Isolated Software Regression Check ($A$ vs $B$):** Runtime outputs (Entity $A$) were compared against frozen expected deterministic outputs (Entity $B$) stored in the manifest:
  $$\text{Regression Concordance} = \frac{\sum_{i=1}^{N} \mathbb{I}(A_i = B_i)}{N}$$
  This check evaluates software code stability only. Entity $B$ reflects prior engine behavior; regression concordance did not contribute to biological concordance metrics.

---

## 3. Results

### 3.1 Evaluation Execution and Cryptographic Verification
The benchmark was executed strictly against the pre-frozen primary evaluation cohort under the immutable protocol locked in Checkpoint CP3. Pre-execution cryptographic verification confirmed that the primary manifest (`research/manifest/phase2c_primary.json`, 59,605 bytes, $N = 55$) matched its locked SHA256 checksum (`39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`). The benchmark protocol (`research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`) matched its pre-recorded SHA256 checksum (`e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`), and software execution was pinned to engine commit `845f595cc039e006d74237945450c7b4a9569ee6`. Cross-referencing against historical development datasets confirmed zero candidate overlap with the historical test cohort (`research/manifest/frozen_test.json`, SHA256: `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994`).

Review status stratification confirmed that 54 of 55 variants (98.18%) possessed $\ge 2$-star review status in ClinVar, and 1 variant (1.82%; candidate `HBB-CP2-245`, $c.380T>G$, $p.Val127Gly$) possessed 3-star expert panel review status. Exactly 0 variants possessed independent non-ClinVar biological corroboration dossiers.

### 3.2 Primary Molecular Consequence Concordance ($A$ vs $C$)
Across the frozen primary cohort of 55 curated *HBB* variants, runtime molecular consequence predictions (Entity $A$) achieved 100.00% concordance with normalized external ClinVar molecular annotations (Entity $C$) (55/55 matches, 0 discrepancies; Table 1). The exact two-sided 95% Clopper-Pearson binomial confidence interval was [93.51%, 100.00%]. Stored deterministic expected outputs (Entity $B$) were isolated from the evaluation loop and did not participate in determining concordance.

#### Table 1: Primary Molecular Consequence Evaluation Summary
| Evaluation Metric | Observed Value | Percentage (%) | Exact 95% Clopper-Pearson CI | Evidentiary Basis |
|---|:---:|:---:|:---:|---|
| **Primary Cohort Denominator ($N$)** | 55 | 100.00% | — | Frozen manifest `phase2c_primary.json` |
| **Molecular Consequence Matches ($k$)** | 55 | 100.00% | **[93.51%, 100.00%]** | Runtime Entity $A$ vs Normalized External Entity $C$ |
| **Molecular Consequence Discrepancies** | 0 | 0.00% | [0.00%, 6.49%] | Zero discordance across 7 represented classes |
| **Execution Failures (`ENGINE_ERROR`)** | 0 | 0.00% | [0.00%, 6.49%] | Zero runtime exceptions or unhandled failures |
| **Syntax / Reference Rejections** | 0 | 0.00% | [0.00%, 6.49%] | All 55 variants valid under canonical reference models (exonic/UTR against `NM_000518.5`, intronic against `NG_000007.3`) |

Classification of the 55 primary records across the pre-specified ten-tier comparison category hierarchy revealed three populated categories:
1. **`EXACT_MOLECULAR_AGREEMENT`:** 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies. This category encompasses 28 coding variants with exact protein nomenclature agreement (`MATCH`) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (`NOT_APPLICABLE`).
2. **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`:** 20 variants (36.36%) exhibited exact primary molecular consequence concordance (Frameshift) accompanied by protein nomenclature format divergence resulting from ClinVar truncated frameshift representations.
3. **`EXTERNAL_ANNOTATION_INCOMPLETE`:** 5 variants (9.09%) exhibited exact primary molecular consequence concordance (Splice Acceptor) where the external ClinVar record omitted a protein consequence string.
4. **All Other Categories:** 0 variants (0.00%) were assigned to `ENGINE_ERROR`, `HGVS_AMBIGUITY`, `REFERENCE_MISMATCH`, `ENGINE_UNSUPPORTED`, `EXTERNAL_CONFLICT`, `PROTEIN_AGREEMENT_CLASS_DIFFERENCE`, or `UNRESOLVED`.

### 3.3 Secondary Protein Nomenclature Representation
Secondary evaluation assessed exact concordance between runtime protein consequence predictions and external ClinVar protein annotations across the 55 primary candidates (Table 2).

Exact protein nomenclature agreement was observed for 28 of 55 variants (50.91%, exact 95% Clopper-Pearson CI: [37.07%, 64.65%]). The remaining 27 variants were categorized into three distinct representation groups:

#### Table 2: Secondary Protein Consequence Nomenclature Breakdown
| Protein Endpoint Status | Candidate Count | Percentage (%) | Class Distribution | Methodological Rationale |
|---|:---:|:---:|---|---|
| **`MATCH`** | **28** | **50.91%** | C01 ($n=14$), C02 ($n=3$), C03 ($n=10$), C06 ($n=1$) | Exact string and semantic identity (all missense, nonsense, synonymous, and one premature stop insertion `p.Glu44Ter`). |
| **`DISCREPANCY` (Format)** | **20** | **36.36%** | C04 ($n=9$ deletions), C06 ($n=11$ duplications) | Truncated frameshift notation in ClinVar (e.g., `p.Glu7fs` or `E7fs`) vs full translation syntax (`p.Glu7GlyfsTer13`). |
| **`INCOMPLETE`** | **5** | **9.09%** | C09 ($n=5$ splice acceptors) | External ClinVar records lack a protein consequence string (`p.?`). |
| **`NOT_APPLICABLE`** | **2** | **3.64%** | C11 ($n=2$ 3' UTR variants) | Non-coding sequence alterations with no protein translation product. |
| **TOTAL** | **55** | **100.00%** | All 7 Represented Classes | Secondary protein concordance: 28/55 (50.91%). |

The 20 format discrepancies occurred exclusively among frameshift variants (Classes C04 and C06). In all 20 cases, the deterministic engine computed complete downstream reading frame translation up to the first termination codon in accordance with HGVS guidelines, whereas ClinVar recorded shorthand strings denoting only the initial affected residue. The underlying molecular consequence classification (Frameshift) was concordant in 100% of these cases; divergence was restricted to repository string formatting conventions.

### 3.4 Results by Represented Biological Variant Class
Stratification of primary molecular consequence concordance across the 11 predefined biological mutation classes is presented in Table 3.

Seven biological mutation classes were represented in the primary cohort, and all seven exhibited 100.0% molecular consequence concordance:
- **Class C01 (Missense SNVs):** 14/14 concordant (100.0%, 95% CI: [76.84%, 100.00%]).
- **Class C02 (Nonsense / Stop-Gain):** 3/3 concordant (100.0%, 95% CI: [29.24%, 100.00%]).
- **Class C03 (Synonymous / Silent):** 10/10 concordant (100.0%, 95% CI: [69.15%, 100.00%]).
- **Class C04 (Frameshift Deletions):** 9/9 concordant (100.0%, 95% CI: [66.37%, 100.00%]).
- **Class C06 (Frameshift Duplications / Insertions):** 12/12 concordant (100.0%, 95% CI: [73.54%, 100.00%]).
- **Class C09 (Splice Acceptor Disruptions):** 5/5 concordant (100.0%, 95% CI: [47.82%, 100.00%]).
- **Class C11 (3' UTR Regulatory Variants):** 2/2 concordant (100.0%, 95% CI: [15.81%, 100.00%]).

#### Table 3: Class-Stratified Benchmark Performance
| Class ID | Biological Variant Class | Primary ($n$) | Successes ($k$) | Discrepancies | Concordance (%) | Exact 95% Clopper-Pearson CI | Representation Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **C01** | Missense SNVs | 14 | 14 | 0 | 100.0% | [76.84%, 100.00%] | Represented ($n = 14$) |
| **C02** | Nonsense (Stop-Gain) | 3 | 3 | 0 | 100.0% | [29.24%, 100.00%] | Represented ($n = 3$, wide CI) |
| **C03** | Synonymous (Silent) | 10 | 10 | 0 | 100.0% | [69.15%, 100.00%] | Represented ($n = 10$) |
| **C04** | Frameshift Deletions | 9 | 9 | 0 | 100.0% | [66.37%, 100.00%] | Represented ($n = 9$) |
| **C05** | In-Frame Indels / Deletions | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C06** | Frameshift Duplications / Insertions | 12 | 12 | 0 | 100.0% | [73.54%, 100.00%] | Represented ($n = 12$) |
| **C07** | In-Frame Insertions / Duplications | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C08** | Splice Donor Disruptions | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C09** | Splice Acceptor Disruptions | 5 | 5 | 0 | 100.0% | [47.82%, 100.00%] | Represented ($n = 5$, wide CI) |
| **C10** | 5' UTR Regulatory Variants | 0 | — | — | — | — | **Not Represented** ($n = 0$) |
| **C11** | 3' UTR Regulatory Variants | 2 | 2 | 0 | 100.0% | [15.81%, 100.00%] | Represented ($n = 2$, wide CI) |
| **TOTAL** | **Primary Evaluation Cohort** | **55** | **55** | **0** | **100.0%** | **[93.51%, 100.00%]** | **7 Classes Represented** |

#### Documentation of Unrepresented Mutation Classes ($n = 0$)
Four biological classes had zero candidates in the primary cohort:
- **Class C05 (In-Frame Indels / Deletions, $n = 0$):** Candidate `HBB-CP2-105` (`c.9_83del`, 25 codons) was relegated to the Conditional cohort due to structural deletion length and single-submitter status.
- **Class C07 (In-Frame Insertions / Duplications, $n = 0$):** Only two clean in-frame duplications existed in the pool; both possessed 0-star ClinVar evidence and were relegated to the Secondary cohort.
- **Class C08 (Splice Donor Disruptions, $n = 0$):** Zero non-conflicting donor variants ($+1, +2, +5$) meeting quality filtering criteria were available in the harvested ClinVar dataset.
- **Class C10 (5' UTR Regulatory Variants, $n = 0$):** All queried promoter variants ($> -50$ bp upstream) exceeded the physical transcript boundary of `NM_000518.5`.

In accordance with protocol rules, these classes are reported as `NOT REPRESENTED IN PRIMARY COHORT`. Algorithmic performance for in-frame indels / deletions, in-frame insertions / duplications, splice donor disruptions, and 5' UTR regulatory variants is unmeasured in this benchmark.

### 3.5 Synthetic Robustness Controls (Experiment D)
Input validation and error handling were evaluated in an isolated negative-control experiment comprising 18 synthetic malformed inputs (Class C12; candidates `HBB-CP2-297` through `HBB-CP2-314`). These controls were completely segregated from the biological primary cohort and were not included in the primary denominator ($N = 55$).

All 18 synthetic negative controls (100.00%, exact 95% Clopper-Pearson CI: [81.47%, 100.00%]) were gracefully rejected by the engine with explicit, typed `AnalysisError` exceptions (Table 4):
- **`INVALID_COORDINATE` ($n = 8$):** Inverted deletion ranges (`c.150_145del`, `c.400_350del`), inverted duplication ranges (`c.250_240dup`), non-consecutive insertion coordinates (`c.50_53insA`, `c.100_104insGCC`, `c.200_205insTT`), base zero violation (`c.0A>G`), and malformed 3' UTR offset (`c.*0A>G`).
- **`OUT_OF_BOUNDS` ($n = 6$):** Coordinates exceeding transcript length (`c.650A>G`, `c.750del`, `c.800dup`) and intronic offsets exceeding physical intron spans (`c.92+250G>A`, `c.93-200G>A` exceeding 130 bp Intron 1; `c.315+950G>A` exceeding 850 bp Intron 2).
- **`SYNTAX_ERROR` ($n = 2$):** Non-standard DNA base in alternate allele (`c.50A>Z`) and malformed HGVS expression syntax (`c.delA`).
- **`REFERENCE_MISMATCH` ($n = 2$):** Exonic reference base mismatch (`c.70T>A`, reference base G) and intronic reference base mismatch (`c.92+1A>G`, genomic reference base G).

Zero unhandled exceptions, uncaught runtime crashes, or silent mispredictions were observed across the adversarial test battery.

#### Table 4: Synthetic Robustness Control Evaluation Breakdown
| Test Category | Tested Inputs ($n$) | Graceful Rejections ($k$) | Error Code Returned | Unhandled Crashes | Result |
|---|:---:|:---:|---|:---:|:---:|
| **Coordinate Geometry & Range Violations** | 8 | 8 | `INVALID_COORDINATE` | 0 | **PASS** |
| **Transcript & Intron Boundary Overflow** | 6 | 6 | `OUT_OF_BOUNDS` | 0 | **PASS** |
| **Malformed Syntax & Non-DNA Bases** | 2 | 2 | `SYNTAX_ERROR` | 0 | **PASS** |
| **Reference Sequence Base Mismatches** | 2 | 2 | `REFERENCE_MISMATCH` | 0 | **PASS** |
| **TOTAL (Experiment D)** | **18** | **18** | **All Typed Errors** | **0** | **100.0% Rejection** |

### 3.6 Software Regression Consistency ($A$ vs $B$)
To verify software execution stability across commits, runtime deterministic engine outputs (Entity $A$) were compared against frozen expected deterministic outputs (Entity $B$) stored in `research/manifest/phase2c_primary.json`.

Runtime outputs reproduced frozen expected values for 100.00% of candidates (55/55 molecular consequence reproductions, 55/55 protein consequence reproductions). This check confirms zero algorithmic drift between dataset freezing and benchmark execution. Because Entity $B$ represents prior engine code outputs rather than external biological truth, this metric serves exclusively as internal software regression metadata and was strictly isolated from external concordance reporting.

### 3.7 Legacy Nomenclature Tracking and Comprehensive Benchmark Synthesis
Historical alias records were audited across all 55 candidates (`research/results/PHASE2C_ERROR_REGISTER.md`). Exactly 33 variants (60.00%) possessed traditional codon (CD) designations or mature protein numbering designations in ClinVar (e.g., `CD 6 -A` for `c.20del`, `CD 22 (GAA>TAA)` for `c.67G>T`, `CD 30 (A>G)` for `c.91A>G`, `CD 42/43 (+T)` for `c.129dup`, and `CD 126 GTG>GGG` for `c.380T>G`). The comparison engine confirmed that all 33 legacy designations reflected non-contradictory historical offsets (-1 codon mature protein shift or standard Italian/Greek/Chinese thalassemia notation) and matched the underlying `NM_000518.5` cDNA coordinates without ambiguity.

#### Table 5: Comprehensive Synthesis of Phase 2C Benchmark Findings
| Evaluation Dimension | Evaluated Entities | Cohort Size ($N$) | Successes ($k$) | Rate (%) | Exact 95% Clopper-Pearson CI | Scientific Interpretation |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Primary Molecular Concordance** | Entity $A$ vs Entity $C$ | **55** | **55** | **100.00%** | **[93.51%, 100.00%]** | Complete concordance between runtime engine and curated ClinVar-derived external molecular annotations across 7 classes. |
| **Secondary Protein Concordance** | Runtime $p.$ vs External $p.$ | **55** | **28** | **50.91%** | **[37.07%, 64.65%]** | Exact protein matching in 28 variants; 20 format differences from truncated frameshifts; 5 incomplete splice strings. |
| **Synthetic Robustness Controls** | Entity $A$ vs Synthetic Malformed | **18** | **18** | **100.00%** | **[81.47%, 100.00%]** | 100% graceful rejection of adversarial inputs via typed `AnalysisError`; zero unhandled runtime crashes. |
| **Software Regression Invariance** | Entity $A$ vs Entity $B$ | **55** | **55** | **100.00%** | — | 100% internal code consistency against frozen expected baseline; zero commit drift. |

---

## 4. Discussion

### 4.1 Principal Findings
The primary objective of this study was to evaluate the computational concordance of a dedicated deterministic molecular consequence pipeline for human beta-globin gene (*HBB*) sequence variants against curated ClinVar-derived external molecular annotations under a predefined, protocol-locked evaluation framework anchored to an immutable dataset manifest. Across the frozen primary evaluation cohort of 55 curated *HBB* variants, runtime molecular consequence predictions (Entity $A$) demonstrated 100.00% concordance with normalized external annotations (Entity $C$) (55/55 matches, 0 discrepancies; exact 95% Clopper-Pearson binomial confidence interval: [93.51%, 100.00%]; Clopper & Pearson, 1934).

Categorization of the 55 primary records across the pre-specified ten-tier comparison hierarchy revealed three populated outcome categories:
1. **`EXACT_MOLECULAR_AGREEMENT`:** Exactly 30 variants (54.55%) exhibited exact primary molecular consequence concordance without protein nomenclature discrepancies, comprising 28 coding variants with exact protein nomenclature agreement (`MATCH`) and 2 non-coding 3' UTR regulatory variants for which protein consequence matching is not applicable (`NOT_APPLICABLE`).
2. **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`:** Exactly 20 frameshift variants (36.36%) exhibited exact primary consequence agreement accompanied by protein nomenclature format divergence resulting from truncated shorthand syntax in external ClinVar records.
3. **`EXTERNAL_ANNOTATION_INCOMPLETE`:** Exactly 5 canonical splice acceptor variants (9.09%) exhibited exact primary consequence agreement where the external ClinVar record omitted a protein consequence string.

Zero candidates were assigned to unhandled execution failures (`ENGINE_ERROR`), reference sequence rejections, sequence ambiguity, or unresolved categories. Secondary evaluation of exact protein nomenclature matching yielded 50.91% concordance (28/55; exact 95% CI: [37.07%, 64.65%]), reflecting external repository formatting conventions rather than algorithmic translation failures. In an isolated negative-control experiment (Experiment D), the engine gracefully rejected 100% of 18 synthetic malformed inputs (exact 95% CI: [81.47%, 100.00%]) with typed `AnalysisError` exceptions and zero unhandled crashes. Furthermore, software regression testing verified 100% reproduction (55/55) of historical expected outputs (Entity $B$), confirming zero algorithmic drift between codebase freezing and benchmark execution.

### 4.2 Interpretation of Molecular Consequence Concordance
Rigorous scientific interpretation requires establishing precisely what the observed 55/55 concordance result demonstrates—and what it does not. The observed concordance demonstrates computational rule execution fidelity: given valid HGVS cDNA syntax anchored to RefSeq `NM_000518.5`, the deterministic engine correctly operationalizes canonical coordinate arithmetic, standard codon translation tables (NCBI Table 1), reading-frame reconstruction, and invariant dinucleotide splice-junction boundaries. For high-confidence ClinVar records spanning seven represented biological mutation classes, the algorithm's outputs match external submitter assertions without discrepancy.

Crucially, this empirical result does not establish independent biological validation, clinical diagnostic accuracy, or clinical pathogenicity prediction. To interpret these findings defensibly, computational genomics studies must maintain strict distinctions among three evidentiary tiers:
1. **Correct execution of a predefined computational comparison:** Verified by protocol-locked execution, deterministic reproduction of Entity $B$, and automated comparison logging.
2. **Concordance observed within a curated evaluation cohort:** Supported by the 55/55 match rate against normalized ClinVar assertions across seven represented biological classes.
3. **Generalization to previously unseen or novel *HBB* variants:** Not established by this study.

The empirical artifacts generated in this study support only the first two tiers. The 55/55 concordance confirms that the deterministic rules were executed accurately according to specification and that the software behaves consistently on clean database submissions. However, because cohort admission was conditioned on prior engine agreement during curation (`comparison_status == "EXACT_AGREEMENT"`), this finding cannot be treated as evidence that the system will exhibit equivalent concordance across unselected clinical sequencing callsets or novel *HBB* alleles.

### 4.3 Protein Nomenclature Representation Differences
The observed disparity between primary molecular consequence concordance (100.00%) and secondary exact protein nomenclature concordance (50.91%) highlights a persistent challenge in computational variant curation: the divergence between full formal HGVS protein descriptions and historical database representation conventions (den Dunnen et al., 2016).

In all 20 frameshift cases cataloged under `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE` (9 deletions in Class C04 and 11 duplications in Class C06), the deterministic engine translated the downstream reading frame in silico until encountering the first termination codon, outputting complete HGVS syntax (e.g., `p.Glu7GlyfsTer13`). Conversely, NCBI ClinVar entries frequently record shorthand notations denoting only the first affected residue (e.g., `p.Glu7fs` or `E7fs`) (Landrum et al., 2018). While both representations identify the identical biological frameshift event at codon 7, exact string comparison fails in the absence of semantic normalization. Similarly, five canonical splice acceptor variants (Class C09) lacked protein strings entirely (`p.?`), reflecting ClinVar submitter practice for non-coding and splice junctions.

The multi-tiered comparison engine proved essential in distinguishing non-biological string formatting discrepancies from true algorithmic mispredictions. This architectural separation prevented artificial deflation of primary consequence concordance while transparently documenting external annotation limitations.

### 4.4 Implications for Deterministic and Reference-Aware Computation
These findings illustrate the operational characteristics of deterministic computation in genomic pipelines. The use of deterministic, rule-based computation makes molecular consequence outputs reproducible under a fixed implementation and reference sequence. Although generative AI can support auxiliary evidence retrieval and summarization, this study did not directly compare LLM-based methods with the deterministic engine and therefore draws no conclusions about their relative error rates or reliability. Deterministic execution itself does not imply that software is error-free; a rule-based pipeline can still contain implementation bugs, incorrect biological assumptions, or incomplete rules.

In the present architecture, core consequence derivation is implemented in pure Python without statistical heuristics, external network calls, or generative AI dependencies (`backend/app/core/consequences.py`). Generative AI capabilities are strictly segregated into an auxiliary, non-evaluative literature retrieval module (`backend/app/ai.py`). Furthermore, the engine is explicitly reference-aware, anchoring all coordinates to RefSeq `NM_000518.5` (MANE Select) (O'Leary et al., 2016; Morales et al., 2022).

This reference-anchored design proved vital in resolving historical hemoglobinopathy nomenclature. In clinical literature, beta-globin mutations have historically been numbered from the mature polypeptide's amino-terminal valine (omitting codon 1 methionine), creating a systematic -1 amino acid offset (Taher et al., 2018; Weatherall, 2010; Thein, 2013; Giardine et al., 2007). Exactly 33 variants in our primary cohort (60.00%) possessed traditional codon (CD) designations (e.g., `CD 6 -A` for `c.20del`, `CD 22` for `c.67G>T`, `CD 30` for `c.91A>G`). Rigorous reference coordinate conversion resolved these historical aliases without ambiguous classification.

### 4.5 Relationship to Existing Variant Annotation Approaches
The deterministic pipeline evaluated in this study addresses a specific operational niche rather than replacing broad genome-scale annotation frameworks. Established multi-gene tools such as the Ensembl Variant Effect Predictor (VEP) (McLaren et al., 2016) and ANNOVAR (Wang et al., 2010) are engineered for high-throughput whole-genome and exome annotation across thousands of genes and diverse transcript isoforms. In contrast, the present implementation provides a focused, locus-specific molecular consequence engine tailored specifically to human *HBB* under RefSeq `NM_000518.5`. This localized architecture prioritizes auditable coordinate arithmetic, transparent execution tracing, and direct handling of legacy beta-globin codon offsets without the extensive system dependencies required by genome-wide annotation suites.

Importantly, deterministic molecular consequence derivation must be strictly distinguished from computational pathogenicity prediction algorithms (Richards et al., 2015). In silico pathogenicity algorithms compute probabilistic deleteriousness or functional damage scores based on phylogenetic sequence conservation, protein structural perturbation, or machine-learning models to predict disease likelihood. By contrast, deterministic consequence computation identifies only the objective transcript alteration and reading-frame state (e.g., synonymous, missense, frameshift, stop-gain) (McLaren et al., 2016; Wang et al., 2010). In accordance with the ACMG/AMP variant interpretation guidelines (Richards et al., 2015), molecular consequence provides foundational structural evidence (such as criterion PVS1 for predicted null variants in genes where loss of function causes disease), but does not itself establish whether a variant is pathogenic or benign in a patient. Maintaining explicit operational separation between objective consequence derivation and evaluative pathogenicity scoring is essential to prevent computational overreach and misinterpretation.

### 4.6 Implications for Reproducible Benchmark Design
A major contribution of this study is the demonstration of an audited, reproducible benchmarking framework for computational genetics. As emphasized by international benchmarking consortia and reproducibility standards (Krusche et al., 2019; Stodden et al., 2016), evaluating bioinformatics software requires predefined protocols locked prior to execution, immutable data baselines, and transparent error tracking.

By recording cryptographic digests for the primary manifest (`phase2c_primary.json`, SHA256: `39eb60de...`), protocol specification (`PHASE2C_BENCHMARK_PROTOCOL.md`, SHA256: `e4bad0a0...`), and software commit (`845f595c...`) prior to benchmark execution, this study enabled objective verification of artifact identity against pre-recorded values and confirmed the absence of code drift or post-hoc manifest modification. However, cryptographic hashing confirms artifact identity and execution immutability rather than preventing retrospective curation selection bias or guaranteeing biological truth. Moreover, structuring the benchmark into four mathematically decoupled evaluation dimensions—primary molecular concordance ($A$ vs $C$), secondary protein syntax, adversarial input robustness (Experiment D, $N = 18$), and software regression ($A$ vs $B$)—prevented internal consistency checks or synthetic controls from contaminating external concordance metrics. This multi-dimensional evaluation architecture provides a practical model for reporting computational performance in specialized genomics tools.

---

## 5. Limitations

### 5.1 Incorporation and Verification Bias
The primary scientific limitation of this study is the presence of substantive incorporation (verification) bias inherent to the cohort qualification protocol. During Checkpoint CP2.2 curation (`run_independent_verification.py`, lines 231–246), candidate admission into the `PROPOSED_PRIMARY` qualification pool explicitly required that runtime engine output match external annotations (`comparison_status == "EXACT_AGREEMENT"`). Candidate variants triggering engine errors, parser rejections, or divergent classifications were systematically diverted into conditional, review-required, or exclusion registries.

Consequently, the evaluation cohort was not selected independently of the engine's deterministic comparison outcome. In diagnostic epidemiology and computational validation, conditioning sample inclusion on agreement with the evaluated test introduces profound incorporation bias. A frozen dataset manifest is not synonymous with an independently selected dataset: cryptographic immutability guarantees reproducibility of the execution, but does not rectify retrospective selection bias. Therefore, the observed 55/55 concordance represents computational rule execution fidelity within a pre-screened, highly concordant subset, and cannot be interpreted as an unbiased estimate of generalization on unselected clinical variants.

### 5.2 External Reference Dependence
A second major limitation is the exclusive dependence on NCBI ClinVar as the sole external comparison reference (Landrum et al., 2018; Landrum et al., 2020). All 55 primary cohort variants originated from ClinVar submissions; exactly zero candidates possessed independent biological corroboration dossiers outside of ClinVar (`independent_non_clinvar_corroboration == "NONE"`). Although 54 of 55 variants (98.18%) possessed $\ge 2$-star review status denoting multiple submitters without conflict, multiple laboratory submissions to a public archive represent diagnostic laboratory consensus rather than independent biological ground truth (Rehm et al., 2015; Harrison et al., 2017).

Public databases can replicate shared reference sequence assumptions, common legacy translation conventions, or systematic annotation artifacts. Without orthogonal corroboration from secondary locus-specific repositories (such as HbVar [Giardine et al., 2007], IthaGenes, or LOVD) or direct experimental sequencing, concordance measures alignment with curated ClinVar-derived external molecular annotations rather than primary biological reality or independent experimental truth.

### 5.3 Mutation Class Coverage
The primary evaluation cohort represents only seven of the eleven predefined biological mutation classes. Four biological classes had zero representation ($n = 0$):
- **Class C05 (In-Frame Indels / Deletions):** Multi-codon deletions in the harvested pool were relegated to conditional status due to structural span.
- **Class C07 (In-Frame Insertions / Duplications):** Clean duplications in the pool possessed low ClinVar evidence (0 stars).
- **Class C08 (Splice Donor Disruptions):** Zero canonical donor variants meeting quality thresholds were available in the harvested pool.
- **Class C10 (5' UTR Regulatory Variants):** Queried promoter variants exceeded the physical transcript boundary of RefSeq `NM_000518.5` ($> -50$ bp).

High pooled concordance across the seven represented classes provides zero empirical performance evidence for these four unrepresented mechanisms. Algorithmic capability for in-frame indels / deletions, in-frame insertions / duplications, splice donor disruptions, and 5' UTR regulatory alterations remains unmeasured in this benchmark.

### 5.4 Protein Annotation Incompleteness
Secondary protein concordance evaluation was constrained by external repository formatting idioms. Exactly 20 of 55 primary candidates (36.36%) exhibited truncated frameshift representations in ClinVar records, and 5 candidates (9.09%) omitted protein consequence strings entirely. While these representation disparities were successfully parsed and categorized by the comparison engine without impacting primary molecular consequence concordance, they prevented full end-to-end string validation of downstream translation for 45.45% of the primary cohort, restricting exact protein matching to 50.91% (28/55).

### 5.5 Sample Size and Statistical Uncertainty
While the pooled primary cohort denominator ($N = 55$) is sufficient to demonstrate basic computational rule stability, several represented biological classes contain very few variants. Specifically, Class C02 (Nonsense SNVs) contains only $n = 3$ variants (exact 95% CI: [29.24%, 100.00%]), Class C09 (Splice Acceptor Disruptions) contains $n = 5$ (exact 95% CI: [47.82%, 100.00%]), and Class C11 (3' UTR Regulatory) contains only $n = 2$ (exact 95% CI: [15.81%, 100.00%]).

The resulting binomial confidence intervals for these subgroups are wide, precluding definitive conclusions regarding class-specific reliability. Furthermore, a modest cohort of 55 curated variants cannot expose subtle edge-case failure modes that might emerge in large-scale clinical sequencing datasets.

### 5.6 Scope of Inference
Finally, the scope of inference is strictly bounded to computational molecular consequence classification from pre-parsed HGVS strings. The software does not process raw sequencing reads, does not perform variant calling, does not evaluate complex structural rearrangements, does not model alternative splicing isoforms beyond RefSeq `NM_000518.5`, and does not assess clinical phenotypes or diagnostic sensitivity. These findings must not be extrapolated to clinical variant interpretation or patient care.

---

## 6. Conclusion

This study evaluated the computational concordance of a dedicated, deterministic molecular consequence engine for sequence variants in the human beta-globin gene (*HBB*). Operating under a predefined and protocol-locked evaluation framework anchored strictly to RefSeq `NM_000518.5`, the runtime engine achieved complete molecular consequence concordance (55/55, 100.00%, exact 95% Clopper-Pearson CI: [93.51%, 100.00%]) with curated ClinVar-derived external molecular annotations across seven biological mutation classes. The evaluation framework successfully isolated primary consequence classification from secondary protein syntax divergence, verified adversarial input-handling robustness across 18 synthetic negative controls, and tracked historical legacy codon numbering offsets.

However, these findings establish computational rule execution fidelity and concordance with curated ClinVar-derived external molecular annotations, not independent biological ground truth, clinical validity, or diagnostic accuracy. Scientific interpretation of the observed concordance is critically bounded by curation incorporation bias, single-database ClinVar provenance without orthogonal secondary corroboration, and the complete absence of four biological mutation classes (C05, C07, C08, and C10). Future research must evaluate deterministic pipelines against prospectively sampled, independently curated variant cohorts that feature pre-fixed eligibility criteria, cross-database corroboration from locus-specific registries, and comprehensive coverage across all biological mutation mechanisms.

---

## 7. References

1. **Clopper CJ, Pearson ES.** The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika*. 1934;26(4):404–413. doi:[10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).
2. **den Dunnen JT, Dalgleish R, Maglott DR, et al.** HGVS Recommendations for the Description of Sequence Variants: 2016 Update. *Hum Mutat*. 2016;37(6):564–569. doi:[10.1002/humu.22981](https://doi.org/10.1002/humu.22981). PMID:[26931183](https://pubmed.ncbi.nlm.nih.gov/26931183/).
3. **Giardine B, van Baal S, Kaimakis P, et al.** HbVar database of human hemoglobin variants and thalassemia mutations: 2007 update. *Hum Mutat*. 2007;28(2):206. doi:[10.1002/humu.9479](https://doi.org/10.1002/humu.9479). PMID:[17221864](https://pubmed.ncbi.nlm.nih.gov/17221864/).
4. **Harrison SM, Dolinsky JS, Knight Johnson AE, et al.** Clinical laboratories collaborate to resolve differences in variant interpretations submitted to ClinVar. *Genet Med*. 2017;19(10):1096–1104. doi:[10.1038/gim.2017.14](https://doi.org/10.1038/gim.2017.14). PMID:[28301460](https://pubmed.ncbi.nlm.nih.gov/28301460/). PMCID:[PMC5600649](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5600649/).
5. **Krusche P, Trigg L, Boutros PC, et al.** Best practices for benchmarking germline small-variant calls in human genomes. *Nat Biotechnol*. 2019;37(5):555–560. doi:[10.1038/s41587-019-0054-x](https://doi.org/10.1038/s41587-019-0054-x). PMID:[30858580](https://pubmed.ncbi.nlm.nih.gov/30858580/). PMCID:[PMC6699627](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6699627/).
6. **Landrum MJ, Lee JM, Benson M, et al.** ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Res*. 2018;46(D1):D1062–D1067. doi:[10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153). PMID:[29165669](https://pubmed.ncbi.nlm.nih.gov/29165669/). PMCID:[PMC5753237](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5753237/).
7. **Landrum MJ, Chitipiralla S, Brown GR, et al.** ClinVar: improvements to accessing data. *Nucleic Acids Res*. 2020;48(D1):D835–D844. doi:[10.1093/nar/gkz972](https://doi.org/10.1093/nar/gkz972). PMID:[31777943](https://pubmed.ncbi.nlm.nih.gov/31777943/). PMCID:[PMC6943040](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6943040/).
8. **McLaren W, Gil L, Hunt SE, et al.** The Ensembl Variant Effect Predictor. *Genome Biol*. 2016;17(1):122. doi:[10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4). PMID:[27268795](https://pubmed.ncbi.nlm.nih.gov/27268795/). PMCID:[PMC4893825](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4893825/).
9. **Morales J, Pujar S, Loveland JE, et al.** A joint NCBI and EMBL-EBI transcript set for clinical genomics and research. *Nature*. 2022;604(7905):310–315. doi:[10.1038/s41586-022-04558-8](https://doi.org/10.1038/s41586-022-04558-8). PMID:[35388217](https://pubmed.ncbi.nlm.nih.gov/35388217/). PMCID:[PMC9007741](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9007741/).
10. **O'Leary NA, Wright MW, Brister JR, et al.** Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. *Nucleic Acids Res*. 2016;44(D1):D733–D745. doi:[10.1093/nar/gkv1189](https://doi.org/10.1093/nar/gkv1189). PMID:[26553804](https://pubmed.ncbi.nlm.nih.gov/26553804/). PMCID:[PMC4702849](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4702849/).
11. **Rehm HL, Berg JS, Brooks LD, et al.** ClinGen — the Clinical Genome Resource. *N Engl J Med*. 2015;372(23):2235–2242. doi:[10.1056/NEJMsr1406261](https://doi.org/10.1056/NEJMsr1406261). PMID:[26014595](https://pubmed.ncbi.nlm.nih.gov/26014595/). PMCID:[PMC4474187](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4474187/).
12. **Richards S, Aziz N, Bale S, et al.** Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genet Med*. 2015;17(5):405–424. doi:[10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30). PMID:[25741868](https://pubmed.ncbi.nlm.nih.gov/25741868/). PMCID:[PMC4544753](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4544753/).
13. **Stodden V, McNutt M, Bailey DH, et al.** Enhancing reproducibility for computational methods. *Science*. 2016;354(6317):1240–1241. doi:[10.1126/science.aah6168](https://doi.org/10.1126/science.aah6168). PMID:[27940837](https://pubmed.ncbi.nlm.nih.gov/27940837/).
14. **Taher AT, Weatherall DJ, Cappellini MD.** Thalassaemia. *Lancet*. 2018;391(10116):155–167. doi:[10.1016/S0140-6736(17)31822-6](https://doi.org/10.1016/S0140-6736(17)31822-6). PMID:[28774421](https://pubmed.ncbi.nlm.nih.gov/28774421/).
15. **Thein SL.** The molecular basis of $\beta$-thalassemia. *Cold Spring Harb Perspect Med*. 2013;3(5):a011700. doi:[10.1101/cshperspect.a011700](https://doi.org/10.1101/cshperspect.a011700). PMID:[23637309](https://pubmed.ncbi.nlm.nih.gov/23637309/). PMCID:[PMC3633182](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3633182/).
16. **Wang K, Li M, Hakonarson H.** ANNOVAR: functional annotation of genetic variants from high-throughput sequencing data. *Nucleic Acids Res*. 2010;38(16):e164. doi:[10.1093/nar/gkq603](https://doi.org/10.1093/nar/gkq603). PMID:[20601685](https://pubmed.ncbi.nlm.nih.gov/20601685/). PMCID:[PMC2938201](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2938201/).
17. **Weatherall DJ.** The inherited diseases of hemoglobin are an emerging global health burden. *Blood*. 2010;115(22):4331–4336. doi:[10.1182/blood-2010-01-251348](https://doi.org/10.1182/blood-2010-01-251348). PMID:[20233970](https://pubmed.ncbi.nlm.nih.gov/20233970/). PMCID:[PMC2881491](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2881491/).

---

## 8. Declarations and Author Information

### Author Details
- **Authors:** [AUTHOR PLACEHOLDER: Full author names, institutional affiliations, and ORCID identifiers to be provided by authors]
- **Corresponding Author:** [CORRESPONDING AUTHOR PLACEHOLDER: Name and institutional email address to be provided by authors]

### Ethics Approval and Consent to Participate
[ETHICS PLACEHOLDER: Formal institutional ethics determination or IRB statement to be provided by authors. Do not assert exemption without institutional or journal confirmation.]

### Consent for Publication
[CONSENT PLACEHOLDER: Author declaration regarding publication consent to be confirmed according to target journal guidelines.]

### Competing Interests
[COMPETING INTERESTS PLACEHOLDER: Formal conflict of interest declaration to be provided by authors.]

### Funding
[FUNDING PLACEHOLDER: Funding sources and grant numbers to be inserted by authors, or declaration that no external funding was received.]

### Authors' Contributions
[CONTRIBUTIONS PLACEHOLDER: Detailed CRediT statement of author contributions to be provided by authors.]

### Acknowledgements
[ACKNOWLEDGEMENTS PLACEHOLDER: Colleague, laboratory, and institutional acknowledgements to be added by authors.]

### Data and Code Availability
[DATA/CODE AVAILABILITY PLACEHOLDER: Verified public repository URLs, Zenodo DOI archive links, and ClinVar accession references to be confirmed and inserted by authors prior to submission.]

