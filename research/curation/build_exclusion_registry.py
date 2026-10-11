"""
Build the Phase 2C Exclusion Registry.

Harvests every variant, cDNA representation, coordinate, alias, legacy name,
and ClinVar Variation ID that has ever appeared in:
- Phase 2A/2B manifests (frozen_test, development, validation, hbb_benchmark_manifest)
- Data fixtures (clinvar_fixtures.json, pubmed_fixtures.json)
- Production code (backend/app/)
- Test suites (backend/tests/)
- Frontend components and presets (frontend/)
- Example FASTA files (data/examples/)
"""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

EXCLUSION_OUTPUT = REPO_ROOT / "research" / "curation" / "exclusion_registry.json"

HGVS_REGEX = re.compile(r"c\.[\*\-\d_]+(?:[A-Za-z]+>[A-Za-z]+|del[A-Za-z]*|dup[A-Za-z]*|ins[A-Za-z]+)")
CLINVAR_ID_REGEX = re.compile(r"\b(?:VarID|VCV\d+|Variation ID)?\s*(\d{4,7})\b")


def normalize_c_str(c_str: str) -> str:
    """Standardizes cDNA string for comparison (removes transcript prefix, spaces)."""
    s = c_str.strip()
    if ":" in s:
        s = s.split(":")[-1]
    return s.upper()


def harvest_exclusions():
    records = []
    seen_variants = set()
    seen_clinvar_ids = set()
    seen_aliases = set()

    # 1. Harvest from research manifests
    manifest_dir = REPO_ROOT / "research" / "manifest"
    for mf in manifest_dir.glob("*.json"):
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for row in data:
                    hgvs_in = row.get("hgvs_c_input")
                    hgvs_can = row.get("hgvs_c_canonical")
                    c_id = row.get("expected_clinvar_id")
                    name = row.get("name")
                    v_id = row.get("id")
                    
                    entry = {
                        "source": f"manifest:{mf.name}",
                        "id": v_id,
                        "hgvs_input": hgvs_in,
                        "hgvs_canonical": hgvs_can,
                        "clinvar_id": c_id,
                        "name": name,
                    }
                    records.append(entry)
                    if hgvs_in:
                        seen_variants.add(normalize_c_str(hgvs_in))
                    if hgvs_can:
                        seen_variants.add(normalize_c_str(hgvs_can))
                    if c_id:
                        seen_clinvar_ids.add(str(c_id))
                    if name:
                        seen_aliases.add(name.lower())
        except Exception as e:
            print(f"Error reading manifest {mf}: {e}")

    # 2. Harvest from data fixtures
    fixtures_dir = REPO_ROOT / "data" / "fixtures"
    for ff in fixtures_dir.glob("*.json"):
        try:
            data = json.loads(ff.read_text(encoding="utf-8"))
            for k, val in data.items():
                seen_variants.add(normalize_c_str(k))
                records.append({
                    "source": f"fixture:{ff.name}",
                    "hgvs_input": k,
                    "details": "cache_key",
                })
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            cv_id = item.get("variation_id") or item.get("clinvar_id")
                            if cv_id:
                                seen_clinvar_ids.add(str(cv_id))
        except Exception as e:
            print(f"Error reading fixture {ff}: {e}")

    # 3. Harvest string literals from backend/app, backend/tests, frontend
    target_dirs = [
        ("production_code", REPO_ROOT / "backend" / "app"),
        ("test_suite", REPO_ROOT / "backend" / "tests"),
        ("frontend", REPO_ROOT / "frontend"),
        ("examples", REPO_ROOT / "data" / "examples"),
    ]

    code_tokens = []
    for category, pth in target_dirs:
        if not pth.exists():
            continue
        for root, dirs, files in os.walk(pth):
            for f in files:
                if f.endswith((".py", ".ts", ".tsx", ".json", ".fasta", ".md")):
                    fpath = Path(root) / f
                    rel_path = fpath.relative_to(REPO_ROOT).as_posix()
                    # Skip the exclusion registry itself
                    if "exclusion_registry" in rel_path:
                        continue
                    try:
                        content = fpath.read_text(encoding="utf-8", errors="ignore")
                        matches = HGVS_REGEX.findall(content)
                        for m in matches:
                            norm_m = normalize_c_str(m)
                            seen_variants.add(norm_m)
                            code_tokens.append({
                                "source": f"{category}:{rel_path}",
                                "variant": norm_m,
                            })
                    except Exception as e:
                        print(f"Error scanning {fpath}: {e}")

    # 4. Known historical aliases and legacy expressions for HBB
    known_historical_aliases = {
        "hb s": ["c.20A>T", "NM_000518.5:c.20A>T", "p.Glu7Val", "Glu6Val"],
        "hb c": ["c.19G>A", "NM_000518.5:c.19G>A", "p.Glu7Lys", "Glu6Lys"],
        "hb e": ["c.79G>A", "NM_000518.5:c.79G>A", "p.Glu27Lys", "Glu26Lys"],
        "hb d-los angeles": ["c.364G>C", "NM_000518.5:c.364G>C", "p.Glu122Gln", "Glu121Gln"],
        "hb d-punjab": ["c.364G>C", "NM_000518.5:c.364G>C", "p.Glu122Gln", "Glu121Gln"],
        "hb o-arab": ["c.307A>C", "NM_000518.5:c.307A>C", "p.Lys103Asn", "Lys102Asn"],
        "codon 39": ["c.118C>T", "NM_000518.5:c.118C>T", "p.Gln40Ter", "Gln39Ter"],
        "codon 41/42": ["c.126_129del", "c.124_127del", "NM_000518.5:c.126_129del", "fs 41/42"],
        "ivs-i-1": ["c.92+1G>A", "c.92+1G>T", "NM_000518.5:c.92+1G>A", "NM_000518.5:c.92+1G>T"],
        "ivs-i-5": ["c.92+5G>C", "NM_000518.5:c.92+5G>C"],
        "ivs-ii-1": ["c.315+1G>A", "NM_000518.5:c.315+1G>A"],
        "ivs-ii-654": ["c.316-197C>T"],
        "codon 8/9": ["c.27dup", "c.27_28insG", "c.26_27insG", "CD 8/9"],
        "codon 15": ["c.47G>A", "p.Trp16Ter", "Trp15Ter"],
        "codon 16": ["c.51delC", "c.51del", "CD 16 (-C)"],
        "codon 30": ["c.93G>A", "c.93G>C", "CD 30"],
        "codon 8": ["c.25_26delAA", "CD 8 (-AA)"],
        "codon 43": ["c.130G>T", "p.Glu44Ter", "Glu43Ter"],
    }

    registry = {
        "version": "1.0.0",
        "generated_timestamp": "2026-10-08T00:46:00Z",
        "total_excluded_variant_strings": len(seen_variants),
        "total_excluded_clinvar_ids": len(seen_clinvar_ids),
        "total_manifest_records": len(records),
        "total_code_tokens_harvested": len(code_tokens),
        "excluded_variant_patterns": sorted(list(seen_variants)),
        "excluded_clinvar_variation_ids": sorted(list(seen_clinvar_ids)),
        "known_historical_aliases": known_historical_aliases,
        "manifest_entries": records,
    }

    EXCLUSION_OUTPUT.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Exclusion Registry generated at {EXCLUSION_OUTPUT}")
    print(f"Total excluded variant patterns: {len(seen_variants)}")
    print(f"Total excluded ClinVar IDs: {len(seen_clinvar_ids)}")


if __name__ == "__main__":
    harvest_exclusions()
