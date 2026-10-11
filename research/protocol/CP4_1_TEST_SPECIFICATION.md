# CP4.1 Benchmark Comparison Test Specification

**Document Status:** LOCKED GOVERNANCE SPECIFICATION  
**Stage:** Phase 2C — CP4.1  
**Scope:** Formal Verification Suite Requirements for CP4.2 Implementation  
**Lock Date:** 2026-10-08  

---

## 1. Overview

This document specifies the exact unit and integration test fixtures required to validate the corrected comparison engine during CP4.2 implementation. No benchmark execution may take place until all tests defined herein achieve 100% PASS without warnings or failures.

---

## 2. Mandatory Synthetic Test Cases

### Test Case 01: Critical Anti-Oracle Test 1 (External Disagreement Detection)
- **Objective:** Prove that the comparison engine detects biological disagreement with external evidence even when the engine agrees with its stored expected output ($A == B$).
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $B$ (Frozen Expected): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $C$ (External Evidence): `molecular = "Nonsense"`, `protein = "N109*"`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`DISCREPANCY`**
  - `secondary_protein_endpoint`: **`DISCREPANCY`**
  - `comparison_category`: **`UNRESOLVED`** (or `EXTERNAL_CONFLICT`)
  - `software_regression_check.regression_concordant`: **`True`**
- **Validation Assertion:** `comparison_category != "EXACT_MOLECULAR_AGREEMENT"` and `primary_endpoint_status == "DISCREPANCY"`.

---

### Test Case 02: Critical Anti-Oracle Test 2 (Expected Disagreement Independence)
- **Objective:** Prove that a divergence between runtime output and stored expected output ($A \neq B$) does **not** corrupt an agreement with external evidence ($A == C$).
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $B$ (Frozen Expected): `molecular = "Nonsense"`, `protein = "p.Asn109Ter"`
  - $C$ (External Evidence): `molecular = "Missense"`, `protein = "N109K"`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`MATCH`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
  - `software_regression_check.regression_concordant`: **`False`**
- **Validation Assertion:** `primary_endpoint_status == "MATCH"` despite `regression_concordant == False`.

---

### Test Case 03: Class C09 Splice Site Disruption Handling
- **Objective:** Verify that missing external protein strings for canonical splice variants do not cause false primary molecular failures or false exact protein matches.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Splice Site Disruption"`, `protein = "p.?"`
  - $B$ (Frozen Expected): `molecular = "Splice Site Disruption"`, `protein = "p.?"`
  - $C$ (External Evidence): `molecular = "Splice Site Disruption"`, `protein = ""`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`INCOMPLETE`**
  - `comparison_category`: **`EXTERNAL_ANNOTATION_INCOMPLETE`**
  - `software_regression_check.regression_concordant`: **`True`**
- **Validation Assertion:** Primary molecular endpoint is credited as `MATCH`, but category is correctly cataloged as `EXTERNAL_ANNOTATION_INCOMPLETE`.

---

### Test Case 04: Class C11 3' UTR Regulatory Variant Handling
- **Objective:** Verify that expected non-coding protein absence is recognized as concordant non-coding behavior rather than missing data.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "3' UTR Regulatory"`, `protein = None`
  - $B$ (Frozen Expected): `molecular = "3' UTR Regulatory"`, `protein = None`
  - $C$ (External Evidence): `molecular = "3' UTR Regulatory"`, `protein = ""`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`NOT_APPLICABLE`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
  - `software_regression_check.regression_concordant`: **`True`**
- **Validation Assertion:** Category is `EXACT_MOLECULAR_AGREEMENT` and protein endpoint is `NOT_APPLICABLE`.

---

### Test Case 05: Clinical Significance Conflict Isolation
- **Objective:** Verify that conflicting clinical pathogenicity assertions across submitters do not taint a valid molecular consequence match.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $C$ (External Evidence): `molecular = "Missense"`, `protein = "N109K"`
  - Clinical Submissions: `["Pathogenic", "Uncertain significance"]`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`MATCH`**
  - `clinical_significance_status`: **`CLINICAL_SIGNIFICANCE_CONFLICT`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
- **Validation Assertion:** Primary endpoint is `MATCH` despite `clinical_significance_status == "CLINICAL_SIGNIFICANCE_CONFLICT"`.

---

### Test Case 06: External Molecular Consequence Conflict
- **Objective:** Verify that when external repositories contain contradictory molecular consequence assertions, the comparison engine flags `EXTERNAL_CONFLICT` without using the engine or Field $B$ to arbitrate.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $B$ (Frozen Expected): `molecular = "Missense"`, `protein = "p.Asn109Lys"`
  - $C$ (External Evidence): Conflicting molecular annotations: `["Missense", "Nonsense"]`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`DISCREPANCY`**
  - `comparison_category`: **`EXTERNAL_CONFLICT`**
- **Validation Assertion:** Does not arbitrarily pick `Missense`. Returns `EXTERNAL_CONFLICT`.

---

### Test Case 07: Frameshift Truncated Protein Syntax
- **Objective:** Verify that truncated ClinVar frameshift notation is mapped to `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Frameshift"`, `protein = "p.Glu7ArgfsTer13"`
  - $C$ (External Evidence): `molecular = "Frameshift"`, `protein = "E7fs"`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`DISCREPANCY`**
  - `comparison_category`: **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`**
- **Validation Assertion:** Molecular endpoint is `MATCH`, protein is `DISCREPANCY`, category is `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`.

---

### Test Case 08: Synonymous Semantic Concordance
- **Objective:** Verify that transcript-level silent notation `p.(=)` and codon-level silent notation `p.Leu69=` are evaluated as semantic protein matches.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Synonymous"`, `protein = "p.(=)"`
  - $C$ (External Evidence): `molecular = "Synonymous"`, `protein = "p.Leu69="`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`MATCH`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
- **Validation Assertion:** Full match on both endpoints.

---

### Test Case 09: Legacy Numbering Preservation
- **Objective:** Verify that legacy candidates with standard RefSeq codon coordinates in ClinVar (e.g. `HBB-CP2-023`, `R31G`) match without requiring offset subtraction.
- **Inputs:**
  - $A$ (Runtime Engine): `molecular = "Missense"`, `protein = "p.Arg31Gly"`
  - $C$ (External Evidence): `molecular = "Missense"`, `protein = "R31G"`
  - `legacy_nomenclature_flag`: `True`
- **Expected Outputs:**
  - `primary_endpoint_status`: **`MATCH`**
  - `secondary_protein_endpoint`: **`MATCH`**
  - `comparison_category`: **`EXACT_MOLECULAR_AGREEMENT`**
- **Validation Assertion:** Codon 31 matches directly; legacy flag preserved in metadata notes.

---

## 3. Abstract Syntax Tree (AST) Static Leakage Test

An automated script `test_ast_anti_leakage.py` will inspect the source code of `phase2c_comparison_engine.py`:
- **Verification Rule:** Confirm zero occurrences of AST `Name` nodes matching:
  - `expected_molecular`
  - `expected_protein`
  - `exp_mol`
  - `exp_prot`
  - `deterministic_molecular_consequence`
  - `deterministic_protein_consequence`
- **Assertion:** Script raises an exception if any expected-field identifier appears in the comparison module.
