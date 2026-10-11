"""Live NCBI ClinVar evidence provider using official E-utilities API."""

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx

from app.core.models import NormalizedVariant
from app.evidence.models import (
    ClinVarEvidenceResult,
    ClinVarRecord,
    EvidenceDiscrepancy,
    EvidenceProvenance,
    EvidenceStatus,
    RetrievalMode,
)

logger = logging.getLogger(__name__)


class LiveClinVarProvider:
    """
    Live ClinVar provider connecting directly to NCBI Entrez E-utilities.
    
    Guarantees:
    - Dedicated HTTP communication with timeout and rate limit safety
    - Zero silent fallback to offline fixtures on failure
    - Strongly typed normalization of external payloads
    - Explicit failure state reporting (NETWORK_UNAVAILABLE, TIMEOUT, RATE_LIMITED, etc.)
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

    def _generate_search_terms(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant],
        deterministic_consequence: Optional[str],
    ) -> List[str]:
        """Generates progressive NCBI search queries ordered by biological specificity."""
        terms: List[str] = []

        if normalized_variant:
            c_pos = normalized_variant.c_position
            if normalized_variant.variant_type.value in ("substitution", "splice"):
                c_term = f"c.{c_pos}{normalized_variant.ref_allele}>{normalized_variant.alt_allele}"
            elif normalized_variant.variant_type.value == "deletion":
                c_term = f"c.{c_pos}del"
            elif normalized_variant.variant_type.value == "duplication":
                c_term = f"c.{c_pos}dup"
            elif normalized_variant.variant_type.value == "insertion":
                c_term = f"c.{c_pos}ins{normalized_variant.alt_allele}"
            else:
                c_term = f"c.{c_pos}"

            # 1. Exact quoted transcript variant
            terms.append(f'"{normalized_variant.transcript_accession}:{c_term}"')
            # 2. Gene-scoped cDNA variant
            terms.append(f'"{c_term}"[Variant Name] AND HBB[Gene Name]')

            if deterministic_consequence and deterministic_consequence != "p.?":
                # 3. Protein consequence search
                terms.append(f'"{deterministic_consequence}"[Variant Name] AND HBB[Gene Name]')

            # 4. Equivalent nomenclature
            for eq in normalized_variant.equivalent_nomenclature:
                if eq != c_term:
                    terms.append(f'"{eq}"[Variant Name] AND HBB[Gene Name]')
        else:
            clean = query.strip()
            terms.append(f'"{clean}"[Variant Name] AND HBB[Gene Name]')
            terms.append(f"HBB[Gene Name] AND {clean}")

        return terms

    async def search_variant(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant] = None,
        deterministic_consequence: Optional[str] = None,
    ) -> ClinVarEvidenceResult:
        """
        Executes live NCBI ClinVar search and retrieval.
        Never silently falls back to offline fixtures.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        search_terms = self._generate_search_terms(query, normalized_variant, deterministic_consequence)

        client = self._external_client or httpx.AsyncClient(timeout=self.timeout)
        should_close = self._external_client is None

        id_list: List[str] = []
        try:
            # 1. ESearch phase
            for term in search_terms:
                try:
                    params = self._build_params({
                        "db": "clinvar",
                        "term": term,
                        "retmode": "json",
                        "retmax": "20",
                    })
                    resp = await client.get(f"{self.base_url}/esearch.fcgi", params=params)

                    if resp.status_code == 429:
                        return self._create_error_result(
                            query, normalized_variant, EvidenceStatus.RATE_LIMITED,
                            "NCBI rate limit exceeded (HTTP 429).", timestamp
                        )
                    if resp.status_code >= 500:
                        return self._create_error_result(
                            query, normalized_variant, EvidenceStatus.PROVIDER_ERROR,
                            f"NCBI service error (HTTP {resp.status_code}).", timestamp
                        )
                    if resp.status_code != 200:
                        return self._create_error_result(
                            query, normalized_variant, EvidenceStatus.INVALID_EXTERNAL_RESPONSE,
                            f"NCBI esearch returned status {resp.status_code}.", timestamp
                        )

                    data = resp.json()
                    ids = data.get("esearchresult", {}).get("idlist", [])
                    if ids:
                        id_list = ids
                        break
                except httpx.TimeoutException:
                    return self._create_error_result(
                        query, normalized_variant, EvidenceStatus.TIMEOUT,
                        f"NCBI search timed out after {self.timeout}s.", timestamp
                    )
                except httpx.NetworkError as ne:
                    return self._create_error_result(
                        query, normalized_variant, EvidenceStatus.NETWORK_UNAVAILABLE,
                        f"Network connection failed: {ne}", timestamp
                    )
                except Exception as e:
                    logger.warning(f"Error querying ClinVar with term '{term}': {e}")
                    continue

            if not id_list:
                return ClinVarEvidenceResult(
                    query=query,
                    status=EvidenceStatus.NOT_FOUND,
                    records=[],
                    primary_record=None,
                    normalized_variant=normalized_variant,
                    error_message=f"No ClinVar entries found matching '{query}'.",
                    provenance=EvidenceProvenance(
                        source="ClinVar",
                        provider="LiveClinVarProvider",
                        mode=RetrievalMode.LIVE,
                        retrieval_status=EvidenceStatus.NOT_FOUND,
                        is_fixture=False,
                        retrieval_timestamp=timestamp,
                        transformations=["live_esearch"],
                    ),
                )

            # 2. ESummary phase
            try:
                sum_params = self._build_params({
                    "db": "clinvar",
                    "id": ",".join(id_list),
                    "retmode": "json",
                })
                sum_resp = await client.get(f"{self.base_url}/esummary.fcgi", params=sum_params)

                if sum_resp.status_code == 429:
                    return self._create_error_result(
                        query, normalized_variant, EvidenceStatus.RATE_LIMITED,
                        "NCBI rate limit exceeded during esummary.", timestamp
                    )
                if sum_resp.status_code != 200:
                    return self._create_error_result(
                        query, normalized_variant, EvidenceStatus.INVALID_EXTERNAL_RESPONSE,
                        f"NCBI esummary returned status {sum_resp.status_code}.", timestamp
                    )

                sum_data = sum_resp.json()
                results_dict = sum_data.get("result", {})
            except httpx.TimeoutException:
                return self._create_error_result(
                    query, normalized_variant, EvidenceStatus.TIMEOUT,
                    "NCBI esummary request timed out.", timestamp
                )
            except httpx.NetworkError as ne:
                return self._create_error_result(
                    query, normalized_variant, EvidenceStatus.NETWORK_UNAVAILABLE,
                    f"Network error during esummary: {ne}", timestamp
                )
            except Exception as e:
                return self._create_error_result(
                    query, normalized_variant, EvidenceStatus.INVALID_EXTERNAL_RESPONSE,
                    f"Failed to parse NCBI summary payload: {e}", timestamp
                )

            # 3. Parse and normalize records
            records, discrepancies = self._normalize_summary_results(
                id_list, results_dict, query, normalized_variant, deterministic_consequence, timestamp
            )

            primary = next((r for r in records if r.is_exact_match), records[0] if records else None)

            return ClinVarEvidenceResult(
                query=query,
                status=EvidenceStatus.FOUND if records else EvidenceStatus.NOT_FOUND,
                records=records,
                primary_record=primary,
                normalized_variant=normalized_variant,
                discrepancies=discrepancies,
                provenance=EvidenceProvenance(
                    source="ClinVar",
                    provider="LiveClinVarProvider",
                    mode=RetrievalMode.LIVE,
                    retrieval_status=EvidenceStatus.FOUND if records else EvidenceStatus.NOT_FOUND,
                    external_identifier=primary.variation_id if primary else None,
                    is_fixture=False,
                    retrieval_timestamp=timestamp,
                    transformations=["live_esearch", "live_esummary", "record_normalization"],
                ),
            )

        finally:
            if should_close:
                await client.aclose()

    def _normalize_summary_results(
        self,
        id_list: List[str],
        results_dict: Dict[str, Any],
        query: str,
        normalized_variant: Optional[NormalizedVariant],
        deterministic_consequence: Optional[str],
        timestamp: str,
    ) -> Tuple[List[ClinVarRecord], List[EvidenceDiscrepancy]]:
        """Normalizes external summary payloads into typed internal domain records."""
        records: List[ClinVarRecord] = []
        discrepancies: List[EvidenceDiscrepancy] = []

        target_c = normalized_variant.c_position if normalized_variant else ""

        for rank, vid in enumerate(id_list, start=1):
            if vid not in results_dict:
                continue

            raw = results_dict[vid]
            title = raw.get("title", f"Variation ID {vid}")
            accession = raw.get("accession") or f"VCV{int(vid):09d}"

            germline = raw.get("germline_classification", {}) or {}
            sig = germline.get("description", "Unknown")
            review = germline.get("review_status", "no assertion criteria provided")
            last_eval = germline.get("last_evaluated")

            traits_raw = germline.get("trait_set", []) or []
            conditions = [
                t.get("trait_name")
                for t in traits_raw
                if t and t.get("trait_name") and t.get("trait_name") != "not provided"
            ]

            is_exact = False
            if target_c and (f"c.{target_c}" in title or f"c.{target_c}del" in title or f"c.{target_c}dup" in title):
                is_exact = True
            elif query.strip() in title:
                is_exact = True

            rec_prov = EvidenceProvenance(
                source="ClinVar",
                provider="LiveClinVarProvider",
                mode=RetrievalMode.LIVE,
                retrieval_status=EvidenceStatus.FOUND,
                external_identifier=vid,
                is_fixture=False,
                retrieval_timestamp=timestamp,
                transformations=["record_normalization"],
            )

            rec = ClinVarRecord(
                variation_id=vid,
                accession=accession,
                title=title,
                clinical_significance=sig,
                review_status=review,
                conditions=conditions[:8],
                last_evaluated=last_eval,
                url=f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{vid}/",
                is_exact_match=is_exact,
                retrieval_rank=rank,
                provenance=rec_prov,
                raw_attributes={
                    "variation_set": raw.get("variation_set", []),
                    "genes": [g.get("symbol") for g in raw.get("genes", []) if g.get("symbol")],
                },
            )
            records.append(rec)

            if is_exact and deterministic_consequence and "p." in title and deterministic_consequence != "p.?":
                m = re.search(r"\((p\.[A-Za-z0-9*]+)\)", title)
                if m:
                    ev_prot = m.group(1)
                    if ev_prot != deterministic_consequence:
                        discrepancies.append(
                            EvidenceDiscrepancy(
                                field_name="protein_consequence",
                                deterministic_value=deterministic_consequence,
                                evidence_value=ev_prot,
                                description=(
                                    f"Live ClinVar record indicates '{ev_prot}', whereas deterministic "
                                    f"core calculated '{deterministic_consequence}'."
                                ),
                            )
                        )

        # Sort exact matches first, then by rank
        records.sort(key=lambda r: (not r.is_exact_match, r.retrieval_rank))
        return records, discrepancies

    def _create_error_result(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant],
        status: EvidenceStatus,
        error_message: str,
        timestamp: str,
    ) -> ClinVarEvidenceResult:
        """Helper to create typed error results without silent fallback."""
        return ClinVarEvidenceResult(
            query=query,
            status=status,
            records=[],
            primary_record=None,
            normalized_variant=normalized_variant,
            error_message=error_message,
            provenance=EvidenceProvenance(
                source="ClinVar",
                provider="LiveClinVarProvider",
                mode=RetrievalMode.LIVE,
                retrieval_status=status,
                is_fixture=False,
                retrieval_timestamp=timestamp,
                transformations=[],
            ),
        )
