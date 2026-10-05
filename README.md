# HBB Mutation Analyzer

**Understand the sequence. Follow the evidence.**

A serious genomic research and educational workbench designed for deterministic sequence comparison, codon transformation analysis, external database evidence retrieval, and evidence-grounded AI research synthesis for the human *HBB* (hemoglobin subunit beta) gene.

---

## The Core Product Experience

```
DNA sequence
    ↓
Deterministic alignment
    ↓
Variant detection
    ↓
Codon consequence (CAG → TAG | Gln → STOP)
    ↓
External scientific evidence (NCBI ClinVar & PubMed)
    ↓
Evidence-grounded AI research synthesis
    ↓
```

> **Local-First Architecture Notice**:  
> This project is engineered to run **100% locally on your workstation**. It does **NOT** depend on Vercel, Render, Google Cloud, or any paid cloud deployment infrastructure. Anyone who clones or downloads this repository can run the entire system locally using standard Python and Node.js runtimes.

---

## Features

* **Deterministic Sequence Calling**: Pairwise global alignment against NCBI RefSeq standards with exact coordinate detection and HGVS 3'-shifting.
* **Dual-Reference Architecture**: Full support for both mRNA cDNA (`NM_000518.5`, 628 bp) and genomic gene locus (`NG_000007.3`, 1,608 bp) references.
* **Codon Consequence Engine**: Mathematical triplet extraction, canonical translation, and stop-gain / missense consequence labeling.
* **Intronic Splice Mutation Support**: Accurate genomic mapping for non-coding splice defects such as IVS1-5 (G>C) (`c.92+5G>C` / `g.70691G>C`).
* **Hardened ClinVar Integration**: Progressive multi-tier NCBI E-utilities queries with candidate scoring, alias harmonization, and false-positive rejection.
* **Curated PubMed Evidence**: Direct and disease-contextual literature retrieval with relevance classification.
* **Indian Thalassemia Screening Panel**: Automated zygosity-aware carrier and affected classification for the 4 most prevalent Indian mutations.
* **Evidence-Grounded Research Copilot**: AI synthesis via Groq (`openai/gpt-oss-120b`) strictly bounded by retrieved evidence, with authoritative deterministic offline fallback.
* **Interactive Gene Structure Map**: Visual representation of exons, introns, and mutation hotspots with interactive selection.
* **Clinical Research Reporting**: One-click generation of exportable Markdown and printable HTML analysis reports.

---

## Fundamental Scientific Principle

The architecture strictly decouples deterministic computation from generative synthesis:
* **The AI must NOT determine biological results.**
* The deterministic bioinformatics engine computes sequence normalization, pairwise alignment against reference `NM_000518.5`, variant coordinates, codon changes, and amino acid consequences.
* The external evidence layer queries authoritative databases (**NCBI ClinVar** and **NCBI PubMed**) via official E-utilities APIs.
* The AI Research Copilot synthesizes only the supplied scientific evidence packet. It never fabricates citations, PMIDs, records, or clinical claims.
* The interface visibly distinguishes **COMPUTED RESULT**, **DATABASE EVIDENCE**, and **AI SYNTHESIS**.

---

## Technology Stack

### Frontend
* **Next.js 14** (App Router)
* **React 18**
* **TypeScript 5**
* **Tailwind CSS** (Editorial scientific theme, monospace alignment grids)
* **Lucide React** (Icons)

### Backend
* **Python 3.14 / 3.11+**
* **FastAPI**
* **Pydantic v2** & **Pydantic Settings**
* **Biopython** (`Bio.Align.PairwiseAligner` for global pairwise alignment)
* **HTTPX** (Asynchronous HTTP client for NCBI E-utilities)
* **Groq SDK** (`groq` for evidence-grounded Research Copilot with `openai/gpt-oss-120b`)
* **Pytest** & **pytest-asyncio**

