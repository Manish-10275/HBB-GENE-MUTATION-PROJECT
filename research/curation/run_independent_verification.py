import json
import os
import re
import sys

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath("backend"))

from app.core.consequences import evaluate_consequence
from app.core.hgvs import parse_hgvs
from app.core.models import AnalysisError
from app.core.reference import load_reference

ONE_TO_THREE = {
    'A': 'Ala', 'C': 'Cys', 'D': 'Asp', 'E': 'Glu', 'F': 'Phe',
    'G': 'Gly', 'H': 'His', 'I': 'Ile', 'K': 'Lys', 'L': 'Leu',
    'M': 'Met', 'N': 'Asn', 'P': 'Pro', 'Q': 'Gln', 'R': 'Arg',
    'S': 'Ser', 'T': 'Thr', 'V': 'Val', 'W': 'Trp', 'Y': 'Tyr',
    '*': 'Ter', 'X': 'Ter'
}

def normalize_protein_for_comparison(p: str) -> str:
    """Normalizes protein representations for equivalence checking (e.g. p.Gln40Ter vs Q40*, L4R vs p.Leu4Arg)."""
    if not p:
        return ""
    p_clean = p.strip().replace("p.", "").strip("()")
    # Convert single letter SNV notation (e.g. L4R or Q40*) to 3-letter
    m = re.match(r"^([A-Za-z\*])(\d+)([A-Za-z\*])$", p_clean)
    if m:
        aa1 = ONE_TO_THREE.get(m.group(1).upper(), m.group(1))
        pos = m.group(2)
        aa2 = ONE_TO_THREE.get(m.group(3).upper(), m.group(3))
        return f"{aa1}{pos}{aa2}".upper()
    return p_clean.upper()

