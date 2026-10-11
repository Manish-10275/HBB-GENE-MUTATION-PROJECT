"""
Main execution harness for HBB Phase 2B Scientific Benchmark.
Evaluates the HBB Mutation Analyzer against independent ground truth manifests.
Enforces cryptographic integrity on the frozen test set to prevent silent tampering or data leakage.
"""

import argparse
import asyncio
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.reference import reference_manager
from app.variants import parse_hgvs_input
from app.clinvar import fetch_clinvar_records

# Research modules
RESEARCH_DIR = ROOT_DIR / "research"
sys.path.insert(0, str(RESEARCH_DIR))

from evaluation.consequence_agreement import evaluate_consequence_agreement
from evaluation.metrics import (
    calculate_binary_confusion_metrics,
    calculate_multiclass_metrics,
    calculate_retrieval_metrics,
    calculate_latency_metrics,
)
from evaluation.report import generate_benchmark_markdown_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("hbb_benchmark")


class FrozenDatasetIntegrityError(Exception):
    """Raised when the frozen test set SHA-256 hash does not match the official recorded signature."""
    pass


def verify_frozen_test_hash() -> str:
    """Verifies that research/manifest/frozen_test.json has not been modified."""
    manifest_dir = RESEARCH_DIR / "manifest"
    test_file = manifest_dir / "frozen_test.json"
    hash_file = manifest_dir / "frozen_test.sha256"

    if not test_file.exists():
        raise FileNotFoundError(f"Frozen test set not found at {test_file}")
    if not hash_file.exists():
        raise FileNotFoundError(f"Frozen test SHA-256 reference file not found at {hash_file}")

    with open(test_file, "rb") as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        expected_hash = first_line.split()[0]

    if current_hash != expected_hash:
        raise FrozenDatasetIntegrityError(
            f"FROZEN TEST SET TAMPERED OR CORRUPTED!\n"
            f"Expected SHA-256: {expected_hash}\n"
            f"Actual SHA-256:   {current_hash}\n"
            f"The frozen test set must remain immutable during evaluation."
        )

    return current_hash


async def evaluate_variant(
    variant_spec: Dict[str, Any],
    mode: str = "offline"
) -> Dict[str, Any]:
    """Runs a single variant through the pipeline and records all predictions and metrics."""
    query = variant_spec["hgvs_c_input"]
    expected_p = variant_spec.get("expected_hgvs_p")
    expected_impact = variant_spec.get("molecular_consequence")
    expected_vid = variant_spec.get("expected_clinvar_id")
    ref_acc = variant_spec.get("reference_accession", "NM_000518.5")

    ref_data = reference_manager.get_reference(ref_acc)

    t0 = time.perf_counter()
    var_model, parse_err = parse_hgvs_input(query, ref_data)
    t_parse_ms = (time.perf_counter() - t0) * 1000.0

    is_rejected = (var_model is None) or (parse_err is not None)
    predicted_p = var_model.hgvs_p if var_model else None
    predicted_impact = var_model.functional_impact if var_model else None

    # Consequence evaluation
    is_exact, is_concordant, comp_details = evaluate_consequence_agreement(
        expected_p=expected_p,
        predicted_p=predicted_p,
        expected_impact=expected_impact,
        predicted_impact=predicted_impact,
        is_rejected=is_rejected,
        expected_rejection_reason=variant_spec.get("expected_rejection_reason"),
    )

    # ClinVar retrieval evaluation (only if not a rejected negative control)
    retrieved_vids = []
    exact_match_vids = []
    rank_0_exact = False

    if not is_rejected and expected_vid:
        try:
            # Query ClinVar client
            clean_term = query.split(":")[-1] if ":" in query else query
            aliases = var_model.equivalent_nomenclature if var_model else None
            p_change = var_model.hgvs_p if var_model else None

            cv_records = await fetch_clinvar_records(
                query_term=clean_term,
                transcript_accession=ref_data.accession,
                variant_aliases=aliases,
                protein_change=p_change,
            )
            retrieved_vids = [r.id for r in cv_records]
            exact_match_vids = [r.id for r in cv_records if r.is_exact_match]
            if cv_records:
                rank_0_exact = cv_records[0].is_exact_match
        except Exception as e:
            logger.warning(f"ClinVar retrieval failed during evaluation of '{query}': {e}")

    total_latency_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "id": variant_spec["id"],
        "name": variant_spec["name"],
        "query": query,
        "variant_class": variant_spec["variant_class"],
        "expected_p": expected_p,
        "predicted_p": predicted_p,
        "expected_impact": expected_impact,
        "predicted_impact": predicted_impact,
        "is_rejected": is_rejected,
        "parse_error": parse_err,
        "is_exact_protein_match": is_exact,
        "is_concordant": is_concordant,
        "comparison_details": comp_details,
        "expected_clinvar_id": expected_vid,
        "retrieved_clinvar_ids": retrieved_vids,
        "exact_match_clinvar_ids": exact_match_vids,
        "rank_0_is_exact": rank_0_exact,
        "latency_ms": round(total_latency_ms, 2),
    }