### Scientific Reference Targets (Dual-Reference Architecture)
* **cDNA Transcript Reference:** `NM_000518.5` (RefSeq MANE Select, CCDS7753.1)
  * Total Length: 628 bp mRNA transcript
  * Coding Sequence (CDS): bases 51 .. 494 (444 bp, 147 codons + 1 stop)
  * Protein ID: `NP_000509.1` (147 amino acids)
* **Genomic Locus Reference:** `NG_000007.3:70545..72152` (RefSeq Genomic Gene Locus)
  * Total Length: 1,608 bp genomic sequence containing 3 exons and 2 introns
  * Coordinates: Exon 1 (1..142), Intron 1 (143..272), Exon 2 (273..495), Intron 2 (496..1345), Exon 3 (1346..1608)
  * Used for intronic splice mutations such as IVS1-5 (G>C)
* **Source:** National Center for Biotechnology Information (NCBI RefSeq)

---

## Project Structure

```
HBB GENE MUTATION PROJECT/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI entrypoint & routing
│   │   ├── config.py         # Application settings
│   │   ├── models.py         # Pydantic request & response contracts
│   │   ├── sequence.py       # Sequence validation & normalization
│   │   ├── reference.py      # Dual-reference manager (NM_000518.5 + NG_000007.3)
│   │   ├── alignment.py      # Pairwise global alignment & coordinate blocks
│   │   ├── variants.py       # Deterministic variant calling & HGVS 3'-shifting
│   │   ├── consequences.py   # Codon translation & protein consequences
│   │   ├── evidence.py       # Structured EvidencePacket assembler
│   │   ├── clinvar.py        # NCBI ClinVar exact match client & fixtures
│   │   ├── pubmed.py         # NCBI PubMed E-utilities client & fixtures
│   │   ├── ai.py             # Groq Research Copilot & fallback engine
│   │   ├── simulator.py      # Educational mutation simulator & screening classifier
│   │   └── reports.py        # Markdown & printable HTML report generator
│   ├── tests/
│   │   ├── test_pipeline.py  # Unit tests for bioinformatics engine
│   │   ├── test_api.py       # API integration tests
│   │   └── test_indian_mutations_and_screening.py # Tests for simulator & panel
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx          # Main scientific research workspace
│   │   └── globals.css
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── SafetyBanner.tsx
│   │   ├── SequenceWorkspace.tsx
│   │   ├── HBBGeneStructureMap.tsx        # Interactive dual-track exon structure map
│   │   ├── ScreeningClassifierBanner.tsx  # Educational zygosity screening banner
│   │   ├── CodonVisualizer.tsx
│   │   ├── AlignmentViewer.tsx
│   │   ├── VariantsTable.tsx
│   │   ├── EvidenceWorkspace.tsx
│   │   ├── DirectVariantSearch.tsx
│   │   ├── ResearchCopilot.tsx
│   │   └── ReportModal.tsx
│   ├── lib/
│   │   ├── api.ts            # Typed backend client
│   │   └── types.ts          # TypeScript interfaces
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
├── data/
│   ├── reference/
│   │   ├── NM_000518.5.fasta # Controlled cDNA transcript reference (628 bp)
│   │   ├── NM_000518.5.json  # cDNA metadata & feature coordinates
│   │   ├── NG_000007.3.fasta # Controlled genomic gene locus reference (1,608 bp)
│   │   ├── NG_000007.3.json  # Genomic locus metadata & exon/intron coordinates
│   │   └── indian_mutations.json # Curated Indian thalassemia panel dataset
│   ├── examples/             # Curated FASTA benchmarks
│   └── fixtures/             # Verified NCBI ClinVar & PubMed fixtures
├── docs/
│   ├── ARCHITECTURE.md       # Architectural specification
│   ├── SCIENTIFIC_METHOD.md  # Biological mathematics & HGVS nomenclature
│   ├── API.md                # REST API reference
│   └── DEMO.md               # End-to-end evaluation & presentation guide
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

---

## Requirements

Ensure the following prerequisites are installed on your host system:
* **Python**: Version 3.11 or newer (Python 3.11 – 3.14 supported)
* **Node.js**: Version 18.x or 20.x LTS (with `npm`)
* **Operating System**: Windows 10/11, macOS, or Linux
* **Internet Connection**: Required for live NCBI E-utilities queries (offline fixtures provided as automatic fallback) and Groq API calls

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Manish-10275/HBB-GENE-MUTATION-PROJECT.git
cd HBB-GENE-MUTATION-PROJECT
```

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
# Windows:
copy .env.example .env

