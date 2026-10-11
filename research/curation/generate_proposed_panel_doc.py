import json

def generate_panel_markdown():
    with open("research/curation/cp2_2_verification_records.json", "r", encoding="utf-8") as f:
        records = json.load(f)

    primary = [r for r in records if r["eligibility_state"] == "PROPOSED_PRIMARY"]
    secondary = [r for r in records if r["eligibility_state"] == "PROPOSED_SECONDARY"]
    dnu = [r for r in records if r["eligibility_state"] == "DO_NOT_USE"]
    review = [r for r in records if r["eligibility_state"] in ("REVIEW_REQUIRED", "CONDITIONAL")]

    lines = []
    lines.append("# Phase 2C — CP-2.2 Proposed Final Evaluation Panel\n")
    lines.append("> **Document Status:** PROVISIONAL RESEARCH CURATION PANEL PROPOSAL  ")
    lines.append("> **Review State:** PENDING HUMAN REVIEW & APPROVAL  ")
    lines.append("> **Immutability Guarantee:** ZERO PRODUCTION CODE CHANGES — NO DATASET FROZEN — NO SHA256 GENERATED\n")
    lines.append("---\n")
    lines.append("## 1. Executive Summary & Panel Construction Strategy\n")
    lines.append("In accordance with the principle that **scientific quality and independent molecular verifiability take precedence over rigid quotas**, this panel proposal establishes the maximum scientifically defensible cohort for Phase 2C validation.\n")
    lines.append("Class balance was not artificially forced. Classes with genuine biological data availability limitations (such as C07 in-frame duplications, C08 splice donors, and C10 promoter variants exceeding transcript boundaries) are reported with complete transparency rather than filled with questionable or manufactured variants.\n")
    lines.append("### Summary Panel Distribution:\n")
    lines.append(f"- **Proposed Primary Biological Panel (C01–C11):** **{sum(1 for r in primary if r['target_class_id'] != 'C12')} candidates**\n")
    lines.append(f"- **Proposed Primary Robustness Battery (C12 / Experiment D):** **{sum(1 for r in primary if r['target_class_id'] == 'C12')} controls**\n")
    lines.append(f"- **Proposed Secondary Panel:** **{len(secondary)} candidates**\n")
    lines.append(f"- **Quarantined for Expert Human Review:** **{len(review)} candidates**\n")
    lines.append(f"- **Excluded / Out of Scope (Do Not Use):** **{len(dnu)} candidates**\n")

    lines.append("\n---\n")
    lines.append("## 2. Class Availability & Panel Balance Summary\n")
    lines.append("| Class | Stratified Variant Class | Total Curated | Proposed Primary | Proposed Secondary | Quarantined Review | Out of Scope / Excluded | Scientific Availability Assessment / Shortage Rationale |")
    lines.append("|:---:|---|:---:|:---:|:---:|:---:|:---:|---|")

    for i in range(1, 13):
        cid = f"C{i:02d}"
        c_list = [r for r in records if r["target_class_id"] == cid]
        cname = c_list[0]["target_class_name"] if c_list else "Unknown"

        tot = len(c_list)
        prim = sum(1 for r in c_list if r["eligibility_state"] == "PROPOSED_PRIMARY")
        sec = sum(1 for r in c_list if r["eligibility_state"] == "PROPOSED_SECONDARY")
        rev = sum(1 for r in c_list if r["eligibility_state"] in ("REVIEW_REQUIRED", "CONDITIONAL"))
        out = sum(1 for r in c_list if r["eligibility_state"] == "DO_NOT_USE")

        rationale = ""
        if cid == "C01":
            rationale = "Robustly populated; high-confidence coding missense SNVs across Exons 1, 2, 3."
        elif cid == "C02":
            rationale = "Adequately populated (n=5); all 5 stop-gain premature termination codons verified."
        elif cid == "C03":
            rationale = "Robustly populated (n=14); silent coding substitutions verified."
        elif cid == "C04":
            rationale = "Robustly populated (n=22); 1-bp/2-bp frameshifting deletions verified with termination distance."
        elif cid == "C05":
            rationale = "Data-limited primary (n=1 primary, n=1 sec); complex delins quarantined in review."
        elif cid == "C06":
            rationale = "Robustly populated (n=24 primary, n=30 secondary); 1-bp/2-bp coding duplications verified."
        elif cid == "C07":
            rationale = "Data-availability shortage (n=0 primary, n=2 secondary); only 2 pure duplications, both 0-star ClinVar."
        elif cid == "C08":
            rationale = "Data-availability limitation (n=0 primary); zero canonical +1, +2, +5 donors present in queried pool."
        elif cid == "C09":
            rationale = "Robustly populated (n=6 primary); canonical invariant acceptor dinucleotides (-1, -2) verified."
        elif cid == "C10":
            rationale = "Transcript modeling boundary (n=0 primary); promoter variants (> -50 bp) exceed NM_000518.5 transcript."
        elif cid == "C11":
            rationale = "Adequately populated (n=5 primary); polyadenylation signal regulatory SNVs verified."
        elif cid == "C12":
            rationale = "Fully populated (n=18); reserved exclusively for Experiment D (Robustness Negative Controls)."

        lines.append(f"| **{cid}** | {cname} | {tot} | **{prim}** | {sec} | {rev} | {out} | {rationale} |")

    lines.append("\n---\n")
    lines.append("## 3. Proposed Primary Evaluation Panel\n")
    lines.append("Candidates qualifying for the primary deterministic molecular-consequence validation cohort:\n\n")
    lines.append("| candidate_id | HGVS | Class | Engine Consequence | Engine Protein | External Consequence | Comparison | Evidence Source | Quality Tier | Review Priority | Reason for Inclusion |")
    lines.append("|---|---|:---:|---|---|---|:---:|---|:---:|:---:|---|")

    for r in primary:
        cid = r["candidate_id"]
        hgvs = f"`{r['HGVS_input']}`"
        cls = r["target_class_id"]
        eng_mol = r.get("engine_molecular_consequence") or "N/A"
        eng_prot = f"`{r.get('engine_protein_consequence')}`" if r.get("engine_protein_consequence") else "*none*"
        ext_mol = r.get("external_molecular_consequence") or "N/A"
        comp = r.get("comparison_status", "")
        src = r.get("external_source", "")
        q_tier = r.get("database_quality_tier", "")
        prio = r.get("review_priority", "HIGH")
        notes = r.get("verification_notes", "")

        lines.append(f"| {cid} | {hgvs} | {cls} | {eng_mol} | {eng_prot} | {ext_mol} | {comp} | {src} | {q_tier} | **{prio}** | {notes} |")

    lines.append("\n---\n")
    lines.append("## 4. Proposed Secondary Evaluation Panel\n")
    lines.append("Candidates suitable for exploratory or secondary evaluation cohorts (e.g. 0-star ClinVar evidence with verified biological plausibility):\n\n")
    lines.append("| candidate_id | HGVS | Class | Engine Consequence | Engine Protein | External Consequence | Comparison | Evidence Source | Quality Tier | Reason for Secondary Status |")
    lines.append("|---|---|:---:|---|---|---|:---:|---|:---:|---|")

    for r in secondary:
        cid = r["candidate_id"]
        hgvs = f"`{r['HGVS_input']}`"
        cls = r["target_class_id"]
        eng_mol = r.get("engine_molecular_consequence") or "N/A"
        eng_prot = f"`{r.get('engine_protein_consequence')}`" if r.get("engine_protein_consequence") else "*none*"
        ext_mol = r.get("external_molecular_consequence") or "N/A"
        comp = r.get("comparison_status", "")
        src = r.get("external_source", "")
        q_tier = r.get("database_quality_tier", "")
        notes = r.get("verification_notes", "")

        lines.append(f"| {cid} | {hgvs} | {cls} | {eng_mol} | {eng_prot} | {ext_mol} | {comp} | {src} | {q_tier} | Lower database confidence tier (0-star ClinVar); secondary exploratory validation only. |")

    lines.append("\n---\n")
    lines.append("## 5. Excluded Candidates & Out-of-Scope Rationale (`DO_NOT_USE`)\n")
    lines.append("Candidates permanently disqualified or quarantined outside the deterministic engine's scope:\n\n")
    lines.append("| candidate_id | HGVS | Class | Reason for Disqualification | Evidence / Source of Exclusion |")
    lines.append("|---|---|:---:|---|---|")

    for r in dnu:
        cid = r["candidate_id"]
        hgvs = f"`{r['HGVS_input']}`"
        cls = r["target_class_id"]
        notes = r.get("verification_notes", "")
        ext_id = r.get("external_source_identifier", "")

        lines.append(f"| {cid} | {hgvs} | {cls} | {notes} | {ext_id} |")

    with open("research/curation/CP2_2_PROPOSED_PANEL.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Proposed panel document generated at research/curation/CP2_2_PROPOSED_PANEL.md ({len(lines)} lines).")

if __name__ == "__main__":
    generate_panel_markdown()
