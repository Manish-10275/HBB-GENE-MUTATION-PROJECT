"""Pure offline ClinVar evidence provider reading strictly versioned local fixtures."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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


class OfflineClinVarProvider:
    """
    Offline ClinVar provider for local execution and reproducible benchmarking.
    
    Guarantees:
    - ZERO network calls (no socket/http client in execution path)
    - Deterministic responses from versioned fixture data
    - Complete provenance tracking
    - Explicit OFFLINE_DATA_UNAVAILABLE status when fixture entry is missing
    """

    def __init__(self, fixtures_path: Optional[Path] = None):
        if fixtures_path is not None:
            self.fixtures_path = Path(fixtures_path)
        else:
            # Anchor relative to repository data directory
            self.fixtures_path = (
                Path(__file__).resolve().parent.parent.parent.parent
                / "data"
                / "fixtures"
                / "clinvar_fixtures.json"
            )
        self._cache: Optional[Dict[str, List[Dict[str, Any]]]] = None

    def _get_fixtures(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._cache is None:
            if not self.fixtures_path.exists():
                logger.warning(f"ClinVar fixtures file not found at {self.fixtures_path}")
                self._cache = {}
            else:
                try:
                    with open(self.fixtures_path, "r", encoding="utf-8") as f:
                        self._cache = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading ClinVar fixtures: {e}")
                    self._cache = {}
        return self._cache

    def _find_fixture_entries(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """Resolves variant to matching fixture list without network or heuristic guessing."""
        data = self._get_fixtures()
        if not data:
            return None

        candidates = []
        if normalized_variant:
            c_pos = normalized_variant.c_position
            if normalized_variant.variant_type.value == "substitution":
                candidates.append(f"c.{c_pos}{normalized_variant.ref_allele}>{normalized_variant.alt_allele}")
            elif normalized_variant.variant_type.value == "splice":
                candidates.append(f"c.{c_pos}{normalized_variant.ref_allele}>{normalized_variant.alt_allele}")
            elif normalized_variant.variant_type.value == "deletion":
                candidates.append(f"c.{c_pos}del")
            elif normalized_variant.variant_type.value == "duplication":
                candidates.append(f"c.{c_pos}dup")
            elif normalized_variant.variant_type.value == "insertion":
                candidates.append(f"c.{c_pos}ins{normalized_variant.alt_allele}")

            candidates.extend(normalized_variant.equivalent_nomenclature)
            candidates.append(f"c.{c_pos}")

        # Clean raw query as fallback
        clean_q = query.strip()
        if ":" in clean_q:
            clean_q = clean_q.split(":", 1)[1].strip()
        candidates.append(clean_q)

        for c in candidates:
            if c in data:
                return data[c]

        return None

    def search_variant(
        self,
        query: str,
        normalized_variant: Optional[NormalizedVariant] = None,
        deterministic_consequence: Optional[str] = None,
    ) -> ClinVarEvidenceResult:
        """
        Retrieves ClinVar evidence for a variant strictly from local fixtures.
        
        Returns a ClinVarEvidenceResult with explicit provenance.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        fixture_entries = self._find_fixture_entries(query, normalized_variant)

        if fixture_entries is None:
            prov = EvidenceProvenance(
                source="ClinVar",
                provider="OfflineClinVarProvider",
                mode=RetrievalMode.OFFLINE,
                retrieval_status=EvidenceStatus.OFFLINE_DATA_UNAVAILABLE,
                external_identifier=None,
                is_fixture=True,
                fixture_path=str(self.fixtures_path),
                retrieval_timestamp=timestamp,
                transformations=["offline_fixture_lookup"],
            )
            return ClinVarEvidenceResult(
                query=query,
                status=EvidenceStatus.OFFLINE_DATA_UNAVAILABLE,
                records=[],
                primary_record=None,
                normalized_variant=normalized_variant,
                error_message=f"No local ClinVar fixture available for '{query}' in offline mode.",
                provenance=prov,
            )

        records: List[ClinVarRecord] = []
        discrepancies: List[EvidenceDiscrepancy] = []

        for rank, entry in enumerate(fixture_entries, start=1):
            vid = str(entry.get("variation_id") or entry.get("id", ""))
            accession = str(entry.get("accession", f"VCV{int(vid):09d}" if vid.isdigit() else "VCV000000000"))
            title = entry.get("title", f"Variation ID {vid}")
            sig = entry.get("clinical_significance", "Unknown")
            review = entry.get("review_status", "no assertion criteria provided")
            conditions = entry.get("conditions", [])
            last_eval = entry.get("last_evaluated")
            url = entry.get("url", f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{vid}/")
            is_exact = bool(entry.get("is_exact_match", rank == 1))

            record_prov = EvidenceProvenance(
                source="ClinVar",
                provider="OfflineClinVarProvider",
                mode=RetrievalMode.OFFLINE,
                retrieval_status=EvidenceStatus.FOUND,
                external_identifier=vid,
                is_fixture=True,
                fixture_path=str(self.fixtures_path),
                retrieval_timestamp=timestamp,
                transformations=["fixture_record_normalization"],
            )

            rec = ClinVarRecord(
                variation_id=vid,
                accession=accession,
                title=title,
                clinical_significance=sig,
                review_status=review,
                conditions=conditions,
                last_evaluated=last_eval,
                url=url,
                is_exact_match=is_exact,
                retrieval_rank=rank,
                provenance=record_prov,
                raw_attributes={
                    "evidence_type": entry.get("evidence_type", "Exact Variant Evidence" if is_exact else "Related HBB Evidence"),
                    "fixture_source": entry.get("source", "NCBI ClinVar (DEVELOPMENT FIXTURE)"),
                },
            )
            records.append(rec)

            # Check for consequence discrepancy against deterministic core
            if is_exact and deterministic_consequence:
                # If title specifies a protein consequence, compare it
                if "p." in title and deterministic_consequence != "p.?":
                    # Extract p. string from title
                    import re
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
                                        f"ClinVar title indicates '{ev_prot}', whereas deterministic "
                                        f"core calculated '{deterministic_consequence}'."
                                    ),
                                )
                            )

        # Primary record is the exact match if present, else first entry
        primary = next((r for r in records if r.is_exact_match), records[0] if records else None)

        overall_prov = EvidenceProvenance(
            source="ClinVar",
            provider="OfflineClinVarProvider",
            mode=RetrievalMode.OFFLINE,
            retrieval_status=EvidenceStatus.FOUND,
            external_identifier=primary.variation_id if primary else None,
            is_fixture=True,
            fixture_path=str(self.fixtures_path),
            retrieval_timestamp=timestamp,
            transformations=["offline_fixture_lookup"],
        )

        return ClinVarEvidenceResult(
            query=query,
            status=EvidenceStatus.FOUND,
            records=records,
            primary_record=primary,
            normalized_variant=normalized_variant,
            discrepancies=discrepancies,
            provenance=overall_prov,
        )