# Linux/macOS:
cp .env.example .env
```

Configuration variables explained:
* `GROQ_API_KEY`: *(Optional)* Groq API key for evidence-grounded Research Copilot synthesis using `openai/gpt-oss-120b`. If omitted, the application operates in 100% authoritative deterministic offline synthesis mode.
* `GROQ_MODEL`: Model identifier (defaults to `openai/gpt-oss-120b`).
* `NCBI_EMAIL`: *(Optional)* Contact email for NCBI E-utilities request headers.
* `NCBI_API_KEY`: *(Optional)* NCBI API key (increases NCBI rate limit from 3 to 10 req/sec).
* `API_BASE_URL`: Local FastAPI URL (default `http://localhost:8000`).
* `CORS_ORIGINS`: Allowed origins for API requests (default `["http://localhost:3000","http://127.0.0.1:3000"]`).

### 3. Backend Setup
```bash
# Create and activate Python virtual environment
python -m venv backend/venv

# Activate on Windows PowerShell:
backend\venv\Scripts\Activate.ps1
# Or on Windows Command Prompt:
backend\venv\Scripts\activate.bat
# Or on Linux/macOS:
source backend/venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 4. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

---

## Local Startup

### Simplest Recommended Startup Command
Start both the FastAPI backend (`http://localhost:8000`) and Next.js frontend (`http://localhost:3000`) with a single command:

* **Cross-Platform Python:**
  ```bash
  python run.py
  ```

* **Windows Batch (One-Click):**
  ```cmd
  run.bat
  ```

* **Windows PowerShell:**
  ```powershell
  .\run.ps1
  ```

* **To stop all services and free ports cleanly:**
  ```cmd
  stop.bat
  # or: python run.py --stop
  ```

**What the launcher handles automatically:**
1. Verifies local Python environment and installs missing packages if needed
2. Automatically copies `.env.example` to `.env` if `.env` does not exist
3. Cleans up any stale processes occupying ports 8000 or 3000
4. Streams color-coded logs from both services in a single terminal
5. Automatically opens `http://localhost:3000` in your default browser once the backend is healthy
6. Cleanly terminates both child processes on `Ctrl+C`

---

## Testing & Verification

Run the core verification commands:

```bash
# 1. Complete backend test suite (78 tests)
pytest -q

# 2. Automated release readiness audit (All 10 stages end-to-end)
python tools/release_audit.py

# 3. Controlled validation benchmark (c.118C>T / p.Gln40Ter)
python tools/benchmark_c118.py

# 4. Frontend type safety and production build
cd frontend
npm run type-check
npm run build
cd ..
```

---

## The c.118C>T Validation Case (Benchmark)

The primary benchmark case is `NM_000518.5:c.118C>T`:
* **cDNA Mutation**: Nucleotide 118 substitution `C` $\to$ `T` (mRNA position 168, codon 40 of 147 canonical codons).
* **Codon Consequence**: Codon 40 changes from `CAG` (encoding Glutamine, Gln) to `TAG` (canonical Amber stop codon).
* **Protein Consequence**: `p.Gln40Ter` (Nonsense / Stop-gain), creating a truncated 39-amino-acid peptide and leading to complete loss of $\beta$-globin synthesis ($\beta^0$-thalassemia).
* **Historical Literature Numbering**: Known historically as **CD39 C>T** or **Q39\*** because mature circulating $\beta$-globin was numbered after post-translational cleavage of the initiator methionine (Met1). The engine deterministically harmonizes both notations.
* **ClinVar Benchmark Record**: **VCV000015402** (Variation ID 15402), classified as **Pathogenic** with review status *criteria provided, multiple submitters, no conflicts*.

