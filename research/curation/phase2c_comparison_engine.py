"""Phase 2C Comparison Engine — External Concordance & Normalization Layer.

This module implements the deterministic comparison semantics locked in CP4.1:
- Primary Endpoint: Runtime Engine Molecular Consequence vs External ClinVar Molecular Annotation (A vs C)
- Secondary Endpoint: Runtime Engine Protein Consequence vs Normalized External Protein Annotation
- Precedence Hierarchy: ENGINE_ERROR > HGVS_AMBIGUITY > REFERENCE_MISMATCH > ENGINE_UNSUPPORTED >
                        EXTERNAL_CONFLICT > EXTERNAL_ANNOTATION_INCOMPLETE > EXACT_MOLECULAR_AGREEMENT >
                        MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE > PROTEIN_AGREEMENT_CLASS_DIFFERENCE > UNRESOLVED

GOVERNANCE CONSTRAINT:
This module evaluates runtime engine outputs against external clinical evidence.
It contains zero reference to internal expected outputs, ensuring complete mathematical isolation.
"""

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Tuple, Union


class ComparisonCategory(str, Enum):
    ENGINE_ERROR = "ENGINE_ERROR"
    HGVS_AMBIGUITY = "HGVS_AMBIGUITY"
    REFERENCE_MISMATCH = "REFERENCE_MISMATCH"
    ENGINE_UNSUPPORTED = "ENGINE_UNSUPPORTED"
    EXTERNAL_CONFLICT = "EXTERNAL_CONFLICT"
    EXTERNAL_ANNOTATION_INCOMPLETE = "EXTERNAL_ANNOTATION_INCOMPLETE"
    EXACT_MOLECULAR_AGREEMENT = "EXACT_MOLECULAR_AGREEMENT"
    MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE = "MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE"
    PROTEIN_AGREEMENT_CLASS_DIFFERENCE = "PROTEIN_AGREEMENT_CLASS_DIFFERENCE"
    UNRESOLVED = "UNRESOLVED"


class PrimaryEndpointStatus(str, Enum):
    MATCH = "MATCH"
    DISCREPANCY = "DISCREPANCY"


class ProteinEndpointStatus(str, Enum):
    MATCH = "MATCH"
    DISCREPANCY = "DISCREPANCY"
    INCOMPLETE = "INCOMPLETE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ClinicalSignificanceStatus(str, Enum):
    NO_CONFLICT = "NO_CONFLICT"
    CLINICAL_SIGNIFICANCE_CONFLICT = "CLINICAL_SIGNIFICANCE_CONFLICT"
    NOT_ASSESSED = "NOT_ASSESSED"


@dataclass
class RuntimeEngineOutput:
    execution_status: str  # "SUCCESS" or "ERROR"
    molecular_consequence: Optional[str]
    protein_consequence: Optional[str]
    error_code: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ExternalClinVarEvidence:
    external_molecular: Optional[Union[str, List[str]]]
    external_protein: Optional[str]
    variation_id: Optional[str] = None
    star_rating: Optional[int] = None
    clinical_significance: Optional[Union[str, List[str]]] = None
    conflicting_molecular: bool = False
    conflicting_clinical: bool = False


@dataclass
class ExternalConcordanceResult:
    comparison_category: str
    primary_endpoint_status: str
    protein_endpoint_status: str
    clinical_significance_status: str
    notes: str
    normalized_runtime_molecular: Optional[str]
    normalized_external_molecular: Optional[str]
    normalized_runtime_protein: Optional[str]
    normalized_external_protein: Optional[str]


# Standard IUPAC 20-amino acid translation dictionary
AA_1_TO_3: Dict[str, str] = {
    "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys",
    "Q": "Gln", "E": "Glu", "G": "Gly", "H": "His", "I": "Ile",
    "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro",
    "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val",
    "*": "Ter", "X": "Ter"
}

