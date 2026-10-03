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
  "openai_configured": false
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

### `GET /examples`
Returns curated validation cases and benchmarks available for single-click loading.

---

## 3. Core Bioinformatics Endpoints

### `POST /analyze`
Normalizes, strictly validates, and aligns an input DNA sequence against NM_000518.5, computing codon transformations and querying external ClinVar and PubMed evidence.

**Request Body:**
```json
{
  "sequence": ">SAMPLE_HBB\nACATTTGCTTCTGACACAAC...",
  "reference_accession": "NM_000518.5"
}
```

**Response `200 OK`:**
```json
{
  "success": true,
  "summary": {
    "reference_accession": "NM_000518.5",
    "reference_length_bp": 628,
    "cds_coordinates": "51..494",
    "sample_length_bp": 628,
    "sequence_identity_pct": 99.84,
    "alignment_score": 1253.0,
    "detected_variants_count": 1
  },
  "alignment": {
    "ref_length": 628,
    "query_length": 628,
    "matches": 627,
    "mismatches": 1,
    "gaps": 0,
    "identity_percentage": 99.84,
    "alignment_score": 1253.0,
    "blocks": [
      {
        "block_index": 1,
        "ref_start": 1,
        "ref_end": 60,
        "query_start": 1,
        "query_end": 60,
        "ref_seq": "ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATC",
        "query_seq": "ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATC",
        "match_line": "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
      }
    ]
  },
  "variants": [
    {
      "id": "var_sub_168_C_T",
      "variant_type": "substitution",
      "ref_position_mrna": 168,
      "c_position": "118",
      "ref_allele": "C",
      "alt_allele": "T",
      "hgvs_c": "NM_000518.5:c.118C>T",
      "hgvs_p": "p.Gln40Ter",
      "codon_change": {
        "codon_number": 40,
        "c_start": 118,
        "c_end": 120,
        "ref_codon": "CAG",
        "sample_codon": "TAG",
        "ref_aa": "Gln",
        "sample_aa": "Ter",
        "ref_aa_single": "Q",
        "sample_aa_single": "*",
        "consequence": "Nonsense (p.Gln40Ter)",
        "is_stop_gain": true,
        "is_stop_loss": false,
        "is_synonymous": false
      },
      "functional_impact": "Nonsense",
      "confidence": "Deterministic"
    }
  ],
  "evidence_packet": { ... }
}
```

---

## 4. Evidence & AI Endpoints

### `GET /variant/search` (or `POST /variant/search`)
Investigates a specific variant directly using HGVS nomenclature (e.g. `c.118C>T` or `NM_000518.5:c.118C>T`).

### `POST /copilot`
Synthesizes research answers strictly grounded in the supplied `evidence_packet`. If `OPENAI_API_KEY` is omitted, returns a deterministic summary without crashing.

### `POST /report`
Compiles the complete `evidence_packet` into a standardized Markdown report and a styled browser-printable HTML document.
