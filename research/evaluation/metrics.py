"""
Statistical and Information Retrieval metrics calculation for HBB Benchmark.
Computes:
- Consequence classification metrics (Accuracy, Sensitivity, Specificity, Precision, Recall, F1, Macro-F1)
- ClinVar retrieval metrics (Hit@1, Recall@5, False-positive rate, Provenance breakdown)
- Benchmark runtime latency (mean, median, p95, min, max)

Hardened against:
- Empty datasets and undefined denominators (returns None / explicit reasons, never false 1.0 perfect scores)
- Mismatched array lengths (explicit ValueError instead of silent zip truncation)
- Silent fallback conflation (tracks live, cached, fixture, and failed retrievals)
"""

from typing import Any, Dict, List, Optional
import statistics


def calculate_binary_confusion_metrics(tp: int, fp: int, fn: int, tn: int) -> Dict[str, Any]:
    """
    Computes standard binary diagnostic performance metrics.
    When a denominator is zero, returns None (JSON null) and includes sample counts
    and clear reasons, rather than misleading 1.0 perfect scores.
    """
    total = tp + fp + fn + tn
    positives = tp + fn
    negatives = tn + fp
    predicted_positives = tp + fp
    predicted_negatives = tn + fn

    sensitivity = round(tp / positives, 4) if positives > 0 else None
    specificity = round(tn / negatives, 4) if negatives > 0 else None
    precision = round(tp / predicted_positives, 4) if predicted_positives > 0 else None
    npv = round(tn / predicted_negatives, 4) if predicted_negatives > 0 else None
    accuracy = round((tp + tn) / total, 4) if total > 0 else None

    if precision is not None and sensitivity is not None:
        if (precision + sensitivity) > 0:
            f1 = round(2 * precision * sensitivity / (precision + sensitivity), 4)
        else:
            f1 = 0.0
    else:
        f1 = None

    reasons: Dict[str, str] = {}
    if positives == 0:
        reasons["sensitivity"] = "Undefined: zero positive cases (tp + fn = 0)"
    if negatives == 0:
        reasons["specificity"] = "Undefined: zero negative cases (tn + fp = 0)"
    if predicted_positives == 0:
        reasons["precision"] = "Undefined: zero positive predictions (tp + fp = 0)"
    if predicted_negatives == 0:
        reasons["npv"] = "Undefined: zero negative predictions (tn + fn = 0)"
    if total == 0:
        reasons["accuracy"] = "Undefined: zero total cases (total = 0)"
    if f1 is None and "sensitivity" not in reasons and "precision" not in reasons:
        reasons["f1_score"] = "Undefined: precision or sensitivity is undefined"

    return {
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "total_samples": total,
        "positive_samples": positives,
        "negative_samples": negatives,
        "sensitivity": sensitivity,
        "recall": sensitivity,
        "specificity": specificity,
        "precision": precision,
        "positive_predictive_value": precision,
        "negative_predictive_value": npv,
        "accuracy": accuracy,
        "f1_score": f1,
        "undefined_reasons": reasons,
    }


def calculate_multiclass_metrics(y_true: List[str], y_pred: List[str]) -> Dict[str, Any]:
    """
    Computes per-class and Macro-averaged classification metrics.
    Strictly verifies equal length of y_true and y_pred (raises ValueError on mismatch).
    Handles empty arrays by returning None rather than false 1.0 scores.
    """
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"Mismatched array lengths: len(y_true)={len(y_true)} != len(y_pred)={len(y_pred)}. "
            f"Silent truncation via zip is prohibited."
        )

    if not y_true:
        return {
            "overall_accuracy": None,
            "macro_f1": None,
            "evaluated_samples": 0,
            "per_class": {},
            "reason": "Empty dataset: zero samples evaluated",
        }

    classes = sorted(list(set(y_true + y_pred)))
    class_metrics: Dict[str, Any] = {}
    f1_list: List[float] = []

    for cls in classes:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp == cls)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != cls and yp == cls)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp != cls)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt != cls and yp != cls)
        support = sum(1 for yt in y_true if yt == cls)

        prec = round(tp / (tp + fp), 4) if (tp + fp) > 0 else None
        rec = round(tp / (tp + fn), 4) if (tp + fn) > 0 else None

        if prec is not None and rec is not None:
            if (prec + rec) > 0:
                f1 = round((2 * prec * rec / (prec + rec)), 4)
            else:
                f1 = 0.0
            f1_list.append(f1)
        else:
            f1 = None

        class_metrics[cls] = {
            "support": support,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
        }

    macro_f1 = round(sum(f1_list) / len(f1_list), 4) if f1_list else None
    overall_acc = round(sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true), 4)

    return {
        "overall_accuracy": overall_acc,
        "macro_f1": macro_f1,
        "evaluated_samples": len(y_true),
        "per_class": class_metrics,
    }


def calculate_retrieval_metrics(
    eval_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes external database retrieval metrics (ClinVar Hit@1, Recall@5, False Match Rate).
    Only includes clinical variants that have an authoritative ClinVar ID ground truth.
    Categorizes retrieval provenance into LIVE, FIXTURE, CACHED, and FAILED.
    """
    clin_eval = [r for r in eval_records if r.get("expected_clinvar_id") is not None]
    if not clin_eval:
        return {
            "evaluated_clinvar_records": 0,
            "hit_at_1": None,
            "hit_at_1_count": 0,
            "recall_at_5": None,
            "recall_at_5_count": 0,
            "false_matches": 0,
            "false_match_rate": None,
            "mean_retrieved_records": None,
            "provenance_breakdown": {
                "live": 0,
                "fixture": 0,
                "cached": 0,
                "failed": 0,
                "other": 0,
            },
            "reason": "No clinical variants with expected ClinVar ID in evaluation set",
        }

    hit_1_count = 0
    recall_5_count = 0
    false_match_count = 0
    total_retrieved = 0

    prov_counts = {"live": 0, "fixture": 0, "cached": 0, "failed": 0, "other": 0}

    for item in clin_eval:
        expected_id = str(item["expected_clinvar_id"])
        retrieved_ids = [str(x) for x in item.get("retrieved_clinvar_ids", [])]
        exact_match_ids = [str(x) for x in item.get("exact_match_clinvar_ids", [])]
        total_retrieved += len(retrieved_ids)

        src = item.get("retrieval_source", "").upper()
        if "LIVE" in src:
            prov_counts["live"] += 1
        elif "FIXTURE" in src:
            prov_counts["fixture"] += 1
        elif "CACHED" in src:
            prov_counts["cached"] += 1
        elif "FAIL" in src or "ERROR" in src:
            prov_counts["failed"] += 1
        else:
            prov_counts["other"] += 1

        # Hit@1: Rank 0 record has exact match flag and matches expected ID
        if retrieved_ids and retrieved_ids[0] == expected_id and item.get("rank_0_is_exact", False):
            hit_1_count += 1

        # Recall@5: Expected ID is in top-5 candidates
        if expected_id in retrieved_ids[:5]:
            recall_5_count += 1

        # False positive check: any ID tagged as exact match that is NOT the expected ID
        for em_id in exact_match_ids:
            if em_id != expected_id:
                false_match_count += 1

    total_n = len(clin_eval)
    return {
        "evaluated_clinvar_records": total_n,
        "hit_at_1": round(hit_1_count / total_n, 4),
        "hit_at_1_count": hit_1_count,
        "recall_at_5": round(recall_5_count / total_n, 4),
        "recall_at_5_count": recall_5_count,
        "false_matches": false_match_count,
        "false_match_rate": round(false_match_count / total_n, 4),
        "mean_retrieved_records": round(total_retrieved / total_n, 2),
        "provenance_breakdown": prov_counts,
    }


def calculate_latency_metrics(latencies_ms: List[float]) -> Dict[str, Any]:
    """Computes runtime latency statistical distribution."""
    if not latencies_ms:
        return {
            "mean_ms": None,
            "median_ms": None,
            "p95_ms": None,
            "min_ms": None,
            "max_ms": None,
            "sample_count": 0,
            "reason": "No latency measurements recorded",
        }

    s_lats = sorted(latencies_ms)
    n = len(s_lats)
    p95_idx = int(0.95 * n) if int(0.95 * n) < n else n - 1

    return {
        "mean_ms": round(statistics.mean(s_lats), 2),
        "median_ms": round(statistics.median(s_lats), 2),
        "p95_ms": round(s_lats[p95_idx], 2),
        "min_ms": round(min(s_lats), 2),
        "max_ms": round(max(s_lats), 2),
        "sample_count": n,
    }
