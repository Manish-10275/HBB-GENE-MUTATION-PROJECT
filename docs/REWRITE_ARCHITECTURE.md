# REWRITE ARCHITECTURE SPECIFICATION
## Clean, Deterministic, and Scientifically Defensible Redesign of the HBB Gene Mutation Analyzer

**Document Version:** 2.1.0  
**Status:** ARCHITECTURAL SPECIFICATION & REWRITE BLUEPRINT (APPROVED WITH CORRECTIONS)  
**Design Philosophy:** Ponytail Methodology (Simplest working design, stdlib-first, deletion over addition, zero speculative abstraction, zero benchmark overfitting)  
**Author:** Computational Biology Architecture Team  

---

## A. CURRENT ARCHITECTURE AUDIT

An audit of the Phase 1, Phase 2A, and Phase 2B codebase reveals architectural erosion and technical debt accumulated across iterative milestone patches:

| Module / Path | Size | Primary Responsibility | Audit Findings & Architectural Flaws | Verdict |
| :--- | :---: | :--- | :--- | :---: |
| `backend/app/variants.py` | 37.3 KB | Variant calling, direct HGVS parsing, nomenclature | **Monolith & Benchmark Leakage.** Houses direct HGVS parsing, pairwise alignment scanning, coordinate math, and hardcoded alias tables. Contains explicit `elif` branches for `c.9del`, `c.92+1G>T`, `c.118C>T`, `c.20A>T`, `c.19G>A`, creating benchmark leakage. | **SPLIT & REWRITE** |
| `backend/app/consequences.py` | 10.9 KB | Codon translation, consequence evaluation | **Solid Biological Logic, Coupled Presentation.** Downstream PTC walking and standard genetic code table are deterministic and sound, but coupled to specific Pydantic model formatting and ad-hoc string returns. | **REWRITE & SIMPLIFY** |
| `backend/app/clinvar.py` | 23.7 KB | NCBI ClinVar retrieval & matching | **Benchmark Contamination & Illusion of Offline Mode.** Hardcodes alias mappings (`KNOWN_HBB_HISTORICAL_ALIASES` mapping `ivs-i-1` $\to$ `c.92+1G>T`). Makes live HTTP calls even when called with `--mode offline`. Contains only 7 dev fixtures; 0 test fixtures. | **SPLIT & REWRITE** |
| `backend/app/reference.py` | 7.8 KB | RefSeq sequence & coordinate loading | **Hidden Global State.** Manages `NM_000518.5` and `NG_000007.3` via a global singleton `reference_manager`. Loads unrelated `indian_mutations.json` within reference manager. | **SIMPLIFY & DECOUPLE** |
| `backend/app/models.py` | 7.7 KB | Pydantic data schemas | **Leaky Layer Boundaries.** Domain models, API request/response DTOs, and diagnostic structures are conflated into a single schema file with deeply nested optional fields. | **REWRITE & MODULARIZE** |
| `backend/app/ai.py` | 42.1 KB | Groq / LLM clinical copilot | **Severe Bloat (42KB).** Giant file with complex prompt generation, schema validation, multi-step retries, and markdown extraction. Must be strictly optional and non-authoritative. | **ISOLATE & DECOUPLE** |
| `backend/app/simulator.py` | 20.5 KB | Educational screening & sequence mutation | **Scope Creep in Core Engine.** Educational screening and clinical classification are coupled into the backend rather than living in an educational extension. | **SEPARATE FROM CORE** |
| `backend/app/pubmed.py` | 9.7 KB | PubMed E-utilities integration | **Over-Engineered Fallback.** 250 lines to query PubMed with complex fallback heuristics. | **SIMPLIFY** |
| `backend/app/alignment.py` | 4.2 KB | BioPython sequence alignment | **Clean but Coupled.** Performs pairwise alignment against `NM_000518.5`. Good candidate for stdlib/Biopython preservation. | **PRESERVE & ADAPT** |
| `backend/app/sequence.py` | 3.8 KB | FASTA parsing & nucleotide validation | **Functional.** Basic nucleotide IUPAC validation and FASTA normalization. | **PRESERVE & ADAPT** |
| `backend/app/reports.py` | 12.8 KB | Report generation (Markdown/HTML) | **Coupled Presentation.** Generates clinical reports; contains speculative clinical interpretation templates. | **SIMPLIFY** |
| `backend/app/main.py` | 17.4 KB | FastAPI routes, presets, orchestration | **Bloated Routes.** Endpoints contain procedural business logic, example sequence loading, and manual error aggregation. | **CLEAN ROUTING ONLY** |
| `frontend/` (Next.js 14) | ~150 KB | Next.js frontend UI | **Fragmented User Flow.** Separate tabs for "Sequence Workspace", "Direct Variant Search", and "Simulator". State is duplicated across components. | **STREAMLINE WORKFLOW** |

