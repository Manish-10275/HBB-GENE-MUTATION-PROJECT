"""Pure offline PubMed evidence provider reading strictly versioned local fixtures."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.evidence.models import (
    EvidenceProvenance,
    EvidenceStatus,
    PubMedArticle,
    PubMedEvidenceResult,
    RetrievalMode,
)

logger = logging.getLogger(__name__)


class OfflinePubMedProvider:
    """
    Offline PubMed provider reading local fixtures with zero network calls.
    """

    def __init__(self, fixtures_path: Optional[Path] = None):
        if fixtures_path is not None:
            self.fixtures_path = Path(fixtures_path)
        else:
            self.fixtures_path = (
                Path(__file__).resolve().parent.parent.parent.parent
                / "data"
                / "fixtures"
                / "pubmed_fixtures.json"
            )
        self._cache: Optional[Dict[str, List[Dict[str, Any]]]] = None

    def _get_fixtures(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._cache is None:
            if not self.fixtures_path.exists():
                logger.warning(f"PubMed fixtures file not found at {self.fixtures_path}")
                self._cache = {}
            else:
                try:
                    with open(self.fixtures_path, "r", encoding="utf-8") as f:
                        self._cache = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading PubMed fixtures: {e}")
                    self._cache = {}
        return self._cache

    def search_literature(self, query: str) -> PubMedEvidenceResult:
        """
        Retrieves PubMed articles matching query from local fixtures.
        Guaranteed zero network requests.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        fixtures = self._get_fixtures()

        clean_q = query.strip()
        if ":" in clean_q:
            clean_q = clean_q.split(":", 1)[1].strip()

        entries: Optional[List[Dict[str, Any]]] = None
        if clean_q in fixtures:
            entries = fixtures[clean_q]
        else:
            for k, v in fixtures.items():
                if k in clean_q or clean_q in k:
                    entries = v
                    break

        if entries is None:
            prov = EvidenceProvenance(
                source="PubMed",
                provider="OfflinePubMedProvider",
                mode=RetrievalMode.OFFLINE,
                retrieval_status=EvidenceStatus.OFFLINE_DATA_UNAVAILABLE,
                external_identifier=None,
                is_fixture=True,
                fixture_path=str(self.fixtures_path),
                retrieval_timestamp=timestamp,
                transformations=["offline_fixture_lookup"],
            )
            return PubMedEvidenceResult(
                query=query,
                status=EvidenceStatus.OFFLINE_DATA_UNAVAILABLE,
                articles=[],
                error_message=f"No local PubMed fixture available for '{query}' in offline mode.",
                provenance=prov,
            )

        articles: List[PubMedArticle] = []
        for item in entries:
            pmid = str(item.get("pmid", ""))
            art_prov = EvidenceProvenance(
                source="PubMed",
                provider="OfflinePubMedProvider",
                mode=RetrievalMode.OFFLINE,
                retrieval_status=EvidenceStatus.FOUND,
                external_identifier=pmid,
                is_fixture=True,
                fixture_path=str(self.fixtures_path),
                retrieval_timestamp=timestamp,
                transformations=["fixture_article_normalization"],
            )
            article = PubMedArticle(
                pmid=pmid,
                title=item.get("title", ""),
                journal=item.get("journal"),
                pub_date=item.get("pub_date"),
                authors=item.get("authors", []),
                url=item.get("url", f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"),
                abstract_snippet=item.get("abstract_snippet"),
                provenance=art_prov,
            )
            articles.append(article)

        overall_prov = EvidenceProvenance(
            source="PubMed",
            provider="OfflinePubMedProvider",
            mode=RetrievalMode.OFFLINE,
            retrieval_status=EvidenceStatus.FOUND,
            external_identifier=articles[0].pmid if articles else None,
            is_fixture=True,
            fixture_path=str(self.fixtures_path),
            retrieval_timestamp=timestamp,
            transformations=["offline_fixture_lookup"],
        )

        return PubMedEvidenceResult(
            query=query,
            status=EvidenceStatus.FOUND,
            articles=articles,
            provenance=overall_prov,
        )
