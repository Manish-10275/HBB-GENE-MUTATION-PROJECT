"""NCBI ClinVar client using official E-utilities API with fixture fallback."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import httpx

from app.config import settings
from app.models import ClinVarRecord

logger = logging.getLogger(__name__)

FIXTURES_PATH = settings.DATA_DIR / "fixtures" / "clinvar_fixtures.json"


def _load_fixtures() -> Dict[str, List[dict]]:
    if FIXTURES_PATH.exists():
        try:
            with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load ClinVar fixtures: {e}")
    return {}


async def fetch_clinvar_records(
    query_term: str,
    max_results: int = 5,
    timeout_seconds: float = 8.0
) -> List[ClinVarRecord]:
    """
    Retrieves ClinVar records for a genomic variant using NCBI E-utilities.

    Handles:
    - Connection timeouts, HTTP errors, rate limiting
    - Structured extraction of clinical significance, review status, and condition traits
    - Safe fallback to verified development fixtures if NCBI is unreachable
    - Never fabricates unverified claims
    """
    clean_term = query_term.strip()
    if not clean_term:
        return []

    # Format search query for ClinVar
    # If standard HGVS or c. notation, ensure HBB context
    if "HBB" not in clean_term:
        search_query = f"HBB[gene] AND {clean_term}"
    else:
        search_query = clean_term

    base_url = settings.NCBI_BASE_URL
    params_search = {
        "db": "clinvar",
        "term": search_query,
        "retmode": "json",
        "retmax": str(max_results)
    }
    if settings.NCBI_API_KEY:
        params_search["api_key"] = settings.NCBI_API_KEY
    if settings.NCBI_EMAIL:
        params_search["email"] = settings.NCBI_EMAIL

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            resp = await client.get(f"{base_url}/esearch.fcgi", params=params_search)
            if resp.status_code != 200:
                logger.warning(f"ClinVar esearch failed with status {resp.status_code}")
                return _check_fixture_fallback(clean_term)

            data = resp.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                # Variant has no records in ClinVar
                return []

            params_sum = {
                "db": "clinvar",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            if settings.NCBI_API_KEY:
                params_sum["api_key"] = settings.NCBI_API_KEY
            if settings.NCBI_EMAIL:
                params_sum["email"] = settings.NCBI_EMAIL

            sum_resp = await client.get(f"{base_url}/esummary.fcgi", params=params_sum)
            if sum_resp.status_code != 200:
                logger.warning(f"ClinVar esummary failed with status {sum_resp.status_code}")
                return _check_fixture_fallback(clean_term)

            sum_data = sum_resp.json()
            results_dict = sum_data.get("result", {})

            records: List[ClinVarRecord] = []
            for vid in id_list:
                if vid in results_dict:
                    raw = results_dict[vid]
                    germline = raw.get("germline_classification", {}) or {}
                    traits_raw = germline.get("trait_set", []) or []
                    conditions = [
                        t.get("trait_name")
                        for t in traits_raw
                        if t and t.get("trait_name")
                    ]

                    accession_val = raw.get("accession") or f"VCV{int(vid):09d}"

                    records.append(
                        ClinVarRecord(
                            id=vid,
                            title=raw.get("title", f"Variation ID {vid}"),
                            accession=accession_val,
                            clinical_significance=germline.get("description", "Unknown"),
                            review_status=germline.get("review_status", "no assertion provided"),
                            conditions=conditions[:8],
                            last_evaluated=germline.get("last_evaluated"),
                            variation_id=vid,
                            source="NCBI ClinVar",
                            url=f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{vid}/"
                        )
                    )
            return records

    except (httpx.RequestError, httpx.TimeoutException, Exception) as exc:
        logger.warning(f"Live ClinVar request encountered exception: {exc}")
        return _check_fixture_fallback(clean_term)


def _check_fixture_fallback(term: str) -> List[ClinVarRecord]:
    """Provides verified fixture data if offline or network error."""
    fixtures = _load_fixtures()
    for key, items in fixtures.items():
        if key in term or term in key:
            logger.info(f"Using verified development fixture for ClinVar query: {term}")
            return [ClinVarRecord(**item) for item in items]
    return []
