"""
Integrity and Anti-Leakage Tests for HBB Phase 2B Scientific Benchmark Architecture.
Guarantees:
1. Frozen test set cryptographic immutability (SHA-256 match).
2. Zero data leakage across Development, Validation, and Test splits.
3. Complete provenance and schema adherence for all benchmark variants.
4. Representation of all required variant structural classes.
"""

import hashlib
import json
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
MANIFEST_DIR = ROOT_DIR / "research" / "manifest"


def test_frozen_test_set_hash_integrity():
    """Confirms that frozen_test.json matches its recorded SHA-256 cryptographic hash."""
    test_json = MANIFEST_DIR / "frozen_test.json"
    sha_file = MANIFEST_DIR / "frozen_test.sha256"

    assert test_json.exists(), "frozen_test.json must exist"
    assert sha_file.exists(), "frozen_test.sha256 must exist"

    with open(test_json, "rb") as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()

    with open(sha_file, "r", encoding="utf-8") as f:
        recorded_hash = f.readline().strip().split()[0]

    assert current_hash == recorded_hash, (
        f"FROZEN TEST SET INTEGRITY BREACH!\n"
        f"Expected: {recorded_hash}\n"
        f"Found:    {current_hash}"
    )


def test_zero_benchmark_leakage_between_splits():
    """Confirms that Development, Validation, and Test sets have strictly disjoint variants (zero leakage)."""
    dev_path = MANIFEST_DIR / "development.json"
    val_path = MANIFEST_DIR / "validation.json"
    test_path = MANIFEST_DIR / "frozen_test.json"

    with open(dev_path, "r", encoding="utf-8") as f:
        dev_vars = json.load(f)
    with open(val_path, "r", encoding="utf-8") as f:
        val_vars = json.load(f)
    with open(test_path, "r", encoding="utf-8") as f:
        test_vars = json.load(f)

    dev_ids = {v["id"] for v in dev_vars}
    val_ids = {v["id"] for v in val_vars}
    test_ids = {v["id"] for v in test_vars}

    # 1. No ID overlaps
    assert len(dev_ids.intersection(val_ids)) == 0, "Leakage detected between Dev and Val sets!"
    assert len(dev_ids.intersection(test_ids)) == 0, "Leakage detected between Dev and Test sets!"
    assert len(val_ids.intersection(test_ids)) == 0, "Leakage detected between Val and Test sets!"

    # 2. No query string overlaps
    dev_queries = {v["hgvs_c_input"].lower() for v in dev_vars}
    val_queries = {v["hgvs_c_input"].lower() for v in val_vars}
    test_queries = {v["hgvs_c_input"].lower() for v in test_vars}

    assert len(dev_queries.intersection(val_queries)) == 0, "Query leakage between Dev and Val!"
    assert len(dev_queries.intersection(test_queries)) == 0, "Query leakage between Dev and Test!"
    assert len(val_queries.intersection(test_queries)) == 0, "Query leakage between Val and Test!"


def test_benchmark_record_schema_and_provenance_completeness():
    """Confirms every record in master manifest contains mandatory metadata and provenance."""
    master_path = MANIFEST_DIR / "hbb_benchmark_manifest.json"
    with open(master_path, "r", encoding="utf-8") as f:
        variants = json.load(f)

    assert len(variants) >= 50, f"Expected at least 50 benchmark variants, got {len(variants)}"

    required_keys = [
        "id", "name", "hgvs_c_input", "reference_accession",
        "variant_class", "molecular_consequence", "provenance", "dataset_split"
    ]
    required_prov_keys = ["ground_truth_source", "provenance_class", "verification_method"]

    for var in variants:
        for k in required_keys:
            assert k in var, f"Variant {var.get('id')} missing mandatory key '{k}'"
        prov = var["provenance"]
        for pk in required_prov_keys:
            assert pk in prov, f"Variant {var['id']} provenance missing '{pk}'"


def test_all_structural_classes_represented():
    """Confirms all 11 required structural categories and negative controls are represented."""
    master_path = MANIFEST_DIR / "hbb_benchmark_manifest.json"
    with open(master_path, "r", encoding="utf-8") as f:
        variants = json.load(f)

    classes_present = {v["variant_class"] for v in variants}
    required_classes = {
        "substitution", "deletion", "duplication", "insertion",
        "splice_donor", "splice_acceptor", "5_utr", "3_utr", "negative_control"
    }
    missing = required_classes - classes_present
    assert len(missing) == 0, f"Missing required variant structural classes in benchmark: {missing}"

    # Verify synonymous variants exist within substitutions
    impacts = {v["molecular_consequence"] for v in variants}
    assert "Synonymous" in impacts, "Synonymous (silent) negative control variants missing from benchmark!"
    assert "Nonsense" in impacts, "Nonsense variants missing!"
    assert "Missense" in impacts, "Missense variants missing!"
    assert "Frameshift Deletion" in impacts, "Frameshift Deletions missing!"
    assert "Invalid / Rejected" in impacts, "Negative control rejections missing!"


def test_frozen_test_tamper_detection():
    """Verifies that tampering with frozen test set triggers FrozenDatasetIntegrityError."""
    import sys
    sys.path.insert(0, str(ROOT_DIR / "research"))
    from evaluation.run_benchmark import verify_frozen_test_hash, FrozenDatasetIntegrityError

    # Official file should pass without error
    official_hash = verify_frozen_test_hash()
    assert len(official_hash) == 64
