"""Live NCBI PubMed evidence provider using official E-utilities API."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

from app.evidence.models import (
    EvidenceProvenance,
    EvidenceStatus,
    PubMedArticle,
    PubMedEvidenceResult,
    RetrievalMode,
)

logger = logging.getLogger(__name__)


class LivePubMedProvider:
    """
    Live PubMed provider connecting directly to NCBI Entrez E-utilities for scientific literature.
    """

    def __init__(
        self,
        base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
        api_key: Optional[str] = None,
        email: Optional[str] = None,
        timeout: float = 10.0,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.email = email
        self.timeout = timeout
        self._external_client = client

    def _build_params(self, extra: Dict[str, str]) -> Dict[str, str]:
        params = dict(extra)
        if self.api_key:
            params["api_key"] = self.api_key
        if self.email:
            params["email"] = self.email
        return params

    async def search_literature(
        self,
        query: str,
        max_results: int = 10,
    ) -> PubMedEvidenceResult:
        """
        Executes live NCBI PubMed search and retrieval.
        Never silently falls back to offline fixtures.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        client = self._external_client or httpx.AsyncClient(timeout=self.timeout)
        should_close = self._external_client is None

        # Build query scoped to HBB / hemoglobinopathy literature
        clean_q = query.strip()
        search_term = f'("{clean_q}" OR HBB) AND (beta thalassemia OR sickle cell OR hemoglobin)'

        try:
            # 1. ESearch
            try:
                params = self._build_params({
                    "db": "pubmed",
                    "term": search_term,
                    "retmode": "json",
                    "retmax": str(max_results),
                    "sort": "pub_date",
                })
                resp = await client.get(f"{self.base_url}/esearch.fcgi", params=params)

                if resp.status_code == 429:
                    return self._create_error_result(
                        query, EvidenceStatus.RATE_LIMITED, "NCBI PubMed rate limit exceeded (HTTP 429).", timestamp
                    )
                if resp.status_code >= 500:
                    return self._create_error_result(
                        query, EvidenceStatus.PROVIDER_ERROR, f"NCBI PubMed error (HTTP {resp.status_code}).", timestamp
                    )
                if resp.status_code != 200:
                    return self._create_error_result(
                        query, EvidenceStatus.INVALID_EXTERNAL_RESPONSE, f"NCBI PubMed search status {resp.status_code}.", timestamp
                    )

                data = resp.json()
                id_list = data.get("esearchresult", {}).get("idlist", [])
            except httpx.TimeoutException:
                return self._create_error_result(
                    query, EvidenceStatus.TIMEOUT, f"PubMed search timed out after {self.timeout}s.", timestamp
                )
            except httpx.NetworkError as ne:
                return self._create_error_result(
                    query, EvidenceStatus.NETWORK_UNAVAILABLE, f"Network error during PubMed search: {ne}", timestamp
                )
            except Exception as e:
                return self._create_error_result(
                    query, EvidenceStatus.INVALID_EXTERNAL_RESPONSE, f"Error parsing PubMed search: {e}", timestamp
                )

            if not id_list:
                return PubMedEvidenceResult(
                    query=query,
                    status=EvidenceStatus.NOT_FOUND,
                    articles=[],
                    error_message=f"No PubMed articles found for '{query}'.",
                    provenance=EvidenceProvenance(
                        source="PubMed",
                        provider="LivePubMedProvider",
                        mode=RetrievalMode.LIVE,
                        retrieval_status=EvidenceStatus.NOT_FOUND,
                        is_fixture=False,
                        retrieval_timestamp=timestamp,
                        transformations=["live_esearch"],
                    ),
                )

            # 2. ESummary
            try:
                sum_params = self._build_params({
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "json",
                })
                sum_resp = await client.get(f"{self.base_url}/esummary.fcgi", params=sum_params)

                if sum_resp.status_code == 429:
                    return self._create_error_result(
                        query, EvidenceStatus.RATE_LIMITED, "NCBI PubMed rate limit exceeded during esummary.", timestamp
                    )
                if sum_resp.status_code != 200:
                    return self._create_error_result(
                        query, EvidenceStatus.INVALID_EXTERNAL_RESPONSE, f"NCBI PubMed esummary status {sum_resp.status_code}.", timestamp
                    )

                sum_data = sum_resp.json()
                results_dict = sum_data.get("result", {})
            except httpx.TimeoutException:
                return self._create_error_result(
                    query, EvidenceStatus.TIMEOUT, "PubMed esummary request timed out.", timestamp
                )
            except httpx.NetworkError as ne:
                return self._create_error_result(
                    query, EvidenceStatus.NETWORK_UNAVAILABLE, f"Network error during PubMed esummary: {ne}", timestamp
                )
            except Exception as e:
                return self._create_error_result(
                    query, EvidenceStatus.INVALID_EXTERNAL_RESPONSE, f"Failed to parse PubMed summary: {e}", timestamp
                )

            # 3. Normalize articles
            articles: List[PubMedArticle] = []
            for pmid in id_list:
                if pmid not in results_dict:
                    continue
                item = results_dict[pmid]
                authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
                art_prov = EvidenceProvenance(
                    source="PubMed",
                    provider="LivePubMedProvider",
                    mode=RetrievalMode.LIVE,
                    retrieval_status=EvidenceStatus.FOUND,
                    external_identifier=pmid,
                    is_fixture=False,
                    retrieval_timestamp=timestamp,
                    transformations=["live_article_normalization"],
                )
                articles.append(
                    PubMedArticle(
                        pmid=pmid,
                        title=item.get("title", f"PMID {pmid}"),
                        journal=item.get("source"),
                        pub_date=item.get("pubdate"),
                        authors=authors,
                        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        provenance=art_prov,
                    )
                )

            return PubMedEvidenceResult(
                query=query,
                status=EvidenceStatus.FOUND if articles else EvidenceStatus.NOT_FOUND,
                articles=articles,
                provenance=EvidenceProvenance(
                    source="PubMed",
                    provider="LivePubMedProvider",
                    mode=RetrievalMode.LIVE,
                    retrieval_status=EvidenceStatus.FOUND if articles else EvidenceStatus.NOT_FOUND,
                    external_identifier=articles[0].pmid if articles else None,
                    is_fixture=False,
                    retrieval_timestamp=timestamp,
                    transformations=["live_esearch", "live_esummary"],
                ),
            )

        finally:
            if should_close:
                await client.aclose()

    def _create_error_result(
        self,
        query: str,
        status: EvidenceStatus,
        error_message: str,
        timestamp: str,
    ) -> PubMedEvidenceResult:
        return PubMedEvidenceResult(
            query=query,
            status=status,
            articles=[],
            error_message=error_message,
            provenance=EvidenceProvenance(
                source="PubMed",
                provider="LivePubMedProvider",
                mode=RetrievalMode.LIVE,
                retrieval_status=status,
                is_fixture=False,
                retrieval_timestamp=timestamp,
                transformations=[],
            ),
        )
