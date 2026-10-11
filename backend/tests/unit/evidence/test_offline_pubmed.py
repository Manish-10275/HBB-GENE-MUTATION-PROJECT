"""Unit tests for OfflinePubMedProvider."""

from app.evidence.models import EvidenceStatus, RetrievalMode
from app.evidence.pubmed_offline import OfflinePubMedProvider


def test_offline_pubmed_retrieval_success():
    provider = OfflinePubMedProvider()
    result = provider.search_literature("c.118C>T")

    assert result.status == EvidenceStatus.FOUND
    assert len(result.articles) > 0
    first = result.articles[0]
    assert first.pmid != ""
    assert first.title != ""
    assert len(first.authors) > 0

    # Provenance audit
    assert result.provenance is not None
    assert result.provenance.provider == "OfflinePubMedProvider"
    assert result.provenance.mode == RetrievalMode.OFFLINE
    assert result.provenance.is_fixture is True


def test_offline_pubmed_missing_query():
    provider = OfflinePubMedProvider()
    result = provider.search_literature("non_existent_mutation_999")

    assert result.status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE
    assert len(result.articles) == 0
    assert result.error_message is not None
    assert result.provenance.retrieval_status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE
