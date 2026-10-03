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
| • Global Alignment    | |   (E-utilities)         | |   Assembler             |
| • Variant Calling     | | • NCBI PubMed Client    | | • AI Research Copilot   |
| • Codon Analysis      | |   (E-utilities)         | |   (OpenAI GPT-4o-mini)  |
| • Protein Consequence | | • Verified Fallback     | | • Report Generator      |
| • NM_000518.5 Ref     | |   Fixtures              | |   (Markdown + HTML)     |
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
* **`reference.py`**: Manages canonical reference data for *Homo sapiens* hemoglobin subunit beta (`NM_000518.5`, CCDS7753.1). Maintains 1-based mRNA coordinates (1..628) and CDS coordinates (51..494, 444 bp).
* **`alignment.py`**: Performs deterministic pairwise global alignment (Needleman-Wunsch algorithm via `Bio.Align.PairwiseAligner`). Computes exact matches, mismatches, gaps, identity percentage, and alignment score, segmenting output into 60 bp monospace blocks with coordinate tracking.
* **`consequences.py`**: Employs NCBI Standard Genetic Code (Table 1) to determine codon triplet transformations, amino acid consequences, stop gain/loss events, and HGVS protein notation (e.g. `p.Gln40Ter`).
* **`variants.py`**: Scans alignment columns to call single nucleotide substitutions, insertions, and deletions, deterministically mapping them to standard HGVS cDNA nomenclature (e.g., `NM_000518.5:c.118C>T`).

### 2.2 External Evidence Layer
* **`clinvar.py`**: Asynchronously queries NCBI ClinVar via Entrez E-utilities (`esearch` + `esummary`). Extracts germline clinical significance (e.g. *Pathogenic*), review status, condition traits, and accession IDs.
* **`pubmed.py`**: Queries NCBI PubMed via Entrez E-utilities to retrieve peer-reviewed primary literature, capturing PMIDs, publication titles, journals, dates, and author lists.
* **Fault Tolerance & Fixtures**: In offline or rate-limited environments, verified fixtures stored under `data/fixtures/` ensure deterministic pipeline reliability, clearly identified with `(DEVELOPMENT FIXTURE)`.

### 2.3 Evidence Packet & AI Copilot Layer
* **`evidence.py`**: Assembles an immutable, inspectable `EvidencePacket` containing analysis metrics, detected variants, codon consequences, ClinVar records, PubMed citations, and standard scientific limitations.
* **`ai.py`**: Coordinates the AI Research Copilot. The system prompt strictly prohibits hallucinations, external claims, medical diagnoses, or ungrounded assertions. In environments without an `OPENAI_API_KEY`, a deterministic summary fallback is executed without crashing.
* **`reports.py`**: Synthesizes the full evidence packet into standard GitHub-flavored Markdown and browser-printable HTML styled for publication and review.

---

## 3. Data Integrity & Safety Principles

1. **Zero Generative Biology**: The LLM is never invoked to predict sequence alignments, locate variants, or compute protein translations.
2. **Provenance Distinction**:
   - **COMPUTED RESULT**: Tagged for facts derived purely from the in silico sequence engine.
   - **DATABASE EVIDENCE**: Tagged for records queried from NCBI ClinVar and PubMed.
   - **AI SYNTHESIS**: Tagged for narrative explanations generated by the copilot.
3. **Clinical Disclaimer**: Prominently presented across the header, footer, copilot, and generated reports stating the application is for research and education only and does not provide clinical diagnoses.
