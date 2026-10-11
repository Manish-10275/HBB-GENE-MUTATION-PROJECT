"""
Consequence agreement evaluation logic for HBB Mutation Analyzer.
Compares predicted HGVS protein consequences (hgvs_p) and functional impacts
against authoritative ground truth assertions.
"""

import re
from typing import Dict, Optional, Tuple


def normalize_protein_change(p_str: Optional[str]) -> Optional[str]:
    """Normalizes HGVS protein strings for flexible comparison."""
    if not p_str:
        return None
    clean = p_str.strip()
    if clean.startswith("NP_000509.1:"):
        clean = clean.replace("NP_000509.1:", "")
    # Remove surrounding parens e.g. p.(=) -> p.=, p.(Phe42fs) -> p.Phe42fs
    clean = re.sub(r"p\.\((.*?)\)", r"p.\1", clean)
    return clean


def evaluate_consequence_agreement(
    expected_p: Optional[str],
    predicted_p: Optional[str],
    expected_impact: str,
    predicted_impact: Optional[str],
    is_rejected: bool,
    expected_rejection_reason: Optional[str] = None
) -> Tuple[bool, bool, Dict[str, Any]]:
    """
    Evaluates agreement between predicted consequence and ground truth.

    Returns:
    - is_exact_match (bool): Exact character match on normalized protein string
    - is_concordant (bool): Biologically concordant (including equivalent short forms or valid rejections)
    - details (dict): Detailed breakdown of comparison
    """
    # Case 1: Expected Rejection (Negative Control)
    if expected_impact == "Invalid / Rejected":
        is_concordant = is_rejected
        is_exact = is_rejected
        return is_exact, is_concordant, {
            "mode": "negative_control",
            "correctly_rejected": is_rejected,
            "expected_impact": expected_impact,
            "predicted_impact": predicted_impact or "Rejected",
        }

    # Case 2: Expected Non-coding / Splice (hgvs_p is p.? or None)
    if expected_p is None or expected_p == "p.?":
        impact_match = False
        if predicted_impact:
            exp_low = expected_impact.lower()
            pred_low = predicted_impact.lower()
            impact_match = (
                exp_low in pred_low
                or pred_low in exp_low
                or ("splice" in exp_low and "splice" in pred_low)
                or ("utr" in exp_low and "utr" in pred_low)
            )

        p_match = (predicted_p == "p.?" or predicted_p is None)
        is_concordant = impact_match and p_match and not is_rejected
        is_exact = (predicted_p == expected_p) and impact_match

        return is_exact, is_concordant, {
            "mode": "non_coding_or_splice",
            "impact_match": impact_match,
            "protein_match": p_match,
            "expected_p": expected_p,
            "predicted_p": predicted_p,
        }

    # Case 3: Coding Protein Alteration
    norm_exp = normalize_protein_change(expected_p)
    norm_pred = normalize_protein_change(predicted_p)

    is_exact = (norm_exp == norm_pred) and not is_rejected

    # Concordance check: handles short form frameshifts e.g. p.Phe42fs matching p.Phe42LeufsTer19
    is_concordant = is_exact
    if not is_exact and norm_exp and norm_pred:
        # Check if short-form fs matches canonical fs
        m_exp_fs = re.search(r"p\.([A-Z][a-z]{2}\d+)", norm_exp)
        m_pred_fs = re.search(r"p\.([A-Z][a-z]{2}\d+)", norm_pred)
        if m_exp_fs and m_pred_fs and m_exp_fs.group(1) == m_pred_fs.group(1):
            if ("fs" in norm_exp or "Ter" in norm_exp) and ("fs" in norm_pred or "Ter" in norm_pred):
                is_concordant = True
        # Check synonymous equivalence e.g. p.= vs p.(=)
        if ("=" in norm_exp and "=" in norm_pred):
            is_concordant = True

    impact_concordant = False
    if predicted_impact:
        exp_imp_low = expected_impact.lower()
        pred_imp_low = predicted_impact.lower()
        impact_concordant = (
            exp_imp_low in pred_imp_low
            or pred_imp_low in exp_imp_low
            or ("frameshift" in exp_imp_low and "frameshift" in pred_imp_low)
        )

    return is_exact, (is_concordant and impact_concordant and not is_rejected), {
        "mode": "coding_consequence",
        "exact_protein_match": is_exact,
        "concordant_protein_match": is_concordant,
        "impact_match": impact_concordant,
        "expected_p": expected_p,
        "predicted_p": predicted_p,
        "expected_impact": expected_impact,
        "predicted_impact": predicted_impact,
    }
