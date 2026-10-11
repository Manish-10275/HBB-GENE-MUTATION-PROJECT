"""Integration tests for LivePubMedProvider using mocked HTTP transport."""

import pytest
import httpx

from app.evidence.models import EvidenceStatus, RetrievalMode
from app.evidence.pubmed_live import LivePubMedProvider


@pytest.mark.asyncio
async def test_live_pubmed_successful_search_and_summary():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "esearch.fcgi" in url_str:
            return httpx.Response(
                200,
                json={"esearchresult": {"idlist": ["41255956"]}},
            )
        elif "esummary.fcgi" in url_str:
            return httpx.Response(
                200,
                json={
                    "result": {
                        "41255956": {
                            "title": "The Masked Thalassemia: CD39 C>T",
                            "source": "Appl Clin Genet",
                            "pubdate": "2025",
                            "authors": [{"name": "Chetta M"}],
                        }
                    }
                },
            )
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LivePubMedProvider(client=client)

    result = await provider.search_literature("c.118C>T")

    assert result.status == EvidenceStatus.FOUND
    assert len(result.articles) == 1
    assert result.articles[0].pmid == "41255956"
    assert result.articles[0].title == "The Masked Thalassemia: CD39 C>T"
    assert result.provenance.mode == RetrievalMode.LIVE
    assert result.provenance.is_fixture is False


@pytest.mark.asyncio
async def test_live_pubmed_timeout_handling():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("Read timed out")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LivePubMedProvider(client=client)

    result = await provider.search_literature("c.118C>T")

    assert result.status == EvidenceStatus.TIMEOUT
    assert len(result.articles) == 0


@pytest.mark.asyncio
async def test_live_pubmed_rate_limited():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="Too Many Requests")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LivePubMedProvider(client=client)

    result = await provider.search_literature("c.118C>T")

    assert result.status == EvidenceStatus.RATE_LIMITED
    assert len(result.articles) == 0


@pytest.mark.asyncio
async def test_live_pubmed_network_error_no_silent_fallback():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Network unreachable")

    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    provider = LivePubMedProvider(client=client)

    result = await provider.search_literature("c.118C>T")

    assert result.status == EvidenceStatus.NETWORK_UNAVAILABLE
    assert len(result.articles) == 0
    assert result.provenance.mode == RetrievalMode.LIVE
    assert result.provenance.is_fixture is False
