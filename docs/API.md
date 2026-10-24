# API Specification — HBB Mutation Analyzer

**Base URL:** `http://localhost:8000` (Backend default)  
**Interactive Swagger UI:** `http://localhost:8000/docs`  
**OpenAPI Specification:** `http://localhost:8000/openapi.json`

---

## 1. System Endpoints

### `GET /health`
Returns health status, active reference target, and backend engine details.

**Response `200 OK`:**
```json
{
  "status": "healthy",
  "service": "HBB Mutation Analyzer API",
  "version": "1.0.0",
  "reference_accession": "NM_000518.5",
  "reference_gene": "HBB",
  "reference_length_bp": 628,
  "cds_coordinates": "51..494",
  "groq_configured": true,
  "groq_model": "openai/gpt-oss-120b"
}
```

---

## 2. Genomic Data Endpoints

### `GET /reference`
Returns canonical sequence and feature annotation for the HBB reference transcript.

**Query Parameters:**
* `accession` *(string, optional, default: "NM_000518.5")*

**Response `200 OK`:**
```json
{
  "gene": "HBB",
  "organism": "Homo sapiens",
  "accession": "NM_000518.5",
  "molecule_type": "mRNA",
  "total_length": 628,
  "cds_start": 51,
  "cds_end": 494,
  "cds_length": 444,
  "protein_id": "NP_000509.1",
  "protein_length": 147,
  "sequence": "ACATTTGCTTCTGACACAACTGTG...",
  "cds_sequence": "ATGGTGCATCTGACTCCTGAGGAG...",
  "protein_sequence": "MVHLTPEEKSAVTALWGKVNVDEV...",
  "exons": [
    {"number": 1, "start": 1, "end": 142},
    {"number": 2, "start": 143, "end": 365},
    {"number": 3, "start": 366, "end": 628}
  ]
}
```

### `GET /reference/list`
Lists available reference sequences (`NM_000518.5` cDNA and `NG_000007.3` genomic locus) with metadata.

### `GET /mutations/indian`
Retrieves the verified four Indian thalassemia mutations panel with curated RefSeq coordinates, biological mechanisms, and ClinVar IDs.

### `GET /simulator/presets`
Returns curated mutation simulation presets for the Indian panel, sickle cell, and validation controls.

### `POST /simulator/generate`
Generates an in silico mutated HBB sequence for educational screening simulation.

**Request Body:**
```json
{
  "preset_id": "ivs1-5"
}
```

### `GET /examples`
Returns curated validation cases and benchmarks available for single-click loading.

---

## 3. Core Bioinformatics Endpoints

### `POST /analyze`
Normalizes, strictly validates, and aligns an input DNA sequence against the selected reference (`NM_000518.5` or `NG_000007.3`), computing codon transformations and querying external ClinVar and PubMed evidence.

**Request Body:**
```json
{
  "sequence": ">SAMPLE_HBB\nACATTTGCTTCTGACACAAC...",
  "reference_accession": "NM_000518.5",
  "zygosity": "heterozygous"
}
```

---

## 4. Evidence & AI Endpoints

### `GET /variant/search`
Investigates a specific variant directly using HGVS nomenclature (e.g. `c.118C>T` or `NM_000518.5:c.118C>T`).

### `POST /copilot`
Synthesizes research answers strictly grounded in the supplied `evidence_packet`. If `GROQ_API_KEY` is omitted, returns a deterministic summary without crashing.

### `POST /report`
Compiles the complete `evidence_packet` into a standardized Markdown report and a styled browser-printable HTML document.

---

## 5. Modular V2 API Endpoints

### `POST /api/v2/analyze/variant`
Analyzes a single sequence variant deterministically with optional ClinVar evidence retrieval. Accepts HGVS cDNA nomenclature (e.g. `c.118C>T`, `c.92_94dup`, `c.9_83del`, `c.442_444del`).

**Request Body (`VariantAnalysisRequest`):**
```json
{
  "query": "c.118C>T",
  "include_evidence": false
}
```

**Alternative GET Method (`GET /api/v2/analyze/variant`):**
* `query` (string, required): HGVS variant string (e.g. `c.118C>T`)
* `include_evidence` (boolean, optional, default: `false`): Whether to fetch ClinVar evidence

**Response `200 OK` (`VariantAnalysisResponse`):**
```json
{
  "input_query": "c.118C>T",
  "normalized_hgvs_c": "NM_000518.5:c.118C>T",
  "transcript_accession": "NM_000518.5",
  "c_position": "118",
  "variant_type": "substitution",
  "region": "exon2",
  "ref_allele": "C",
  "alt_allele": "T",
  "mrna_position": 168,
  "genomic_accession": "NG_000007.3",
  "genomic_coordinate": 70842,
  "hgvs_p": "p.Gln40Ter",
  "molecular_impact": "Nonsense",
  "codon_change": {
    "codon_number": 40,
    "c_start": 118,
    "c_end": 120,
    "ref_codon": "CAG",
    "sample_codon": "TAG",
    "ref_aa": "Gln",
    "sample_aa": "Ter",
    "is_stop_gain": true,
    "is_stop_loss": false,
    "is_synonymous": false
  },
  "ptc_coordinate": 40,
  "confidence": "Deterministic",
  "equivalent_nomenclature": [
    "c.118C>T",
    "CD39 C>T",
    "Q39*"
  ],
  "nomenclature_notes": "Codon 39 historically numbered from post-cleavage Val1.",
  "evidence_status": null,
  "clinvar_evidence": null,
  "discrepancies": []
}
```

**Validation Error Response (`400 Bad Request`):**
Returned on syntax errors, coordinate bounds failures, or reference mismatches.
```json
{
  "detail": {
    "error_code": "REFERENCE_MISMATCH",
    "message": "Reference base mismatch at c.118: expected 'C', query specified 'A'",
    "details": {
      "coordinate": "118",
      "expected_base": "C"
    }
  }
}
```

