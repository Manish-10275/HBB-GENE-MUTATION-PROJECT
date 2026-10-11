import json
from collections import Counter

with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
    data = json.load(f)

candidates = data["candidates"]
metadata = data["metadata"]

print("TOTAL CANDIDATES:", len(candidates))

# Breakdown by status
status_counts = Counter(c["exclusion_status"] for c in candidates)
print("\nSTATUS BREAKDOWN:")
for s, n in status_counts.items():
    print(f"  {s}: {n}")

# Breakdown by Class ID
print("\nCLASS ID BREAKDOWN (Total / Eligible / Excluded / Review Required):")
for i in range(1, 13):
    cid = f"C{i:02d}"
    c_list = [c for c in candidates if c["target_class_id"] == cid]
    el = sum(1 for c in c_list if c["exclusion_status"] == "ELIGIBLE")
    ex = sum(1 for c in c_list if c["exclusion_status"] == "EXCLUDED")
    rr = sum(1 for c in c_list if c["exclusion_status"] == "REVIEW_REQUIRED")
    cname = c_list[0]["target_class_name"] if c_list else "Unknown"
    print(f"  {cid} ({cname:35}): Total={len(c_list):2} | Eligible={el:2} | Excluded={ex:2} | ReviewReq={rr:2}")

# Breakdown by Provenance / Source Class
print("\nSOURCE PROVENANCE CLASS BREAKDOWN:")
source_counts = Counter(c["source_class"] for c in candidates)
for sc, n in source_counts.items():
    print(f"  {sc}: {n}")

# Excluded variants details
print("\nEXCLUDED CANDIDATES AUDIT (Total: %d):" % status_counts.get("EXCLUDED", 0))
for c in candidates:
    if c["exclusion_status"] == "EXCLUDED":
        print(f"  ID: {c['candidate_id']} | cDNA: {c['HGVS_input']:18} | Source: {c['external_database_identifier']:10} | Reason: {c['exclusion_reason']}")

# Review Required variants details
print("\nREVIEW REQUIRED CANDIDATES AUDIT (Total: %d):" % status_counts.get("REVIEW_REQUIRED", 0))
for c in candidates:
    if c["exclusion_status"] == "REVIEW_REQUIRED":
        print(f"  ID: {c['candidate_id']} | Class: {c['target_class_id']} | cDNA: {c['HGVS_input']:20} | Prot: {str(c['reported_protein_consequence']):25} | Reason: {c['exclusion_reason']}")

# Adversarial Controls (Class E) details
print("\nADVERSARIAL NEGATIVE CONTROLS (C12) (Total: %d):" % sum(1 for c in candidates if c["target_class_id"] == "C12"))
for c in candidates:
    if c["target_class_id"] == "C12":
        print(f"  ID: {c['candidate_id']} | cDNA: {c['HGVS_input']:18} | Notes: {c['curator_notes']}")
