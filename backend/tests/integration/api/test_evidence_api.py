"""Integration tests for evidence and health diagnostics endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_analyze_with_offline_evidence():
    resp = client.post(
        "/api/v2/analyze/variant",
        json={"query": "c.118C>T", "include_evidence": True},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["hgvs_p"] == "p.Gln40Ter"
    assert data["evidence_status"] == "FOUND"
    assert data["clinvar_evidence"] is not None
    assert data["clinvar_evidence"]["primary_record"]["variation_id"] == "15402"
    assert data["clinvar_evidence"]["primary_record"]["clinical_significance"] == "Pathogenic"
    assert data["clinvar_evidence"]["provenance"]["mode"] == "offline"


def test_api_clinvar_evidence_endpoint_found():
    resp = client.get("/api/v2/evidence/clinvar?query=c.118C%3ET")
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "FOUND"
    assert len(data["records"]) > 0
    assert data["primary_record"]["variation_id"] == "15402"
    assert data["provenance"]["mode"] == "offline"


def test_api_clinvar_evidence_endpoint_unavailable():
    resp = client.get("/api/v2/evidence/clinvar?query=c.999C%3ET")
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "OFFLINE_DATA_UNAVAILABLE"
    assert data["primary_record"] is None
    assert data["error_message"] is not None


def test_api_pubmed_evidence_endpoint_found():
    resp = client.get("/api/v2/evidence/pubmed?query=c.118C%3ET")
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "FOUND"
    assert len(data["articles"]) > 0
    assert data["articles"][0]["pmid"] != ""


def test_api_pubmed_evidence_endpoint_unavailable():
    resp = client.get("/api/v2/evidence/pubmed?query=non_existent_mutation_999")
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "OFFLINE_DATA_UNAVAILABLE"
    assert len(data["articles"]) == 0


def test_api_v2_health_diagnostics():
    resp = client.get("/api/v2/health")
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "healthy"
    assert data["reference_availability"]["NM_000518.5"] is True
    assert data["reference_availability"]["NG_000007.3"] is True
    assert data["evidence_provider_mode"] == "offline"
    assert data["fixture_availability"]["clinvar_fixtures.json"] is True
    assert data["fixture_availability"]["pubmed_fixtures.json"] is True