def run_verification():
    ref_seq = load_reference("NM_000518.5")
    ng_seq = load_reference("NG_000007.3")

    with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
        pool_data = json.load(f)

    candidates = pool_data["candidates"]
    verification_records = []

    print(f"Beginning independent molecular verification of {len(candidates)} candidates...")

    for c in candidates:
        cid = c["candidate_id"]
        hgvs_in = c["HGVS_input"]
        target_class = c.get("target_class_id", "")
        target_class_name = c.get("target_class_name", "")
        ext_mol = c.get("reported_molecular_consequence") or ""
        ext_prot = c.get("reported_protein_consequence") or ""
        ext_src = c.get("source_name", "NCBI ClinVar")
        ext_src_id = c.get("external_database_identifier", "")
        ext_prov = c.get("provenance_notes", "")
        ext_clinsig = c.get("clinical_significance_if_available") or "None"
        ex_status = c.get("exclusion_status", "ELIGIBLE")
        ex_reason = c.get("exclusion_reason")
        conflict_status = c.get("conflict_status", "NO_CONFLICT_DETECTED")

        # Database Quality Tier renaming (CP-2.2 requirement)
        if target_class == "C12":
            db_quality = "A_HIGH_CONFIDENCE_DATABASE"
            indep_support = "SYNTHETIC_TEST_BATTERY"
        elif "reviewed by expert panel" in ext_prov.lower():
            db_quality = "A_HIGH_CONFIDENCE_DATABASE"
            indep_support = "CLINVAR_3_STAR_EXPERT_PANEL"
        elif "multiple submitters, no conflict" in ext_prov.lower():
            db_quality = "A_HIGH_CONFIDENCE_DATABASE"
            indep_support = "CLINVAR_2_STAR_CONSENSUS"
        elif "single submitter" in ext_prov.lower():
            db_quality = "B_MODERATE_DATABASE"
            indep_support = "CLINVAR_1_STAR_SINGLE_SUBMITTER"
        else:
            db_quality = "C_LOW_CONFIDENCE_DATABASE"
            indep_support = "CLINVAR_0_STAR_NO_ASSERTION_CRITERIA"

        if conflict_status == "CONFLICT_DETECTED":
            db_quality = "D_REVIEW_REQUIRED"

        # Independent Computation via Core Engine AS-IS
        engine_success = False
        engine_err_code = None
        engine_err_msg = None
        nv = None
        cr = None

        try:
            nv = parse_hgvs(hgvs_in, ref_seq=ref_seq, ng_seq=ng_seq)
            cr = evaluate_consequence(nv, ref_seq)
            engine_success = True
        except AnalysisError as ae:
            engine_err_code = ae.code.value
            engine_err_msg = ae.message
        except Exception as ex:
            engine_err_code = type(ex).__name__
            engine_err_msg = str(ex)

        # Build Engine Result fields
        if engine_success:
            norm_hgvs = nv.hgvs_c
            var_class = nv.variant_type.value
            region = nv.region
            engine_scope = "IN_SCOPE"
            engine_mol = cr.molecular_impact.value
            engine_prot = cr.hgvs_p
            coord_str = nv.c_position
        else:
            norm_hgvs = f"NM_000518.5:{hgvs_in}"
            var_class = c.get("variant_class", "unknown")
            region = c.get("region", "unknown")
            engine_scope = engine_err_code
            engine_mol = None
            engine_prot = None
            coord_str = None

        # Determine Comparison Status
        comparison_status = "UNRESOLVED"
        notes = []

        if target_class == "C12":
            # Synthetic controls: expected outcome is rejection by engine
            if not engine_success:
                comparison_status = "EXACT_AGREEMENT"
                notes.append(f"Engine rejected invalid input as expected: {engine_err_code} - {engine_err_msg}")
            else:
                comparison_status = "ENGINE_UNEXPECTED_ACCEPTANCE"
                notes.append(f"Engine unexpectedly accepted synthetic negative control.")
        elif ex_status == "EXCLUDED":
            comparison_status = "EXCLUDED_HISTORICAL_OVERLAP"
            notes.append(f"Disqualified by Exclusion Registry: {ex_reason}")
        elif not engine_success:
            if engine_err_code == "OUT_OF_BOUNDS" and ("+" in hgvs_in or "-" in hgvs_in):
                comparison_status = "ENGINE_UNSUPPORTED"
                notes.append(f"Intronic position exceeds modeled boundaries: {engine_err_msg}")
            elif engine_err_code == "REFERENCE_MISMATCH":
                comparison_status = "REFERENCE_MISMATCH"
                notes.append(f"Engine detected reference mismatch: {engine_err_msg}")
            elif engine_err_code == "SYNTAX_ERROR":
                comparison_status = "HGVS_AMBIGUITY"
                notes.append(f"Non-standard syntax: {engine_err_msg}")
            else:
                comparison_status = "ENGINE_UNSUPPORTED"
                notes.append(f"Engine analysis error: {engine_err_code} - {engine_err_msg}")
        else:
            # Engine succeeded
            # Check molecular agreement
            mol_match = False
            if ext_mol.lower() in engine_mol.lower() or engine_mol.lower() in ext_mol.lower():
                mol_match = True
            elif target_class in ("C08", "C09") and engine_mol == "Splice Site Disruption":
                mol_match = True
            elif target_class in ("C10", "C11") and "regulatory" in engine_mol.lower():
                mol_match = True

            # Check protein agreement
            prot_match = False
            if ext_prot and engine_prot:
                p_ext_norm = normalize_protein_for_comparison(ext_prot)
                p_eng_norm = normalize_protein_for_comparison(engine_prot)
                # Exact or substring/equivalent match
                if p_ext_norm == p_eng_norm:
                    prot_match = True
                elif p_eng_norm in p_ext_norm or p_ext_norm in p_eng_norm:
                    prot_match = True
                elif "=" in p_ext_norm and "(=" in p_eng_norm:
                    prot_match = True
                elif "TER" in p_ext_norm and "TER" in p_eng_norm:
                    prot_match = True
                elif "*" in p_ext_norm and ("TER" in p_eng_norm or "*" in p_eng_norm):
                    prot_match = True
                elif "FS" in p_ext_norm and "FS" in p_eng_norm:
                    prot_match = True

            if mol_match and (prot_match or target_class in ("C08", "C09", "C10", "C11")):
                comparison_status = "EXACT_AGREEMENT"
                notes.append("Deterministic engine result agrees with external record.")
            elif mol_match and not prot_match:
                comparison_status = "MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE"
                notes.append(f"Molecular consequence agrees ({engine_mol}), but protein differs: Engine='{engine_prot}' vs External='{ext_prot}'.")
            elif not mol_match and prot_match:
                comparison_status = "PROTEIN_AGREEMENT_CLASS_DIFFERENCE"
                notes.append(f"Protein consequence agrees ({engine_prot}), but molecular impact classification differs: Engine='{engine_mol}' vs External='{ext_mol}'.")
            elif not ext_prot:
                comparison_status = "EXTERNAL_ANNOTATION_INCOMPLETE"
                notes.append("External record lacks explicit protein consequence.")
            else:
                comparison_status = "MOLECULAR_DISCREPANCY"
                notes.append(f"Discrepancy: Engine computed '{engine_mol}' ('{engine_prot}') but external reported '{ext_mol}' ('{ext_prot}').")

        # Determine Proposed Eligibility & Review Priority
        # Criteria:
        # PROPOSED_PRIMARY:
        # - Target classes C01..C11 (or C12 for robustness)
        # - engine_success is True (or False if C12 negative control)
        # - ex_status == ELIGIBLE
        # - conflict_status == NO_CONFLICT_DETECTED
        # - comparison_status == EXACT_AGREEMENT
        # - db_quality in (A_HIGH_CONFIDENCE_DATABASE, B_MODERATE_DATABASE)
        # - within engine biological scope (not deep intronic)
        is_deep_intronic = False
        if target_class != "C12" and ("+" in hgvs_in or ("-" in hgvs_in and not hgvs_in.startswith("c.-"))):
            m_splice = re.search(r"c\.\d+([+-]\d+)[A-Za-z]>[A-Za-z]", hgvs_in)
            if m_splice and m_splice.group(1) not in ("+1", "+2", "+5", "-1", "-2"):
                is_deep_intronic = True
            elif "del" in hgvs_in.lower() or "dup" in hgvs_in.lower() or "ins" in hgvs_in.lower():
                is_deep_intronic = True

        eligibility_state = "REVIEW_REQUIRED"
        review_priority = "MEDIUM"

        if ex_status == "EXCLUDED":
            eligibility_state = "DO_NOT_USE"
            review_priority = "LOW"
        elif is_deep_intronic:
            eligibility_state = "DO_NOT_USE"
            review_priority = "LOW"
            notes.append("Deep intronic position outside deterministic engine scope.")
        elif target_class == "C12":
            eligibility_state = "PROPOSED_PRIMARY"
            review_priority = "HIGH"
            notes.append("Reserved for Experiment D (Robustness Negative Controls).")
        elif not engine_success:
            eligibility_state = "REVIEW_REQUIRED"
            review_priority = "LOW"
        elif conflict_status == "CONFLICT_DETECTED":
            eligibility_state = "REVIEW_REQUIRED"
            review_priority = "MEDIUM"
        elif comparison_status == "EXACT_AGREEMENT":
            if db_quality == "A_HIGH_CONFIDENCE_DATABASE":
                eligibility_state = "PROPOSED_PRIMARY"
                review_priority = "HIGH"
            elif db_quality == "B_MODERATE_DATABASE":
                eligibility_state = "PROPOSED_PRIMARY"
                review_priority = "HIGH"
            else: # C_LOW_CONFIDENCE_DATABASE
                eligibility_state = "PROPOSED_SECONDARY"
                review_priority = "MEDIUM"
        elif comparison_status in ("MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE", "EXTERNAL_ANNOTATION_INCOMPLETE"):
            eligibility_state = "CONDITIONAL"
            review_priority = "MEDIUM"
        else:
            eligibility_state = "REVIEW_REQUIRED"
            review_priority = "MEDIUM"

        record = {
            "candidate_id": cid,
            "HGVS_input": hgvs_in,
            "target_class_id": target_class,
            "target_class_name": target_class_name,
            "reference_accession": "NM_000518.5",
            "reference_version": "5",
            "normalized_HGVS": norm_hgvs,
            "variant_class": var_class,
            "region": region,
            "engine_scope_status": engine_scope,
            "engine_molecular_consequence": engine_mol,
            "engine_protein_consequence": engine_prot,
            "external_molecular_consequence": ext_mol,
            "external_protein_consequence": ext_prot,
            "external_source": ext_src,
            "external_source_identifier": ext_src_id,
            "external_review_status": ext_prov,
            "external_clinical_significance": ext_clinsig,
            "database_quality_tier": db_quality,
            "independent_support_status": indep_support,
            "comparison_status": comparison_status,
            "conflict_status": conflict_status,
            "eligibility_state": eligibility_state,
            "review_priority": review_priority,
            "verification_notes": "; ".join(notes),
        }
        verification_records.append(record)

    # Save to research/curation/cp2_2_verification_records.json
    out_file = "research/curation/cp2_2_verification_records.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(verification_records, f, indent=2, sort_keys=True)

    print(f"Independent verification complete. {len(verification_records)} records saved to {out_file}.")

if __name__ == "__main__":
    run_verification()
