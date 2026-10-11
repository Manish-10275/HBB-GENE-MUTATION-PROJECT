# Phase 5.2C — Methods Section Draft

> **Document Type:** MANUSCRIPT METHODS SECTION DRAFT  
> **Target Manuscript:** HBB Gene Mutation Analyzer Research Manuscript  
> **Stage:** Phase 5.2C (Methods Section Authoring)  
> **Governing Baseline:** `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md`, `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`, `research/protocol/CP3_PROTOCOL_LOCK_REPORT.md`, `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md`  
> **Frozen Primary Dataset:** `research/manifest/phase2c_primary.json` (SHA256: `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96`)  
> **Benchmark Protocol SHA256:** `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`  
> **Engine Git Commit:** `845f595cc039e006d74237945450c7b4a9569ee6`  
> **Environment Baseline:** Python 3.14.7 on Windows 10 (AMD64)  
> **Quality Standard:** Absolute artifact fidelity; zero post-hoc claim inflation; complete mathematical separation of comparators ($A$ vs $C$ vs $B$); explicit disclosure of curation incorporation bias.

---

# Methods

## 1. Study Design and Evaluation Objective
This study was designed as an independent, reproducible computational concordance evaluation of a deterministic molecular consequence engine for sequence variants in the human beta-globin gene (*HBB*). The primary objective was to evaluate whether a rule-based algorithm anchored strictly to reference transcript coordinates could derive molecular consequences concordant with curated, high-confidence external annotations derived from the National Center for Biotechnology Information (NCBI) ClinVar database under a locked, pre-specified evaluation protocol. 

The study design adheres to established guidelines for reproducible computational genomics and variant benchmarking (Krusche et al., 2019; Stodden et al., 2016). Crucially, the evaluation was designed exclusively as a computational concordance assessment of molecular consequence categorization (e.g., Missense, Nonsense, Frameshift, Splice Acceptor). It was not designed as, and does not constitute, an independent biological validation study (as no in vitro cellular assays, cDNA sequencing, or patient tissue analyses were performed), a clinical validation study, an evaluation of clinical utility, or a test of diagnostic sensitivity and specificity.

To prevent methodological circularity and outcome bias, the benchmark evaluation framework enforces strict mathematical and operational separation among three distinct data entities:
- **Entity $A$ (Runtime Engine Output):** The molecular consequence and protein consequence strings generated de novo by the deterministic engine during benchmark execution.
- **Entity $B$ (Frozen Expected Output):** Historical deterministic outputs stored in the candidate manifest during preliminary development, preserved strictly for post-hoc software regression and internal self-consistency checks.
- **Entity $C$ (External Molecular Annotation):** Independent molecular consequence consensus assertions curated from NCBI ClinVar records and normalized through locked semantic rules.

The primary evaluation endpoint of this study compares **Entity $A$ directly against Entity $C$ ($A$ vs $C$)**. Entity $B$ was completely excluded from the primary evaluation logic and did not participate in determining biological or external concordance.

---