# Molecular category normalization mapping
MOLECULAR_ONTOLOGY_MAP: Dict[str, str] = {
    "missense": "Missense",
    "missense_variant": "Missense",
    "missense variant": "Missense",
    "nonsense": "Nonsense",
    "stop_gained": "Nonsense",
    "stop gained": "Nonsense",
    "synonymous": "Synonymous",
    "synonymous_variant": "Synonymous",
    "synonymous variant": "Synonymous",
    "silent": "Synonymous",
    "frameshift": "Frameshift",
    "frameshift_variant": "Frameshift",
    "frameshift variant": "Frameshift",
    "splice site disruption": "Splice Site Disruption",
    "splice_acceptor_variant": "Splice Site Disruption",
    "splice_donor_variant": "Splice Site Disruption",
    "splice site": "Splice Site Disruption",
    "splice acceptor": "Splice Site Disruption",
    "splice donor": "Splice Site Disruption",
    "3' utr regulatory": "3' UTR Regulatory",
    "3_prime_utr_variant": "3' UTR Regulatory",
    "3' utr": "3' UTR Regulatory",
    "5' utr regulatory": "5' UTR Regulatory",
    "5_prime_utr_variant": "5' UTR Regulatory",
    "5' utr": "5' UTR Regulatory",
    "in-frame indel": "In-Frame Indel",
    "inframe_indel": "In-Frame Indel",
    "inframe_deletion": "In-Frame Indel",
    "inframe_insertion": "In-Frame Indel",
}


def normalize_molecular_category(val: Optional[Union[str, List[str]]]) -> Optional[str]:
    """Deterministically normalizes molecular consequence categories across ontologies."""
    if val is None:
        return None
    if isinstance(val, list):
        if not val:
            return None
        # If all items normalize to same, return that; else return "CONFLICT"
        norm_list = [normalize_molecular_category(x) for x in val]
        unique_norms = set(norm_list)
        if len(unique_norms) == 1:
            return norm_list[0]
        return "CONFLICT"

    clean = str(val).strip().lower()
    return MOLECULAR_ONTOLOGY_MAP.get(clean, str(val).strip())


def parse_protein_consequence(p: Optional[str]) -> Tuple[str, Optional[int], Optional[str], Optional[str], Optional[Any]]:
    """Deterministically parses a protein consequence string into a canonical tuple.

    Returns:
        (variant_type, codon_pos, ref_aa_3letter, alt_aa_3letter_or_Ter, extra_detail)
    """
    if p is None or str(p).strip() in ("", "None", "null", "none"):
        return ("ABSENT", None, None, None, None)

    s = str(p).strip()

    if s == "p.?":
        return ("SPLICE_UNKNOWN", None, None, None, None)

    if s in ("p.(=)", "p.="):
        return ("SYNONYMOUS_CDS", None, None, None, None)

    # Codon-specific synonymous: p.Leu69=, L69=, p.L69=
    m_syn = re.match(r"^p?\.?([A-Z][a-z]{2}|[A-Z])(\d+)=$", s)
    if m_syn:
        ref_raw, pos = m_syn.groups()
        ref_3 = AA_1_TO_3.get(ref_raw, ref_raw)
        return ("SYNONYMOUS_CODON", int(pos), ref_3, "=", None)

    # Nonsense with 3-letter ref: p.Gln128Ter, p.Gln128*, Gln128Ter
    m_non_3 = re.match(r"^p?\.?([A-Z][a-z]{2})(\d+)(?:Ter|\*|X)$", s)
    if m_non_3:
        ref_3, pos = m_non_3.groups()
        return ("NONSENSE", int(pos), ref_3, "Ter", None)

    # Nonsense with 1-letter ref: Q128*, Q128Ter, p.Q128*
    m_non_1 = re.match(r"^p?\.?([A-Z])(\d+)(?:\*|Ter|X)$", s)
    if m_non_1:
        ref_1, pos = m_non_1.groups()
        return ("NONSENSE", int(pos), AA_1_TO_3.get(ref_1, ref_1), "Ter", None)

    # Full HGVS Frameshift: p.Glu7ArgfsTer13, p.Val127GlufsTer8
    m_fs_full = re.match(r"^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})fs(?:Ter|\*)(\d+|\?)$", s)
    if m_fs_full:
        ref_3, pos, alt_3, off = m_fs_full.groups()
        return ("FRAMESHIFT_FULL", int(pos), ref_3, alt_3, int(off) if off.isdigit() else None)

    # Truncated Frameshift: E7fs, p.E7fs, Glu7fs
    m_fs_trunc = re.match(r"^p?\.?([A-Z][a-z]{2}|[A-Z])(\d+)fs$", s)
    if m_fs_trunc:
        ref_raw, pos = m_fs_trunc.groups()
        ref_3 = AA_1_TO_3.get(ref_raw, ref_raw)
        return ("FRAMESHIFT_TRUNC", int(pos), ref_3, None, None)

    # Missense with 3-letter IUPAC: p.Asn109Lys, Asn109Lys
    m_mis_3 = re.match(r"^p?\.?([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$", s)
    if m_mis_3:
        ref_3, pos, alt_3 = m_mis_3.groups()
        if alt_3 == "Ter":
            return ("NONSENSE", int(pos), ref_3, "Ter", None)
        return ("MISSENSE", int(pos), ref_3, alt_3, None)

    # Missense with 1-letter IUPAC: N109K, p.N109K
    m_mis_1 = re.match(r"^p?\.?([A-Z])(\d+)([A-Z])$", s)
    if m_mis_1:
        ref_1, pos, alt_1 = m_mis_1.groups()
        return ("MISSENSE", int(pos), AA_1_TO_3.get(ref_1, ref_1), AA_1_TO_3.get(alt_1, alt_1), None)

    return ("UNPARSED", None, None, None, s)


