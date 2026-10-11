import json
from collections import Counter

with open("research/curation/cp2_2_verification_records.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Total verification records: {len(records)}")

comp_counts = Counter(r["comparison_status"] for r in records)
print("\n=== COMPARISON STATUS DISTRIBUTION ===")
for st, cnt in comp_counts.most_common():
    print(f"  {st:40}: {cnt:3} ({cnt/len(records)*100:.1f}%)")

elig_counts = Counter(r["eligibility_state"] for r in records)
print("\n=== ELIGIBILITY STATE DISTRIBUTION ===")
for el, cnt in elig_counts.most_common():
    print(f"  {el:25}: {cnt:3} ({cnt/len(records)*100:.1f}%)")

prio_counts = Counter(r["review_priority"] for r in records)
print("\n=== REVIEW PRIORITY DISTRIBUTION ===")
for p, cnt in prio_counts.most_common():
    print(f"  {p:15}: {cnt:3} ({cnt/len(records)*100:.1f}%)")

print("\n=== CLASS-BY-CLASS VERIFICATION & PROPOSED STATUS ===")
header = f"{'Class':5} | {'Name':32} | {'Total':5} | {'Primary':7} | {'Secondary':9} | {'Cond':5} | {'Review':6} | {'DoNotUse':8}"
print(header)
print("-" * len(header))

for i in range(1, 13):
    cid = f"C{i:02d}"
    c_list = [r for r in records if r["target_class_id"] == cid]
    cname = c_list[0]["target_class_name"] if c_list else "Unknown"
    
    tot = len(c_list)
    prim = sum(1 for r in c_list if r["eligibility_state"] == "PROPOSED_PRIMARY")
    sec = sum(1 for r in c_list if r["eligibility_state"] == "PROPOSED_SECONDARY")
    cond = sum(1 for r in c_list if r["eligibility_state"] == "CONDITIONAL")
    rev = sum(1 for r in c_list if r["eligibility_state"] == "REVIEW_REQUIRED")
    dnu = sum(1 for r in c_list if r["eligibility_state"] == "DO_NOT_USE")
    
    print(f"{cid:5} | {cname:32} | {tot:5} | {prim:7} | {sec:9} | {cond:5} | {rev:6} | {dnu:8}")

print("\n=== PROPOSED PRIMARY (BIOLOGICAL ONLY, C01-C11) ===")
bio_prim = [r for r in records if r["eligibility_state"] == "PROPOSED_PRIMARY" and r["target_class_id"] != "C12"]
print(f"Total Biological Primary Candidates: {len(bio_prim)}")
bio_sec = [r for r in records if r["eligibility_state"] == "PROPOSED_SECONDARY" and r["target_class_id"] != "C12"]
print(f"Total Biological Secondary Candidates: {len(bio_sec)}")
robust_prim = [r for r in records if r["target_class_id"] == "C12"]
print(f"Total Robustness Controls (Experiment D): {len(robust_prim)}")
