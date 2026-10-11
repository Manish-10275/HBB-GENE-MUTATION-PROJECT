"""Zero-network guard test proving offline providers make no network requests."""

import socket
import pytest
from app.evidence.clinvar_offline import OfflineClinVarProvider
from app.evidence.models import EvidenceStatus
from app.evidence.pubmed_offline import OfflinePubMedProvider


def test_offline_providers_zero_network_guarantee(monkeypatch):
    """
    Guards that OfflineClinVarProvider and OfflinePubMedProvider execute
    with ZERO network calls by blocking all socket connect operations.
    """
    def forbidden_connect(*args, **kwargs):
        pytest.fail("Network call attempted during offline provider execution!")

    monkeypatch.setattr(socket.socket, "connect", forbidden_connect)

    # 1. Test Offline ClinVar with known variant
    clinvar = OfflineClinVarProvider()
    res1 = clinvar.search_variant("c.118C>T")
    assert res1.status == EvidenceStatus.FOUND

    # 2. Test Offline ClinVar with unknown variant
    res2 = clinvar.search_variant("c.999C>T")
    assert res2.status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE

    # 3. Test Offline PubMed with known query
    pubmed = OfflinePubMedProvider()
    p_res1 = pubmed.search_literature("c.118C>T")
    assert p_res1.status == EvidenceStatus.FOUND

    # 4. Test Offline PubMed with unknown query
    p_res2 = pubmed.search_literature("unknown_query_123")
    assert p_res2.status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE
