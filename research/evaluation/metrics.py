"""
Statistical and Information Retrieval metrics calculation for HBB Benchmark.
Computes:
- Consequence classification metrics (Accuracy, Sensitivity, Specificity, Precision, Recall, F1, Macro-F1)
- ClinVar retrieval metrics (Hit@1, Recall@5, False-positive rate)
- Benchmark runtime latency (mean, median, p95, min, max)
"""

from typing import Any, Dict, List, Optional, Set
import statistics


def calculate_binary_confusion_metrics(tp: int, fp: int, fn: int, tn: int) -> Dict[str, float]:
    """Computes standard binary diagnostic performance metrics."""
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 1.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 1.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 1.0
    f1 = 2 * precision * sensitivity / (precision + sensitivity) if (precision + sensitivity) > 0 else 0.0

    return {
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "sensitivity": round(sensitivity, 4),
        "recall": round(sensitivity, 4),
        "specificity": round(specificity, 4),
        "precision": round(precision, 4),
        "positive_predictive_value": round(precision, 4),
        "negative_predictive_value": round(npv, 4),
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1, 4),
    }


def calculate_multiclass_metrics(y_true: List[str], y_pred: List[str]) -> Dict[str, Any]:
    """Computes per-class and Macro-averaged classification metrics."""
    classes = sorted(list(set(y_true + y_pred)))
    class_metrics = {}
    f1_list = []

    for cls in classes:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp == cls)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != cls and yp == cls)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp != cls)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt != cls and yp != cls)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
        f1_list.append(f1)

        class_metrics[cls] = {
            "support": sum(1 for yt in y_true if yt == cls),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
        }

    macro_f1 = sum(f1_list) / len(f1_list) if f1_list else 0.0
    overall_acc = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true) if y_true else 1.0

    return {
        "overall_accuracy": round(overall_acc, 4),
        "macro_f1": round(macro_f1, 4),
        "per_class": class_metrics,
    }


def calculate_retrieval_metrics(
    eval_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes external database retrieval metrics (ClinVar Hit@1, Recall@5, False Match Rate).
    Only includes clinical variants that have an authoritative ClinVar ID ground truth.
    """
    clin_eval = [r for r in eval_records if r.get("expected_clinvar_id") is not None]
    if not clin_eval:
        return {
            "evaluated_clinvar_records": 0,
            "hit_at_1": 1.0,
            "recall_at_5": 1.0,
            "false_match_rate": 0.0,
            "mean_retrieved_records": 0.0,
        }

    hit_1_count = 0
    recall_5_count = 0
    false_match_count = 0
    total_retrieved = 0

    for item in clin_eval:
        expected_id = str(item["expected_clinvar_id"])
        retrieved_ids = [str(x) for x in item.get("retrieved_clinvar_ids", [])]
        exact_match_ids = [str(x) for x in item.get("exact_match_clinvar_ids", [])]
        total_retrieved += len(retrieved_ids)

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
    }


def calculate_latency_metrics(latencies_ms: List[float]) -> Dict[str, float]:
    """Computes runtime latency statistical distribution."""
    if not latencies_ms:
        return {"mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

    s_lats = sorted(latencies_ms)
    n = len(s_lats)
    p95_idx = int(0.95 * n) if int(0.95 * n) < n else n - 1

    return {
        "mean_ms": round(statistics.mean(s_lats), 2),
        "median_ms": round(statistics.median(s_lats), 2),
        "p95_ms": round(s_lats[p95_idx], 2),
        "min_ms": round(min(s_lats), 2),
        "max_ms": round(max(s_lats), 2),
    }