---

## B. PROBLEMS IN CURRENT IMPLEMENTATION

### 1. Benchmark Contamination (Overfitting to Test Cases)
The current codebase contains explicit hardcoded dictionaries that artificially boost benchmark scores:
- `backend/app/variants.py:211`: `aliases = ["c.9delT", "c.9del", "c.8delA", "c.8del"]` directly leaks frozen test variant `HBB-BM-006`.
- `backend/app/clinvar.py:49`: `"ivs-i-1": "c.92+1G>T"` and `variants.py:203`: `aliases = ["c.92+1G>T", "IVS-I-1 G>T", ...]` hardcode historical nomenclature for `HBB-BM-029`.
- `backend/app/main.py:195, 202`: Preset definitions hardcode `c.117_118insA` (`HBB-BM-027`) and `c.118del` (`HBB-BM-020`).

### 2. Fake Offline Mode & Untenable Network Dependency
- `run_benchmark.py --mode offline` passes `mode="offline"` to `evaluate_variant`, but `fetch_clinvar_records` ignores it and initiates live network requests via `httpx.AsyncClient`.
- `clinvar_fixtures.json` only contains 7 development variants. If network fails or is disconnected, all 13 test ClinVar queries fail.

### 3. Conflation of Scientific Rule Engine with Clinical Claims
- The current implementation blends deterministic sequence mathematics with speculative clinical risk classifications and treatment disclaimers.
- Clinical claims ("Pathogenic", "Carrier screening positive") are presented without rigorous population frequency context.

### 4. Excessive Complexity & Monolithic Design
- Monolithic files (`variants.py` at 37 KB, `simulator.py` at 20 KB) mixing parsing, regexes, coordinate arithmetic, and reporting.
- Conflating AI assistance with deterministic molecular interpretation.

---

## C. COMPONENTS TO PRESERVE CONCEPTUALLY

The following algorithms and scientific concepts represent verified, working bioinformatics logic and will be preserved:
1. **Downstream Frameshift PTC Walking (`consequences.py`):** The logic that translates an altered reading frame downstream until reaching the first in-frame termination codon (`TAA`, `TAG`, `TGA`) and computes canonical HGVS notation (e.g. `p.Gln40ArgfsTer21`).
2. **Canonical Exon/Intron Coordinate Translation (`reference.py`):** The exact physical genomic mapping of RefSeq `NM_000518.5` (Exons 1–3, CDS 51..494) and `NG_000007.3` (Intron 1: 130 bp, Intron 2: 850 bp).
3. **Deterministic IUPAC Sequence Alignment (`alignment.py` / `sequence.py`):** Global/local alignment with gap penalty scoring using BioPython.
4. **Three-Tier Evidence Classification Scheme:** Segregating Exact Matches (Tier 1), Gene-Related Matches (Tier 2), and General Locus Records (Tier 3).
5. **Strict Local-First Architecture:** The entire core pipeline must run without cloud credentials, API keys, or paid infrastructure.

---

## D. COMPONENTS TO REWRITE

1. **HGVS Pipeline (`core/hgvs.py`):** Clean, decoupled parsing pipeline with zero benchmark shortcuts:
   $$	ext{Raw Input} \longrightarrow 	ext{Syntax Parser} \longrightarrow 	ext{Normalized Variant} \longrightarrow 	ext{Reference Validation} \longrightarrow 	ext{Coordinate Mapping} \longrightarrow 	ext{Consequence Evaluation}$$
