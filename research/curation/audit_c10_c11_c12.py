import json

with open("research/curation/cp2_2_verification_records.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print("=== C10 AUDIT ===")
c10 = [r for r in records if r["target_class_id"] == "C10"]
for r in c10:
    print(f"{r['candidate_id']:12} | {r['HGVS_input']:25} | {r['comparison_status']:25} | {r['eligibility_state']:18} | {r['verification_notes']}")

print("\n=== C11 AUDIT ===")
c11 = [r for r in records if r["target_class_id"] == "C11"]
for r in c11:
    print(f"{r['candidate_id']:12} | {r['HGVS_input']:25} | {r['comparison_status']:25} | {r['eligibility_state']:18} | {r['verification_notes']}")

print("\n=== C12 AUDIT ===")
c12 = [r for r in records if r["target_class_id"] == "C12"]
for r in c12:
    print(f"{r['candidate_id']:12} | {r['HGVS_input']:25} | {r['comparison_status']:25} | {r['eligibility_state']:18} | {r['verification_notes']}")
