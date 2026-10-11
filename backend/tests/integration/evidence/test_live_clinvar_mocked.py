"""Integration tests for LiveClinVarProvider using mocked HTTP transport."""

import pytest
import httpx

from app.core.hgvs import parse_hgvs
from app.evidence.clinvar_live import LiveClinVarProvider
from app.evidence.models import EvidenceStatus, RetrievalMode


@pytest.mark.asyncio
async def test_live_clinvar_successful_search_and_summary():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "esearch.fcgi" in url_str:
            return httpx.Response(
                200,
                json={"esearchresult": {"idlist": ["15402", "15488"]}},
            )
        elif "esummary.fcgi" in url_str:
            return httpx.Response(
                200,
                json={
                    "result": {
                        "15402": {
                            "title": "NM_000518.5(HBB):c.118C>T (p.Gln40Ter)",
                            "accession": "VCV000015402",
                            "germline_classification": {
                                "description": "Pathogenic",
                                "review_status": "criteria provided, multiple submitters, no conflicts",
                                "last_evaluated": "2024/04/18",
                                "trait_set": [{"trait_name": "Beta-thalassemia"}],
                            },
                        },
                        "15488": {
                            "title": "NM_000518.5(HBB):c.*111A>G",
                            "accession": "VCV000015488",
                            "germline_classification": {
                                "description": "Pathogenic",
                                "review_status": "reviewed by expert panel",
                                "trait_set": [{"trait_name": "Beta-thalassemia"}],
                            },
                        },
                    }
                },
            )
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)
    variant = parse_hgvs("c.118C>T")

    result = await provider.search_variant("c.118C>T", normalized_variant=variant)

    assert result.status == EvidenceStatus.FOUND
    assert result.primary_record is not None
    assert result.primary_record.variation_id == "15402"
    assert result.primary_record.accession == "VCV000015402"
    assert result.primary_record.clinical_significance == "Pathogenic"
    assert result.primary_record.is_exact_match is True
    assert result.provenance.mode == RetrievalMode.LIVE
    assert result.provenance.is_fixture is False


@pytest.mark.asyncio
async def test_live_clinvar_network_failure_no_silent_fallback():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused by remote host")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)

    result = await provider.search_variant("c.118C>T")

    # MUST report NETWORK_UNAVAILABLE, never silently fall back to offline fixture!
    assert result.status == EvidenceStatus.NETWORK_UNAVAILABLE
    assert result.primary_record is None
    assert len(result.records) == 0
    assert result.provenance.mode == RetrievalMode.LIVE
    assert result.provenance.is_fixture is False


@pytest.mark.asyncio
async def test_live_clinvar_timeout_handling():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("Read timed out")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)

    result = await provider.search_variant("c.118C>T")

    assert result.status == EvidenceStatus.TIMEOUT
    assert result.primary_record is None


@pytest.mark.asyncio
async def test_live_clinvar_rate_limited():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="Too Many Requests")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)

    result = await provider.search_variant("c.118C>T")

    assert result.status == EvidenceStatus.RATE_LIMITED
    assert result.primary_record is None


@pytest.mark.asyncio
async def test_live_clinvar_server_error():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="Internal Server Error")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)

    result = await provider.search_variant("c.118C>T")

    assert result.status == EvidenceStatus.PROVIDER_ERROR
    assert result.primary_record is None


@pytest.mark.asyncio
async def test_live_clinvar_not_found():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"esearchresult": {"idlist": []}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LiveClinVarProvider(client=client)

    result = await provider.search_variant("c.999C>T")

    assert result.status == EvidenceStatus.NOT_FOUND
    assert result.primary_record is None
    assert len(result.records) == 0