---

## Manual Reviewer Walkthrough (Demo Guide)

To evaluate the application locally as a reviewer:

1. **Launch Services**:
   Run `python run.py` (or `run.bat`). Wait until `http://localhost:3000` opens in your browser.
2. **Load Benchmark Case**:
   In the **Sequence Input & Screening Simulator** card, click the amber badge:
   `★ Benchmark c.118C>T`.
   Notice the sequence auto-populates with the verified mutant sequence and target is set to `NM_000518.5`.
3. **Execute Deterministic Analysis**:
   Click the dark **Analyze Sequence** button.
4. **Inspect Gene Map & Metrics**:
   Observe the top metrics strip showing 99.84% identity, 1 detected variant, and live NCBI hit counts.
   The **HBB Gene Structure Map** visually highlights Exon 2 and the codon 40 locus.
5. **Inspect Codon Visualizer**:
   Review the primary visual insight: Codon 40 `CAG (Gln)` $\to$ `TAG (Ter)` marked with a crimson **NONSENSE / STOP-GAIN** badge.
6. **Review External Scientific Evidence**:
   Open the **External Scientific Evidence** accordion:
   - ClinVar card shows **VCV000015402** classified as **EXACT VARIANT MATCH** (Score 100/100, Pathogenic).
   - PubMed literature displays verified peer-reviewed articles with direct relevance tags.
7. **Interact with AI Research Copilot**:
   Scroll to the **AI Research Copilot** panel.
   Type a research inquiry such as:
   *"Why does the CAG to TAG change cause premature termination?"*
   Verify the six-section structured response:
   - `DIRECT SCIENTIFIC ANSWER`
   - `A. COMPUTED FACTS`
   - `B. DATABASE EVIDENCE`
   - `C. ESTABLISHED BIOLOGICAL KNOWLEDGE`
   - `D. AI SYNTHESIS` (or `D. DETERMINISTIC SYNTHESIS` in fallback mode)
   - `EVIDENCE LIMITATIONS`
8. **Export Formal Report**:
   Click the **Export Report** button in the top navigation header.
   View the generated research report, copy markdown, or print as clinical research documentation.

---

## Role of AI & Provenance Guardrails

The AI Research Copilot exists exclusively as a **natural language synthesis and educational explanation layer**:
* **Deterministic Engine Is Authoritative**: In silico alignment, coordinate mapping, and codon translation are computed mathematically by the Python engine. The AI has zero role in determining whether a mutation exists.
* **NCBI Data Is Authoritative**: ClinVar classifications and PubMed citations are fetched directly from NCBI E-utilities. The AI is strictly forbidden from inventing PMIDs or database entries.
* **Dual Provenance Modes**:
  1. *Live Groq Mode*: When `GROQ_API_KEY` is present and active, Groq synthesizes the structured packet using `openai/gpt-oss-120b`.
  2. *Deterministic Fallback Mode*: If Groq is unconfigured, rate-limited, or unavailable, the application immediately falls back to a deterministic, rule-based synthesis.
* **Strict Anti-Hallucination Boundaries**:
  - Rejects answers citing non-existent PMIDs.
  - Rejects claims contradicting the authoritative ClinVar classification.
  - Clearly labels biological interpretations (such as nonsense-mediated decay) as unmeasured hypotheses.

---

## ClinVar Retrieval Methodology & Hardening

NCBI ClinVar retrieval uses a hardened, multi-stage pipeline designed to ensure true variants are never buried or misidentified:

1. **Progressive Query Strategy**:
   - **Primary Tier**: Specific HGVS cDNA string with gene qualification (e.g. `c.118C>T[Variant Name] AND HBB[Gene Name]`).
   - **Transcript Qualification**: Full transcript-qualified notation (e.g. `"NM_000518.5:c.118C>T"`).
   - **Genomic Translation**: Automatic conversion to RefSeq genomic coordinates (`NG_000007.3:g.70691G>C` for `c.92+5G>C`).
   - **Historical Alias Expansion**: Inclusion of historical literature names (e.g., `CD39 C>T`, `Q39*`, `codon 39 C->T`).

2. **Window Expansion (`retmax=50`)**:
   - NCBI ESearch default limits (`retmax=5` or `10`) historically caused true variants to be truncated when multiple related HBB submissions exist. The engine requests up to 50 records to evaluate candidate rankings comprehensively.

3. **Candidate Verification & Rejection**:
   - **Exact Variant Match (Score 95–100)**: Verified identity on cDNA coordinate, ref/alt alleles, and protein consequence.
   - **Compound Variant Rejection**: Explicitly rejects complex multi-variant records containing the target variant as a sub-component.
   - **Allele Mismatch Rejection**: Rejects entries sharing the coordinate but having different alternate alleles (e.g. `c.118C>A`).
   - **Related HBB Record (Score 30–60)**: Clearly demarcated if only contextual locus records exist.

---

## Troubleshooting

### 1. Port 8000 or 3000 is Already in Use
If another process is using port 8000 or 3000:
```cmd
# Stop all running services cleanly:
stop.bat
# Or using python:
python run.py --stop
```
The launcher will terminate any orphaned processes and free the ports.

### 2. Python is Not Found on Windows
If `python` is not recognized in your terminal, use `run.bat` directly. It automatically searches for the project's virtual environment at `backend\venv\Scripts\python.exe`.

### 3. Rate Limit Reached on Groq (HTTP 429)
If Groq returns a rate limit warning:
- The application **does not fail**. It automatically activates the authoritative **Deterministic Fallback Mode**.
- Section D of the copilot will be labeled `D. DETERMINISTIC SYNTHESIS`, preserving full scientific accuracy.

### 4. NCBI E-Utilities Connectivity Issues
If NCBI is slow or unreachable:
- Set `NCBI_API_KEY` in `.env` to raise rate limits from 3 to 10 requests/sec.
- If the internet is disconnected, the engine automatically falls back to verified offline fixtures (`data/fixtures/clinvar_fixtures.json` and `data/fixtures/pubmed_fixtures.json`).

### 5. Frontend Missing Dependencies
If `tsc` or `next` reports missing modules:
```bash
cd frontend
npm install
cd ..
```

---

## Scientific Limitations

* **In Silico Assessment Only**: All variant consequences, alignments, and screening classifications represent computational models based on NCBI reference standards (`NM_000518.5` and `NG_000007.3`).
* **Non-Experimental Transcript Stability**: Predictions of transcript degradation (such as Nonsense-Mediated mRNA Decay, NMD) are mechanistic hypotheses and have not been confirmed by experimental RNA stability assays for the patient sample.
* **Epistatic Modifiers**: Clinical severity in $\beta$-thalassemia is strongly influenced by secondary genetic modifiers (e.g., $\alpha$-globin gene duplications/deletions, *BCL11A* variants, *HBS1L-MYB* intergenic loci) not evaluated by this single-locus analyzer.
* **Complex Structural Variants**: Large genomic deletions (>1 kb) and complex structural rearrangements require chromosomal microarray or optical genome mapping rather than short-sequence alignment.

---

## Safety & Educational Use Disclaimer

> **FOR RESEARCH AND EDUCATIONAL USE ONLY.**  
> This software is designed strictly for bioinformatics research, computational benchmarking, and educational training. It does not provide medical diagnoses, treatment recommendations, or personalized healthcare guidance. All computational findings must be verified using certified clinical diagnostic procedures (e.g., Sanger sequencing, next-generation sequencing, and hemoglobin capillary electrophoresis) before any clinical application.

