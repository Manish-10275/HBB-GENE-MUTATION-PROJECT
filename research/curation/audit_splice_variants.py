import json
import re

with open("research/curation/candidate_pool.json", "r", encoding="utf-8") as f:
    pool = json.load(f)["candidates"]

splice_vars = [c for c in pool if c["target_class_id"] in ("C08", "C09")]
print(f"Total C08/C09 candidates: {len(splice_vars)}\n")

canonical_donor = []
canonical_acceptor = []
deep_intronic = []
complex_intronic = []

for c in splice_vars:
    cdna = c["HGVS_input"]
    cid = c["target_class_id"]
    status = c["exclusion_status"]
    prov = c["provenance_notes"]
    uid = c["external_database_identifier"]
    
    # Check if complex indel
    if "dup" in cdna.lower() or "ins" in cdna.lower() or "del" in cdna.lower():
        complex_intronic.append(c)
        continue
    
    # Parse offset
    m = re.search(r"c\.\d+([+-]\d+)[A-Za-z]>[A-Za-z]", cdna)
    if m:
        offset = m.group(1)
        offset_val = int(offset)
        if offset in ("+1", "+2", "+5"):
            canonical_donor.append((c, offset))
        elif offset in ("-1", "-2"):
            canonical_acceptor.append((c, offset))
        elif offset in ("-3", "+3", "+4", "+6"):
            # Splice consensus flanking
            deep_intronic.append((c, offset, "flanking_consensus"))
        else:
            # Deep intronic
            deep_intronic.append((c, offset, "deep_intronic"))
    else:
        complex_intronic.append(c)

print(f"=== CANONICAL DONORS (+1, +2, +5) (n={len(canonical_donor)}) ===")
for c, off in canonical_donor:
    print(f"  {c['candidate_id']:12} | {c['HGVS_input']:18} | {off:4} | {c['exclusion_status']:15} | {c['provenance_notes']}")

print(f"\n=== CANONICAL ACCEPTORS (-1, -2) (n={len(canonical_acceptor)}) ===")
for c, off in canonical_acceptor:
    print(f"  {c['candidate_id']:12} | {c['HGVS_input']:18} | {off:4} | {c['exclusion_status']:15} | {c['provenance_notes']}")

print(f"\n=== DEEP INTRONIC / NON-CANONICAL (n={len(deep_intronic)}) ===")
for c, off, kind in deep_intronic:
    print(f"  {c['candidate_id']:12} | {c['HGVS_input']:18} | {off:6} ({kind:18}) | {c['exclusion_status']:15} | {c['provenance_notes']}")

print(f"\n=== COMPLEX INTRONIC INDELS (n={len(complex_intronic)}) ===")
for c in complex_intronic:
    print(f"  {c['candidate_id']:12} | {c['HGVS_input']:30} | {c['exclusion_status']:15} | {c['provenance_notes']}")
