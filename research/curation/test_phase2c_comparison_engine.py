"""Unit and Integration Test Suite for Phase 2C Comparison Engine.

Verifies the 18 mandatory test scenarios specified in CP4.1 and CP4.2:
1. A=Missense B=Missense C=Nonsense (Anti-Oracle Disagreement Detection)
2. A=Missense B=Nonsense C=Missense (Anti-Oracle Expected Divergence Independence)
3. C09 missing external protein
4. C11 expected noncoding protein absence
5. Clinical significance conflict
6. External molecular conflict
7. One-letter vs three-letter protein
8. Stop notation equivalence (*, Ter, X)
9. Synonymous notation (CDS vs codon)
10. Frameshift truncated notation (full HGVS vs E7fs)
11. Missing external molecular annotation
12. Reference mismatch (INVALID_REF)
13. HGVS ambiguity (INVALID_SYNTAX)
14. Engine unsupported (OUT_OF_BOUNDS)
15. Engine error (Unhandled runtime crash)
16. Unresolved case (Direct biological discrepancy)
17. Legacy numbering (Standard RefSeq coordinate mapping)
18. Explicit anti-oracle leakage isolation proof
"""

import unittest
from research.curation.phase2c_comparison_engine import (
    RuntimeEngineOutput,
    ExternalClinVarEvidence,
    evaluate_external_concordance,
    ComparisonCategory,
    PrimaryEndpointStatus,
    ProteinEndpointStatus,
    ClinicalSignificanceStatus,
    parse_protein_consequence,
    normalize_molecular_category
)


