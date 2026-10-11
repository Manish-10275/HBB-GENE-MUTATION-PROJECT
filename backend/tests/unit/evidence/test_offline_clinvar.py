"""Unit tests for OfflineClinVarProvider."""

from app.core.hgvs import parse_hgvs
from app.evidence.clinvar_offline import OfflineClinVarProvider
from app.evidence.models import EvidenceStatus, RetrievalMode


def test_offline_clinvar_retrieval_success():
    provider = OfflineClinVarProvider()
    result = provider.search_variant("c.118C>T")

    assert result.status == EvidenceStatus.FOUND
    assert result.primary_record is not None
    assert result.primary_record.variation_id == "15402"
    assert result.primary_record.accession == "VCV000015402"
    assert result.primary_record.clinical_significance == "Pathogenic"
    assert result.primary_record.is_exact_match is True

    # Provenance audit
    assert result.provenance is not None
    assert result.provenance.provider == "OfflineClinVarProvider"
    assert result.provenance.mode == RetrievalMode.OFFLINE
    assert result.provenance.is_fixture is True
    assert result.provenance.retrieval_status == EvidenceStatus.FOUND


def test_offline_clinvar_with_normalized_variant():
    provider = OfflineClinVarProvider()
    variant = parse_hgvs("c.20A>T")
    result = provider.search_variant("c.20A>T", normalized_variant=variant)

    assert result.status == EvidenceStatus.FOUND
    assert result.primary_record is not None
    assert result.primary_record.variation_id == "15333"
    assert "Hb SS disease" in result.primary_record.conditions or "Beta-thalassemia HBB/LCRB" in result.primary_record.conditions
    assert len(result.records) >= 1


def test_offline_clinvar_candidate_ranking():
    provider = OfflineClinVarProvider()
    result = provider.search_variant("c.118C>T")

    assert len(result.records) > 1
    # First record must be the exact match
    assert result.records[0].is_exact_match is True
    assert result.records[0].variation_id == "15402"
    # Secondary record is related
    assert result.records[1].is_exact_match is False


def test_offline_clinvar_missing_fixture_returns_explicit_unavailable():
    provider = OfflineClinVarProvider()
    result = provider.search_variant("c.999C>T")

    assert result.status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE
    assert result.primary_record is None
    assert len(result.records) == 0
    assert result.error_message is not None
    assert "offline mode" in result.error_message.lower()

    # Provenance records the unavailability explicitly
    assert result.provenance is not None
    assert result.provenance.retrieval_status == EvidenceStatus.OFFLINE_DATA_UNAVAILABLE
    assert result.provenance.mode == RetrievalMode.OFFLINE
    assert result.provenance.is_fixture is True
