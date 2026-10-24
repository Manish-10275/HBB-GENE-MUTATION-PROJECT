"""
Automated regression tests for evaluation pipeline defect fixes (Phase 2).
Covers:
- Defect 1: Typing import in consequence_agreement.py (Any).
- Defect 2: Truthful mode handling (offline mode prevents network calls).
- Defect 3: Explicit provenance tracking (LIVE vs FIXTURE vs CACHED vs FAILED).
- Defect 4: Metric calculations returning None on empty/zero denominators rather than 1.0.
- Defect 5: Multi-class metric length mismatch assertion (prohibits silent zip truncation).
- Defect 6: Report generation resilience to None metrics and empty datasets.
"""

import inspect
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from research.evaluation.consequence_agreement import (
    evaluate_consequence_agreement,
    normalize_protein_change,
)
from research.evaluation.metrics import (
    calculate_binary_confusion_metrics,
    calculate_multiclass_metrics,
    calculate_retrieval_metrics,
    calculate_latency_metrics,
)
from research.evaluation.report import generate_benchmark_markdown_report
from app.clinvar import fetch_clinvar_records


def test_consequence_agreement_typing_and_signature():
    """Defect #1 Regression: Verifies typing annotations evaluate cleanly without NameError."""
    sig = inspect.signature(evaluate_consequence_agreement)
    ret = sig.return_annotation
    assert "Any" in str(ret) or "dict" in str(ret).lower()

    # Functional evaluation
    is_exact, is_concordant, details = evaluate_consequence_agreement(
        expected_p="p.Gln40Ter",
        predicted_p="p.Gln40Ter",
        expected_impact="Nonsense",
        predicted_impact="Nonsense",
        is_rejected=False,
    )
    assert is_exact is True
    assert is_concordant is True
    assert isinstance(details, dict)


def test_metrics_length_mismatch_raises_value_error():
    """Defect #5 Regression: Verifies length mismatch raises ValueError instead of silent zip truncation."""
    y_true = ["Missense", "Synonymous"]
    y_pred = ["Missense"]

    with pytest.raises(ValueError, match="Mismatched array lengths"):
        calculate_multiclass_metrics(y_true, y_pred)


def test_metrics_empty_datasets_return_none_not_one():
    """Defect #4 Regression: Verifies empty datasets return None (null), never false perfect 1.0 scores."""
    # 1. Binary confusion metrics on empty dataset
    bin_empty = calculate_binary_confusion_metrics(tp=0, fp=0, fn=0, tn=0)
    assert bin_empty["accuracy"] is None
    assert bin_empty["sensitivity"] is None
    assert bin_empty["specificity"] is None
    assert bin_empty["precision"] is None
    assert bin_empty["f1_score"] is None
    assert "accuracy" in bin_empty["undefined_reasons"]

    # 2. Multiclass metrics on empty arrays
    mc_empty = calculate_multiclass_metrics([], [])
    assert mc_empty["overall_accuracy"] is None
    assert mc_empty["macro_f1"] is None
    assert mc_empty["evaluated_samples"] == 0

    # 3. Retrieval metrics on empty evaluation set
    ret_empty = calculate_retrieval_metrics([])
    assert ret_empty["evaluated_clinvar_records"] == 0
    assert ret_empty["hit_at_1"] is None
    assert ret_empty["recall_at_5"] is None
    assert ret_empty["false_match_rate"] is None
    assert ret_empty["mean_retrieved_records"] is None

    # 4. Latency metrics on empty measurements
    lat_empty = calculate_latency_metrics([])
    assert lat_empty["mean_ms"] is None
    assert lat_empty["median_ms"] is None
    assert lat_empty["sample_count"] == 0


def test_metrics_zero_denominators_return_none_with_reasons():
    """Defect #4 Regression: Verifies specific zero denominators are reported as None with explicit reason."""
    # Only negative controls evaluated (tp = 0, fn = 0, tn = 10, fp = 0)
    bin_negs = calculate_binary_confusion_metrics(tp=0, fp=0, fn=0, tn=10)
    assert bin_negs["specificity"] == 1.0
    assert bin_negs["sensitivity"] is None
    assert "zero positive cases" in bin_negs["undefined_reasons"]["sensitivity"]
    assert bin_negs["precision"] is None
    assert "zero positive predictions" in bin_negs["undefined_reasons"]["precision"]

    # Only positive cases evaluated (tp = 10, fn = 0, tn = 0, fp = 0)
    bin_pos = calculate_binary_confusion_metrics(tp=10, fp=0, fn=0, tn=0)
    assert bin_pos["sensitivity"] == 1.0
    assert bin_pos["specificity"] is None
    assert "zero negative cases" in bin_pos["undefined_reasons"]["specificity"]


@pytest.mark.asyncio
async def test_clinvar_mode_offline_strictly_prevents_network():
    """Defect #2 Regression: Verifies mode='offline' executes without initiating any HTTP connections."""
    with patch("httpx.AsyncClient") as mock_client:
        records = await fetch_clinvar_records("c.118C>T", mode="offline")
        # Assert httpx.AsyncClient was never called
        mock_client.assert_not_called()

        assert len(records) > 0
        assert "Fixture" in records[0].source
        assert records[0].is_exact_match is True


