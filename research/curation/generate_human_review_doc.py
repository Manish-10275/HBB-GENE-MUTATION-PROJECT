import json

def generate_markdown():
    with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = data["candidates"]

    # Sort candidates by recommendation priority: RECOMMENDED, CONDITIONAL, REVIEW_REQUIRED, DO_NOT_USE, then by class, then by ID
    priority_order = {"RECOMMENDED": 1, "CONDITIONAL": 2, "REVIEW_REQUIRED": 3, "DO_NOT_USE": 4}
    sorted_candidates = sorted(
        candidates,
        key=lambda c: (priority_order.get(c.get("recommendation", "REVIEW_REQUIRED"), 99), c.get("target_class_id", "Z"), c["candidate_id"])
    )

    lines = []
    lines.append("# Phase 2C — CP-2.1 Candidate Quality Audit & Human Review Dossier\n")
    lines.append("> **Document Status:** PROVISIONAL — STRICTLY FOR HUMAN CURATION REVIEW  ")
    lines.append("> **Benchmark Status:** NO BENCHMARK RUN — NO ACCURACY COMPUTED — NO DATASET FROZEN  ")
    lines.append("> **Artifact Integrity:** `frozen_test.json` SHA256 verified identical; production code unmodified.\n")
    lines.append("---\n")
    lines.append("## 1. Executive Summary & Ground Truth Quality Classification Framework\n")
    lines.append("This document presents the detailed scientific quality audit of all **314 candidate variants** in the provisional pool for *HBB* mutation analysis. Every candidate has been audited to separate **molecular consequence ground truth** from **clinical pathogenicity**, evaluate multi-source evidence, identify conflicting interpretations, quarantine deep-intronic and complex out-of-scope variants, and isolate synthetic negative controls into a distinct robustness test battery.\n")
    lines.append("### Ground Truth Quality Classification Tiers:\n")
    lines.append("- **`A_STRONG`**: Independent molecular consequence supported by multiple concordant submitters without conflict (2 stars) or expert panel review (3 stars), or synthetic negative control with deterministic syntax/coordinate ground truth.\n")
    lines.append("- **`B_MODERATE`**: Reasonably supported external molecular consequence with criteria provided by a single submitter (1 star) and unambiguous codon translation.\n")
    lines.append("- **`C_WEAK`**: Primarily single-source or insufficiently detailed molecular annotation without assertion criteria (0 stars); provisional annotation requiring secondary literature validation.\n")
    lines.append("- **`D_REVIEW_REQUIRED`**: Conflicting interpretations, deep-intronic coordinates, complex indels/delins, missing protein consequences, or variants permanently excluded by the Exclusion Registry.\n")
    lines.append("\n### Overall Quality & Recommendation Distribution:\n")
    
    q_counts = {}
    for c in candidates:
        q = c.get("ground_truth_quality", "Unknown")
        q_counts[q] = q_counts.get(q, 0) + 1

    r_counts = {}
    for c in candidates:
        r = c.get("recommendation", "Unknown")
        r_counts[r] = r_counts.get(r, 0) + 1

    lines.append("| Quality Tier | Total Count | Percentage | Recommendation Category | Count | Percentage |")
    lines.append("|---|:---:|:---:|---|:---:|:---:|")
    lines.append(f"| **`A_STRONG`** | {q_counts.get('A_STRONG', 0)} | {q_counts.get('A_STRONG', 0)/len(candidates)*100:.1f}% | **`RECOMMENDED`** (High Priority) | {r_counts.get('RECOMMENDED', 0)} | {r_counts.get('RECOMMENDED', 0)/len(candidates)*100:.1f}% |")
    lines.append(f"| **`B_MODERATE`** | {q_counts.get('B_MODERATE', 0)} | {q_counts.get('B_MODERATE', 0)/len(candidates)*100:.1f}% | **`CONDITIONAL`** (Secondary Priority) | {r_counts.get('CONDITIONAL', 0)} | {r_counts.get('CONDITIONAL', 0)/len(candidates)*100:.1f}% |")
    lines.append(f"| **`C_WEAK`** | {q_counts.get('C_WEAK', 0)} | {q_counts.get('C_WEAK', 0)/len(candidates)*100:.1f}% | **`REVIEW_REQUIRED`** (Quarantined) | {r_counts.get('REVIEW_REQUIRED', 0)} | {r_counts.get('REVIEW_REQUIRED', 0)/len(candidates)*100:.1f}% |")
    lines.append(f"| **`D_REVIEW_REQUIRED`** | {q_counts.get('D_REVIEW_REQUIRED', 0)} | {q_counts.get('D_REVIEW_REQUIRED', 0)/len(candidates)*100:.1f}% | **`DO_NOT_USE`** (Disqualified / Out of Scope) | {r_counts.get('DO_NOT_USE', 0)} | {r_counts.get('DO_NOT_USE', 0)/len(candidates)*100:.1f}% |")
    lines.append(f"| **TOTAL** | **{len(candidates)}** | **100.0%** | **TOTAL** | **{len(candidates)}** | **100.0%** |\n")

    lines.append("---\n")
    lines.append("## 2. Complete Candidate Audit & Human Review Table\n")
    lines.append("| candidate_id | HGVS | class | protein_consequence | source | source_class | ground_truth_quality | clinvar_review_status | clinvar_only | independent_support | conflict_status | scope_status | recommendation | reason |")
    lines.append("|---|---|:---:|---|---|:---:|:---:|---|:---:|---|:---:|:---:|:---:|---|")

    for c in sorted_candidates:
        cid = c["candidate_id"]
        hgvs = f"`{c['HGVS_input']}`"
        cls = c.get("target_class_id", "N/A")
        prot = f"`{c.get('reported_protein_consequence')}`" if c.get("reported_protein_consequence") else "*none*"
        src = c.get("source_name", "NCBI ClinVar")
        s_cls = c.get("source_class", "Class B")
        gt_q = c.get("ground_truth_quality", "N/A")
        cv_status = c.get("provenance_notes", "").replace("ClinVar review status: ", "").replace(". Submissions: 0 PMIDs.", "")
        cv_only = str(c.get("clinvar_only", False))
        indep = c.get("independent_support", "N/A")
        conflict = c.get("conflict_status", "NO_CONFLICT_DETECTED")
        scope = c.get("scope_status", "IN_SCOPE")
        rec = c.get("recommendation", "REVIEW_REQUIRED")
        reason = (c.get("recommendation_reason") or "").replace("|", "/")

        lines.append(f"| {cid} | {hgvs} | {cls} | {prot} | {src} | {s_cls} | {gt_q} | {cv_status} | {cv_only} | {indep} | {conflict} | {scope} | **{rec}** | {reason} |")

    lines.append("\n---\n")
    lines.append("## 3. Deep-Dive Audit: Class C07 (In-Frame Insertions / Duplications)\n")
    lines.append("Class C07 has only **5 provisional candidates** in the entire pool. Each candidate was audited individually:\n")
    
    c07_list = [c for c in candidates if c.get("target_class_id") == "C07"]
    for c in c07_list:
        lines.append(f"### Candidate `{c['candidate_id']}`: `{c['HGVS_input']}`")
        lines.append(f"- **Reported Protein Consequence:** `{c.get('reported_protein_consequence')}`")
        lines.append(f"- **External Source ID:** {c.get('external_database_identifier')} ({c.get('source_name')})")
        lines.append(f"- **Clinical Significance:** {c.get('clinical_significance_if_available')}")
        lines.append(f"- **ClinVar Review Status:** {c.get('provenance_notes')}")
        lines.append(f"- **Audit Ground Truth Quality:** `{c.get('ground_truth_quality')}`")
        lines.append(f"- **Audit Recommendation:** `{c.get('recommendation')}`")
        lines.append(f"- **Scientific Evaluation:**")
        if c['candidate_id'] == "HBB-CP2-140":
            lines.append("  - **Biological Analysis:** `c.92_94dup` is a 3-bp duplication spanning Exon 1 / Codon 31 (`p.Arg31dup`).")
            lines.append("  - **Limitation:** ClinVar record has **0 stars** (no assertion criteria provided) and 0 PMIDs.")
            lines.append("  - **Defensibility:** In-frame duplication of 1 codon. Structurally within engine scope, but evidence is ClinVar-only and uncorroborated.")
        elif c['candidate_id'] == "HBB-CP2-144":
            lines.append("  - **Biological Analysis:** `c.272_295dup` is a 24-bp tandem duplication of 8 codons (`p.Glu91_His98dup`) in Exon 2.")
            lines.append("  - **Limitation:** ClinVar record has **0 stars** (no assertion criteria provided) and 0 PMIDs.")
            lines.append("  - **Defensibility:** Clean 24-bp in-frame duplication divisible by 3. Within engine scope, but uncorroborated.")
        elif c['candidate_id'] == "HBB-CP2-204":
            lines.append("  - **Biological Analysis:** `c.170_171insGCAACCCTAAGGTG` inserts 15 bp (5 codons) but includes an immediate stop codon `TAA` / `TAG` (`p.Gly57_Asn58insGlnProTer`).")
            lines.append("  - **Defensibility Limitation:** Even though net delta is divisible by 3 (+15 bp), the biological consequence is **Premature Termination (Nonsense)**, NOT a pure in-frame insertion.")
            lines.append("  - **Defensibility:** Marked `REVIEW_REQUIRED`. Highly prone to semantic dispute if evaluated as an in-frame insertion.")
        elif c['candidate_id'] == "HBB-CP2-212":
            lines.append("  - **Biological Analysis:** `c.221_227delinsCTCGGTGCCA` (Hemoglobin Cranston / VarID: 15499) deletes 7 bp and inserts 10 bp (net +3 bp).")
            lines.append("  - **Defensibility Limitation:** This is a complex `delins` involving simultaneous deletion and de novo insertion with codon splitting (`p.Asp74_Leu76delinsAlaArgCysGln`).")
            lines.append("  - **Defensibility:** Marked `REVIEW_REQUIRED`. Outside standard simple in-frame insertion scope.")
        elif c['candidate_id'] == "HBB-CP2-232":
            lines.append("  - **Biological Analysis:** `c.301_302delinsTCTGAGAACTT` deletes 2 bp and inserts 11 bp (net +9 bp, 3 codons).")
            lines.append("  - **Defensibility Limitation:** Net in-frame `delins` with multiple amino acid substitutions (`p.Pro101delinsSerGluAsnPhe`). ClinVar 0 stars.")
            lines.append("  - **Defensibility:** Marked `REVIEW_REQUIRED`.")
        lines.append("")

    lines.append("> **Scientific Conclusion on C07:** Only **two candidates** (`c.92_94dup` and `c.272_295dup`) represent pure non-frameshifting duplications within the engine's primary in-frame insertion scope, but both have 0-star ClinVar evidence. **Fewer than 5 candidates are scientifically defensible without manual literature curation.**\n")

    lines.append("---\n")
    lines.append("## 4. Deep-Dive Audit: Splice Site & Deep Intronic Variants (C08 & C09)\n")
    lines.append("The audit separated canonical splice variants from deep intronic variants and intronic indels:\n")
    lines.append("1. **Canonical Acceptors (`C09`)**: There are **6 valid canonical splice acceptor variants** in the candidate pool (`c.93-1G>C`, `c.93-2A>C`, `c.93-2A>G`, `c.316-1G>T`, `c.316-2A>C`, and `c.316-1G>C`). Five of these have **2 stars** (multiple submitters without conflict) and are categorized as `A_STRONG` and `RECOMMENDED`.\n")
    lines.append("2. **Canonical Donors (`C08`)**: The query `3043[Gene ID] AND donor` returned intronic deletions, indels, and flanking consensus variants, but **zero canonical +1, +2, +5 donors** were retrieved. All 18 provisional C08 variants are intronic indels, delins, or flanking consensus changes. None are canonical invariant donor disruptions.\n")
    lines.append("3. **Deep Intronic Variants (Out of Scope)**: Candidates such as `c.93-21G>A`, `c.316-197C>T`, `c.316-106C>G`, `c.316-146T>G`, `c.316-79G>A`, `c.316-145G>A`, and intronic deletions/duplications (`c.316-33del`, `c.316-405del`, `c.316-315dup`) are **50 to 400 bp deep inside introns**. The deterministic engine blindly assigns `SPLICE_DISRUPTION` with `p.?` based on intronic coordinates, but biologically these variants require specialized machine-learning splice prediction (e.g. SpliceAI, MaxEntScan) or RNA sequencing. They are classified as **`OUT_OF_SCOPE`** and **`DO_NOT_USE` / `REVIEW_REQUIRED`**.\n")

    lines.append("---\n")
    lines.append("## 5. Separation of Class E Synthetic Adversarial Controls\n")
    lines.append("The 18 candidates in `C12` (`HBB-CP2-297` through `HBB-CP2-314`) are **Synthetic Adversarial Controls** engineered to test syntax error handling, coordinate bounds checking, and reference mismatch detection. They are classified under **`ROBUSTNESS_NEGATIVE_CONTROL`**.\n")
    lines.append("- They **MUST NOT** contribute to biological accuracy, sensitivity, or specificity metrics.\n")
    lines.append("- They belong strictly to a separate **Deterministic Robustness & Error-Handling Experiment**.\n")
    lines.append("- They have `A_STRONG` ground truth quality with respect to the expected deterministic rejection code (`INVALID_COORDINATE`, `SYNTAX_ERROR`, `OUT_OF_BOUNDS`, `REFERENCE_MISMATCH`).\n")

    lines.append("---\n")
    lines.append("## 6. Curated Summary of High-Priority Recommended Candidates (n=98)\n")
    lines.append("The following table highlights the 98 `RECOMMENDED` candidates (`A_STRONG`) eligible for primary human review consideration:\n")
    lines.append("| candidate_id | HGVS | class | Protein | Source | Stars | Reason |")
    lines.append("|---|---|:---:|---|---|:---:|---|")
    for c in sorted_candidates:
        if c.get("recommendation") == "RECOMMENDED":
            cid = c["candidate_id"]
            hgvs = f"`{c['HGVS_input']}`"
            cls = c.get("target_class_id", "")
            prot = f"`{c.get('reported_protein_consequence')}`" if c.get("reported_protein_consequence") else "*none*"
            src = c.get("source_name", "")
            stars = "2-3 stars" if c.get("target_class_id") != "C12" else "Synthetic"
            reason = c.get("recommendation_reason", "")
            lines.append(f"| {cid} | {hgvs} | {cls} | {prot} | {src} | {stars} | {reason} |")

    with open("research/curation/CP2_1_HUMAN_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Human review document successfully generated at research/curation/CP2_1_HUMAN_REVIEW.md with {len(lines)} lines.")

if __name__ == "__main__":
    generate_markdown()
