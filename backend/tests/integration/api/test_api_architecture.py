"""Architectural boundary and dependency direction enforcement tests."""

import re
from pathlib import Path


def test_core_does_not_import_evidence_or_api():
    core_dir = Path(__file__).resolve().parent.parent.parent.parent / "app" / "core"
    assert core_dir.exists()

    forbidden_patterns = [
        r"from\s+app\.evidence",
        r"import\s+app\.evidence",
        r"from\s+app\.services",
        r"import\s+app\.services",
        r"from\s+app\.api",
        r"import\s+app\.api",
        r"from\s+app\.clinvar",
        r"from\s+app\.pubmed",
    ]

    for py_file in core_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for pat in forbidden_patterns:
            matches = re.findall(pat, content)
            assert not matches, f"Core file {py_file.name} violates dependency boundary by importing: {matches}"


def test_new_api_routes_do_not_import_legacy_biology_files():
    api_routes = Path(__file__).resolve().parent.parent.parent.parent / "app" / "api" / "routes.py"
    assert api_routes.exists()

    content = api_routes.read_text(encoding="utf-8")
    forbidden = [
        r"from\s+app\.variants",
        r"import\s+app\.variants",
        r"from\s+app\.consequences",
        r"import\s+app\.consequences",
        r"from\s+app\.reference\s+import",
    ]

    for pat in forbidden:
        matches = re.findall(pat, content)
        assert not matches, f"api/routes.py illegally imports legacy module: {matches}"


def test_no_hardcoded_benchmark_variation_ids_in_api_or_services():
    services_dir = Path(__file__).resolve().parent.parent.parent.parent / "app" / "services"
    api_dir = Path(__file__).resolve().parent.parent.parent.parent / "app" / "api"

    benchmark_vids = ["15402", "15333", "15447", "15417", "36308", "869321", "15126"]

    for folder in [services_dir, api_dir]:
        for py_file in folder.glob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            for vid in benchmark_vids:
                # Disallow hardcoded string literals matching specific ClinVar IDs
                assert f'"{vid}"' not in content, f"Hardcoded benchmark ClinVar ID {vid} found in {py_file.name}"
                assert f"'{vid}'" not in content, f"Hardcoded benchmark ClinVar ID {vid} found in {py_file.name}"