def test_retrieval_provenance_breakdown_tracking():
    """Defect #3 Regression: Verifies retrieval provenance is tracked into distinct categories."""
    mock_records = [
        {"expected_clinvar_id": "15406", "retrieved_clinvar_ids": ["15406"], "exact_match_clinvar_ids": ["15406"], "rank_0_is_exact": True, "retrieval_source": "LIVE"},
        {"expected_clinvar_id": "15407", "retrieved_clinvar_ids": ["15407"], "exact_match_clinvar_ids": ["15407"], "rank_0_is_exact": True, "retrieval_source": "FIXTURE"},
        {"expected_clinvar_id": "15408", "retrieved_clinvar_ids": ["15408"], "exact_match_clinvar_ids": ["15408"], "rank_0_is_exact": True, "retrieval_source": "CACHED"},
        {"expected_clinvar_id": "15409", "retrieved_clinvar_ids": [], "exact_match_clinvar_ids": [], "rank_0_is_exact": False, "retrieval_source": "FAILED"},
    ]

    ret_metrics = calculate_retrieval_metrics(mock_records)
    prov = ret_metrics["provenance_breakdown"]
    assert prov["live"] == 1
    assert prov["fixture"] == 1
    assert prov["cached"] == 1
    assert prov["failed"] == 1
    assert ret_metrics["hit_at_1"] == 0.75


def test_report_generation_with_none_metrics(tmp_path: Path):
    """Defect #6 Regression: Verifies report generator handles None metrics without raising exceptions."""
    eval_summary = {
        "split": "test",
        "mode": "offline",
        "total_variants": 0,
        "concordant_variants": 0,
        "exact_matches": 0,
        "concordance_rate": None,
        "exact_match_rate": None,
        "sensitivity": None,
        "specificity": None,
        "precision": None,
        "f1_score": None,
        "discrepancy_count": 0,
        "discrepancies_formatted": "None",
    }
    class_metrics = calculate_multiclass_metrics([], [])
    retrieval_metrics = calculate_retrieval_metrics([])
    latency_metrics = calculate_latency_metrics([])

    report_md = generate_benchmark_markdown_report(
        eval_summary=eval_summary,
        class_metrics=class_metrics,
        retrieval_metrics=retrieval_metrics,
        latency_metrics=latency_metrics,
        split_name="test",
        output_dir=tmp_path
    )

    assert "N/A" in report_md
    assert (tmp_path / "BENCHMARK_REPORT.md").exists()
    assert (tmp_path / "tables" / "table1_variant_class_accuracy.md").exists()


def test_delins_parsing_and_consequences():
    """Defect #7 Regression: Verifies HGVS delins variants are parsed with correct codon consequences."""
    from app.reference import reference_manager
    from app.variants import parse_hgvs_input

    ref = reference_manager.get_reference("NM_000518.5")

    # In-frame single amino acid substitution
    var1, err1 = parse_hgvs_input("c.19_20delinsAT", ref)
    assert err1 is None
    assert var1 is not None
    assert var1.functional_impact == "In-frame Indel"
    assert var1.hgvs_p == "p.Glu7Met"

    # In-frame multi-amino acid substitution
    var2, err2 = parse_hgvs_input("c.10_16delinsTCTGACT", ref)
    assert err2 is None
    assert var2 is not None
    assert var2.functional_impact == "In-frame Indel"
    assert var2.hgvs_p == "p.Leu4_Pro6delinsSerAspSer"

    # In-frame insertion with net gain
    var3, err3 = parse_hgvs_input("c.301_302delinsTCTGAGAACTT", ref)
    assert err3 is None
    assert var3 is not None
    assert var3.functional_impact == "In-frame Indel"
    assert var3.hgvs_p == "p.Pro101delinsSerGluAsnPhe"

    # Frameshift delins
    var4, err4 = parse_hgvs_input("c.385_388delinsCCACA", ref)
    assert err4 is None
    assert var4 is not None
    assert "Frameshift" in var4.functional_impact
    assert "fs" in var4.hgvs_p


def test_coordinate_star_zero_rejection():
    """Defect #8 Regression: Verifies invalid coordinate c.*0 is rejected as out-of-bounds."""
    from app.reference import reference_manager
    from app.variants import parse_hgvs_input

    ref = reference_manager.get_reference("NM_000518.5")

    var, err = parse_hgvs_input("c.*0A>G", ref)
    assert var is None
    assert err is not None
    assert "out of bounds" in err.lower() or "invalid" in err.lower()


def test_delins_invalid_base_rejection():
    """Defect #9 Regression: Verifies non-standard IUPAC base in delins is rejected."""
    from app.reference import reference_manager
    from app.variants import parse_hgvs_input

    ref = reference_manager.get_reference("NM_000518.5")

    var, err = parse_hgvs_input("c.152_153delinsAR", ref)
    assert var is None
    assert err is not None
    assert "Invalid nucleotide sequence" in err
