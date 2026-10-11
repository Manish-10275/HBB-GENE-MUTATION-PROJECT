# CP4 Implementation and Verification Checklist

**Document Status:** DESIGN CHECKLIST ONLY  
**Stage:** Phase 2C — CP4  
**Purpose:** Pre-Execution Governance and Verification Checklist for Corrected Comparison Pipeline  

---

## 1. File Immutability Constraints

Before any CP4 implementation work begins, verify that all frozen assets remain unmodified:

| File Path | Constraint | Verification Method | Status |
|---|---|---|:---:|
| `backend/app/*` (all production code) | **STRICTLY IMMUTABLE** | `git diff --exit-code backend/app/` | **LOCKED** |
| `research/manifest/phase2c_primary.json` | **STRICTLY IMMUTABLE** | SHA256 matches `39eb60de...` | **LOCKED** |
| `research/manifest/phase2c_primary.sha256` | **STRICTLY IMMUTABLE** | Content matches `39eb60de...` | **LOCKED** |
| `research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | **STRICTLY IMMUTABLE** | `git diff --exit-code research/protocol/PHASE2C_BENCHMARK_PROTOCOL.md` | **LOCKED** |
| `research/manifest/frozen_test.json` (Phase 2B) | **STRICTLY IMMUTABLE** | SHA256 matches `2f6b8842...` | **LOCKED** |
| `research/manifest/frozen_test.sha256` (Phase 2B) | **STRICTLY IMMUTABLE** | Content matches `2f6b8842...` | **LOCKED** |

---

## 2. Permitted Files for CP4 Implementation

The following files are authorized for creation or modification during CP4 implementation:

| File Path | Action Permitted | Rationale |
|---|---|---|
| `research/protocol/CP4_BENCHMARK_COMPARISON_CORRECTION_DESIGN.md` | Create / Maintain | Primary architectural specification |
| `research/protocol/CP4_COMPARISON_MAPPING.md` | Create / Maintain | Normalization and mapping rules |
| `research/protocol/CP4_IMPLEMENTATION_CHECKLIST.md` | Create / Maintain | Audit and verification checklist |
| `research/curation/phase2c_comparison_engine.py` | Create (New Module) | Dedicated, isolated external comparison & normalization engine |
| `research/curation/test_phase2c_comparison_engine.py` | Create (New Module) | Unit test suite verifying all 18 test matrix conditions |
| `research/curation/run_phase2c_benchmark.py` | Refactor (Execution Script) | Update to use isolated comparison engine while preserving dataset freeze |

---

## 3. Anti-Oracle Leakage Verification Checklist

To mathematically guarantee that internal expected values ($B$) cannot influence external biological concordance ($A \text{ vs } C$):

- [ ] **Check 1: Function Signature Isolation**  
  The external comparison function (`evaluate_external_concordance`) MUST accept ONLY:
  ```python
  evaluate_external_concordance(
      runtime_molecular: Optional[str],
      runtime_protein: Optional[str],
      runtime_status: str,
      runtime_error: Optional[str],
      external_molecular: Optional[str],
      external_protein: Optional[str],
      candidate_class: str
  ) -> ExternalConcordanceResult
  ```
  `expected_molecular` and `expected_protein` MUST NOT be passed into this function.

- [ ] **Check 2: AST Static Analysis Audit**  
  Run Python Abstract Syntax Tree (AST) inspection script verifying that inside `phase2c_comparison_engine.py`:
  - No reference to `expected_molecular` or `exp_mol` exists.
  - No reference to `expected_protein` or `exp_prot` exists.
  - No reference to `deterministic_molecular_consequence` exists.
  - No reference to `deterministic_protein_consequence` exists.

- [ ] **Check 3: Synthetic Divergence Test**  
  Execute unit test with intentionally divergent inputs:
  - Runtime Engine: `A_mol = "Missense"`, `A_prot = "p.Asn109Lys"`
  - Stored Expected: `B_mol = "Missense"`, `B_prot = "p.Asn109Lys"`
  - External Evidence: `C_mol = "Nonsense"`, `C_prot = "p.Asn109Ter"`
  - **Pass Requirement:** Output category MUST NOT be `EXACT_MOLECULAR_AGREEMENT`. Must report `UNRESOLVED` or `EXTERNAL_CONFLICT`, with `primary_endpoint_status = "DISCREPANCY"`.

---

## 4. Test Matrix Verification Checklist

Before executing any benchmark run, all 18 test cases in the CP4 Test Matrix must achieve `100% PASS`:

- [ ] Case 01: Exact Missense Agreement (`p.Asn109Lys` vs `N109K`) $\rightarrow$ `EXACT_MOLECULAR_AGREEMENT`, `MATCH`
- [ ] Case 02: Exact Nonsense Agreement (`p.Gln128Ter` vs `Q128*`) $\rightarrow$ `EXACT_MOLECULAR_AGREEMENT`, `MATCH`
- [ ] Case 03: Synonymous Semantic Agreement (`p.(=)` vs `p.Leu69=`) $\rightarrow$ `EXACT_MOLECULAR_AGREEMENT`, `MATCH`
- [ ] Case 04: Frameshift Truncated Notation (`p.Glu7ArgfsTer13` vs `E7fs`) $\rightarrow$ `MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`, `MATCH` (mol), `DISCREPANCY` (prot)
- [ ] Case 05: Class Mismatch (`Missense` vs `Nonsense`) $\rightarrow$ `UNRESOLVED`, `DISCREPANCY`
- [ ] Case 06: Missing External Protein in Splice (`p.?` vs `""`) $\rightarrow$ `EXTERNAL_ANNOTATION_INCOMPLETE`, `DISCREPANCY`
- [ ] Case 07: Missing External Protein in 3' UTR (`None` vs `""`) $\rightarrow$ Handled under Non-Coding Protocol Rule
- [ ] Case 08: Missing External Molecular Annotation (`Missense` vs `""`) $\rightarrow$ `EXTERNAL_ANNOTATION_INCOMPLETE`, `DISCREPANCY`
- [ ] Case 09: External Conflict (Conflicting Submissions) $\rightarrow$ `EXTERNAL_CONFLICT`, `DISCREPANCY`
- [ ] Case 10: Reference Nucleotide Mismatch (`INVALID_REF`) $\rightarrow$ `REFERENCE_MISMATCH`, `DISCREPANCY`
- [ ] Case 11: HGVS Ambiguity (`INVALID_SYNTAX`) $\rightarrow$ `HGVS_AMBIGUITY`, `DISCREPANCY`
- [ ] Case 12: Engine Unsupported Scope (`OUT_OF_BOUNDS`) $\rightarrow$ `ENGINE_UNSUPPORTED`, `DISCREPANCY`
- [ ] Case 13: Runtime Exception / Unhandled Crash $\rightarrow$ `ENGINE_ERROR`, `DISCREPANCY`
- [ ] Case 14: Protein 1-Letter vs 3-Letter Full Range $\rightarrow$ Verified across all 20 amino acids
- [ ] Case 15: Stop Notation Equivalences (`Ter`, `*`, `X`) $\rightarrow$ All resolve to canonical termination
- [ ] Case 16: Legacy Numbering Candidate Consistency $\rightarrow$ Standard RefSeq coordinates preserved
- [ ] Case 17: Independent Regression Check ($A == B$ while $A \neq C$) $\rightarrow$ Regression `PASS`, External `DISCREPANCY`
- [ ] Case 18: Critical Anti-Oracle Test ($A=\text{Mis}, B=\text{Mis}, C=\text{Non}$) $\rightarrow$ `DISCREPANCY`

---

## 5. Post-Implementation Acceptance Protocol

Only after:
1. All unit tests pass,
2. AST static analysis confirms zero oracle leakage,
3. All 10 protocol categories are demonstrated reachable,
may CP4 proceed to CP4.1 (Corrected Benchmark Execution).
