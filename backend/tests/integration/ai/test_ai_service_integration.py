"""Integration tests for AI Copilot service orchestration and v2 API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_ai_service, get_variant_service
from app.main import app
from app.services.ai_service import AiCopilotService
from app.services.variant_service import VariantService

client = TestClient(app)


@pytest.mark.asyncio
async def test_ai_copilot_service_orchestration_flow():
    """Verifies that AiCopilotService correctly consumes the output of VariantService."""
    var_service = get_variant_service()
    ai_service = get_ai_service()

    # Step 1: Deterministic variant analysis
    analysis_result = await var_service.analyze_variant("c.118C>T", include_evidence=True)
    assert analysis_result.consequence.hgvs_p == "p.Gln40Ter"
    assert analysis_result.consequence.molecular_impact.value == "Nonsense"

    # Step 2: AI synthesis grounded strictly on analysis_result
    copilot_res = await ai_service.synthesize_variant_analysis(
        analysis_result=analysis_result,
        question="What is the consequence of this mutation?",
        include_literature=False,
    )

    assert copilot_res.status in ("success", "no_key", "error")
    assert "p.Gln40Ter" in copilot_res.answer
    assert "c.118C>T" in copilot_res.answer
    assert "DIRECT SCIENTIFIC ANSWER" in copilot_res.provenance_sections
    assert "A. COMPUTED FACTS" in copilot_res.provenance_sections



def test_v2_api_copilot_synthesize_endpoint_success():
    """Verifies that POST /api/v2/copilot/synthesize returns 200 with grounded synthesis."""
    payload = {
        "query": "c.118C>T",
        "question": "Why does this variant cause premature termination?",
        "include_evidence": True,
        "include_literature": False,
    }
    resp = client.post("/api/v2/copilot/synthesize", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert "answer" in data
    assert "p.Gln40Ter" in data["answer"]
    assert "c.118C>T" in data["answer"]
    assert "provenance_sections" in data
    assert "DIRECT SCIENTIFIC ANSWER" in data["provenance_sections"]
    assert "A. COMPUTED FACTS" in data["provenance_sections"]
    assert data["fallback"] in (True, False)
    assert data["provenance_label"] in ("Deterministic synthesis", "Live Groq synthesis")


def test_v2_api_copilot_synthesize_endpoint_fallback_when_no_key(monkeypatch):
    """Verifies that endpoint falls back gracefully to deterministic synthesis when no key."""
    monkeypatch.setattr("app.config.settings.GROQ_API_KEY", "")
    payload = {
        "query": "c.118C>T",
        "question": "Explain consequences.",
    }
    resp = client.post("/api/v2/copilot/synthesize", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["fallback"] is True
    assert data["provenance_label"] == "Deterministic synthesis"


def test_v2_api_copilot_synthesize_endpoint_invalid_syntax():
    """Verifies that POST /api/v2/copilot/synthesize rejects malformed queries with 400."""
    payload = {
        "query": "invalid_mutation_syntax",

        "question": "What does this do?",
    }
    resp = client.post("/api/v2/copilot/synthesize", json=payload)
    assert resp.status_code == 400
    data = resp.json()
    assert "detail" in data
