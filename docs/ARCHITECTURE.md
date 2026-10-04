# System Architecture — HBB Mutation Analyzer

**Understand the sequence. Follow the evidence.**

---

## 1. Architectural Philosophy

The **HBB Mutation Analyzer** is designed around a fundamental scientific principle:
> **The AI must NOT determine biological results.**
> The deterministic bioinformatics engine computes all sequence comparisons, codon changes, and protein consequences. External scientific databases provide curated clinical annotations. The AI layer is strictly an evidence-grounded synthesizer that only reasons over and explains facts present in the assembled scientific evidence packet.

```
+-------------------------------------------------------------------------------+
|                             USER INTERACTION LAYER                            |
|             (Next.js 14, React 18, TypeScript, Tailwind CSS)                  |
+---------------------------------------+---------------------------------------+
                                        |
                   HTTP / REST (Pydantic Typed Contracts)
                                        |
+---------------------------------------v---------------------------------------+
|                       FASTAPI APPLICATION CORE (Python)                       |
|   /analyze  |  /variant/search  |  /copilot  |  /report  |  /health  |  /examples |
+-------------------+-------------------+-------------------+-------------------+
                    |                   |                   |
                    v                   v                   v
+-----------------------+ +-------------------------+ +-------------------------+
|  DETERMINISTIC ENGINE | |     EVIDENCE LAYER      | |     SYNTHESIS LAYER     |
|                       | |                         | |                         |
| • Normalization       | | • NCBI ClinVar Client   | | • Evidence Packet       |
| • Global Alignment    | |   (Exact match + retmax)| |   Assembler             |
| • Variant Calling     | | • NCBI PubMed Client    | | • AI Research Copilot   |
| • HGVS 3'-Shifting    | |   (E-utilities)         | |   (Groq LLM)            |
| • Dual References     | | • Verified Fallback     | | • Educational Simulator |
| • (cDNA + Genomic)    | |   Fixtures              | | • Report Generator      |
+-----------------------+ +-------------------------+ +-------------------------+
            |                               |                           |
            +-------------------------------+---------------------------+
                                            |
                                            v
                        +---------------------------------------+
                        |      STRUCTURED EVIDENCE PACKET       |
                        | (Immutable context provided to AI)    |
                        +---------------------------------------+
```

---

## 2. Component Boundaries & Responsibilities

### 2.1 Deterministic Bioinformatics Layer (`backend/app/`)
* **`sequence.py`**: Validates DNA alphabets strictly (`A`, `C`, `G`, `T`), strips FASTA formatting and whitespace, flags RNA (`U`) or non-canonical characters, and computes GC percentages.
* **`reference.py`**: Manages dual-reference data: canonical cDNA transcript (`NM_000518.5`, 628 bp) and genomic gene locus (`NG_000007.3:70545..72152`, 1,608 bp with 3 exons and 2 introns).
* **`alignment.py`**: Performs deterministic pairwise global alignment (Needleman-Wunsch algorithm via `Bio.Align.PairwiseAligner`). Computes exact matches, mismatches, gaps, identity percentage, and alignment score, segmenting output into 60 bp monospace blocks with coordinate tracking.
* **`consequences.py`**: Employs NCBI Standard Genetic Code (Table 1) to determine codon triplet transformations, amino acid consequences, stop gain/loss events, and HGVS protein notation (e.g. `p.Gln40Ter`).
* **`variants.py`**: Scans alignment columns to call single nucleotide substitutions, insertions, duplications, and deletions with standard HGVS 3'-shifting (e.g., `NM_000518.5:c.126_129del`, `c.27dup`).
* **`simulator.py`**: Simulates in silico mutations (the 4 Indian thalassemia panel mutations, sickle cell, HbC, and controls) and executes rule-based zygosity screening classification.

### 2.2 External Evidence Layer
* **`clinvar.py`**: Asynchronously queries NCBI ClinVar via Entrez E-utilities using a progressive search strategy (`[Variant Name]` + `HBB[Gene Name]`, quoted transcript HGVS, genomic translation, and `retmax=50` window expansion). Enforces deterministic post-retrieval verification to disqualify compound heterozygotes and separate exact variant evidence from related or general HBB records.
* **`pubmed.py`**: Queries NCBI PubMed via Entrez E-utilities to retrieve peer-reviewed primary literature, capturing PMIDs, publication titles, journals, dates, and author lists.
* **Fault Tolerance & Fixtures**: In offline or rate-limited environments, verified fixtures stored under `data/fixtures/` ensure deterministic pipeline reliability, clearly identified with `(DEVELOPMENT FIXTURE)`.

### 2.3 Evidence Packet & AI Copilot Layer
* **`evidence.py`**: Assembles an immutable, inspectable `EvidencePacket` containing analysis metrics, detected variants, codon consequences, ClinVar records, PubMed citations, and standard scientific limitations.
* **`ai.py`**: Coordinates the AI Research Copilot powered by Groq (`openai/gpt-oss-120b`). The system prompt strictly prohibits hallucinations, external claims, medical diagnoses, or ungrounded assertions. In environments without an active key or during rate limits, an authoritative deterministic summary fallback is executed without crashing.
* **`reports.py`**: Synthesizes the full evidence packet into standard GitHub-flavored Markdown and browser-printable HTML styled for publication and review.

---

## 3. Automated Release Readiness Architecture (`tools/release_audit.py`)

A single, reproducible release readiness audit command (`python tools/release_audit.py` or `python run.py --release-audit`):
1. **ClinVar Hardening Audit**: Runs 9/9 dedicated tests in `backend/tests/test_clinvar_retrieval_hardening.py`.
2. **Complete Backend Test Suite**: Runs all 78 tests across the test suite (`backend/tests/`).
3. **Doctor System Diagnostics**: Executes 18/18 checks in `tools/doctor.py`.
4. **Frontend TypeScript Check**: Executes `tsc --noEmit` across the Next.js frontend.
5. **Frontend Production Build**: Compiles production Next.js artifacts via `next build`.
6. **Scientific Consistency Checks**: Verifies codon mutations, consequences, and screening classifications in silico.
7. **Evidence Provenance & Grounding Boundaries**: Validates strict separation of facts, database citations, and AI narrative.
8. **Repository Cleanliness & Secret Protection**: Ensures zero leaked credentials and no lingering scratch files.
9. **Report Generation**: Emits `reports/release_readiness_report.json` and `reports/RELEASE_READINESS_REPORT.md`.
10. **Documentation Synchronization**: Syncs verified test and pipeline metrics across documentation.

---

## 4. Data Integrity & Safety Principles

1. **Zero Generative Biology**: The LLM is never invoked to predict sequence alignments, locate variants, or compute protein translations.
2. **Provenance Distinction**:
   - **COMPUTED FACTS**: Derived purely from the in silico sequence engine.
   - **DATABASE EVIDENCE**: Queried from NCBI ClinVar and PubMed.
   - **ESTABLISHED BIOLOGICAL KNOWLEDGE**: Universal genetic code and translation mechanics.
   - **AI SYNTHESIS / DETERMINISTIC SYNTHESIS**: Strictly grounded explanations.
   - **EVIDENCE LIMITATIONS**: Explicit scope boundaries.
3. **Clinical Disclaimer**: Prominently presented across the header, footer, copilot, and generated reports stating the application is for research and education only and does not provide clinical diagnoses.
