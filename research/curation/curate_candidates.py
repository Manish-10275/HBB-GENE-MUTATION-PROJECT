"""
Candidate Pool Curation and Exclusion Audit Engine for Phase 2C Checkpoint CP-2.

Fetches authentic HBB records from NCBI ClinVar across 11 positive biological classes,
screens every candidate against exclusion_registry.json (including aliases and VarIDs),
assembles Class E adversarial negative controls, and records comprehensive provenance.

OUTPUT: research/curation/candidate_pool.json
DOES NOT touch production code or benchmark manifests.
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUSION_FILE = REPO_ROOT / "research" / "curation" / "exclusion_registry.json"
CANDIDATE_POOL_FILE = REPO_ROOT / "research" / "curation" / "candidate_pool.json"

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def load_exclusions() -> Tuple[Set[str], Set[str], Dict[str, List[str]]]:
    data = json.loads(EXCLUSION_FILE.read_text(encoding="utf-8"))
    excluded_variants = {v.upper() for v in data.get("excluded_variant_patterns", [])}
    excluded_ids = {str(i) for i in data.get("excluded_clinvar_variation_ids", [])}
    historical_aliases = data.get("known_historical_aliases", {})
    return excluded_variants, excluded_ids, historical_aliases


def normalize_c(c_str: str) -> str:
    s = c_str.strip()
    if ":" in s:
        s = s.split(":")[-1]
    return s.upper()


def search_category(query: str, retmax: int = 50) -> List[str]:
    params = {
        "db": "clinvar",
        "term": query,
        "retmode": "json",
        "retmax": str(retmax),
    }
    resp = requests.get(ESEARCH_URL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("esearchresult", {}).get("idlist", [])


def fetch_summaries(id_list: List[str]) -> Dict[str, Any]:
    if not id_list:
        return {}
    results = {}
    for i in range(0, len(id_list), 40):
        batch = id_list[i : i + 40]
        params = {
            "db": "clinvar",
            "id": ",".join(batch),
            "retmode": "json",
        }
        resp = requests.get(ESUMMARY_URL, params=params, timeout=25)
        resp.raise_for_status()
        data = resp.json().get("result", {})
        for uid in batch:
            if uid in data:
                results[uid] = data[uid]
        time.sleep(0.4)
    return results


def parse_clinvar_record(uid: str, rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    title = rec.get("title") or ""
    var_set = rec.get("variation_set", [])
    if not var_set:
        return None
    var_obj = var_set[0]

    cdna = var_obj.get("cdna_change")
    if not cdna or not cdna.startswith("c."):
        m = re.search(r"c\.([\*\-\d_]+(?:[A-Za-z]+>[A-Za-z]+|del[A-Za-z]*|dup[A-Za-z]*|ins[A-Za-z]+))", title)
        if m:
            cdna = f"c.{m.group(1)}"
        else:
            return None

    prot = rec.get("protein_change")
    if not prot:
        m_p = re.search(r"\((p\.[A-Za-z0-9_=\*\?]+)\)", title)
        if m_p:
            prot = m_p.group(1)

    mol_conseq_list = rec.get("molecular_consequence_list", [])
    clinsig_obj = rec.get("germline_classification", {})
    clinsig = clinsig_obj.get("description")
    review_status = clinsig_obj.get("review_status")

    aliases = var_obj.get("aliases", [])
    v_type = var_obj.get("variant_type", "")

    # Supporting submissions & citations
    supporting = rec.get("supporting_submissions", {})
    sc_records = supporting.get("scv", [])
    pmids = set()
    for scv in sc_records:
        if isinstance(scv, dict):
            for cit in scv.get("citations", []):
                pmid = cit.get("pmid")
                if pmid:
                    pmids.add(str(pmid))

    canonical_hgvs = f"NM_000518.5:{cdna}"

    return {
        "uid": uid,
        "title": title,
        "cdna": cdna,
        "canonical_hgvs": canonical_hgvs,
        "prot": prot,
        "mol_conseq_list": mol_conseq_list,
        "clinsig": clinsig,
        "review_status": review_status,
        "aliases": aliases,
        "variant_type": v_type,
        "pmids": sorted(list(pmids)),
    }


def categorize_variant(cdna: str, prot: Optional[str], mol_conseq_list: List[str]) -> Tuple[str, str, str, str]:
    """
    Returns (class_id, class_name, structural_type, region)
    """
    c_norm = cdna.upper()
    mc_lower = [str(x).lower() for x in mol_conseq_list]

    is_synonymous = any("synonymous" in x for x in mc_lower) or (prot and "=" in prot)
    is_nonsense = any("nonsense" in x or "stop" in x for x in mc_lower) or (prot and any(s in prot for s in ["TER", "*"]))
    is_inframe = any("inframe" in x for x in mc_lower)
    is_frameshift = any("frameshift" in x for x in mc_lower)

    if "C.-" in c_norm:
        return "C10", "5' UTR Regulatory Variants", "regulatory_utr", "5' UTR"
    if "C.*" in c_norm:
        return "C11", "3' UTR Regulatory Variants", "regulatory_utr", "3' UTR"

    if "+" in c_norm or ("-" in c_norm and not "C.-" in c_norm):
        if "+1" in c_norm or "+2" in c_norm or "+5" in c_norm:
            return "C08", "Splice Donor Disruptions", "splice", "Splice Donor"
        elif "-1" in c_norm or "-2" in c_norm:
            return "C09", "Splice Acceptor Disruptions", "splice", "Splice Acceptor"
        else:
            return "C08", "Splice Disruptions", "splice", "Intron"

    if "DELINS" in c_norm:
        m = re.search(r"C\.(\d+)(?:_(\d+))?DELINS([A-Z]+)", c_norm)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else start
            del_len = end - start + 1
            ins_len = len(m.group(3))
            diff = ins_len - del_len
            if diff % 3 == 0:
                if diff > 0:
                    return "C07", "In-Frame Insertions / Duplications", "insertion", "Exon"
                elif diff < 0:
                    return "C05", "In-Frame Deletions", "deletion", "Exon"
                else:
                    return "C05", "In-Frame Indel", "indel", "Exon"
            else:
                if diff > 0:
                    return "C06", "Frameshift Duplications / Insertions", "insertion", "Exon"
                else:
                    return "C04", "Frameshift Deletions", "deletion", "Exon"
        else:
            if is_inframe:
                return "C05", "In-Frame Deletions", "deletion", "Exon"
            return "C04", "Frameshift Deletions", "deletion", "Exon"

    if "DEL" in c_norm:
        m = re.search(r"C\.(\d+)_(\d+)DEL([A-Z]*)", c_norm)
        if m:
            start, end = int(m.group(1)), int(m.group(2))
            length = end - start + 1
            if length % 3 == 0 or is_inframe:
                return "C05", "In-Frame Deletions", "deletion", "Exon"
            else:
                return "C04", "Frameshift Deletions", "deletion", "Exon"
        else:
            if is_inframe:
                return "C05", "In-Frame Deletions", "deletion", "Exon"
            return "C04", "Frameshift Deletions", "deletion", "Exon"

    if "DUP" in c_norm:
        m = re.search(r"C\.(\d+)_(\d+)DUP([A-Z]*)", c_norm)
        if m:
            start, end = int(m.group(1)), int(m.group(2))
            length = end - start + 1
            if length % 3 == 0 or is_inframe:
                return "C07", "In-Frame Insertions / Duplications", "duplication", "Exon"
            else:
                return "C06", "Frameshift Duplications / Insertions", "duplication", "Exon"
        else:
            if is_inframe:
                return "C07", "In-Frame Insertions / Duplications", "duplication", "Exon"
            return "C06", "Frameshift Duplications / Insertions", "duplication", "Exon"

    if "INS" in c_norm:
        m = re.search(r"INS([A-Z]+)", c_norm)
        if m:
            ins_len = len(m.group(1))
            if ins_len % 3 == 0 or is_inframe:
                return "C07", "In-Frame Insertions / Duplications", "insertion", "Exon"
            else:
                return "C06", "Frameshift Duplications / Insertions", "insertion", "Exon"
        else:
            if is_inframe:
                return "C07", "In-Frame Insertions / Duplications", "insertion", "Exon"
            return "C06", "Frameshift Duplications / Insertions", "insertion", "Exon"

    if ">" in c_norm:
        if is_nonsense:
            return "C02", "Nonsense (Stop-Gain)", "substitution", "Exon"
        if is_synonymous:
            return "C03", "Synonymous (Silent)", "substitution", "Exon"
        return "C01", "Missense SNVs", "substitution", "Exon"

    return "C01", "Unclassified", "substitution", "Exon"


def map_molecular_consequence(class_id: str, prot: Optional[str]) -> str:
    mapping = {
        "C01": "Missense",
        "C02": "Nonsense",
        "C03": "Synonymous",
        "C04": "Frameshift",
        "C05": "In-frame Indel",
        "C06": "Frameshift",
        "C07": "In-frame Indel",
        "C08": "Splice Site Disruption",
        "C09": "Splice Site Disruption",
        "C10": "5' UTR Regulatory",
        "C11": "3' UTR Regulatory",
        "C12": "Adversarial Control",
    }
    return mapping.get(class_id, "Unknown")


def build_candidate_pool():
    excluded_variants, excluded_ids, historical_aliases = load_exclusions()
    print(f"Loaded {len(excluded_variants)} excluded variants and {len(excluded_ids)} excluded IDs.")

    queries = [
        ("C01", "3043[Gene ID] AND missense", 50),
        ("C02", "3043[Gene ID] AND nonsense", 40),
        ("C03", "3043[Gene ID] AND synonymous", 30),
        ("C04_C05", "3043[Gene ID] AND deletion", 60),
        ("C06_C07_dup", "3043[Gene ID] AND duplication", 100),
        ("C06_C07_ins", "3043[Gene ID] AND insertion", 60),
        ("C05_C07_inframe", "3043[Gene ID] AND in-frame", 20),
        ("C05_C07_indel", "3043[Gene ID] AND indel", 30),
        ("C08_donor", "3043[Gene ID] AND donor", 40),
        ("C09_acceptor", "3043[Gene ID] AND acceptor", 40),
        ("C10_5utr", "3043[Gene ID] AND 5 prime UTR", 20),
        ("C10_promoter", "3043[Gene ID] AND promoter", 40),
        ("C11_3utr", "3043[Gene ID] AND 3 prime UTR", 20),
    ]

    all_uids = []
    uid_to_query_class = {}
    for qclass, qstr, rmax in queries:
        uids = search_category(qstr, retmax=rmax)
        print(f"Query {qclass:16} -> {len(uids)} uids")
        for u in uids:
            if u not in uid_to_query_class:
                all_uids.append(u)
                uid_to_query_class[u] = qclass

    print(f"Total unique ClinVar UIDs fetched: {len(all_uids)}")
    summaries = fetch_summaries(all_uids)
    print(f"Retrieved {len(summaries)} record summaries.")

    candidates = []
    seen_cdna = set()
    candidate_idx = 1
    timestamp_now = datetime.now(timezone.utc).isoformat()

    # Track quotas per class
    class_counts = {f"C{i:02d}": 0 for i in range(1, 13)}

    for uid, rec in summaries.items():
        parsed = parse_clinvar_record(uid, rec)
        if not parsed:
            continue

        cdna = parsed["cdna"]
        norm_cdna = normalize_c(cdna)
        if norm_cdna in seen_cdna:
            continue
        seen_cdna.add(norm_cdna)

        class_id, class_name, var_type, region = categorize_variant(
            cdna, parsed["prot"], parsed["mol_conseq_list"]
        )

        # Check Exclusion Registry
        is_excluded = False
        exclusion_reason = None

        if norm_cdna in excluded_variants:
            is_excluded = True
            exclusion_reason = f"Exclusion Registry: cDNA string '{norm_cdna}' previously exposed in codebase or Phase 2B manifests."
        elif str(uid) in excluded_ids:
            is_excluded = True
            exclusion_reason = f"Exclusion Registry: ClinVar Variation ID '{uid}' previously exposed in fixtures or manifests."
        else:
            # Check aliases
            for al in parsed["aliases"]:
                if al.lower() in historical_aliases:
                    is_excluded = True
                    exclusion_reason = f"Exclusion Registry: Historical alias '{al}' matches known benchmark variant."
                    break

        # Check ground truth clarity
        status = "ELIGIBLE"
        independence_status = "GENUINELY_INDEPENDENT"
        curator_notes = "Curated from NCBI ClinVar record."

        if is_excluded:
            status = "EXCLUDED"
            independence_status = "PREVIOUSLY_EXPOSED"
        else:
            # Audit ground truth quality
            if not parsed["prot"] and class_id in ["C01", "C02", "C03", "C04", "C05", "C06", "C07"]:
                status = "REVIEW_REQUIRED"
                curator_notes = "Missing explicit protein consequence in ClinVar summary; requires sequence walk verification."
            elif not parsed["pmids"] and (not parsed["review_status"] or "criteria provided" not in parsed["review_status"]):
                status = "REVIEW_REQUIRED"
                curator_notes = "Single submitter without PMID citations; review required before inclusion."

        # Assign provenance class
        source_class = "Class B"
        if parsed["pmids"]:
            source_class = "Class B/C"

        record = {
            "candidate_id": f"HBB-CP2-{candidate_idx:03d}",
            "HGVS_input": cdna,
            "reference_transcript": "NM_000518.5",
            "reference_version": "NM_000518.5",
            "variant_class": var_type,
            "region": region,
            "source_class": source_class,
            "source_name": "NCBI ClinVar",
            "source_identifier": f"VCV_{uid}",
            "publication_identifier": parsed["pmids"],
            "external_database_identifier": f"VarID:{uid}",
            "reported_molecular_consequence": map_molecular_consequence(class_id, parsed["prot"]),
            "reported_protein_consequence": parsed["prot"],
            "clinical_significance_if_available": parsed["clinsig"],
            "legacy_nomenclature_if_present": parsed["aliases"],
            "canonical_HGVS_if_available": parsed["canonical_hgvs"],
            "ground_truth_status": "External Database Interpretation (Class B)",
            "independence_status": independence_status,
            "provenance_notes": f"ClinVar review status: {parsed['review_status'] or 'None'}. Submissions: {len(parsed['pmids'])} PMIDs.",
            "retrieval_timestamp": timestamp_now,
            "exclusion_status": status,
            "exclusion_reason": exclusion_reason,
            "curator_notes": curator_notes,
            "target_class_id": class_id,
            "target_class_name": class_name,
        }

        candidates.append(record)
        class_counts[class_id] += 1
        candidate_idx += 1

    # -------------------------------------------------------------
    # Add Class E Adversarial Negative Controls (18 variants)
    # Structured battery across 6 distinct failure mechanisms
    # -------------------------------------------------------------
    negative_controls = [
        # 1. Inverted coordinate ranges
        ("c.150_145del", "deletion", "Exon", "Inverted start/end coordinates (start 150 > end 145)", "INVALID_COORDINATE"),
        ("c.400_350del", "deletion", "Exon", "Inverted start/end coordinates (start 400 > end 350)", "INVALID_COORDINATE"),
        ("c.250_240dup", "duplication", "Exon", "Inverted start/end coordinates (start 250 > end 240)", "INVALID_COORDINATE"),
        # 2. Non-consecutive insertion coordinates
        ("c.50_53insA", "insertion", "Exon", "Non-consecutive insertion coordinates (flanking positions must differ by 1)", "SYNTAX_ERROR"),
        ("c.100_104insGCC", "insertion", "Exon", "Non-consecutive insertion coordinates (flanking positions must differ by 1)", "SYNTAX_ERROR"),
        ("c.200_205insTT", "insertion", "Exon", "Non-consecutive insertion coordinates (flanking positions must differ by 1)", "SYNTAX_ERROR"),
        # 3. Physical transcript boundary out-of-bounds
        ("c.650A>G", "substitution", "Exon", "cDNA position exceeds physical transcript length (628 bp)", "OUT_OF_BOUNDS"),
        ("c.750del", "deletion", "Exon", "cDNA position exceeds physical transcript length (628 bp)", "OUT_OF_BOUNDS"),
        ("c.800dup", "duplication", "Exon", "cDNA position exceeds physical transcript length (628 bp)", "OUT_OF_BOUNDS"),
        # 4. Intronic physical boundary out-of-bounds
        ("c.92+250G>A", "splice", "Intron 1", "Intronic coordinate exceeds physical length of Intron 1 (130 bp)", "OUT_OF_BOUNDS"),
        ("c.93-200G>A", "splice", "Intron 1", "Intronic coordinate exceeds physical length of Intron 1 (130 bp)", "OUT_OF_BOUNDS"),
        ("c.315+950G>A", "splice", "Intron 2", "Intronic coordinate exceeds physical length of Intron 2 (850 bp)", "OUT_OF_BOUNDS"),
        # 5. Coordinate syntax errors & Base zero
        ("c.0A>G", "substitution", "Exon", "Base zero (c.0) is not recognized by HGVS nomenclature", "INVALID_COORDINATE"),
        ("c.*0A>G", "regulatory_utr", "3' UTR", "Base zero offset in 3' UTR is invalid in HGVS", "INVALID_COORDINATE"),
        ("c.50A>Z", "substitution", "Exon", "Invalid nucleotide character 'Z' outside IUPAC standard", "SYNTAX_ERROR"),
        ("c.delA", "deletion", "Exon", "Malformed syntax missing nucleotide position", "SYNTAX_ERROR"),
        # 6. Reference allele mismatches
        ("c.70T>A", "substitution", "Exon", "Reference nucleotide mismatch: query states T at c.70, but NM_000518.5 has A", "REFERENCE_MISMATCH"),
        ("c.92+1A>G", "splice", "Splice Donor", "Reference nucleotide mismatch: query states A at donor +1, but reference has G", "REFERENCE_MISMATCH"),
    ]

    for neg_input, v_type, reg, rationale, err_code in negative_controls:
        # Check against exclusion registry
        norm_n = normalize_c(neg_input)
        is_ex = norm_n in excluded_variants
        ex_reason = f"Exclusion Registry: pattern '{norm_n}' previously exposed." if is_ex else None

        record = {
            "candidate_id": f"HBB-CP2-{candidate_idx:03d}",
            "HGVS_input": neg_input,
            "reference_transcript": "NM_000518.5",
            "reference_version": "NM_000518.5",
            "variant_class": v_type,
            "region": reg,
            "source_class": "Class E",
            "source_name": "Synthetic Adversarial Control",
            "source_identifier": f"SYNTH_NEG_{err_code}",
            "publication_identifier": [],
            "external_database_identifier": None,
            "reported_molecular_consequence": "Invalid / Rejected",
            "reported_protein_consequence": None,
            "clinical_significance_if_available": None,
            "legacy_nomenclature_if_present": [],
            "canonical_HGVS_if_available": None,
            "ground_truth_status": f"Synthetic Control: expected rejection [{err_code}]",
            "independence_status": "GENUINELY_INDEPENDENT" if not is_ex else "PREVIOUSLY_EXPOSED",
            "provenance_notes": f"Engineered negative control testing {rationale}.",
            "retrieval_timestamp": timestamp_now,
            "exclusion_status": "EXCLUDED" if is_ex else "ELIGIBLE",
            "exclusion_reason": ex_reason,
            "curator_notes": f"Designed to verify {err_code} rejection without silent guessing.",
            "target_class_id": "C12",
            "target_class_name": "Adversarial Negative Controls",
        }
        candidates.append(record)
        class_counts["C12"] += 1
        candidate_idx += 1

    payload = {
        "metadata": {
            "generated_timestamp": timestamp_now,
            "total_candidates_curated": len(candidates),
            "eligible_candidates": sum(1 for c in candidates if c["exclusion_status"] == "ELIGIBLE"),
            "excluded_candidates": sum(1 for c in candidates if c["exclusion_status"] == "EXCLUDED"),
            "review_required_candidates": sum(1 for c in candidates if c["exclusion_status"] == "REVIEW_REQUIRED"),
            "class_distribution": class_counts,
        },
        "candidates": candidates,
    }

    CANDIDATE_POOL_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nCandidate pool saved to {CANDIDATE_POOL_FILE}")
    print(f"Total candidates: {len(candidates)}")
    print(f"Eligible: {payload['metadata']['eligible_candidates']}")
    print(f"Excluded: {payload['metadata']['excluded_candidates']}")
    print(f"Review Required: {payload['metadata']['review_required_candidates']}")
    print("Class distribution:")
    for cid, cnt in sorted(class_counts.items()):
        print(f"  {cid}: {cnt}")


if __name__ == "__main__":
    build_candidate_pool()
