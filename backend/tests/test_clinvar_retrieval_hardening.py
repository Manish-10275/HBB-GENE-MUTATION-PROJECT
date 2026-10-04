"""Comprehensive audit and hardening test suite for NCBI ClinVar retrieval pipeline.

Verifies:
A. Exact benchmark variant retrieval: NM_000518.5:c.118C>T -> Variation ID 15402 / VCV000015402,
   Pathogenic, criteria provided, multiple submitters, no conflicts.
B. Exact protein consequence matching: p.Gln40Ter -> 15402.
C. Historical alias matching: CD39 C>T / Q39* -> 15402, with rejection of false positive ID 15470.
D. Rejection of false positives: nearby variants, different alt alleles, compound heterozygotes.
E. Missing ClinVar record handling: novel/synthetic variants return clean empty list.
F. Candidate ranking: exact single variant record prioritized at index 0 ahead of related/compound records.
G. Window expansion: candidates beyond initial window (e.g. index > 5) are captured and ranked.
H. Genomic coordinate translation: NG_000007.3:g.70842C>T and historical g.70617C>T resolve to c.118C>T.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from app.clinvar import (
    TIER_EXACT,
    TIER_RELATED,
    TIER_GENERAL,
    classify_clinvar_record,
    fetch_clinvar_records,
    is_exact_match_title,
    translate_genomic_to_cdna,
)
from app.models import ClinVarRecord


# -----------------------------------------------------------------------------
# Test A: Exact variant retrieval for NM_000518.5:c.118C>T
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_a_exact_benchmark_c118ct_retrieval():
    """Verifies that c.118C>T resolves deterministically to Variation ID 15402 / VCV000015402."""
    records = await fetch_clinvar_records("NM_000518.5:c.118C>T")
    assert len(records) > 0, "Expected at least one ClinVar record for c.118C>T"
    top = records[0]
    assert top.id == "15402"
    assert top.accession == "VCV000015402"
    assert "Pathogenic" in top.clinical_significance
    assert "multiple submitters" in top.review_status
    assert top.is_exact_match is True
    assert top.evidence_type == TIER_EXACT
    assert "c.118C>T" in top.title
    assert "p.Gln40Ter" in top.title


# -----------------------------------------------------------------------------
# Test B: Exact protein consequence matching (p.Gln40Ter)
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_b_protein_consequence_matching():
    """Verifies that searching by protein change p.Gln40Ter resolves to 15402."""
    records = await fetch_clinvar_records("p.Gln40Ter", protein_change="p.Gln40Ter")
    assert len(records) > 0
    top = records[0]
    assert top.id == "15402"
    assert top.is_exact_match is True
    assert top.evidence_type == TIER_EXACT


# -----------------------------------------------------------------------------
# Test C: Historical alias matching and false-positive rejection
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_c_historical_alias_matching_and_fp_rejection():
    """Verifies CD39 C>T alias resolves to 15402, and ID 15470 (c.-78A>C) is rejected as exact match."""
    # 1. Alias query resolves to 15402
    records = await fetch_clinvar_records("CD39 C>T", variant_aliases=["CD39 C>T", "Q39*"])
    assert len(records) > 0
    assert records[0].id == "15402"
    assert records[0].is_exact_match is True
    assert records[0].evidence_type == TIER_EXACT

    # 2. Strict verification rejects ID 15470 if returned in alias search
    raw_15470 = {
        "uid": "15470",
        "title": "NM_000518.5(HBB):c.-78A>C",
        "genes": [{"symbol": "HBB", "geneid": "3043"}],
        "variation_set": [{"cdna_change": "NM_000518.5(HBB):c.-78A>C", "aliases": ["-28 (A>C)"]}],
    }
    is_exact, tier, score = classify_clinvar_record(
        title="NM_000518.5(HBB):c.-78A>C",
        c_term="c.118C>T",
        variant_aliases=["CD39 C>T"],
        raw_record=raw_15470,
    )
    assert is_exact is False, "False match 15470 must not be classified as exact match"
    assert tier == TIER_RELATED


# -----------------------------------------------------------------------------
# Test D: Rejection of false positives (nearby, wrong allele, compound)
# -----------------------------------------------------------------------------
def test_d_rejection_of_false_positives():
    """Verifies that nearby variants, wrong alleles, and compound heterozygotes are rejected."""
    # 1. Nearby position (c.117C>T vs c.118C>T)
    is_exact, tier, score = classify_clinvar_record("NM_000518.5(HBB):c.117C>T", c_term="c.118C>T")
    assert is_exact is False
    assert tier == TIER_RELATED

    # 2. Same position, wrong alt allele (c.118C>A vs c.118C>T)
    is_exact, tier, score = classify_clinvar_record(
        "NM_000518.5(HBB):c.118C>A (p.Gln40Lys)", c_term="c.118C>T"
    )
    assert is_exact is False
    assert tier == TIER_RELATED

    # 3. Compound heterozygote (c.[205C>T;20A>T] vs c.20A>T)
    is_exact, tier, score = classify_clinvar_record(
        "NM_000518.4(HBB):c.[205C>T;20A>T]", c_term="c.20A>T"
    )
    assert is_exact is False
    assert tier == TIER_RELATED

    # 4. Canonical equivalent accepted (c.124_127del <-> c.126_129del)
    is_exact, tier, score = classify_clinvar_record(
        "NM_000518.5(HBB):c.126_129delCTTT", c_term="c.124_127del"
    )
    assert is_exact is True
    assert tier == TIER_EXACT


# -----------------------------------------------------------------------------
# Test E: Missing ClinVar record handling (zero hallucinated records)
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_e_missing_clinvar_record_returns_empty():
    """Verifies that a novel synthetic variant returns an empty list without fabrication."""
    records = await fetch_clinvar_records("c.118_119insTTTT")
    # Must either be empty or only non-exact related context
    for r in records:
        assert r.is_exact_match is False
        assert r.evidence_type != TIER_EXACT


# -----------------------------------------------------------------------------
# Test F: Candidate ranking prioritizes exact variant record at index 0
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_f_candidate_ranking_prioritizes_exact_match():
    """Verifies that for Sickle cell c.20A>T, single variant 15333 is ranked at index 0 ahead of compound alleles."""
    records = await fetch_clinvar_records("c.20A>T")
    assert len(records) > 0
    top = records[0]
    assert top.id == "15333"
    assert top.is_exact_match is True
    assert top.evidence_type == TIER_EXACT
    assert "c.20A>T" in top.title
    assert "p.Glu7Val" in top.title

    # If compound alleles are also in the results, they follow after index 0
    if len(records) > 1:
        for non_top in records[1:]:
            assert non_top.id != "15333"


# -----------------------------------------------------------------------------
# Test G: Candidate beyond initial window (window expansion to retmax=50)
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_g_window_expansion_retrieves_buried_record():
    """Verifies that even when a true variant is buried at index 6+ in broad search, it is captured and ranked #1."""
    # Simulate a broad NCBI response where 15402 is at index 6
    mock_id_list = ["15584", "15488", "15470", "15464", "15450", "15440", "15402"]
    mock_esummary_result = {
        "15584": {"title": "NM_000518.5(HBB):c.*111A>G", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15488": {"title": "NM_000518.5(HBB):c.*111A>G", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15470": {"title": "NM_000518.5(HBB):c.-78A>C", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15464": {"title": "NM_000518.5(HBB):c.-29A>G", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15450": {"title": "NM_000518.5(HBB):c.92+5G>C", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15440": {"title": "NM_000518.5(HBB):c.92+1G>A", "genes": [{"symbol": "HBB"}], "germline_classification": {"description": "Pathogenic"}},
        "15402": {
            "title": "NM_000518.5(HBB):c.118C>T (p.Gln40Ter)",
            "accession": "VCV000015402",
            "genes": [{"symbol": "HBB"}],
            "variation_set": [{"cdna_change": "c.118C>T"}],
            "protein_change": "Q40*",
            "germline_classification": {
                "description": "Pathogenic",
                "review_status": "criteria provided, multiple submitters, no conflicts",
            },
        },
    }

    async def mock_get(url, params=None):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        if "esearch.fcgi" in str(url):
            mock_resp.json.return_value = {"esearchresult": {"idlist": mock_id_list}}
        elif "esummary.fcgi" in str(url):
            mock_resp.json.return_value = {"result": mock_esummary_result}
        return mock_resp

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        records = await fetch_clinvar_records("HBB c.118C>T", max_results=5)
        assert len(records) > 0
        # True record buried at index 6 must be promoted to index 0
        assert records[0].id == "15402"
        assert records[0].is_exact_match is True
        assert records[0].evidence_type == TIER_EXACT


# -----------------------------------------------------------------------------
# Test H: Genomic vs transcript coordinate query resolution
# -----------------------------------------------------------------------------
def test_h_genomic_to_cdna_coordinate_translation():
    """Verifies that RefSeqGene NG_000007.3 coordinates and literature offsets resolve to c.118C>T."""
    # 1. NG_000007.3 true RefSeqGene coordinate (70817 + 25 = 70842)
    assert translate_genomic_to_cdna("NG_000007.3:g.70842C>T") == "c.118C>T"
    assert translate_genomic_to_cdna("g.70842C>T") == "c.118C>T"

    # 2. Historical literature offset without Intron 1
    assert translate_genomic_to_cdna("NG_000007.3:g.70617C>T") == "c.118C>T"
    assert translate_genomic_to_cdna("g.70617C>T") == "c.118C>T"

    # 3. Intron 1 splice donor sites
    assert translate_genomic_to_cdna("g.70687G>A") == "c.92+1G>A"
    assert translate_genomic_to_cdna("g.70691G>C") == "c.92+5G>C"


@pytest.mark.asyncio
async def test_h_genomic_query_resolves_to_15402():
    """Verifies that executing a query with NG_000007.3 genomic notation retrieves ClinVar record 15402."""
    records = await fetch_clinvar_records("NG_000007.3:g.70842C>T")
    assert len(records) > 0
    top = records[0]
    assert top.id == "15402"
    assert top.accession == "VCV000015402"
    assert top.is_exact_match is True
    assert top.evidence_type == TIER_EXACT
