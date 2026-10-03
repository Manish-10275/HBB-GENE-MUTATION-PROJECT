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
* **OpenAI SDK** (AI Research Copilot)
* **Pytest** & **pytest-asyncio**

### Scientific Reference Target
* **Gene:** *HBB* (Homo sapiens hemoglobin subunit beta)
* **Accession:** `NM_000518.5` (RefSeq MANE Select, CCDS7753.1)
* **Protein ID:** `NP_000509.1` (147 amino acids)
* **Coding Sequence (CDS):** bases 51 .. 494 (444 bp, 147 codons + 1 stop)
* **Source:** National Center for Biotechnology Information (NCBI)

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
│   │   ├── reference.py      # NM_000518.5 reference manager & coordinates
│   │   ├── alignment.py      # Pairwise global alignment & coordinate blocks
│   │   ├── variants.py       # Deterministic variant calling & HGVS mapping
│   │   ├── consequences.py   # Codon translation & protein consequences
│   │   ├── evidence.py       # Structured EvidencePacket assembler
│   │   ├── clinvar.py        # NCBI ClinVar E-utilities client & fixtures
│   │   ├── pubmed.py         # NCBI PubMed E-utilities client & fixtures
│   │   ├── ai.py             # Evidence-grounded AI Research Copilot
│   │   └── reports.py        # Markdown & printable HTML report generator
│   ├── tests/
│   │   ├── test_pipeline.py  # Unit tests for bioinformatics engine
│   │   └── test_api.py       # API integration tests
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
│   │   ├── NM_000518.5.fasta # Controlled local reference sequence
│   │   └── NM_000518.5.json  # Reference metadata & feature coordinates
│   ├── examples/             # Curated FASTA benchmarks (WT, Sickle, Gln40Ter)
│   └── fixtures/             # Verified NCBI ClinVar & PubMed fixtures
├── docs/
│   ├── ARCHITECTURE.md       # Architectural specification
│   ├── SCIENTIFIC_METHOD.md  # Biological mathematics & HGVS nomenclature
│   ├── API.md                # REST API reference
│   └── DEMO.md               # End-to-end evaluation & presentation guide
├── .env.example
├── .gitignore
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
* `OPENAI_API_KEY`: *(Optional)* Enables live LLM research synthesis. If omitted, the copilot executes deterministic evidence summaries without crashing.
* `NCBI_EMAIL`: *(Optional)* Your email for NCBI E-utilities.
* `NCBI_API_KEY`: *(Optional)* Increases NCBI rate limit from 3 req/sec to 10 req/sec.

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

### Start the Backend Server
```bash
# In project root with active venv:
$env:PYTHONPATH="backend"
backend/venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API will be available at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.

### Start the Frontend Application
```bash
cd frontend
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Running the Test Suite

### Backend Tests
Execute the full pytest suite covering sequence validation, pairwise alignment, variant detection, codon translation, ClinVar/PubMed parsing, and API endpoints:
```bash
$env:PYTHONPATH="backend"
backend/venv/Scripts/python.exe -m pytest backend/tests -v
```

### Frontend Typecheck & Build
```bash
cd frontend
npx tsc --noEmit
npm run build
```

---

## Controlled Validation Case

The benchmark sequence `data/examples/validation_c118C_T.fasta` tests the complete analytical pipeline:
* **Mutation:** Single nucleotide substitution $c.118C>T$ in the *HBB* coding region.
* **Codon Transformation:** Codon 40 ($c.118..120$) `CAG` $\rightarrow$ `TAG`.
* **Amino Acid Shift:** Glutamine ($\text{Gln}$) $\rightarrow$ $\text{STOP (Ter)}$.
* **Consequence:** Nonsense mutation (`p.Gln40Ter`), historically known as Codon 39 nonsense in legacy hemoglobin literature.
* **ClinVar Evidence:** Classified as **Pathogenic** for $\beta$-thalassemia.

---

## Safety & Research Disclaimer

> **FOR RESEARCH AND EDUCATIONAL USE ONLY.**  
> This application does not provide medical diagnoses, treatment recommendations, or clinical interpretations. All computational findings represent in silico evaluations and must be confirmed via certified diagnostic sequencing and clinical laboratory workflows before any medical consideration.
