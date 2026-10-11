import json
from collections import Counter

with open("research/curation/exclusion_registry.json", "r", encoding="utf-8") as f:
    ex_reg = json.load(f)

print("=== EXCLUSION REGISTRY AUDIT ===")
print("Total excluded patterns:", len(ex_reg["excluded_variant_patterns"]))
print("Total excluded ClinVar IDs:", len(ex_reg["excluded_clinvar_variation_ids"]))
print("Total historical aliases:", len(ex_reg["known_historical_aliases"]))
print("Manifest records loaded:", ex_reg.get("total_manifest_records"))
print("Code tokens harvested:", ex_reg.get("total_code_tokens_harvested"))

with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
    pool_data = json.load(f)

candidates = pool_data["candidates"]

# Annotation quality stats for Class B
class_b = [c for c in candidates if c["source_class"] == "Class B"]
print(f"\n=== CLASS B ANNOTATION QUALITY (n={len(class_b)}) ===")
has_pmid = sum(1 for c in class_b if len(c.get("publication_identifier", [])) > 0)
no_pmid = sum(1 for c in class_b if len(c.get("publication_identifier", [])) == 0)
print(f"Variants with >= 1 PMID: {has_pmid} ({has_pmid/len(class_b)*100:.1f}%)")
print(f"Variants with 0 PMIDs: {no_pmid} ({no_pmid/len(class_b)*100:.1f}%)")

clinsig_counts = Counter(c.get("clinical_significance_if_available") for c in class_b)
print("\nClinical Significance breakdown:")
for cs, cnt in clinsig_counts.most_common():
    print(f"  {cs}: {cnt}")

review_status_counts = Counter()
for c in class_b:
    prov = c.get("provenance_notes", "")
    if "criteria provided, single submitter" in prov:
        review_status_counts["1 star (single submitter)"] += 1
    elif "criteria provided, multiple submitters, no conflicts" in prov:
        review_status_counts["2 stars (multiple submitters, no conflict)"] += 1
    elif "reviewed by expert panel" in prov:
        review_status_counts["3 stars (expert panel)"] += 1
    elif "practice guideline" in prov:
        review_status_counts["4 stars (practice guideline)"] += 1
    elif "conflicting" in prov.lower():
        review_status_counts["1 star (conflicting interpretations)"] += 1
    else:
        review_status_counts["Other / no assertion criteria"] += 1

print("\nReview Status Breakdown:")
for rs, cnt in review_status_counts.most_common():
    print(f"  {rs}: {cnt}")
