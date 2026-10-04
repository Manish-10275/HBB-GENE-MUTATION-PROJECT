from datetime import datetime, timezone
import json
import logging
from typing import Dict, List, Optional, Tuple
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
    timeout_seconds: float = 8.0,
    variant_aliases: Optional[List[str]] = None,
) -> List[PubMedRecord]:
    """
    Retrieves scientific publications from PubMed matching variant and gene terms.

    Handles:
    - Connection timeouts, HTTP errors, rate limiting
    - Structured metadata extraction: PMID, title, authors, journal, pubdate
    - Strict 3-level evidence classification: DIRECT VARIANT EVIDENCE, RELATED GENE OR DISEASE EVIDENCE, CONTEXTUAL EVIDENCE
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
                return _check_fixture_fallback(clean_term, variant_aliases)

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
                return _check_fixture_fallback(clean_term, variant_aliases)

            sum_data = sum_resp.json()
            results_dict = sum_data.get("result", {})

            records: List[PubMedRecord] = []
            retrieval_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            for pmid in id_list:
                if pmid in results_dict:
                    raw = results_dict[pmid]
                    authors = [
                        a.get("name")
                        for a in raw.get("authors", [])
                        if a and a.get("name")
                    ]

                    t_str = raw.get("title", "")
                    is_direct, ev_type = classify_pubmed_evidence(
                        title=t_str,
                        query_term=clean_term,
                        abstract=None,
                        variant_aliases=variant_aliases,
                    )
                    records.append(
                        PubMedRecord(
                            pmid=pmid,
                            title=t_str,
                            journal=raw.get("source", ""),
                            pub_date=raw.get("pubdate", ""),
                            authors=authors[:6],
                            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                            abstract_snippet=None,
                            source="Live NCBI PubMed",
                            is_exact_match=is_direct,
                            is_direct_evidence=is_direct,
                            evidence_type=ev_type,
                            retrieval_date=retrieval_date_str,
                        )
                    )
            return records

    except (httpx.RequestError, httpx.TimeoutException, Exception) as exc:
        logger.warning(f"Live PubMed request encountered exception: {exc}")
        return _check_fixture_fallback(clean_term, variant_aliases)


def classify_pubmed_evidence(
    title: str,
    query_term: str,
    abstract: Optional[str] = None,
    variant_aliases: Optional[List[str]] = None,
) -> Tuple[bool, str]:
    """
    Classifies a PubMed record strictly into three evidence categories:
    1. DIRECT VARIANT EVIDENCE:
       Retrieved publication text specifically contains the active variant
       identifier, cDNA mutation, codon change, or unambiguous canonical alias.
    2. RELATED GENE OR DISEASE EVIDENCE:
       Publication discusses HBB, beta thalassemia, hemoglobinopathies, or
       globin biology without explicitly citing this specific variant.
    3. CONTEXTUAL EVIDENCE:
       Broader biomedical literature (general molecular genetics, techniques,
       or non-specific disease biology).
    """
    text = f"{title} {abstract or ''}".lower()
    q = query_term.lower().strip()

    # 1. Check user-supplied or detected variant aliases
    if variant_aliases:
        for alias in variant_aliases:
            a_clean = alias.lower().strip()
            if a_clean and a_clean in text:
                return True, "DIRECT VARIANT EVIDENCE"

    # 2. Check exact cDNA term match if specific (e.g. c.118c>t)
    if q and len(q) > 4 and q in text:
        return True, "DIRECT VARIANT EVIDENCE"

    # 3. Known canonical HBB mutation markers & aliases
    known_aliases: Dict[str, List[str]] = {
        "c.118c>t": [
            "cd39", "cd 39", "codon 39", "codon39",
            "gln40ter", "q40ter", "q40*", "gln40*",
            "q39*", "gln39ter", "q39ter", "gln39*",
            "cag to tag", "cag->tag", "cag>tag",
            "c.118c>t", "118c>t", "c.118 c>t",
        ],
        "c.20a>t": [
            "hbs", "sickle", "glu7val", "e7v", "glu6val", "e6v",
            "codon 6", "codon 7", "cd6", "cd7", "c.20a>t",
        ],
        "c.19g>a": [
            "hbc", "glu7lys", "e7k", "glu6lys", "e6k", "codon 6", "cd6", "c.19g>a"
        ],
        "c.92+5g>c": ["ivs-i-5", "ivs1-5", "ivs-1-5", "c.92+5", "ivs 1-5"],
        "c.92+1g>t": ["ivs-i-1", "ivs1-1", "ivs-1-1", "c.92+1", "ivs 1-1"],
        "c.124_127del": ["fs 41/42", "codon 41/42", "cd 41/42", "c.124_127del", "codon 41", "codon 42"],
        "c.126_129del": ["fs 41/42", "codon 41/42", "cd 41/42", "c.126_129del", "codon 41", "codon 42"],
        "c.27dup": ["codon 8/9", "cd 8/9", "+g codon 8", "c.26_27insg", "insg", "c.27dup"],
    }

    for key, markers in known_aliases.items():
        if key in q or q in key:
            if any(m in text for m in markers):
                return True, "DIRECT VARIANT EVIDENCE"

    # 4. Check for related gene or disease evidence
    related_keywords = [
        "hbb", "beta-globin", "beta globin", "β-globin",
        "beta-thalassemia", "beta thalassemia", "β-thalassemia",
        "thalassemia", "hemoglobin", "hemoglobinopathy", "hemoglobinopathies",
        "hba", "hba2", "hbf", "globin", "erythroid"
    ]
    if any(k in text for k in related_keywords):
        return False, "RELATED GENE OR DISEASE EVIDENCE"

    # 5. Otherwise contextual evidence
    return False, "CONTEXTUAL EVIDENCE"


def classify_pubmed_relevance(
    title: str,
    query_term: str,
    abstract: Optional[str] = None,
    variant_aliases: Optional[List[str]] = None,
) -> Tuple[bool, str]:
    """Backward compatible alias for classify_pubmed_evidence."""
    return classify_pubmed_evidence(title, query_term, abstract, variant_aliases)


def _check_fixture_fallback(term: str, variant_aliases: Optional[List[str]] = None) -> List[PubMedRecord]:
    """Provides verified fixture data if offline or network error."""
    fixtures = _load_fixtures()
    retrieval_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for key, items in fixtures.items():
        if key in term or term in key:
            logger.info(f"Using verified development fixture for PubMed query: {term}")
            res: List[PubMedRecord] = []
            for item in items:
                rec = PubMedRecord(**item)
                rec.source = "Development Fixture (NCBI PubMed)"
                is_direct, ev_type = classify_pubmed_evidence(
                    rec.title, term, rec.abstract_snippet, variant_aliases
                )
                rec.is_exact_match = is_direct
                rec.is_direct_evidence = is_direct
                rec.evidence_type = ev_type
                rec.retrieval_date = retrieval_date_str
                res.append(rec)
            return res
    return []