2. **Consequence Evaluator (`core/consequences.py`):** Pure functional engine taking a validated variant and reference transcript, returning structured `ConsequenceResult` (impact type, protein HGVS, affected codon). Operates from biological rules, not benchmark fixtures.
3. **Evidence Providers (`evidence/clinvar/`):**
   - Structurally separate providers: `OfflineClinVarProvider` (reading versioned local fixture DB with zero network capability) and `LiveClinVarProvider` (calling NCBI Entrez with rate-limiting and timeouts).
   - Zero hardcoded variant alias dictionaries.
4. **Data Models (`core/models.py`):** Clean, strongly-typed domain models and typed error taxonomy.
5. **FastAPI Routes (`api/`):** Thin controller layer delegating strictly to domain services.
6. **Frontend Workflow (`frontend/`):** Unified scientific workbench focusing strictly on input $\to$ mapping $\to$ consequence $\to$ evidence $\to$ provenance.

---

## E. COMPONENTS TO REMOVE (YAGNI PRUNING)

1. **REMOVE Hardcoded Alias Dictionaries:** Delete `KNOWN_HBB_HISTORICAL_ALIASES` in `clinvar.py` and `get_equivalent_nomenclature` in `variants.py`. Aliases must follow general HGVS normalization rules or external database indexing, never hardcoded variant strings.
2. **REMOVE In-Core Educational Simulator:** Decouple `simulator.py` from the core bioinformatics API. Educational simulation presets belong in a separate extension or demo script, not in core variant interpretation.
3. **REMOVE Duplicate Preset Files & Fixture Overlap:** Prune redundant example files and ensure fixtures only contain verified reference data.

---

## F. NEW ARCHITECTURE PRINCIPLES & STRICT DOMAIN BOUNDARIES

The rewritten system enforces strict domain separation:

```
backend/app/
├── core/                  # DETERMINISTIC SCIENTIFIC ENGINE (Zero network, zero AI)
│   ├── models.py          # Pure domain models and typed error taxonomy
│   ├── reference.py       # RefSeq transcript & genomic sequence loaders + coordinate mapping
│   ├── hgvs.py            # HGVS syntax parsing, normalization, reference validation
│   ├── consequences.py    # Codon translation, PTC downstream walking, splice consequences
│   └── alignment.py       # Sequence alignment & variant caller
├── evidence/              # EXTERNAL RETRIEVAL & RESEARCH LAYER
│   ├── clinvar_offline.py # Offline provider (Zero network, reads local versioned fixtures)
│   ├── clinvar_live.py    # Live NCBI Entrez provider (Rate-limited, timeout-protected)
│   ├── pubmed.py          # PubMed bibliographic retrieval
│   └── copilot.py         # Optional AI synthesis (non-authoritative, provenance-preserving)
└── api/                   # HTTP PRESENTATION & CONTROLLER
    ├── schemas.py         # Request and response DTOs
    └── routes.py          # FastAPI endpoint routers
```

### Strict Domain Invariants:
1. **No Circularity:** `core/` depends ONLY on Python stdlib and BioPython. It knows NOTHING about ClinVar, PubMed, AI, or HTTP APIs.
2. **Research Isolation:** `research/` is completely decoupled. Production code must NEVER import from `research/`. Production code must NEVER import benchmark manifests, test sets, or expected outputs.
3. **Historical Immutability:** Historical Phase 2B artifacts (`research/manifest/`, `research/results/`, `docs/PHASE_2B_SCIENTIFIC_INTEGRITY_AUDIT.md`) are immutable historical records. They will NOT be modified or overwritten.
4. **No Benchmark-Driven Coding:** Implementation logic must stem purely from biological rules and software requirements. Inspecting a benchmark test case to write a specific `if/elif` branch is strictly prohibited.

---

## G. STRICT HGVS PARSING PIPELINE

The HGVS processing pipeline is decomposed into discrete, single-responsibility phases:

