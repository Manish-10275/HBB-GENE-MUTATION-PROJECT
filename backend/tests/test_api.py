"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.reference import reference_manager

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["reference_accession"] == "NM_000518.5"
    assert data["reference_gene"] == "HBB"


def test_reference_endpoint():
    response = client.get("/reference")
    assert response.status_code == 200
    data = response.json()
    assert data["accession"] == "NM_000518.5"
    assert data["cds_start"] == 51
    assert data["cds_end"] == 494
    assert len(data["sequence"]) == 628


def test_examples_endpoint():
    response = client.get("/examples")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 4
    val_cases = [item for item in items if item.get("is_validation_case")]
    assert len(val_cases) >= 1
    assert "c.118C>T" in val_cases[0]["title"]


def test_analyze_endpoint_validation_case():
    ref = reference_manager.get_reference("NM_000518.5")
    # Mutate c.118 (index 167)
    mut_seq = ref.sequence[:167] + "T" + ref.sequence[168:]

    response = client.post("/analyze", json={"sequence": mut_seq})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["variants"]) == 1

    var = data["variants"][0]
    assert var["hgvs_c"] == "NM_000518.5:c.118C>T"
    assert var["hgvs_p"] == "p.Gln40Ter"
    assert var["functional_impact"] == "Nonsense"
    assert var["codon_change"]["ref_codon"] == "CAG"
    assert var["codon_change"]["sample_codon"] == "TAG"
    assert var["codon_change"]["ref_aa"] == "Gln"
    assert var["codon_change"]["sample_aa"] == "Ter"

    # Evidence packet present
    packet = data["evidence_packet"]
    assert packet is not None
    assert "HBB-EXP-" in packet["analysis_id"]


def test_analyze_endpoint_invalid_sequence():
    response = client.post("/analyze", json={"sequence": "ACGTUGAT"})
    assert response.status_code == 400
    data = response.json()
    assert "validation failed" in data["detail"]["message"].lower()


def test_variant_search_endpoint():
    response = client.get("/variant/search?query=c.118C>T")
    assert response.status_code == 200
    data = response.json()
    assert data["standardized_hgvs_c"] == "NM_000518.5:c.118C>T"
    assert "clinvar_records" in data
    assert "pubmed_records" in data


def test_copilot_endpoint_no_key_fallback():
    # Test that copilot doesn't crash without OpenAI API key, but provides grounded response
    ref = reference_manager.get_reference("NM_000518.5")
    mut_seq = ref.sequence[:167] + "T" + ref.sequence[168:]
    an_res = client.post("/analyze", json={"sequence": mut_seq}).json()
    packet = an_res["evidence_packet"]

    payload = {
        "question": "What is the codon and protein consequence of this variant?",
        "evidence_packet": packet,
        "conversation_history": []
    }
    response = client.post("/copilot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "c.118C>T" in data["answer"]
    assert "Gln" in data["answer"] or "Ter" in data["answer"] or "p.Gln40Ter" in data["answer"]
    assert len(data["evidence_used"]) >= 1


def test_report_endpoint():
    ref = reference_manager.get_reference("NM_000518.5")
    mut_seq = ref.sequence[:167] + "T" + ref.sequence[168:]
    an_res = client.post("/analyze", json={"sequence": mut_seq}).json()
    packet = an_res["evidence_packet"]

    response = client.post("/report", json={"evidence_packet": packet, "copilot_summary": "Test synthesis summary."})
    assert response.status_code == 200
    data = response.json()
    assert "markdown_content" in data
    assert "html_content" in data
    assert "HBB Genomic Variant Analysis Report" in data["title"]
    assert "c.118C>T" in data["markdown_content"]
    assert "p.Gln40Ter" in data["markdown_content"]


def test_cors_preflight_localhost():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_preflight_disallowed_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "https://unauthorized-domain.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") is None


def test_cors_frontend_origin_configuration(monkeypatch):
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.config import Settings

    custom_settings = Settings(FRONTEND_ORIGIN="https://hbb-mutation-analyzer.netlify.app")
    assert "https://hbb-mutation-analyzer.netlify.app" in custom_settings.effective_cors_origins
    assert "*" not in custom_settings.effective_cors_origins

    test_app = FastAPI()
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=custom_settings.effective_cors_origins,
        allow_origin_regex=custom_settings.CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    test_app.get("/health")(lambda: {"status": "ok"})
    test_client = TestClient(test_app)

    # Allowed production Netlify origin
    resp = test_client.options(
        "/health",
        headers={
            "Origin": "https://hbb-mutation-analyzer.netlify.app",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "https://hbb-mutation-analyzer.netlify.app"

    # Localhost continues to work
    resp_local = test_client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp_local.status_code == 200
    assert resp_local.headers.get("access-control-allow-origin") == "http://localhost:3000"

    # Arbitrary unauthorized origin is blocked
    resp_bad = test_client.options(
        "/health",
        headers={
            "Origin": "https://malicious-site.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp_bad.headers.get("access-control-allow-origin") is None


def test_cors_wildcard_rejection():
    from app.config import Settings
    s = Settings(CORS_ORIGINS="*")
    assert "*" not in s.effective_cors_origins
    s_list = Settings(CORS_ORIGINS=["*"])
    assert "*" not in s_list.effective_cors_origins


