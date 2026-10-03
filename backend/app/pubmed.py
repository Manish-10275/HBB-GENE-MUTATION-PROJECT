"""NCBI PubMed client using official E-utilities API with fixture fallback."""

import json
import logging
from typing import Dict, List
import httpx

from app.config import settings
from app.models import PubMedRecord

logger = logging.getLogger(__name__)

FIXTURES_PATH = settings.DATA_DIR / "fixtures" / "pubmed_fixtures.json"


def _load_fixtures() -> Dict[str, List[dict]]:
    if FIXTURES_PATH.exists():
        try:
            with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load PubMed fixtures: {e}")
    return {}


async def fetch_pubmed_records(
    query_term: str,
    max_results: int = 5,
    timeout_seconds: float = 8.0
) -> List[PubMedRecord]:
    """
    Retrieves scientific publications from PubMed matching variant and gene terms.

    Handles:
    - Connection timeouts, HTTP errors, rate limiting
    - Structured metadata extraction: PMID, title, authors, journal, pubdate
    - Safe fallback to verified development fixtures if NCBI is unreachable
    - Never fabricates fake literature
    """
    clean_term = query_term.strip()
    if not clean_term:
        return []

    # Structure PubMed query term
    if "HBB" not in clean_term:
        search_query = f"HBB AND {clean_term}"
    else:
        search_query = clean_term

    base_url = settings.NCBI_BASE_URL
    params_search = {
        "db": "pubmed",
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
                logger.warning(f"PubMed esearch failed with status {resp.status_code}")
                return _check_fixture_fallback(clean_term)

            data = resp.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return []

            params_sum = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            if settings.NCBI_API_KEY:
                params_sum["api_key"] = settings.NCBI_API_KEY
            if settings.NCBI_EMAIL:
                params_sum["email"] = settings.NCBI_EMAIL

            sum_resp = await client.get(f"{base_url}/esummary.fcgi", params=params_sum)
            if sum_resp.status_code != 200:
                logger.warning(f"PubMed esummary failed with status {sum_resp.status_code}")
                return _check_fixture_fallback(clean_term)

            sum_data = sum_resp.json()
            results_dict = sum_data.get("result", {})

            records: List[PubMedRecord] = []
            for pmid in id_list:
                if pmid in results_dict:
                    raw = results_dict[pmid]
                    authors = [
                        a.get("name")
                        for a in raw.get("authors", [])
                        if a and a.get("name")
                    ]

                    records.append(
                        PubMedRecord(
                            pmid=pmid,
                            title=raw.get("title", ""),
                            journal=raw.get("source", ""),
                            pub_date=raw.get("pubdate", ""),
                            authors=authors[:6],
                            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                            abstract_snippet=None,
                            source="Live NCBI PubMed"
                        )
                    )
            return records

    except (httpx.RequestError, httpx.TimeoutException, Exception) as exc:
        logger.warning(f"Live PubMed request encountered exception: {exc}")
        return _check_fixture_fallback(clean_term)


def _check_fixture_fallback(term: str) -> List[PubMedRecord]:
    """Provides verified fixture data if offline or network error."""
    fixtures = _load_fixtures()
    for key, items in fixtures.items():
        if key in term or term in key:
            logger.info(f"Using verified development fixture for PubMed query: {term}")
            res: List[PubMedRecord] = []
            for item in items:
                rec = PubMedRecord(**item)
                rec.source = "Development Fixture (NCBI PubMed)"
                res.append(rec)
            return res
    return []
