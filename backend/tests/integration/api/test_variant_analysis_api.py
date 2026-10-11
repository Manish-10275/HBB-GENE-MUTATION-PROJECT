"""Integration tests for the v2 variant analysis API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_analyze_missense_snv():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.20A>T"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["normalized_hgvs_c"] == "NM_000518.5:c.20A>T"
    assert data["hgvs_p"] == "p.Glu7Val"
    assert data["molecular_impact"] == "Missense"
    assert data["variant_type"] == "substitution"
    assert data["region"] == "Exon 1"
    assert data["codon_change"]["ref_aa"] == "Glu"
    assert data["codon_change"]["sample_aa"] == "Val"


def test_api_analyze_nonsense_snv():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.118C>T"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["normalized_hgvs_c"] == "NM_000518.5:c.118C>T"
    assert data["hgvs_p"] == "p.Gln40Ter"
    assert data["molecular_impact"] == "Nonsense"
    assert data["ptc_coordinate"] == 40
    assert data["codon_change"]["is_stop_gain"] is True


def test_api_analyze_synonymous_snv():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.9T>C"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["molecular_impact"] == "Synonymous"
    assert data["hgvs_p"] == "p.(=)"
    assert data["codon_change"]["is_synonymous"] is True


def test_api_analyze_frameshift_deletion():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.126_129del"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["normalized_hgvs_c"] == "NM_000518.5:c.126_129del"
    assert data["hgvs_p"] == "p.Phe42LeufsTer19"
    assert data["molecular_impact"] == "Frameshift"
    assert data["ptc_coordinate"] == 60
    assert data["ref_allele"] == "CTTT"
    assert data["alt_allele"] == "-"


def test_api_analyze_single_deletion():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.9del"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["hgvs_p"] == "p.Leu4Ter"
    assert data["molecular_impact"] == "Frameshift"
    assert data["ptc_coordinate"] == 4


def test_api_analyze_duplication():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.27dup"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["hgvs_p"] == "p.Ser10ValfsTer14"
    assert data["molecular_impact"] == "Frameshift"
    assert data["variant_type"] == "duplication"


def test_api_analyze_insertion():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.27_28insG"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["hgvs_p"] == "p.Ser10ValfsTer14"
    assert data["molecular_impact"] == "Frameshift"
    assert data["variant_type"] == "insertion"


def test_api_analyze_in_frame_deletion():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.127_129del"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["molecular_impact"] == "In-frame Indel"
    assert "del" in data["hgvs_p"]


def test_api_analyze_splice_variant():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.92+5G>C"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["normalized_hgvs_c"] == "NM_000518.5:c.92+5G>C"
    assert data["molecular_impact"] == "Splice Site Disruption"
    assert data["hgvs_p"] == "p.?"
    assert data["region"] == "Intron 1"
    assert data["genomic_accession"] == "NG_000007.3"
    assert data["genomic_coordinate"] == 70691


def test_api_analyze_utr_variants():
    # 5' UTR
    resp5 = client.post("/api/v2/analyze/variant", json={"query": "c.-50A>G"})
    assert resp5.status_code == 200
    data5 = resp5.json()
    assert data5["molecular_impact"] == "5' UTR Regulatory"
    assert data5["hgvs_p"] is None
    assert data5["region"] == "5' UTR"

    # 3' UTR
    resp3 = client.post("/api/v2/analyze/variant", json={"query": "c.*10C>T"})
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["molecular_impact"] == "3' UTR Regulatory"
    assert data3["hgvs_p"] is None
    assert data3["region"] == "3' UTR"


def test_api_get_endpoint():
    resp = client.get("/api/v2/analyze/variant?query=c.118C%3ET")
    assert resp.status_code == 200
    data = resp.json()
    assert data["hgvs_p"] == "p.Gln40Ter"


def test_api_error_reference_mismatch():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.118A>T"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error_code"] == "REFERENCE_MISMATCH"
    assert "Reference base mismatch" in detail["message"]


def test_api_error_invalid_coordinate():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.0C>T"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error_code"] == "INVALID_COORDINATE"


def test_api_error_out_of_bounds():
    resp = client.post("/api/v2/analyze/variant", json={"query": "c.999C>T"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error_code"] == "OUT_OF_BOUNDS"


def test_api_error_syntax_error():
    resp = client.post("/api/v2/analyze/variant", json={"query": "not_an_hgvs_string"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error_code"] == "SYNTAX_ERROR"


def test_api_error_unsupported_variant():
    resp = client.post("/api/v2/analyze/variant", json={"query": "NM_999999.1:c.100A>G"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error_code"] == "UNSUPPORTED_VARIANT"