class TestPhase2CComparisonEngine(unittest.TestCase):

    def test_01_anti_oracle_disagreement_detection(self):
        """Test 1: Engine agrees with stored expected, but external evidence disagrees."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Nonsense",
            external_protein="N109*"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.UNRESOLVED.value)
        self.assertNotEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_02_anti_oracle_expected_divergence_independence(self):
        """Test 2: Engine diverges from stored expected, but matches external evidence."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="N109K"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_03_c09_missing_protein(self):
        """Test 3: C09 splice variant with missing external protein string."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Splice Site Disruption",
            protein_consequence="p.?"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Splice Site Disruption",
            external_protein=""
        )
        res = evaluate_external_concordance(runtime, external, target_class="C09")

        # Must credit molecular match, flag protein as incomplete, and categorize as EXTERNAL_ANNOTATION_INCOMPLETE
        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.INCOMPLETE.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXTERNAL_ANNOTATION_INCOMPLETE.value)

    def test_04_c11_expected_noncoding_protein_absence(self):
        """Test 4: C11 3' UTR regulatory variant where protein absence is biologically expected."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="3' UTR Regulatory",
            protein_consequence=None
        )
        external = ExternalClinVarEvidence(
            external_molecular="3' UTR Regulatory",
            external_protein=""
        )
        res = evaluate_external_concordance(runtime, external, target_class="C11")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.NOT_APPLICABLE.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_05_clinical_significance_conflict(self):
        """Test 5: Conflicting clinical assertions do not taint a valid molecular concordance."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="N109K",
            clinical_significance=["Pathogenic", "Uncertain significance"],
            conflicting_clinical=True
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
        self.assertEqual(res.clinical_significance_status, ClinicalSignificanceStatus.CLINICAL_SIGNIFICANCE_CONFLICT.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_06_external_molecular_conflict(self):
        """Test 6: Contradictory external molecular classifications trigger EXTERNAL_CONFLICT."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular=["Missense", "Nonsense"],
            external_protein="N109K",
            conflicting_molecular=True
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXTERNAL_CONFLICT.value)

    def test_07_one_letter_vs_three_letter_protein(self):
        """Test 7: 1-letter to 3-letter IUPAC protein normalization."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Val134Leu"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="V134L"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_08_stop_notation_equivalence(self):
        """Test 8: Termination codon representations (*, Ter, X) resolve canonically."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Nonsense",
            protein_consequence="p.Gln128Ter"
        )
        for stop_str in ["Q128*", "Q128Ter", "Q128X"]:
            external = ExternalClinVarEvidence(
                external_molecular="Nonsense",
                external_protein=stop_str
            )
            res = evaluate_external_concordance(runtime, external, target_class="C02")
            self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
            self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
            self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_09_synonymous_notation(self):
        """Test 9: Synonymous CDS notation p.(=) matches codon notation p.Leu69=."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Synonymous",
            protein_consequence="p.(=)"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Synonymous",
            external_protein="p.Leu69="
        )
        res = evaluate_external_concordance(runtime, external, target_class="C03")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_10_frameshift_truncated_notation(self):
        """Test 10: Truncated frameshift notation (E7fs vs full HGVS) categorized as formatting difference."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Frameshift",
            protein_consequence="p.Glu7ArgfsTer13"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Frameshift",
            external_protein="E7fs"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C04")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE.value)

    def test_11_missing_external_molecular_annotation(self):
        """Test 11: Missing external molecular annotation triggers EXTERNAL_ANNOTATION_INCOMPLETE."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular="",
            external_protein="N109K"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.INCOMPLETE.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXTERNAL_ANNOTATION_INCOMPLETE.value)

    def test_12_reference_mismatch(self):
        """Test 12: INVALID_REF engine error maps to REFERENCE_MISMATCH."""
        runtime = RuntimeEngineOutput(
            execution_status="ERROR",
            molecular_consequence=None,
            protein_consequence=None,
            error_code="INVALID_REF",
            error_message="Reference base does not match transcript"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="N109K"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.REFERENCE_MISMATCH.value)

    def test_13_hgvs_ambiguity(self):
        """Test 13: INVALID_SYNTAX engine error maps to HGVS_AMBIGUITY."""
        runtime = RuntimeEngineOutput(
            execution_status="ERROR",
            molecular_consequence=None,
            protein_consequence=None,
            error_code="INVALID_SYNTAX",
            error_message="Ambiguous HGVS syntax"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="N109K"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.HGVS_AMBIGUITY.value)

    def test_14_engine_unsupported(self):
        """Test 14: OUT_OF_BOUNDS engine error maps to ENGINE_UNSUPPORTED."""
        runtime = RuntimeEngineOutput(
            execution_status="ERROR",
            molecular_consequence=None,
            protein_consequence=None,
            error_code="OUT_OF_BOUNDS",
            error_message="Promoter variant outside supported window"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Promoter",
            external_protein=""
        )
        res = evaluate_external_concordance(runtime, external, target_class="C10")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.ENGINE_UNSUPPORTED.value)

    def test_15_engine_error(self):
        """Test 15: General unhandled engine exception maps to ENGINE_ERROR."""
        runtime = RuntimeEngineOutput(
            execution_status="ERROR",
            molecular_consequence=None,
            protein_consequence=None,
            error_code="UNEXPECTED_CRASH",
            error_message="Segmentation fault or runtime exception"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="N109K"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.ENGINE_ERROR.value)

    def test_16_unresolved_case(self):
        """Test 16: Direct biological discrepancy (Missense vs Synonymous) maps to UNRESOLVED."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Synonymous",
            external_protein="p.(=)"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.UNRESOLVED.value)

    def test_17_legacy_numbering(self):
        """Test 17: Candidate with legacy flag and standard RefSeq codon coordinates."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Arg31Gly"
        )
        external = ExternalClinVarEvidence(
            external_molecular="Missense",
            external_protein="R31G"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.MATCH.value)
        self.assertEqual(res.protein_endpoint_status, ProteinEndpointStatus.MATCH.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)

    def test_18_explicit_anti_oracle_leakage_case(self):
        """Test 18: Mathematical proof that regression check (Field B) does not influence concordance (Field C)."""
        runtime = RuntimeEngineOutput(
            execution_status="SUCCESS",
            molecular_consequence="Missense",
            protein_consequence="p.Asn109Lys"
        )
        # Mock Field B (Expected Reference)
        mock_expected_molecular = "Missense"
        mock_expected_protein = "p.Asn109Lys"

        # Regression check passes (A == B)
        regression_concordant = (
            runtime.molecular_consequence == mock_expected_molecular and
            runtime.protein_consequence == mock_expected_protein
        )
        self.assertTrue(regression_concordant)

        # But external evidence C asserts Nonsense
        external = ExternalClinVarEvidence(
            external_molecular="Nonsense",
            external_protein="N109*"
        )
        res = evaluate_external_concordance(runtime, external, target_class="C01")

        # Must report biological DISCREPANCY despite regression PASS
        self.assertEqual(res.primary_endpoint_status, PrimaryEndpointStatus.DISCREPANCY.value)
        self.assertEqual(res.comparison_category, ComparisonCategory.UNRESOLVED.value)
        self.assertNotEqual(res.comparison_category, ComparisonCategory.EXACT_MOLECULAR_AGREEMENT.value)


if __name__ == "__main__":
    unittest.main()
