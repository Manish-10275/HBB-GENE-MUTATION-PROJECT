import json

with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
    data = json.load(f)

candidates = data["candidates"]

print("=== SUMMARY BY CLASS ===")
class_counts = {}
for c in candidates:
    cid = c.get("target_class_id", "Unknown")
    status = c.get("exclusion_status", "Unknown")
    class_counts.setdefault(cid, {})
    class_counts[cid][status] = class_counts[cid].get(status, 0) + 1

for cid in sorted(class_counts.keys()):
    counts = class_counts[cid]
    total = sum(counts.values())
    print(f"{cid:5}: Total={total:3} | {counts}")

print("\n=== DUP / INS VARIANTS ===")
for c in candidates:
    cdna = c["HGVS_input"]
    if "dup" in cdna.lower() or "ins" in cdna.lower():
        cid = c.get("target_class_id")
        prot = c.get("reported_protein_consequence")
        status = c.get("exclusion_status")
        notes = c.get("exclusion_reason")
        print(f"{c['candidate_id']:12} | {cid:4} | {cdna:30} | {str(prot):30} | {status} | {notes}")