## 2. Reference Sequence and Transcript Model
All sequence coordinates, genomic boundaries, and translation models in this study were anchored to versioned, curated RefSeq reference accessions (O'Leary et al., 2016). The human *HBB* locus is situated on the short arm of chromosome 11 (11p15.4). In accordance with the Matched Annotation from NCBI and EMBL-EBI (MANE) initiative, RefSeq accession `NM_000518.5` was selected as the canonical MANE Select transcript model (Morales et al., 2022). Genomic sequence context was defined by RefSeqGene accession `NG_000007.3` on build GRCh38.

The transcript model for `NM_000518.5` spans 626 transcribed nucleotides, comprising three coding exons and two intervening introns:
- **Exon 1:** Transcript nucleotides 1–142, containing 50 bp of 5' untranslated region ($c.-50$ to $c.-1$) and 92 bp of coding sequence ($c.1$ to $c.92$).
- **Intron 1:** 130 bp intervening sequence situated between $c.92$ and $c.93$.
- **Exon 2:** Transcript nucleotides 143–365, containing 223 bp of coding sequence ($c.93$ to $c.315$).
- **Intron 2:** 850 bp intervening sequence situated between $c.315$ and $c.316$.
- **Exon 3:** Transcript nucleotides 366–626, containing 129 bp of coding sequence ($c.316$ to $c.444$) and 132 bp of 3' untranslated region ($c.*1$ to $c.*132$).

The complete coding sequence (CDS) comprises 444 nucleotides ($c.1$ to $c.444$, 148 codons including termination), translating to a 147-amino-acid pre-protein (`NP_000509.1`). In human physiology, post-translational removal of the amino-terminal initiator methionine yields the 146-amino-acid mature $\beta$-globin polypeptide (Thein, 2013). Reference sequences, exon-intron boundaries, and codon dictionaries were stored as immutable data structures within `backend/app/core/reference.py` to ensure that coordinate conversion between cDNA ($c.$) positions and full transcript positions remained strictly deterministic.

---

## 3. Variant Representation and HGVS Handling
Sequence variants were represented using Human Genome Variation Society (HGVS) sequence variant nomenclature recommendations (den Dunnen et al., 2016). Input processing was implemented in a dedicated, pure-Python parsing module (`backend/app/core/hgvs.py`) that enforces a five-stage biological validation pipeline:
1. **Input Sanitization & Accession Validation:** Verifies that variant strings adhere to HGVS syntax and match authorized *HBB* reference accessions (`NM_000518.5` or `NG_000007.3`).
2. **Grammar and Token Parsing:** Employs regular expression grammars to decompose variant strings into coordinate offsets, variant types (substitutions, deletions, insertions, duplications), reference alleles, and alternate alleles.
3. **Biological Coordinate Integrity:** Verifies that coordinates exist within valid transcript ranges. In accordance with HGVS standards, base zero ($c.0$) is strictly rejected; the nucleotide immediately preceding the translation initiation site ($c.1$) is indexed as $c.-1$.
4. **Reference Allele Confirmation:** Performs an exact string match between the asserted reference nucleotide in the HGVS expression and the actual nucleotide present in the underlying `NM_000518.5` sequence at the specified coordinate. Any mismatch triggers an explicit `REFERENCE_MISMATCH` error.
5. **Canonical Normalization:** Converts valid expressions into a typed `NormalizedVariant` data structure, standardizing indels into uppercase DNA bases and converting intronic relative coordinates into transcript offsets.

### Resolution of Historical Codon Numbering Offsets
In hemoglobin clinical literature and legacy mutation databases, $\beta$-globin variants have historically been numbered starting from the amino-terminal valine of the mature polypeptide (omitting the initiator methionine) (Thein, 2013; Giardine et al., 2007). This historical convention created a systematic 1-amino-acid discrepancy relative to modern HGVS guidelines, in which codon 1 designates the initiator methionine. For example, the sickle cell mutation historically described as "Glu6Val" corresponds under HGVS nomenclature to `p.Glu7Val` ($c.20A>T$), and the hemoglobin E mutation historically designated as "Glu26Lys" corresponds to `p.Glu27Lys` ($c.79G>A$). The parser and normalization pipeline strictly enforces modern HGVS nomenclature anchored to codon 1 of `NM_000518.5` while mapping legacy aliases during curation to ensure syntactic consistency across historical records.

---

## 4. Deterministic Molecular Consequence Computation
Molecular consequence prediction was executed by a standalone deterministic bioinformatics engine (`backend/app/core/consequences.py`). The engine executes rule-based sequence transformations implemented entirely in pure Python, containing zero stochastic machine-learning models, zero calls to large language model (LLM) APIs, and zero external network dependencies.

The computation employs the Standard Genetic Code (NCBI Translation Table 1) to derive consequences across defined mutation categories:
- **Coding Single Nucleotide Variants (SNVs):** For substitutions situated within $c.1..c.444$, the engine calculates the affected codon index ($\lceil c\_pos / 3 \rceil$), extracts the wild-type triplet from the reference sequence, substitutes the mutant base at the corresponding intra-codon position ($0, 1,$ or $2$), and translates both triplets. The event is categorized as **Synonymous** if the translated amino acid is unchanged, **Missense** if an alternative amino acid is encoded, or **Nonsense** if a premature termination codon (`Ter`, `*`) is introduced.
- **Frameshift Indels (Deletions, Insertions, Duplications):** For insertions, duplications, or deletions whose net length is not a multiple of 3, the engine reconstructs the mutant transcript in silico. It identifies the first altered codon, translates subsequent codons in the shifted reading frame until encountering the first in-frame termination codon (`TAA`, `TAG`, `TGA`), and constructs full HGVS protein consequence syntax (e.g., `p.Glu7GlyfsTer...`).
- **Canonical Splicing Disruptions:** Variants located within the invariant 2-bp donor dinucleotide (`GT`, e.g., $c.92+1, c.92+2, c.315+1, c.315+2$) or acceptor dinucleotide (`AG`, e.g., $c.93-2, c.93-1, c.316-2, c.316-1$) at exon-intron boundaries are categorized respectively as **Splice Donor** or **Splice Acceptor** disruptions.
- **Untranslated Regions (UTRs):** Variants situated at $c. < 1$ are classified as **5' UTR Regulatory**, and variants situated at $c. > 444$ ($c.*1..c.*132$) are classified as **3' UTR Regulatory**.

### Architectural Decoupling from AI Layer
In the complete software application, generative artificial intelligence (via the Gemini API) is utilized strictly within a separate evidence retrieval and literature summarization module (`backend/app/ai.py`). The core consequence engine evaluated in this benchmark is architecturally decoupled from the AI layer; no generative model participated in consequence derivation, codon translation, or benchmark evaluation.

---

## 5. External Annotation Reference and Provenance
The external reference comparator (Entity $C$) was curated from NCBI ClinVar (Landrum et al., 2018; Landrum et al., 2020). ClinVar aggregates variant submissions from clinical diagnostic laboratories, academic research centers, and expert panels.

### Provenance Profile of the Benchmark Cohort
Every variant included in the primary evaluation cohort ($N = 55$) was derived from ClinVar records:
- **Database Origin:** 100% (55/55) of candidates possess valid ClinVar Variation IDs and Variation Change Version (VCV) records.
- **Evidence Review Tiers:** 54 candidates (98.18%) possessed a review status of $\ge 2$ stars (criteria provided, multiple submitters, no conflicts). One candidate (1.82%; candidate `HBB-CP2-072`, $c.67G>T$, $p.Glu23Ter$) possessed a 3-star review status (reviewed by an expert panel). Zero candidates possessed 0-star (no criteria) or 1-star (single submitter) review ratings in the primary cohort.
- **Independent Corroboration:** Exactly 0 of the 55 primary candidates possessed independent biological corroboration dossiers outside of ClinVar records. In manifest metadata, the attribute `independent_non_clinvar_corroboration` is recorded as `"NONE"` for all 55 variants.

### Consensus Nature of Comparator
ClinVar entries reflect submitter consensus and reference assertions rather than primary in vitro experimental data (Harrison et al., 2017). Although 98.18% of primary records represent multiple-submitter consensus, multiple laboratory submissions to a central public repository do not constitute independent biological validation experiments.

### Offline Execution Guarantee
To guarantee absolute benchmark reproducibility and prevent data drift from live database updates, all ClinVar annotations, review tiers, and submitter assertion strings were harvested, verified, and frozen into the local manifest (`research/manifest/phase2c_primary.json`). At benchmark execution time, the comparison engine operated strictly against this frozen manifest with zero network socket connections.

---

## 6. Cohort Construction and Eligibility Criteria
The primary evaluation cohort ($N = 55$) was established through a multi-stage curation and qualification pipeline designed during Checkpoints CP2.1 through CP2.3 of the research protocol:

```
Harvested Candidate Pool (N = 314)
│
├── Synthetic Negative Controls (Class C12: N = 18) ──> Segregated to Experiment D
│
└── Biological Candidate Pool (N = 296)
    │
    ├── Disqualified in CP2.1/CP2.2 (DO_NOT_USE: N = 53)
    │   ├── Historical Phase 2B Overlap: N = 20
    │   ├── Deep Intronic / Out of Scope: N = 19
    │   └── Phase 2A Prior Exposure: N = 14
    │
    ├── Relegated in CP2.2 (REVIEW_REQUIRED: N = 73)
    │   ├── Unsupported Promoter (> -50 bp): N = 31
    │   ├── HGVS Ambiguity / Complex Indels: N = 22
    │   ├── Low Evidence Tier (0-Star) / Conflicts: N = 18
    │   └── Ontology Discrepancies: N = 2
    │
    ├── Relegated in CP2.2 (PROPOSED_SECONDARY: N = 42)
    │   └── 0-Star ClinVar records without assertion criteria
    │
    ├── Relegated in CP2.2 (CONDITIONAL: N = 9)
    │   └── Incomplete protein annotations or format differences
    │
    └── Qualified Primary Pool in CP2.2 (PROPOSED_PRIMARY: N = 119)
        │
        ├── Relegated in CP2.3 (CONDITIONAL: N = 64)
        │   ├── 1-Star Single Submitter ClinVar Evidence: N = 63
        │   └── Multi-Codon Deletion (25 codons): N = 1
        │
        └── Approved Primary Cohort (APPROVED: N = 55)
            └── Formally Locked in CP2.3.2 and Frozen in CP3
```

### Methodological Disclosure of Incorporation / Verification Bias
A critical methodological finding established during the CP4.4 scientific audit (`research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md`, Section 5) must be explicitly disclosed: **candidate admission into the primary evaluation cohort incorporated deterministic engine agreement during curation**.

Specifically, in `research/curation/run_independent_verification.py` (lines 231–246), assignment of a biological candidate to the `PROPOSED_PRIMARY` eligibility tier explicitly required that `comparison_status == "EXACT_AGREEMENT"`. Candidates where the deterministic engine encountered errors, where HGVS parsing failed, or where runtime output diverged from external annotations were systematically diverted into `REVIEW_REQUIRED`, `CONDITIONAL`, or `DO_NOT_USE`. Furthermore, the subsequent human review protocol (`run_cp2_3_human_review.py`) exclusively sampled candidates from `PROPOSED_PRIMARY`.

In clinical epidemiology and computational validation, this practice introduces **incorporation bias** (also termed **verification bias**). Because cohort eligibility was conditioned on initial agreement with the deterministic engine, the primary cohort ($N = 55$) represents an **artificially enriched, highly concordant subset**. The resulting benchmark evaluates **software self-consistency, deterministic rule execution fidelity, and consensus database alignment on clean records**, rather than an unbiased, unselected prospective sample of all *HBB* variants.

---

## 7. Benchmark Freeze and Reproducibility Specifications
To eliminate post-hoc parameter tuning, cherry-picking, or data alteration, the evaluation cohort, execution protocol, and software environment were formally frozen prior to corrected benchmark execution:
- **Primary Manifest:** `research/manifest/phase2c_primary.json`
- **Candidate Count:** Exactly $N = 55$ biological variants.
- **Primary Manifest SHA256:** `39eb60de0e60dea8a76f2290912905b197fb1a04b738f72b0493bcdab2e0eb96` (verified against `phase2c_primary.sha256`).
- **Benchmark Protocol Document:** `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` (Version 1.0.0; SHA256: `e4bad0a095cdfa8112a649f3d8a0794cf0078d218611bb965020b100ba368969`).
- **Historical Baseline Manifest:** `research/manifest/frozen_test.json` (SHA256: `2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994`; 0 overlapping candidates).
- **Target Engine Commit:** Git commit `845f595cc039e006d74237945450c7b4a9569ee6`.
- **Execution Environment:** Python 3.14.7 (AMD64) on Windows 10 (Build 10.0.19045), recorded in `research/protocol/PHASE2C_ENVIRONMENT_RECORD.json`.

Execution was managed by a standardized runner script (`research/curation/run_phase2c_benchmark.py`) that performed mandatory pre-execution hash verification of the dataset and protocol before invoking the comparison engine.

---

## 8. Primary and Secondary Endpoints

### Primary Evaluation Endpoint ($A$ vs $C$)
The predefined primary endpoint was **Molecular Consequence Concordance**, defined as the proportion of primary cohort candidates for which the runtime deterministic engine consequence (Entity $A$) matched the normalized external ClinVar molecular annotation (Entity $C$):
$$\text{Primary Concordance} = \frac{\sum_{i=1}^{N} \mathbb{I}(A_i^{\text{mol}} = C_i^{\text{mol}})}{N}$$
Primary concordance status was categorized as a binary outcome:
- `MATCH`: Runtime normalized consequence is identical to external normalized annotation.
- `DISCREPANCY`: Runtime normalized consequence differs from external normalized annotation.

### Secondary Endpoints
1. **Protein Consequence Concordance:** Evaluates exact string and semantic matching between runtime protein predictions and normalized external protein annotations. Classified into four discrete statuses:
   - `MATCH`: Exact semantic nomenclature agreement (e.g., `p.Glu7Val` vs `p.Glu7Val`).
   - `DISCREPANCY`: Divergence in protein representation (e.g., engine-derived complete frameshift syntax vs ClinVar truncated representation).
   - `INCOMPLETE`: External ClinVar record lacks a protein consequence string.
   - `NOT_APPLICABLE`: Non-coding variants (e.g., UTR variants) where no protein alteration exists.
2. **Ten-Tier Error Category Hierarchy:** Categorizes every candidate according to a fixed, pre-specified precedence hierarchy designed to identify the root cause of any failure mode:
   $$\text{ENGINE\_ERROR} > \text{HGVS\_AMBIGUITY} > \text{REFERENCE\_MISMATCH} > \text{ENGINE\_UNSUPPORTED} >$$
   $$\text{EXTERNAL\_CONFLICT} > \text{EXTERNAL\_ANNOTATION\_INCOMPLETE} > \text{EXACT\_MOLECULAR\_AGREEMENT} >$$
   $$\text{MOLECULAR\_AGREEMENT\_PROTEIN\_DIFFERENCE} > \text{PROTEIN\_AGREEMENT\_CLASS\_DIFFERENCE} > \text{UNRESOLVED}$$

### Normalization of External Annotations
To enable rigorous computational comparison without penalizing cosmetic syntax variations, external ClinVar annotations were normalized through locked semantic rules (`research/curation/phase2c_comparison_engine.py`):
- **Molecular Category Normalization:** Maps Sequence Ontology synonyms to unified categories (e.g., `"missense_variant"`, `"missense variant"` $\to$ `"Missense"`; `"stop_gained"` $\to$ `"Nonsense"`; `"frameshift_variant"` $\to$ `"Frameshift"`; `"splice_acceptor_variant"` $\to$ `"Splice Acceptor"`).
- **Truncated Frameshift Normalization:** NCBI ClinVar frequently stores shorthand frameshift expressions denoting only the initial affected amino acid (e.g., `p.Glu7fs` or `E7fs`) rather than full translation syntax terminating at the stop codon (`p.Glu7GlyfsTer...`). The normalization module parses both formats to verify concordance of the initial affected residue and codon index.
- **Incomplete Splice Records:** Five canonical splice acceptor candidates (Class C09) lacked protein consequence strings in ClinVar records; these were classified as `EXTERNAL_ANNOTATION_INCOMPLETE` for protein evaluation while remaining fully evaluable for primary molecular consequence concordance.

---

## 9. Statistical Analysis
All statistical calculations were pre-specified in `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md`.

### Confidence Interval Calculation
Proportional success metrics ($k / n$) were evaluated using exact 95% two-sided binomial confidence intervals via the Clopper-Pearson method (Clopper & Pearson, 1934). Standard normal asymptotic approximations (Wald intervals) fail when observed success equals 100% ($k = n$) due to zero standard error. 

The exact Clopper-Pearson lower limit ($\theta_L$) and upper limit ($\theta_U$) were computed from the incomplete beta distribution by solving:
$$\sum_{x=k}^{n} \binom{n}{x} \theta_L^x (1 - \theta_L)^{n-x} = \frac{\alpha}{2} \quad (\text{for } k > 0)$$
$$\sum_{x=0}^{k} \binom{n}{x} \theta_U^x (1 - \theta_U)^{n-x} = \frac{\alpha}{2} \quad (\text{for } k < n)$$
with significance level $\alpha = 0.05$. When $k = n$, the upper confidence limit is exactly $1.00$ ($100.00\%$), and the lower limit simplifies to $\theta_L = (\alpha / 2)^{1/n} = (0.025)^{1/55} \approx 93.51\%$.

### Scope of Statistical Inference
The Clopper-Pearson confidence interval quantifies sampling uncertainty under the mathematical assumption of independent Bernoulli trials drawn from the specified cohort distribution. **This statistical interval does not correct for selection bias, incorporation bias, reference transcript dependency, or the absence of orthogonal secondary database corroboration.** It must not be interpreted as representing population-wide biological accuracy across all clinical *HBB* variants.

### Class Stratification and Zero-Count Policy
Concordance metrics were stratified across biological mutation classes. In accordance with Section 2.3 of the locked protocol, classes with zero primary candidates ($n = 0$) were reported explicitly as `NOT REPRESENTED IN PRIMARY COHORT` (CI: `null`), strictly prohibiting the assignment of artificial 0% or 100% values.

---

## 10. Synthetic Robustness Controls and Software Regression

### Synthetic Robustness Controls (Experiment D)
To evaluate the engine's error-handling architecture, an isolated cohort of 18 synthetic negative controls (Class C12) was constructed. These inputs represent malformed HGVS strings, out-of-bounds coordinates, non-existent transcript accessions, and reference nucleotide mismatches:
- **Design Mandate:** Evaluated strictly as a separate robustness experiment. C12 inputs were **never pooled into the primary biological denominator ($N = 55$)**.
- **Evaluation Criterion:** Robustness success was defined as graceful rejection with a typed `AnalysisError` (e.g., `INVALID_COORDINATE`, `OUT_OF_BOUNDS`, `REFERENCE_MISMATCH`, `SYNTAX_ERROR`) without silent mispredictions, uncaught runtime exceptions, or server crashes.

### Isolated Software Regression Check ($A$ vs $B$)
To verify that codebase modifications during development did not alter historical deterministic behavior, runtime engine outputs (Entity $A$) were compared against frozen expected deterministic outputs (Entity $B$) stored in the manifest:
$$\text{Regression Concordance} = \frac{\sum_{i=1}^{N} \mathbb{I}(A_i = B_i)}{N}$$
This check evaluates **software regression and code consistency only**. Entity $B$ reflects prior engine behavior, not external biological evidence; regression concordance was tracked as isolated technical metadata and did not contribute to biological performance metrics.

---

## 11. Methodological Limitations and Risk Disclosures
In accordance with authoring guardrails locked in `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md`, the methods are bounded by seven fundamental scientific limitations:

1. **Incorporation / Verification Bias:** As detailed in Section 6, admission into the primary evaluation cohort required deterministic engine concordance (`comparison_status == "EXACT_AGREEMENT"`). The 55-variant cohort is enriched for concordant records and evaluates computational rule fidelity rather than unselected prospective diagnostic accuracy.
2. **Single Database Provenance:** 100% of variants were derived from NCBI ClinVar consensus submissions. Zero candidates have finalized corroboration dossiers from secondary locus-specific databases (e.g., HbVar, IthaGenes, LOVD) or direct wet-lab sequencing.
3. **Unrepresented Mutation Classes:** Four of 11 biological mutation classes had zero representation in the primary cohort ($n = 0$ for C05 in-frame indels, C07 in-frame duplications, C08 splice donor disruptions, and C10 5' UTR regulatory variants). Performance across these mechanisms remains unmeasured.
4. **Small Subgroup Sample Sizes:** Represented classes C02 (Nonsense, $n = 3$), C09 (Splice Acceptor, $n = 5$), and C11 (3' UTR, $n = 2$) have modest sample sizes, yielding wide class-specific confidence intervals (e.g., C11 95% CI: [15.81%, 100.00%]).
5. **Secondary Protein Nomenclature Divergence:** Due to historical ClinVar formatting idioms (20 truncated frameshift representations and 5 omitted splice protein strings), exact protein nomenclature concordance was 50.91% (28/55).
6. **Transcript Model Exclusivity:** The engine is anchored exclusively to RefSeq `NM_000518.5`. Alternative splice isoforms, deep intronic mutations beyond defined intronic boundaries, and non-canonical promoter variants ($< -50$ bp) are outside the operational domain of this system.
7. **Orthogonality to Clinical Pathogenicity:** The pipeline computes molecular consequence categories. It does not perform clinical variant interpretation, does not assign ACMG pathogenicity classifications (Pathogenic vs Benign), and does not predict clinical phenotypic severity in patients.

---

## References

1. **Clopper CJ, Pearson ES.** The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika*. 1934;26(4):404–413. doi:[10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).
2. **den Dunnen JT, Dalgleish R, Maglott DR, et al.** HGVS Recommendations for the Description of Sequence Variants: 2016 Update. *Hum Mutat*. 2016;37(6):564–569. doi:[10.1002/humu.22981](https://doi.org/10.1002/humu.22981).
3. **Giardine B, van Baal S, Kaimakis P, et al.** HbVar database of human hemoglobin variants and thalassemia mutations: 2007 update. *Hum Mutat*. 2007;28(2):206. doi:[10.1002/humu.9479](https://doi.org/10.1002/humu.9479).
4. **Harrison SM, Dolinsky JS, Knight Johnson AE, et al.** Clinical laboratories collaborate to resolve differences in variant interpretations submitted to ClinVar. *Genet Med*. 2017;19(10):1096–1104. doi:[10.1038/gim.2017.14](https://doi.org/10.1038/gim.2017.14).
5. **Krusche P, Trigg L, Boutros PC, et al.** Best practices for benchmarking germline small-variant calls in human genomes. *Nat Biotechnol*. 2019;37(5):555–560. doi:[10.1038/s41587-019-0054-x](https://doi.org/10.1038/s41587-019-0054-x).
6. **Landrum MJ, Lee JM, Benson M, et al.** ClinVar: improving access to variant interpretations and supporting evidence. *Nucleic Acids Res*. 2018;46(D1):D1062–D1067. doi:[10.1093/nar/gkx1153](https://doi.org/10.1093/nar/gkx1153).
7. **Landrum MJ, Chitipothu S, Liu C, et al.** ClinVar: public archive of interpretations of clinically relevant variants. *Nucleic Acids Res*. 2020;48(D1):D835–D844. doi:[10.1093/nar/gkz1014](https://doi.org/10.1093/nar/gkz1014).
8. **Morales J, Pujar S, Loveland JE, et al.** A joint NCBI and EMBL-EBI transcript set for clinical genomics and research. *Nature*. 2022;604(7905):310–315. doi:[10.1038/s41586-022-04558-8](https://doi.org/10.1038/s41586-022-04558-8).
9. **O'Leary NA, Wright MW, Brister JR, et al.** Reference sequence (RefSeq) database at NCBI: current status, taxonomic expansion, and functional annotation. *Nucleic Acids Res*. 2016;44(D1):D733–D745. doi:[10.1093/nar/gkv1189](https://doi.org/10.1093/nar/gkv1189).
10. **Richards S, Aziz N, Bale S, et al.** Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genet Med*. 2015;17(5):405–424. doi:[10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30).
11. **Stodden V, McNutt M, Bailey DH, et al.** Enhancing reproducibility for computational methods. *Science*. 2016;354(6317):1240–1241. doi:[10.1126/science.aah6168](https://doi.org/10.1126/science.aah6168).
12. **Thein SL.** The molecular basis of $\beta$-thalassemia. *Cold Spring Harb Perspect Med*. 2013;3(5):a011700. doi:[10.1101/cshperspect.a011700](https://doi.org/10.1101/cshperspect.a011700).

---

## Internal Repository Artifact Provenance Register

In accordance with Phase 5.2C quality controls, all project-specific statements in the Methods draft correspond directly to audited repository artifacts:

| Subsection | Factual Topic | Authoritative Repository Artifact | Exact Artifact Location / Key |
|---|---|---|---|
| **§1** | Study Design & Entity Definitions ($A, B, C$) | `research/protocol/CP4_1_DECISION_MATRIX.md` | Sections 2.1–2.4 |
| **§2** | Reference Transcript & Genomic Coordinates | `backend/app/core/reference.py` | Model `ReferenceSequence`; lines 11–31 |
| **§3** | HGVS Parser Pipeline & Codon Offsets | `backend/app/core/hgvs.py` | Function `parse_hgvs`; lines 32–46 |
| **§4** | Deterministic Consequence Logic | `backend/app/core/consequences.py` | Functions `evaluate_consequence`, `evaluate_substitution` |
| **§5** | External Annotation Provenance & Review Tiers | `research/manifest/phase2c_primary.json` | All 55 records (`clinvar_star_rating`, `clinvar_variation_id`) |
| **§6** | Curation Funnel & Incorporation Bias | `research/results/CP4_4_SCIENTIFIC_INTERPRETATION_BIAS_AUDIT.md` | Section 4 (Funnel) & Section 5 (Verification Bias) |
| **§7** | Manifest Hash & Environment Baseline | `research/protocol/PHASE2C_ENVIRONMENT_RECORD.json` | Keys `dataset.dataset_sha256`, `repository.git_commit` |
| **§8** | Precedence Hierarchy & Normalization Rules | `research/curation/phase2c_comparison_engine.py` | Enums `ComparisonCategory`, function `evaluate_external_concordance` |
| **§9** | Exact Clopper-Pearson CI & Statistics | `research/curation/run_phase2c_benchmark.py` | Functions `binom_cdf`, `clopper_pearson_interval`; lines 26–64 |
| **§10** | Robustness Controls & Software Regression | `research/results/phase2c_benchmark_summary.json` | Keys `robustness_experiment`, `software_regression_metadata` |
| **§11** | Seven Locked Methodological Limitations | `research/manuscript/MANUSCRIPT_EVIDENCE_MATRIX.md` | Section 4.9 (CLM-LIM-01 through CLM-LIM-15) |
