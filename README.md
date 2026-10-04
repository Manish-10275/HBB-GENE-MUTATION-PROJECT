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
Exportable research report
```

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

## Installation & Setup

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key configuration parameters:
* `GROQ_API_KEY`: *(Optional)* Groq API key for evidence-grounded natural language copilot synthesis using `openai/gpt-oss-120b`. If omitted, the copilot executes in deterministic offline fallback mode with zero hallucination.
* `GROQ_MODEL`: *(Optional)* Model name (defaults to `openai/gpt-oss-120b`).
* `NCBI_EMAIL`: *(Optional)* Email address for NCBI E-utilities identification.
* `NCBI_API_KEY`: *(Optional)* NCBI API key (increases rate limit from 3 to 10 req/sec).

### 2. Backend Setup
```bash
# Create and activate Python virtual environment
python -m venv backend/venv

# Windows PowerShell:
backend/venv/Scripts/Activate.ps1
# Linux/macOS:
source backend/venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

---

## Running the Application

### Option A: One-Click / Single Command (Recommended)

You can launch both the FastAPI backend and Next.js frontend together with a single script:

* **Windows Batch (Double-click or terminal):**
  ```cmd
  run.bat
  ```
  *(or double-click `run.bat` in Windows File Explorer)*

* **PowerShell:**
  ```powershell
  .\run.ps1
  ```

* **Python (Cross-platform):**
  ```bash
  python run.py
  ```

* **To stop all running services cleanly:**
  ```cmd
  stop.bat
  ```

**Features included in the launcher:**
- Automatically checks/copies `.env` from `.env.example` if missing
- Automatically uses the virtual environment at `backend\venv`
- Automatically cleans up any orphaned processes holding ports 8000 or 3000
- Displays color-tagged live logs for both services in a single unified window
- Automatically opens `http://localhost:3000` in your default browser once the backend is healthy
- Cleanly terminates both services when you press `Ctrl+C`

Optional flags:
- `--separate` : Launch backend and frontend in separate command windows (Windows)
- `--backend-only` : Start only the backend API server
- `--frontend-only` : Start only the Next.js frontend
- `--no-browser` : Do not automatically open the browser
- `--stop` : Stop running servers and free ports 8000 and 3000

---

### Option B: Manual Execution (Separate Terminals)

#### 1. Start the Backend Server
```bash
# In project root with active venv:
$env:PYTHONPATH="backend"
backend/venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API will be available at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.

#### 2. Start the Frontend Application
```bash
cd frontend
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Automated Release Readiness & Test Suite

### 1. Single-Command Release Readiness Audit (Recommended)
Executes the full automated release pipeline (ClinVar hardening audit, complete 78-test backend suite, 18-point doctor diagnostics, frontend typecheck, production build, scientific consistency checks, evidence provenance checks, and repository cleanliness):

* **Windows Command Prompt / Batch:**
  ```cmd
  run_release_audit.bat
  ```
* **PowerShell:**
  ```powershell
  .\run_release_audit.ps1
  ```
* **Python Launcher:**
  ```bash
  python run.py --release-audit
  ```
* **Direct Python Execution:**
  ```bash
  python tools/release_audit.py
  ```

Outputs human-readable report `reports/RELEASE_READINESS_REPORT.md` and machine-readable `reports/release_readiness_report.json`.

### 2. Complete Backend Test Suite (78 Tests)
```bash
backend/venv/Scripts/python.exe -m pytest backend/tests -v
```

### 3. Dedicated ClinVar Hardening Audit (9 Tests)
```bash
backend/venv/Scripts/python.exe -m pytest backend/tests/test_clinvar_retrieval_hardening.py -v
```

### 4. System Diagnostics (18 Subsystem Checks)
```bash
backend/venv/Scripts/python.exe tools/doctor.py
```

### 5. Frontend TypeScript Check & Production Build
```bash
cd frontend
npm run type-check
npm run build
```
```

---

## Seven Authoritatively Verified Benchmark Mutations

The application includes seven curated and scientifically verified benchmark mutations:

| Mutation | Coordinate Type | HGVS Nomenclature | Biological Consequence | ClinVar ID | Clinical Phenotype |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **c.118C>T** | Transcript `NM_000518.5` | `c.118C>T`<br>`p.Gln40Ter` | Nonsense mutation at codon 40 (`CAG` $\to$ `TAG`) | **15402** | $\beta^0$ Thalassemia |
| **c.20A>T** | Transcript `NM_000518.5` | `c.20A>T`<br>`p.Glu7Val` | Missense sickle cell substitution at codon 7 (`GAG` $\to$ `GTG`) | **15333** | Sickle Cell Trait / Disease |
| **c.19G>A** | Transcript `NM_000518.5` | `c.19G>A`<br>`p.Glu7Lys` | Missense Hemoglobin C substitution at codon 7 (`GAG` $\to$ `AAG`) | **15126** | Hemoglobin C Trait / Disease |
| **IVS1-5 (G>C)** | Genomic `NG_000007.3` | `c.92+5G>C`<br>`g.70691G>C` | Intron 1 +5 donor splice site defect | **15447** | $\beta^+$ Thalassemia |
| **Cd41/42 (-TCTT)** | Transcript `NM_000518.5` | `c.126_129del`<br>`p.Phe42fs` | 4-bp frameshift deletion with HGVS 3'-shifting | **15417** | $\beta^0$ Thalassemia |
| **Cd8/9 (+G)** | Transcript `NM_000518.5` | `c.27dup`<br>`p.Ser10fs` | Exon 1 single-G duplication causing reading frameshift | **36308** | $\beta^0$ Thalassemia |
| **Cd30 (G>C)** | Transcript `NM_000518.5` | `c.93G>C`<br>`p.Arg31Ser` | Exon 1 terminal nucleotide / splice junction defect | **869321** | $\beta^0$ / Severe $\beta^+$ |

---

## Safety & Research Disclaimer

> **FOR RESEARCH AND EDUCATIONAL USE ONLY.**  
> This application does not provide medical diagnoses, treatment recommendations, or clinical interpretations. All computational findings represent in silico evaluations and must be confirmed via certified diagnostic sequencing, HPLC hemoglobin chromatography, and clinical laboratory workflows before any medical consideration.