```
[Raw User Input]
       │
       ▼
[Phase 1: HGVS Syntax Parser]
       │ Parses syntax strings (e.g. "c.118C>T", "c.92+1G>T", "c.9del", "c.27dup", "c.27_28insG")
       │ Emits SYNTAX_ERROR if grammar is malformed (e.g. non-IUPAC bases, inverted coordinates)
       ▼
[Phase 2: Normalized Variant Domain Object]
       │ Structured AST: c_pos, variant_type, ref_stated, alt_stated, etc.
       ▼
[Phase 3: Reference Sequence Validation]
       │ Verifies reference allele matches RefSeq NM_000518.5 (or NG_000007.3)
       │ Emits REFERENCE_MISMATCH if stated ref != actual reference base
       │ Emits OUT_OF_BOUNDS if position exceeds transcript or intron lengths
       ▼
[Phase 4: Coordinate Mapping]
       │ Computes exact CDS coordinate, relative mRNA position, exon/intron region, genomic offset
       ▼
[Phase 5: Consequence Evaluation]
       │ Translates codons, walks downstream PTC if frameshift, evaluates splice disruption
       │ Emits ConsequenceResult(hgvs_p, molecular_impact, codon_change)
```

The HGVS parser contains ZERO ClinVar logic, PubMed logic, UI logic, benchmark logic, or AI logic.

---

## H. TYPED DOMAIN ERROR TAXONOMY

Rather than relying on `None` or ad-hoc error strings, all failures in the core engine emit typed domain errors:

```python
# core/models.py
from enum import Enum

class AnalysisErrorCode(str, Enum):
    SYNTAX_ERROR = "SYNTAX_ERROR"                             # Malformed HGVS string, missing operators
    REFERENCE_MISMATCH = "REFERENCE_MISMATCH"                 # Query stated ref base != actual reference sequence
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"                           # Coordinate exceeds transcript or intron boundary
    INVALID_COORDINATE = "INVALID_COORDINATE"                 # Base zero (c.0), inverted range (c.129_126)
    UNSUPPORTED_VARIANT = "UNSUPPORTED_VARIANT"               # Complex structural breaks, multi-gene fusions
    AMBIGUOUS_VARIANT = "AMBIGUOUS_VARIANT"                   # Variant with undefined biological resolution
    EXTERNAL_SOURCE_UNAVAILABLE = "EXTERNAL_SOURCE_UNAVAILABLE" # Network down or offline fixture missing

@dataclass(frozen=True)
class AnalysisError:
    code: AnalysisErrorCode
    message: str
    details: Optional[Dict[str, Any]] = None
```

---

## I. DOMAIN MODELS

```python
# core/models.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

class VariantType(str, Enum):
    SUBSTITUTION = "substitution"
    DELETION = "deletion"
    INSERTION = "insertion"
    DUPLICATION = "duplication"
    SPLICE = "splice"
    REGULATORY_UTR = "regulatory_utr"

class MolecularImpact(str, Enum):
    SYNONYMOUS = "Synonymous"
    MISSENSE = "Missense"
    NONSENSE = "Nonsense"
    FRAMESHIFT = "Frameshift"
    IN_FRAME_INDEL = "In-frame Indel"
    SPLICE_DISRUPTION = "Splice Site Disruption"
    REGULATORY_5_UTR = "5' UTR Regulatory"
    REGULATORY_3_UTR = "3' UTR Regulatory"
    UNKNOWN = "Unknown"

@dataclass(frozen=True)
class NormalizedVariant:
    transcript_accession: str
    c_position: str
    variant_type: VariantType
    ref_allele: str
    alt_allele: str
    hgvs_c: str
    region: str
    mrna_position: Optional[int] = None
    genomic_accession: Optional[str] = None
    genomic_coordinate: Optional[int] = None

@dataclass(frozen=True)
class ConsequenceResult:
    hgvs_p: Optional[str]
    molecular_impact: MolecularImpact
    codon_change: Optional[str]
    ptc_coordinate: Optional[int] = None
    confidence: str = "Deterministic"

@dataclass(frozen=True)
class ClinVarHit:
    variation_id: str
    accession: str
    title: str
    clinical_significance: str
    review_status: str
    is_exact_match: bool
    evidence_tier: str
    retrieval_mode: str  # "offline_fixture" | "live_ncbi"
    source_url: str
```

