import json
import re

def audit_candidates():
    with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = data["candidates"]
    metadata = data.get("metadata", {})

    print(f"Auditing {len(candidates)} candidates...")

    for c in candidates:
        cid = c["candidate_id"]
        cdna = c["HGVS_input"]
        target_class = c["target_class_id"]
        status = c["exclusion_status"]
        prot = c.get("reported_protein_consequence") or ""
        prov = c.get("provenance_notes", "")
        clinsig = c.get("clinical_significance_if_available") or "None"
        ex_reason = c.get("exclusion_reason")

        # 1. Research Category & Robustness Controls
        if target_class == "C12":
            c["research_category"] = "ROBUSTNESS_NEGATIVE_CONTROL"
            c["scope_status"] = "ROBUSTNESS_CONTROL"
            c["ground_truth_quality"] = "A_STRONG"
            c["clinvar_only"] = False
            c["independent_support"] = "Synthetic Adversarial Control Battery (Deterministic Test Framework)"
            c["conflict_status"] = "NO_CONFLICT_DETECTED"
            c["recommendation"] = "RECOMMENDED"
            c["recommendation_reason"] = "Valid negative control testing deterministic error handling and coordinate/syntax validation; reserved for Robustness Experiment (not biological accuracy panel)."
            continue

        c["research_category"] = "BIOLOGICAL_VALIDATION"
        c["clinvar_only"] = True  # Primary source is ClinVar database

        # 2. Extract ClinVar Review Level & Stars
        review_stars = 0
        review_desc = "no assertion criteria"
        if "reviewed by expert panel" in prov.lower():
            review_stars = 3
            review_desc = "3 stars (reviewed by expert panel)"
        elif "multiple submitters, no conflict" in prov.lower():
            review_stars = 2
            review_desc = "2 stars (criteria provided, multiple submitters, no conflicts)"
        elif "single submitter" in prov.lower():
            review_stars = 1
            review_desc = "1 star (criteria provided, single submitter)"
        elif "conflicting" in prov.lower():
            review_stars = 1
            review_desc = "1 star (conflicting interpretations)"

        # Independent Support description
        c["independent_support"] = f"ClinVar Record ({review_desc})"

        # 3. Conflict Detection
        conflict = False
        conflict_notes = []
        if "conflicting" in clinsig.lower() or "conflicting" in prov.lower():
            conflict = True
            conflict_notes.append("Conflicting clinical pathogenicity interpretations reported in ClinVar.")

        if "," in prot:
            conflict = True
            conflict_notes.append(f"Multiple alternative protein consequence annotations ({prot}).")

        c["conflict_status"] = "CONFLICT_DETECTED" if conflict else "NO_CONFLICT_DETECTED"

        # 4. Excluded Candidates
        if status == "EXCLUDED":
            c["scope_status"] = "EXCLUDED_HISTORICAL_OVERLAP"
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "DO_NOT_USE"
            c["recommendation_reason"] = f"Permanently disqualified by Exclusion Registry: {ex_reason}"
            continue

        # 5. Scope & Complexity Assessment
        is_deep_intronic = False
        is_complex_indel = False
        is_canonical_splice = False

        # Intronic checks
        if "+" in cdna or ("-" in cdna and not cdna.startswith("c.-")):
            m_splice = re.search(r"c\.\d+([+-]\d+)[A-Za-z]>[A-Za-z]", cdna)
            if m_splice:
                offset_str = m_splice.group(1)
                offset = int(offset_str)
                if offset_str in ("+1", "+2", "+5"):
                    is_canonical_splice = True
                elif offset_str in ("-1", "-2"):
                    is_canonical_splice = True
                else:
                    is_deep_intronic = True
            else:
                # Intronic indel / delins
                is_complex_indel = True

        # Exonic complex indels
        if "delins" in cdna.lower():
            is_complex_indel = True

        # Check for non-standard repeat count syntax
        if "[" in cdna or "]" in cdna:
            c["scope_status"] = "NON_STANDARD_SYNTAX"
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "REVIEW_REQUIRED"
            c["recommendation_reason"] = "Bracketed repeat unit syntax (e.g. c.19GAG[1]); requires normalization to standard HGVS deletion interval (e.g. c.18_20del) before engine evaluation."
            continue

        if is_deep_intronic:
            c["scope_status"] = "OUT_OF_SCOPE"
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "DO_NOT_USE"
            c["recommendation_reason"] = "Deep intronic variant outside deterministic core scope; requires in silico splice-site prediction (e.g. SpliceAI) not implemented in deterministic engine."
            continue

        if is_complex_indel:
            c["scope_status"] = "OUT_OF_SCOPE"
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "REVIEW_REQUIRED"
            c["recommendation_reason"] = "Complex indel/delins requiring manual sequence walk verification and biological splice/reading frame inspection before panel admission."
            continue

        # Check for missing protein in coding classes
        if not prot and target_class in ("C01", "C02", "C03", "C04", "C05", "C06", "C07"):
            c["scope_status"] = "INCOMPLETE_ANNOTATION"
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "REVIEW_REQUIRED"
            c["recommendation_reason"] = "Missing explicit protein consequence in external record; sequence walk verification required."
            continue

        # 6. Quality Classification for In-Scope Variants
        c["scope_status"] = "IN_SCOPE"

        if conflict:
            c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
            c["recommendation"] = "REVIEW_REQUIRED"
            c["recommendation_reason"] = "; ".join(conflict_notes)
        elif review_stars >= 2:
            # 2 or 3 stars with concordant data
            c["ground_truth_quality"] = "A_STRONG"
            c["recommendation"] = "RECOMMENDED"
            c["recommendation_reason"] = f"Strong molecular concordance ({review_desc}) with unambiguous coding/protein annotation."
        elif review_stars == 1:
            c["ground_truth_quality"] = "B_MODERATE"
            c["recommendation"] = "CONDITIONAL"
            c["recommendation_reason"] = "Single submitter with criteria provided (1 star); valid molecular consequence but limited independent corroboration."
        else:
            # 0 stars
            c["ground_truth_quality"] = "C_WEAK"
            c["recommendation"] = "CONDITIONAL"
            c["recommendation_reason"] = "No assertion criteria provided in external record (0 stars); provisional annotation requiring secondary literature validation."

        # Special C07 evaluation
        if target_class == "C07":
            if "ter" in prot.lower() or "*" in prot:
                c["ground_truth_quality"] = "D_REVIEW_REQUIRED"
                c["recommendation"] = "REVIEW_REQUIRED"
                c["recommendation_reason"] = f"In-frame insertion introduces immediate premature termination codon ({prot}); biological consequence is nonsense, not neutral in-frame insertion."

    # Save updated candidate pool
    metadata["audit_stage"] = "CP-2.1 Quality Audit"
    metadata["last_audited"] = "2026-10-08T08:45:00+00:00"
    data["metadata"] = metadata

    with open("research/curation/candidate_pool.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    print("Quality audit successfully applied to research/curation/candidate_pool.json.")

if __name__ == "__main__":
    audit_candidates()
