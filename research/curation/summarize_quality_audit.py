import json
from collections import Counter

with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
    data = json.load(f)

candidates = data["candidates"]

print(f"TOTAL CANDIDATES: {len(candidates)}")

# Quality distribution
q_counts = Counter(c.get("ground_truth_quality") for c in candidates)
print("\n=== GROUND TRUTH QUALITY DISTRIBUTION ===")
for q, cnt in q_counts.most_common():
    print(f"  {q:18}: {cnt:3} ({cnt/len(candidates)*100:.1f}%)")

# Recommendation distribution
rec_counts = Counter(c.get("recommendation") for c in candidates)
print("\n=== RECOMMENDATION DISTRIBUTION ===")
for r, cnt in rec_counts.most_common():
    print(f"  {r:18}: {cnt:3} ({cnt/len(candidates)*100:.1f}%)")

# Scope distribution
scope_counts = Counter(c.get("scope_status") for c in candidates)
print("\n=== SCOPE STATUS DISTRIBUTION ===")
for s, cnt in scope_counts.most_common():
    print(f"  {s:30}: {cnt:3} ({cnt/len(candidates)*100:.1f}%)")

# ClinVar-only vs Multi-source / Synthetic
clinvar_only_cnt = sum(1 for c in candidates if c.get("clinvar_only") is True)
synthetic_cnt = sum(1 for c in candidates if c.get("research_category") == "ROBUSTNESS_NEGATIVE_CONTROL")
print(f"\nClinVar-only candidates: {clinvar_only_cnt}")
print(f"Synthetic Robustness Controls: {synthetic_cnt}")

# Conflict count
conflict_cnt = sum(1 for c in candidates if c.get("conflict_status") == "CONFLICT_DETECTED")
print(f"Conflict count: {conflict_cnt}")

# Deep-intronic & complex indels count
deep_intronic_cnt = sum(1 for c in candidates if "Deep intronic" in c.get("recommendation_reason", ""))
complex_indel_cnt = sum(1 for c in candidates if "Complex indel" in c.get("recommendation_reason", ""))
print(f"Deep intronic count: {deep_intronic_cnt}")
print(f"Complex / unsupported indel count: {complex_indel_cnt}")

# Class-by-class table
print("\n=== CLASS-BY-CLASS QUALITY TABLE ===")
header = f"{'Class':5} | {'Name':32} | {'Total':5} | {'Strong':6} | {'Mod':5} | {'Weak':5} | {'Review':6} | {'OutScope':8} | {'Rec':5} | {'Cond':5} | {'DoNotUse':8}"
print(header)
print("-" * len(header))

for i in range(1, 13):
    cid = f"C{i:02d}"
    c_list = [c for c in candidates if c["target_class_id"] == cid]
    cname = c_list[0]["target_class_name"] if c_list else "Unknown"
    
    tot = len(c_list)
    strong = sum(1 for c in c_list if c.get("ground_truth_quality") == "A_STRONG")
    mod = sum(1 for c in c_list if c.get("ground_truth_quality") == "B_MODERATE")
    weak = sum(1 for c in c_list if c.get("ground_truth_quality") == "C_WEAK")
    rev = sum(1 for c in c_list if c.get("ground_truth_quality") == "D_REVIEW_REQUIRED")
    outscope = sum(1 for c in c_list if c.get("scope_status") in ("OUT_OF_SCOPE", "EXCLUDED_HISTORICAL_OVERLAP"))
    
    rec = sum(1 for c in c_list if c.get("recommendation") == "RECOMMENDED")
    cond = sum(1 for c in c_list if c.get("recommendation") == "CONDITIONAL")
    dnu = sum(1 for c in c_list if c.get("recommendation") == "DO_NOT_USE")
    
    print(f"{cid:5} | {cname:32} | {tot:5} | {strong:6} | {mod:5} | {weak:5} | {rev:6} | {outscope:8} | {rec:5} | {cond:5} | {dnu:8}")