def normalize_consequence_category(impact: Optional[str]) -> str:
    """Harmonizes detailed impact descriptions into canonical molecular consequence categories."""
    if not impact:
        return "Invalid / Rejected"
    low = impact.lower()
    if "nonsense" in low:
        return "Nonsense"
    if "missense" in low:
        return "Missense"
    if "synonymous" in low:
        return "Synonymous"
    if "frameshift" in low:
        return "Frameshift"
    if "in-frame" in low or "in frame" in low:
        return "In-frame Indel"
    if "splice" in low:
        return "Splice Site"
    if "5' utr" in low or "5 utr" in low:
        return "5' UTR"
    if "3' utr" in low or "3 utr" in low:
        return "3' UTR"
    if "invalid" in low or "reject" in low:
        return "Invalid / Rejected"
    return impact


async def run_benchmark(
    split: str = "test",
    mode: str = "offline",
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Executes the full scientific benchmark harness."""
    out_dir = output_dir or (RESEARCH_DIR / "results")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Enforce frozen test integrity check
    frozen_hash = verify_frozen_test_hash()
    logger.info(f"Verified frozen test set integrity (SHA-256: {frozen_hash})")

    # 2. Select manifest
    manifest_dir = RESEARCH_DIR / "manifest"
    if split == "test":
        target_file = manifest_dir / "frozen_test.json"
    elif split == "dev":
        target_file = manifest_dir / "development.json"
    elif split == "val":
        target_file = manifest_dir / "validation.json"
    elif split == "all":
        target_file = manifest_dir / "hbb_benchmark_manifest.json"
    else:
        raise ValueError(f"Unknown split '{split}'. Choose from test, dev, val, all.")

    logger.info(f"Loading benchmark split '{split}' from {target_file}")
    with open(target_file, "r", encoding="utf-8") as f:
        variants = json.load(f)

    logger.info(f"Loaded {len(variants)} benchmark variants. Starting evaluation in mode: {mode}")

    # 3. Evaluate each variant sequentially
    results = []
    latencies = []
    y_true_impact = []
    y_pred_impact = []

    tp, fp, fn, tn = 0, 0, 0, 0

    for idx, spec in enumerate(variants, 1):
        res = await evaluate_variant(spec, mode=mode)
        results.append(res)
        latencies.append(res["latency_ms"])

        exp_imp = spec["molecular_consequence"]
        pred_imp = res["predicted_impact"] or "Invalid / Rejected"
        y_true_impact.append(normalize_consequence_category(exp_imp))
        y_pred_impact.append(normalize_consequence_category(pred_imp))

        # Binary diagnostic classification (Valid biological variant vs Invalid negative control)
        is_neg = (exp_imp == "Invalid / Rejected")
        if not is_neg:
            if res["is_concordant"]:
                tp += 1
            else:
                fn += 1
        else:
            if res["is_rejected"]:
                tn += 1
            else:
                fp += 1

        status_sym = "[PASS]" if res["is_concordant"] else "[FAIL]"
        logger.info(f"[{idx:02d}/{len(variants):02d}] {status_sym} {spec['id']}: {spec['hgvs_c_input']:18} -> {str(res['predicted_p']):20} ({res['latency_ms']:.1f} ms)")

    # 4. Compute aggregate metrics
    conf_metrics = calculate_binary_confusion_metrics(tp, fp, fn, tn)
    mc_metrics = calculate_multiclass_metrics(y_true_impact, y_pred_impact)
    retrieval_metrics = calculate_retrieval_metrics(results)
    latency_metrics = calculate_latency_metrics(latencies)

    concordant_count = sum(1 for r in results if r["is_concordant"])
    exact_count = sum(1 for r in results if r["is_exact_protein_match"])
    total_count = len(results)
    concordance_rate = concordant_count / total_count if total_count > 0 else 1.0

    discrepancies = [r for r in results if not r["is_concordant"]]
    disc_formatted = ""
    if discrepancies:
        disc_lines = ["\n### Discrepancy Breakdown:\n"]
        for d in discrepancies:
            disc_lines.append(f"- **{d['id']} ({d['query']})**: Expected `{d['expected_impact']}` / `{d['expected_p']}`, got `{d['predicted_impact']}` / `{d['predicted_p']}`. Details: {d['comparison_details']}")
        disc_formatted = "\n".join(disc_lines)

    eval_summary = {
        "split": split,
        "mode": mode,
        "total_variants": total_count,
        "concordant_variants": concordant_count,
        "exact_matches": exact_count,
        "concordance_rate": round(concordance_rate, 4),
        "exact_match_rate": round(exact_count / total_count, 4) if total_count > 0 else 1.0,
        "sensitivity": conf_metrics["sensitivity"],
        "specificity": conf_metrics["specificity"],
        "precision": conf_metrics["precision"],
        "f1_score": conf_metrics["f1_score"],
        "discrepancy_count": len(discrepancies),
        "discrepancies_formatted": disc_formatted,
    }

    # 5. Emit reports and tables
    report_md = generate_benchmark_markdown_report(
        eval_summary=eval_summary,
        class_metrics=mc_metrics,
        retrieval_metrics=retrieval_metrics,
        latency_metrics=latency_metrics,
        split_name=split,
        output_dir=out_dir
    )

    # 6. Save raw results & metrics JSON
    with open(out_dir / "benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": eval_summary,
            "confusion_metrics": conf_metrics,
            "multiclass_metrics": mc_metrics,
            "retrieval_metrics": retrieval_metrics,
            "latency_metrics": latency_metrics,
            "variants": results,
        }, f, indent=2)

    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": eval_summary,
            "confusion_metrics": conf_metrics,
            "multiclass_metrics": mc_metrics,
            "retrieval_metrics": retrieval_metrics,
            "latency_metrics": latency_metrics,
        }, f, indent=2)

    logger.info("=" * 60)
    logger.info(f"BENCHMARK COMPLETED SUCCESSFULLY ON SPLIT '{split.upper()}'")
    logger.info(f"Concordance Rate: {concordance_rate * 100:.2f}% ({concordant_count}/{total_count})")
    logger.info(f"Sensitivity:      {conf_metrics['sensitivity'] * 100:.2f}%")
    logger.info(f"Specificity:      {conf_metrics['specificity'] * 100:.2f}%")
    logger.info(f"ClinVar Hit@1:    {retrieval_metrics.get('hit_at_1', 0.0) * 100:.2f}%")
    logger.info(f"Macro-F1 Score:   {mc_metrics['macro_f1']:.4f}")
    logger.info(f"Mean Latency:     {latency_metrics['mean_ms']} ms")
    logger.info("=" * 60)

    return eval_summary


def main():
    parser = argparse.ArgumentParser(description="HBB Gene Mutation Analyzer - Scientific Benchmark")
    parser.add_argument("--split", choices=["test", "dev", "val", "all"], default="test", help="Dataset split to evaluate (default: test)")
    parser.add_argument("--mode", choices=["offline", "online"], default="offline", help="Execution mode (default: offline)")
    parser.add_argument("--output", type=str, default=None, help="Output directory for reports and metrics")

    args = parser.parse_args()
    out_path = Path(args.output) if args.output else None

    asyncio.run(run_benchmark(split=args.split, mode=args.mode, output_dir=out_path))


if __name__ == "__main__":
    main()
