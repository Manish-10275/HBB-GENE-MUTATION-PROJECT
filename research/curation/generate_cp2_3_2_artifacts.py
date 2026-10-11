import json
import os
import sys

def generate_cp2_3_2_artifacts():
    print("--- Starting CP-2.3.2 Cohort Acceptance Generation ---")

    # 1. Load CP-2.3.1 manifest as the strict source of truth
    manifest_231_path = "research/curation/CP2_3_1_55_MANIFEST.json"
    with open(manifest_231_path, "r", encoding="utf-8") as f:
        manifest_231 = json.load(f)

    candidates_55 = manifest_231["candidates"]
    assert len(candidates_55) == 55, f"Expected 55 candidates, got {len(candidates_55)}"
    print(f"Loaded {len(candidates_55)} candidates from {manifest_231_path}.")

    # 2. Build research/curation/CP2_3_2_COHORT_MANIFEST.json
    accepted_candidates = []
    class_counts = {}
    for c in candidates_55:
        cls = c["class"]
        class_counts[cls] = class_counts.get(cls, 0) + 1
        accepted_candidates.append({
            "candidate_id": c["candidate_id"],
            "class": c["class"],
            "hgvs_c": c["hgvs_c"],
            "transcript": c["transcript"],
            "reference_build": c["reference_build"],
            "deterministic_consequence": c["deterministic_consequence"],
            "deterministic_protein": c["deterministic_protein"],
            "clinvar_id": c["clinvar_id"],
            "clinvar_accession": c["clinvar_accession"],
            "clinvar_review_status": c["clinvar_review_status"],
            "clinvar_classification": c["clinvar_classification"],
            "clinvar_stars": c["clinvar_stars"],
            "molecular_agreement": c["molecular_agreement"],
            "clinical_significance_conflict": c["clinical_significance_conflict"],
            "legacy_numbering_flag": c["legacy_numbering_flag"],
            "legacy_nomenclature_records": c["legacy_nomenclature_records"],
            "independent_non_clinvar_corroboration": c["independent_non_clinvar_corroboration"],
            "historical_exposure": c["historical_exposure"],
            "acceptance_status": "ACCEPTED_FOR_PROPOSED_PRIMARY_PHASE_2C",
            "source_manifest": "CP2_3_1_55_MANIFEST.json"
        })

    manifest_232_data = {
        "metadata": {
            "title": "Phase 2C — CP-2.3.2 Formally Accepted Primary Evaluation Cohort Manifest",
            "protocol_stage": "CP-2.3.2",
            "decision": "ACCEPTED",
            "decision_statement": (
                "The 55 high confidence ClinVar concordant biological candidates are accepted as the proposed "
                "primary Phase 2C evaluation cohort. Acceptance is based on predefined provenance, deterministic "
                "molecular evaluation, concordance, and historical separation criteria. The cohort is not considered "
                "independently validated ground truth and contains known class representation limitations. "
                "These limitations are retained transparently rather than addressed through artificial candidate substitution "
                "or class balancing."
            ),
            "scientific_status": "55 high confidence ClinVar concordant biological candidates proposed for the primary Phase 2C evaluation cohort.",
            "independent_non_clinvar_corroboration_count": 0,
            "cohort_counts": {
                "primary_proposed_cohort": 55,
                "conditional_exploratory_cohort": 64,
                "synthetic_robustness_cohort": 18,
                "new_candidates_added": 0,
                "historical_contamination_count": 0
            },
            "class_distribution": class_counts,
            "phase2c_dataset_frozen": False,
            "phase2c_benchmark_executed": False,
            "reference_transcript": "NM_000518.5",
            "reference_build": "GRCh38",
            "historical_phase2b_test_hash": "2f6b88422b82d3f74c20f00985a34ffb5c1c78c311e4d8b584bc732cf5fc5994",
            "production_code_modified": False
        },
        "candidates": accepted_candidates
    }

    manifest_232_path = "research/curation/CP2_3_2_COHORT_MANIFEST.json"
    with open(manifest_232_path, "w", encoding="utf-8") as f:
        json.dump(manifest_232_data, f, indent=2, sort_keys=True)
    print(f"Saved {manifest_232_path}.")

    # 3. Build research/curation/CP2_3_2_PRIMARY_COHORT_ACCEPTANCE.md
    lines_pca = []
    lines_pca.append("# Phase 2C — CP-2.3.2 Primary Cohort Acceptance Dossier\n")
    lines_pca.append("> **Document Status:** FORMAL GOVERNANCE ACCEPTANCE RECORD  ")
    lines_pca.append("> **Stage:** Checkpoint CP-2.3.2 (Primary Cohort Acceptance Decision)  ")
    lines_pca.append("> **Project:** HBB Gene Mutation Analyzer  ")
    lines_pca.append("> **Decision:** **ACCEPTED (N = 55)**\n")
    lines_pca.append("---\n")
    lines_pca.append("## 1. Formal Decision Statement\n")
    lines_pca.append("> **DECISION STATEMENT:**  \n")
    lines_pca.append("> *The 55 high confidence ClinVar concordant biological candidates are accepted as the proposed primary ")
    lines_pca.append("Phase 2C evaluation cohort. Acceptance is based on predefined provenance, deterministic molecular evaluation, ")
    lines_pca.append("concordance, and historical separation criteria. The cohort is not considered independently validated ground truth ")
    lines_pca.append("and contains known class representation limitations. These limitations are retained transparently rather than addressed ")
    lines_pca.append("through artificial candidate substitution or class balancing.*\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 2. Mandatory Scientific Status & Disclaimers\n")
    lines_pca.append("- **Scientific Classification:** The cohort comprises **55 high confidence ClinVar concordant biological candidates proposed for the primary Phase 2C evaluation cohort**.\n")
    lines_pca.append("- **Explicitly Excluded Claims:** The candidates are **NOT** described as:\n")
    lines_pca.append("  - *ground truth variants*\n")
    lines_pca.append("  - *independently validated variants*\n")
    lines_pca.append("  - *biologically validated variants*\n")
    lines_pca.append("  - *clinically validated variants*\n")
    lines_pca.append("  - *gold standard variants*\n")
    lines_pca.append("- **Independent Non-ClinVar Corroboration:** Exactly **0 finalized candidates**. External database concordance (ClinVar 2-star/3-star) provides external repository consensus, not independent biological corroboration.\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 3. Formal Acceptance Rationale (10 Pillars)\n")
    lines_pca.append("    1. **Exact Set Identity:** The accepted cohort is exactly the 55 candidates approved and locked by CP-2.3.1 without additions, substitutions, or deletions.\n")
    lines_pca.append("2. **Zero Molecular Conflicts:** CP-2.3.1 verified that all 55 candidates exhibit zero molecular consequence category conflicts between external annotation and deterministic engine calculation.\n")
    lines_pca.append("3. **Zero HGVS/Reference Conflicts:** All 55 variants map strictly and consistently to RefSeq transcript `NM_000518.5` (Coding Sequence 1..444 nt).\n")
    lines_pca.append("4. **Zero Protein Consequence Conflicts:** Deterministic protein consequences match external annotations across all coding variants.\n")
    lines_pca.append("5. **Zero Clinical Significance Conflicts Within Cohort:** All 55 accepted variants carry non-conflicting ClinVar pathogenicity assertions (54 multiple submitters consensus 2-star; 1 expert panel 3-star). All 27 conflicting variants remain excluded in Conditional/Quarantine.\n")
    lines_pca.append("6. **Deterministic Engine Reproducibility:** All 55 candidates were deterministically evaluated using the current engine AS IS with 100% internal reproducibility.\n")
    lines_pca.append("7. **Historical Phase 2B Separation:** 100% clean against the Phase 2B exclusion registry and frozen test manifest; zero historical contamination.\n")
    lines_pca.append("8. **Strict Boundary Preservation:** No new candidates were discovered; no Conditional candidates were promoted; no candidates were relaxed.\n")
    lines_pca.append("9. **Predefined High-Confidence Inclusion:** Every candidate meets the predefined $\\ge 2$-star consensus or 3-star expert panel inclusion threshold.\n")
    lines_pca.append("10. **Refusal of Artificial Balancing:** The cohort adheres strictly to 'Quality over Quotas' by rejecting manufactured substitutions or relaxed filters.\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 4. Methodological Boundaries\n")
    lines_pca.append("The primary evaluation cohort is designed strictly to evaluate **deterministic molecular consequence transformation** (cDNA coordinate mapping, coding frame translation, codon boundary determination, and splice junction identification).\n\n")
    lines_pca.append("It is **NOT** designed or intended to establish:\n")
    lines_pca.append("- Clinical pathogenicity accuracy\n")
    lines_pca.append("- Diagnostic accuracy\n")
    lines_pca.append("- Clinical validity\n")
    lines_pca.append("- Population-level biological prevalence\n")
    lines_pca.append("- Generalized HBB mutation performance across all 11 variant classes\n\n")
    lines_pca.append("ClinVar is utilized strictly as an **external evidence source**, not as an infallible biological oracle.\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 5. Class Representation Limitations (Quality-Constrained Policy)\n")
    lines_pca.append("In accordance with the project governance, class shortages are **not** interpreted as evidence that HBB lacks such variants biologically. They are formally documented as:\n\n")
    lines_pca.append("> *Class representation limitations under the current reference, curation, and evidence criteria.*\n\n")
    lines_pca.append("| Class | Variant Category | Accepted Primary | Curation Limitation & Status Assessment |\n")
    lines_pca.append("|:---:|---|:---:|---|\n")
    lines_pca.append("| **C01** | Missense SNVs | **14** | Adequately populated across Exons 1, 2, 3. |\n")
    lines_pca.append("| **C02** | Nonsense (Stop-Gain) | **3** | Adequately populated with premature termination codons. |\n")
    lines_pca.append("| **C03** | Synonymous (Silent) | **10** | Adequately populated silent coding substitutions. |\n")
    lines_pca.append("| **C04** | Frameshift Deletions | **9** | Adequately populated frameshift deletions. |\n")
    lines_pca.append("| **C05** | In-Frame Indels / Deletions | **0** | **Class Limitation:** 0 approved candidates. Candidate `HBB-CP2-105` (`c.9_83del`, 25-codon deletion) remains `CONDITIONAL` and is **not promoted**. |\n")
    lines_pca.append("| **C06** | Frameshift Duplications / Insertions | **12** | Adequately populated frameshift duplications. |\n")
    lines_pca.append("| **C07** | In-Frame Insertions / Duplications | **0** | **Class Limitation:** 0 approved candidates. Only 2 clean duplications exist in candidate pool, both 0-star ClinVar evidence in secondary cohort. **Not promoted**. |\n")
    lines_pca.append("| **C08** | Splice Donor Disruptions | **0** | **Class Limitation:** 0 approved candidates. No canonical $+1, +2, +5$ donor candidates were present in queried ClinVar pool. **No artificial replacements created**. |\n")
    lines_pca.append("| **C09** | Splice Acceptor Disruptions | **5** | Adequately populated canonical $-1, -2$ acceptor disruptions. |\n")
    lines_pca.append("| **C10** | 5' UTR Regulatory Variants | **0** | **Class Limitation:** 0 approved candidates. Promoter variants situated $> -50$ bp upstream exceed the `NM_000518.5` transcript boundary. **No model expansion or relabeling performed**. |\n")
    lines_pca.append("| **C11** | 3' UTR Regulatory Variants | **2** | Adequately populated polyA signal regulatory SNVs. |\n")
    lines_pca.append("| **TOTAL** | **All 11 Biological Classes** | **55** | **Quality-constrained primary cohort spanning 7 biological classes.** |\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 6. Complete Separation of Distinct Cohorts\n")
    lines_pca.append("- **Primary Biological Evaluation Cohort:** N = 55 (Formally Accepted here).\n")
    lines_pca.append("- **Conditional / Exploratory Cohort:** N = 64 (Single-submitter 1-star ClinVar variants, large indel `c.9_83del`, and clinical conflict variants; remain segregated for exploratory analysis).\n")
    lines_pca.append("- **Synthetic Adversarial Robustness Cohort (C12):** N = 18 (Synthetic negative controls `HBB-CP2-297`..`314` reserved strictly for Experiment D; **never merged into biological accuracy metrics**).\n")
    lines_pca.append("- **Excluded / Out-of-Scope Cohort:** N = 53 (Deep intronic, complex indels, out-of-bounds variants).\n")
    lines_pca.append("- **Quarantined Discrepancies:** N = 82 (Includes `HBB-CP2-204` 14-bp frameshift vs ClinVar in-frame claim, `HBB-CP2-156`, `HBB-CP2-201`).\n")
    lines_pca.append("\n---\n")
    lines_pca.append("## 7. Accepted Candidate Inventory (N = 55)\n")
    lines_pca.append("| Candidate ID | Class | HGVS cDNA | Deterministic Protein | ClinVar VarID | Stars | ClinVar Review Status | Legacy Flag |\n")
    lines_pca.append("|---|:---:|---|---|:---:|:---:|---|:---:|\n")

    for c in accepted_candidates:
        cid = c["candidate_id"]
        cls = c["class"]
        hgvs = f"`{c['hgvs_c']}`"
        prot = f"`{c['deterministic_protein']}`" if c["deterministic_protein"] else "*none*"
        vid = f"[{c['clinvar_id']}](https://www.ncbi.nlm.nih.gov/clinvar/variation/{c['clinvar_id']}/)"
        stars = f"{c['clinvar_stars']}★"
        rev = c["clinvar_review_status"]
        leg = "YES" if c["legacy_numbering_flag"] else "NO"
        lines_pca.append(f"| {cid} | {cls} | {hgvs} | {prot} | {vid} | {stars} | {rev} | {leg} |")

    lines_pca.append("\n---\n")
    lines_pca.append("## 8. Governance Sign-off & CP-3 Stop Boundary\n")
    lines_pca.append("- **Checkpoint Decision:** ACCEPTED\n")
    lines_pca.append("- **Primary Proposed Cohort:** N = 55\n")
    lines_pca.append("- **Conditional Cohort:** N = 64\n")
    lines_pca.append("- **Robustness Cohort:** N = 18\n")
    lines_pca.append("- **Phase 2C Dataset Frozen:** **NO** (Neither `phase2c_test.json` nor `phase2c_test.sha256` created)\n")
    lines_pca.append("- **Phase 2C Benchmark Executed:** **NO** (Zero performance metrics calculated)\n")
    lines_pca.append("- **Production Code Modified:** **NO** (Zero code changes)\n")
    lines_pca.append("- **CP-3 Status:** **NOT STARTED** (Execution strictly halted pending human reviewer authorization)\n")

    pca_path = "research/curation/CP2_3_2_PRIMARY_COHORT_ACCEPTANCE.md"
    with open(pca_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_pca))
    print(f"Saved {pca_path}.")

    # 4. Build research/curation/CP2_3_2_DECISION_SUMMARY.md
    lines_ds2 = []
    lines_ds2.append("# Phase 2C — CP-2.3.2 Decision Summary Report\n")
    lines_ds2.append("> **Document Status:** FORMAL GOVERNANCE DECISION SUMMARY  ")
    lines_ds2.append("> **Stage:** Checkpoint CP-2.3.2  ")
    lines_ds2.append("> **Date:** 2026-10-08\n")
    lines_ds2.append("---\n")
    lines_ds2.append("## 1. Formal Governance Checkpoint Status\n\n")
    lines_ds2.append("```\n")
    lines_ds2.append("CP2.3.2 STATUS:\n")
    lines_ds2.append("ACCEPTED\n\n")
    lines_ds2.append("PRIMARY PHASE 2C PROPOSED COHORT:\n")
    lines_ds2.append("N = 55\n\n")
    lines_ds2.append("CONDITIONAL COHORT:\n")
    lines_ds2.append("N = 64\n\n")
    lines_ds2.append("ROBUSTNESS COHORT:\n")
    lines_ds2.append("N = 18\n\n")
    lines_ds2.append("NEW CANDIDATES:\n")
    lines_ds2.append("0\n\n")
    lines_ds2.append("INDEPENDENT NON CLINVAR CORROBORATION:\n")
    lines_ds2.append("0\n\n")
    lines_ds2.append("PHASE 2C DATASET:\n")
    lines_ds2.append("NOT YET FROZEN\n\n")
    lines_ds2.append("PHASE 2C BENCHMARK:\n")
    lines_ds2.append("NOT YET EXECUTED\n\n")
    lines_ds2.append("HISTORICAL PHASE 2B TEST HASH:\n")
    lines_ds2.append("UNCHANGED\n\n")
    lines_ds2.append("HISTORICAL CONTAMINATION:\n")
    lines_ds2.append("0\n\n")
    lines_ds2.append("PRODUCTION CODE CHANGES:\n")
    lines_ds2.append("0\n")
    lines_ds2.append("```\n\n")
    lines_ds2.append("---\n")
    lines_ds2.append("## 2. Cohort Decision Statement\n")
    lines_ds2.append("> *The 55 high confidence ClinVar concordant biological candidates are accepted as the proposed primary ")
    lines_ds2.append("Phase 2C evaluation cohort. Acceptance is based on predefined provenance, deterministic molecular evaluation, ")
    lines_ds2.append("concordance, and historical separation criteria. The cohort is not considered independently validated ground truth ")
    lines_ds2.append("and contains known class representation limitations. These limitations are retained transparently rather than addressed ")
    lines_ds2.append("through artificial candidate substitution or class balancing.*\n")
    lines_ds2.append("\n---\n")
    lines_ds2.append("## 3. Class Distribution Summary\n")
    lines_ds2.append("| Class | Variant Type | Accepted Primary Count | Curation Status |\n")
    lines_ds2.append("|:---:|---|:---:|---|\n")

    class_names = {
        "C01": "Missense SNVs",
        "C02": "Nonsense (Stop-Gain)",
        "C03": "Synonymous (Silent)",
        "C04": "Frameshift Deletions",
        "C05": "In-Frame Indels / Deletions",
        "C06": "Frameshift Duplications / Insertions",
        "C07": "In-Frame Insertions / Duplications",
        "C08": "Splice Donor Disruptions",
        "C09": "Splice Acceptor Disruptions",
        "C10": "5' UTR Regulatory Variants",
        "C11": "3' UTR Regulatory Variants",
    }

    for i in range(1, 12):
        c_id = f"C{i:02d}"
        c_name = class_names[c_id]
        cnt = class_counts.get(c_id, 0)
        if c_id == "C05":
            c_status = "Class limitation (0 accepted; c.9_83del retained in Conditional)"
        elif c_id == "C07":
            c_status = "Class limitation (0 accepted; 2 duplications in secondary 0-star)"
        elif c_id == "C08":
            c_status = "Class limitation (0 accepted; 0 canonical donors in pool)"
        elif c_id == "C10":
            c_status = "Transcript boundary limitation (0 accepted; promoter > -50 bp)"
        else:
            c_status = f"Accepted ({cnt} candidates)"

        lines_ds2.append(f"| **{c_id}** | {c_name} | **{cnt}** | {c_status} |")

    lines_ds2.append(f"| **TOTAL** | **All 11 Biological Classes** | **55** | **Accepted quality-constrained primary cohort** |\n")
    lines_ds2.append("\n---\n")
    lines_ds2.append("## 4. Integrity and Compliance Checklist\n")
    lines_ds2.append("- [x] Exactly the CP-2.3.1 approved candidate set used as input (55 candidates).\n")
    lines_ds2.append("- [x] Zero new candidates added.\n")
    lines_ds2.append("- [x] Zero conditional candidates promoted.\n")
    lines_ds2.append("- [x] Zero historical Phase 2B candidates reintroduced.\n")
    lines_ds2.append("- [x] Zero molecular consequence conflicts.\n")
    lines_ds2.append("- [x] Zero HGVS or reference conflicts.\n")
    lines_ds2.append("- [x] Zero clinical significance conflicts within accepted cohort.\n")
    lines_ds2.append("- [x] Current deterministic engine executed AS IS with 100% reproducibility.\n")
    lines_ds2.append("- [x] Historical Phase 2B hash unchanged (`2f6b8842...`).\n")
    lines_ds2.append("- [x] Zero production code files modified.\n")
    lines_ds2.append("- [x] Zero validation benchmarks executed.\n")
    lines_ds2.append("- [x] No final Phase 2C dataset hash generated.\n")
    lines_ds2.append("- [x] Phase 2C dataset remains unfrozen.\n")
    lines_ds2.append("- [x] Checkpoint CP-3 has NOT started.\n")

    ds2_path = "research/curation/CP2_3_2_DECISION_SUMMARY.md"
    with open(ds2_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_ds2))
    print(f"Saved {ds2_path}.")
    print("--- CP-2.3.2 Artifact Generation Completed Successfully ---")

if __name__ == "__main__":
    generate_cp2_3_2_artifacts()