---

## J. EVIDENCE PROVIDER ARCHITECTURE (STRUCTURALLY ISOLATED OFFLINE MODE)

To guarantee zero network requests in offline mode, separate classes are implemented:

```
                            ┌────────────────────────┐
                            │  ClinVarProviderBase   │
                            │  (Abstract Interface)  │
                            └───────────┬────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
       ┌─────────────────────────┐             ┌─────────────────────────┐
       │  OfflineClinVarProvider │             │   LiveClinVarProvider   │
       ├─────────────────────────┤             ├─────────────────────────┤
       │ Reads local JSON file   │             │ Uses httpx.AsyncClient  │
       │ ZERO network sockets    │             │ Calls NCBI E-utilities  │
       │ Deterministic lookup    │             │ Rate limits + timeout   │
       └─────────────────────────┘             └─────────────────────────┘
```

An `OfflineClinVarProvider` physically lacks network imports or HTTP client code, making accidental network leakage structurally impossible.

---

## K. AI RESEARCH COPILOT PRINCIPLES

1. **Strictly Optional:** The entire core pipeline functions identically whether an LLM API key is present or absent.
2. **Never Authoritative:** AI output is restricted to synthesizing already-retrieved evidence. It is strictly prohibited from computing coordinates, codons, or molecular consequences.
3. **Provenance Enforced:** Every AI-generated statement must cite retrieved evidence chunks.
4. **Deterministic Fallback:** If the external LLM API is unavailable, the copilot emits a structured, deterministic template summary without crashing.

---

## L. TESTING ARCHITECTURE

Tests are structured into four strictly decoupled directories:

```
backend/tests/
├── unit/           # GENERAL BEHAVIOR: Parsers, codon translation, coordinate arithmetic
│   ├── test_reference.py
│   ├── test_hgvs_parser.py
│   ├── test_consequences.py
│   └── test_errors.py
├── integration/    # LAYER BOUNDARIES: Service orchestration, offline provider isolation
│   ├── test_offline_clinvar.py
│   └── test_api_routes.py
├── scientific/     # INDEPENDENT BIOLOGY: Known general HBB biology (e.g. HbS, HbC, invariant splice)
│   └── test_established_biology.py
└── research/       # FROZEN BENCHMARKS: Historical Phase 2B evaluation (isolated from unit runs)
    └── test_historical_benchmark.py
```

---

## M. REWRITE ACCEPTANCE CRITERIA

The rewrite will be certified complete if and only if all the following criteria are satisfied:

- **A. No Benchmark-Specific Logic in Production:** Zero hardcoded benchmark variant strings (`c.9del`, `c.92+1G>T`, `c.118del`, etc.) exist in `backend/app/`.
- **B. Clean Dependency Direction:** Strict one-way dependencies (`api` $	o$ `evidence` $	o$ `core`). Core has zero external network/DB dependencies.
- **C. Deterministic Core Interpretation:** Molecular consequences follow strictly from genetic code and sequence logic.
- **D. True Offline Evidence Mode:** Offline mode executes with network disabled and makes zero HTTP requests.
- **E. Strong Unit and Integration Coverage:** Comprehensive test suite covering valid and invalid inputs across all variant classes.
- **F. Core Functionality Retained/Improved:** Full support for substitutions, indels, frameshifts, splice variants, and UTR variants.
- **G. Historical Phase 2B Artifacts Preserved:** No modification to historical research manifests or results.
- **H. Local-First Execution:** Runs fully locally without cloud accounts or paid APIs.
- **I. Static Verification Passes:** Type checking (`tsc`) and frontend production build succeed with 0 errors.
- **J. No Silent Guessing:** Ambiguous or malformed inputs emit explicit typed domain errors.
- **K. Architecture Documented:** Clear docstrings and structural guides throughout.
- **L. Independent Testability:** Core implementation is verified on general unit tests before evaluating any benchmark dataset.