def evaluate_external_concordance(
    runtime_output: RuntimeEngineOutput,
    external_evidence: ExternalClinVarEvidence,
    target_class: str
) -> ExternalConcordanceResult:
    """Evaluates runtime deterministic engine output strictly against external ClinVar evidence.

    Follows the 10-level Precedence Hierarchy locked in CP4.1:
    1. ENGINE_ERROR
    2. HGVS_AMBIGUITY
    3. REFERENCE_MISMATCH
    4. ENGINE_UNSUPPORTED
    5. EXTERNAL_CONFLICT
    6. EXTERNAL_ANNOTATION_INCOMPLETE
    7. EXACT_MOLECULAR_AGREEMENT
    8. MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE
    9. PROTEIN_AGREEMENT_CLASS_DIFFERENCE
    10. UNRESOLVED
    """
    # -------------------------------------------------------------
    # Priority 1-4: Engine Execution Errors & Boundary Checks
    # -------------------------------------------------------------
    if runtime_output.execution_status == "ERROR":
        err = runtime_output.error_code or ""
        msg = runtime_output.error_message or "Engine execution failed"

        if err in ("INVALID_SYNTAX", "UNSUPPORTED_SYNTAX"):
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.HGVS_AMBIGUITY.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=ClinicalSignificanceStatus.NOT_ASSESSED.value,
                notes=f"HGVS syntax ambiguity: {msg}",
                normalized_runtime_molecular=None,
                normalized_external_molecular=normalize_molecular_category(external_evidence.external_molecular),
                normalized_runtime_protein=None,
                normalized_external_protein=external_evidence.external_protein
            )
        elif err == "INVALID_REF":
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.REFERENCE_MISMATCH.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=ClinicalSignificanceStatus.NOT_ASSESSED.value,
                notes=f"Reference mismatch: {msg}",
                normalized_runtime_molecular=None,
                normalized_external_molecular=normalize_molecular_category(external_evidence.external_molecular),
                normalized_runtime_protein=None,
                normalized_external_protein=external_evidence.external_protein
            )
        elif err in ("OUT_OF_BOUNDS", "DEEP_INTRONIC"):
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.ENGINE_UNSUPPORTED.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=ClinicalSignificanceStatus.NOT_ASSESSED.value,
                notes=f"Variant lies outside engine supported boundary: {msg}",
                normalized_runtime_molecular=None,
                normalized_external_molecular=normalize_molecular_category(external_evidence.external_molecular),
                normalized_runtime_protein=None,
                normalized_external_protein=external_evidence.external_protein
            )
        else:
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.ENGINE_ERROR.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=ClinicalSignificanceStatus.NOT_ASSESSED.value,
                notes=f"Runtime engine exception: {msg}",
                normalized_runtime_molecular=None,
                normalized_external_molecular=normalize_molecular_category(external_evidence.external_molecular),
                normalized_runtime_protein=None,
                normalized_external_protein=external_evidence.external_protein
            )

    # -------------------------------------------------------------
    # Clinical Significance Status (Orthogonal Audit Field)
    # -------------------------------------------------------------
    if external_evidence.conflicting_clinical:
        clin_stat = ClinicalSignificanceStatus.CLINICAL_SIGNIFICANCE_CONFLICT.value
    elif isinstance(external_evidence.clinical_significance, list) and len(set(external_evidence.clinical_significance)) > 1:
        clin_stat = ClinicalSignificanceStatus.CLINICAL_SIGNIFICANCE_CONFLICT.value
    elif not external_evidence.clinical_significance or external_evidence.clinical_significance in ("", "None", "NOT_ASSESSED"):
        clin_stat = ClinicalSignificanceStatus.NOT_ASSESSED.value
    else:
        clin_stat = ClinicalSignificanceStatus.NO_CONFLICT.value

    # -------------------------------------------------------------
    # Normalization of Runtime and External Evidence
    # -------------------------------------------------------------
    norm_A_mol = normalize_molecular_category(runtime_output.molecular_consequence)
    norm_C_mol = normalize_molecular_category(external_evidence.external_molecular)

    parsed_A_prot = parse_protein_consequence(runtime_output.protein_consequence)
    parsed_C_prot = parse_protein_consequence(external_evidence.external_protein)

    # -------------------------------------------------------------
    # Priority 5: External Evidence Molecular Conflict
    # -------------------------------------------------------------
    if external_evidence.conflicting_molecular or norm_C_mol == "CONFLICT":
        return ExternalConcordanceResult(
            comparison_category=ComparisonCategory.EXTERNAL_CONFLICT.value,
            primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
            protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
            clinical_significance_status=clin_stat,
            notes="Conflicting external molecular consequence assertions in ClinVar",
            normalized_runtime_molecular=norm_A_mol,
            normalized_external_molecular="CONFLICT",
            normalized_runtime_protein=runtime_output.protein_consequence,
            normalized_external_protein=external_evidence.external_protein
        )

    # -------------------------------------------------------------
    # Priority 6: External Annotation Incompleteness
    # -------------------------------------------------------------
    # Sub-case A: Missing external molecular consequence
    if norm_C_mol is None or norm_C_mol in ("", "None"):
        return ExternalConcordanceResult(
            comparison_category=ComparisonCategory.EXTERNAL_ANNOTATION_INCOMPLETE.value,
            primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
            protein_endpoint_status=ProteinEndpointStatus.INCOMPLETE.value,
            clinical_significance_status=clin_stat,
            notes="External ClinVar record lacks molecular consequence classification",
            normalized_runtime_molecular=norm_A_mol,
            normalized_external_molecular=None,
            normalized_runtime_protein=runtime_output.protein_consequence,
            normalized_external_protein=external_evidence.external_protein
        )

    is_noncoding_class = (
        target_class in ("C10", "C11") or
        norm_A_mol in ("3' UTR Regulatory", "5' UTR Regulatory")
    )

    # Sub-case B: Coding or splice variant where external protein is absent
    if not is_noncoding_class and parsed_C_prot[0] == "ABSENT":
        if norm_A_mol == norm_C_mol:
            # Locked rule for C09 & coding variants with molecular match but missing external protein:
            # Primary molecular endpoint is MATCH, protein is INCOMPLETE, category is EXTERNAL_ANNOTATION_INCOMPLETE.
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.EXTERNAL_ANNOTATION_INCOMPLETE.value,
                primary_endpoint_status=PrimaryEndpointStatus.MATCH.value,
                protein_endpoint_status=ProteinEndpointStatus.INCOMPLETE.value,
                clinical_significance_status=clin_stat,
                notes="Molecular consequence concordant; external record lacks predicted protein annotation",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=None
            )
        else:
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.UNRESOLVED.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.INCOMPLETE.value,
                clinical_significance_status=clin_stat,
                notes="Molecular consequence discrepant and external record lacks protein annotation",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=None
            )

    # -------------------------------------------------------------
    # Non-Coding Regulatory Variant Evaluation (e.g. C11 3' UTR)
    # -------------------------------------------------------------
    if is_noncoding_class:
        if norm_A_mol == norm_C_mol:
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value,
                primary_endpoint_status=PrimaryEndpointStatus.MATCH.value,
                protein_endpoint_status=ProteinEndpointStatus.NOT_APPLICABLE.value,
                clinical_significance_status=clin_stat,
                notes="Non-coding regulatory concordance; protein alteration not applicable",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=None,
                normalized_external_protein=None
            )
        else:
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.UNRESOLVED.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.NOT_APPLICABLE.value,
                clinical_significance_status=clin_stat,
                notes="Non-coding regulatory molecular consequence discrepancy",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=None,
                normalized_external_protein=None
            )

    # -------------------------------------------------------------
    # Coding Protein Equivalence Evaluation
    # -------------------------------------------------------------
    prot_exact_match = False
    prot_format_diff = False

    t_A, pos_A, ref_A, alt_A, extra_A = parsed_A_prot
    t_C, pos_C, ref_C, alt_C, extra_C = parsed_C_prot

    if t_A == "MISSENSE" and t_C == "MISSENSE":
        if pos_A == pos_C and ref_A == ref_C and alt_A == alt_C:
            prot_exact_match = True
    elif t_A == "NONSENSE" and t_C == "NONSENSE":
        if pos_A == pos_C and ref_A == ref_C:
            prot_exact_match = True
    elif t_A in ("SYNONYMOUS_CDS", "SYNONYMOUS_CODON") and t_C in ("SYNONYMOUS_CDS", "SYNONYMOUS_CODON"):
        # Semantic synonymous equivalence: both assert zero translated amino acid change
        prot_exact_match = True
    elif t_A == "FRAMESHIFT_FULL" and t_C == "FRAMESHIFT_TRUNC":
        # Truncated frameshift notation (e.g. p.Glu7ArgfsTer13 vs E7fs)
        if pos_A == pos_C and ref_A == ref_C:
            prot_format_diff = True
    elif t_A == "FRAMESHIFT_FULL" and t_C == "FRAMESHIFT_FULL":
        if pos_A == pos_C and ref_A == ref_C and alt_A == alt_C and extra_A == extra_C:
            prot_exact_match = True
        elif pos_A == pos_C and ref_A == ref_C:
            prot_format_diff = True

    mol_match = (norm_A_mol == norm_C_mol)

    # -------------------------------------------------------------
    # Priority 7-10: Molecular and Protein Concordance Decision
    # -------------------------------------------------------------
    if mol_match:
        if prot_exact_match:
            # Priority 7
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value,
                primary_endpoint_status=PrimaryEndpointStatus.MATCH.value,
                protein_endpoint_status=ProteinEndpointStatus.MATCH.value,
                clinical_significance_status=clin_stat,
                notes="Exact molecular and protein concordance with external ClinVar annotation",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=external_evidence.external_protein
            )
        elif prot_format_diff:
            # Priority 8
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE.value,
                primary_endpoint_status=PrimaryEndpointStatus.MATCH.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=clin_stat,
                notes="Molecular consequence concordant; external protein notation truncated/representational",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=external_evidence.external_protein
            )
        else:
            # Molecular matches but protein residue/position differs
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE.value,
                primary_endpoint_status=PrimaryEndpointStatus.MATCH.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=clin_stat,
                notes="Molecular consequence concordant; protein consequences differ",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=external_evidence.external_protein
            )
    else:
        if prot_exact_match:
            # Priority 9
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.PROTEIN_AGREEMENT_CLASS_DIFFERENCE.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.MATCH.value,
                clinical_significance_status=clin_stat,
                notes="Protein consequence concordant; classification ontology differs",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=external_evidence.external_protein
            )
        else:
            # Priority 10
            return ExternalConcordanceResult(
                comparison_category=ComparisonCategory.UNRESOLVED.value,
                primary_endpoint_status=PrimaryEndpointStatus.DISCREPANCY.value,
                protein_endpoint_status=ProteinEndpointStatus.DISCREPANCY.value,
                clinical_significance_status=clin_stat,
                notes="Direct biological consequence disagreement between engine output and external annotation",
                normalized_runtime_molecular=norm_A_mol,
                normalized_external_molecular=norm_C_mol,
                normalized_runtime_protein=runtime_output.protein_consequence,
                normalized_external_protein=external_evidence.external_protein
            )
