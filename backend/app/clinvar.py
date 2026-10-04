"""NCBI ClinVar client using official E-utilities API with fixture fallback,
progressive tiered searching, deterministic exact match verification, and
strict three-tier evidence classification.
"""

from datetime import datetime, timezone
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import httpx

from app.config import settings
from app.models import ClinVarRecord

logger = logging.getLogger(__name__)

FIXTURES_PATH = settings.DATA_DIR / "fixtures" / "clinvar_fixtures.json"

# Three-tier evidence classification constants
TIER_EXACT = "EXACT VARIANT MATCH"
TIER_RELATED = "RELATED HBB RECORD"
TIER_GENERAL = "GENERAL HBB / BETA THALASSEMIA RECORD"

# Historical and literature aliases mapped to canonical cDNA notation
KNOWN_HBB_HISTORICAL_ALIASES: Dict[str, str] = {
    "cd39 c>t": "c.118C>T",
    "cd39": "c.118C>T",
    "cd 39": "c.118C>T",
    "codon 39": "c.118C>T",
    "codon 39 c>t": "c.118C>T",
    "codon 39 (c>t)": "c.118C>T",
    "q39*": "c.118C>T",
    "gln39ter": "c.118C>T",
    "p.gln39*": "c.118C>T",
    "q40*": "c.118C>T",
    "gln40ter": "c.118C>T",
    "p.gln40ter": "c.118C>T",
    "cd6 g>a": "c.19G>A",
    "cd6 a>t": "c.20A>T",
    "hbs": "c.20A>T",
    "hbc": "c.19G>A",
    "hbe": "c.79G>A",
    "cd26 g>a": "c.79G>A",
    "ivs-i-5": "c.92+5G>C",
    "ivs1-5": "c.92+5G>C",
    "ivs-1-5": "c.92+5G>C",
    "ivs-i-1": "c.92+1G>T",
    "ivs1-1": "c.92+1G>T",
    "ivs-1-1": "c.92+1G>T",
    "cd41/42": "c.124_127del",
    "cd 41/42": "c.124_127del",
    "cd8/9": "c.27dup",
    "cd 8/9": "c.27dup",
}

# Canonical equivalents in HBB mutation nomenclature
CANONICAL_EQUIVALENTS: Dict[str, str] = {
    "c.124_127del": "c.126_129del",
    "c.126_129del": "c.124_127del",
    "c.26_27insG": "c.27dup",
    "c.26_27insg": "c.27dup",
    "c.27dup": "c.26_27insG",
}


def _load_fixtures() -> Dict[str, List[dict]]:
    """Loads offline development fixtures if present."""
    if FIXTURES_PATH.exists():
        try:
            with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load ClinVar fixtures: {e}")
    return {}


def translate_genomic_to_cdna(genomic_term: str) -> Optional[str]:
    """
    Translates genomic coordinates on NG_000007.3 or GRCh38 to standard NM_000518.5 cDNA notation.

    Genomic locus architecture on RefSeqGene NG_000007.3:
    - Exon 1 coding (70595..70686): c.1..c.92
    - Intron 1 (70687..70816): c.92+1..c.92+130
    - Exon 2 (70817..71039): c.93..c.315 (Codon 40 c.118 is 70817 + 25 = 70842)
    - Intron 2 (71040..71889): c.315+1..c.315+850
    - Exon 3 coding (71890..72018): c.316..c.444

    Also handles historical literature notation NG_000007.3:g.70617C>T (calculated
    without Intron 1 offset for c.118).
    """
    g_clean = genomic_term.strip()
    m = re.search(r"g\.(\d+)([A-Za-z]+)>([A-Za-z]+)", g_clean, re.IGNORECASE)
    if not m:
        return None

    pos = int(m.group(1))
    ref = m.group(2).upper()
    alt = m.group(3).upper()

    # Historical literature offset (naive 70499 + 118 = 70617)
    if pos == 70617:
        return f"c.118{ref}>{alt}"

    # True RefSeqGene NG_000007.3 coordinates
    if 70817 <= pos <= 71039:
        c_pos = 93 + (pos - 70817)
        return f"c.{c_pos}{ref}>{alt}"
    if 70595 <= pos <= 70686:
        c_pos = pos - 70594
        return f"c.{c_pos}{ref}>{alt}"
    if 70687 <= pos <= 70816:
        c_pos = f"92+{pos - 70686}"
        return f"c.{c_pos}{ref}>{alt}"
    if 71040 <= pos <= 71889:
        c_pos = f"315+{pos - 71039}"
        return f"c.{c_pos}{ref}>{alt}"
    if 71890 <= pos <= 72018:
        c_pos = 316 + (pos - 71890)
        return f"c.{c_pos}{ref}>{alt}"

    return None


def classify_clinvar_record(
    title: str,
    c_term: Optional[str] = None,
    protein_change: Optional[str] = None,
    variant_aliases: Optional[List[str]] = None,
    raw_record: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, int]:
    """
    Deterministically evaluates a ClinVar record against the active target variant.

    Returns:
        (is_exact_match: bool, evidence_tier: str, priority_score: int)

    Evidence tiers:
    1. EXACT VARIANT MATCH (score 95-100):
       Matches exact coordinate, alteration alleles, and/or protein consequence.
       Explicitly excludes compound heterozygotes.
    2. RELATED HBB RECORD (score 30-60):
       Variants in the HBB gene at different positions, different alleles, or compound heterozygotes.
    3. GENERAL HBB / BETA THALASSEMIA RECORD (score 20):
       Gene-level, condition-level, or unspecific records in HBB.
    """
    if not title:
        return False, TIER_GENERAL, 0

    title_clean = title.strip()
    raw = raw_record or {}
    genes = raw.get("genes", [])
    is_hbb = (
        "HBB" in title_clean
        or any(g.get("symbol") == "HBB" or str(g.get("geneid")) == "3043" for g in genes)
    )
    if not is_hbb:
        return False, TIER_GENERAL, 0

    # 1. Compound / Complex allele disqualification
    v_set = raw.get("variation_set", [])
    var_obj = v_set[0] if v_set else {}
    cdna_change = var_obj.get("cdna_change", "")
    if "[" in title_clean or ";" in title_clean or "[" in cdna_change or ";" in cdna_change:
        # Compound heterozygotes or multi-variant genotypes containing the variant
        return False, TIER_RELATED, 40

    # 2. Target Variation ID / VCV match
    target_id = raw.get("query_target_id")
    if target_id:
        t_str = str(target_id)
        if (
            t_str == str(raw.get("uid", ""))
            or t_str == str(raw.get("id", ""))
            or f"VCV{int(t_str):09d}" == str(raw.get("accession", ""))
            or t_str.upper() == str(raw.get("accession", "")).upper()
        ):
            return True, TIER_EXACT, 100

    # 3. Exact cDNA and allele verification
    if c_term:
        c_clean = c_term.strip()
        escaped = re.escape(c_clean)
        pattern = rf"(?::|\b){escaped}(?:\s|\(|$)"
        if re.search(pattern, title_clean) or re.search(pattern, cdna_change):
            # Strict substitution allele check (e.g. c.118C>T must not match c.118C>A)
            sub_m = re.match(r"^c\.(\*?-?\d+)([A-Za-z]+)>([A-Za-z]+)$", c_clean)
            if sub_m:
                req_alt = sub_m.group(3).upper()
                title_sub = re.search(
                    rf"(?::|\b)c\.{re.escape(sub_m.group(1))}[A-Za-z]>([A-Za-z])(?:\s|\(|$)",
                    title_clean,
                )
                if title_sub and title_sub.group(1).upper() != req_alt:
                    # Same position, different alt allele -> RELATED, not exact
                    return False, TIER_RELATED, 60
            return True, TIER_EXACT, 100

        # Canonical equivalent check (e.g. c.124_127del <-> c.126_129del)
        if c_clean in CANONICAL_EQUIVALENTS:
            eq_target = CANONICAL_EQUIVALENTS[c_clean]
            eq_esc = re.escape(eq_target)
            eq_pattern = rf"(?::|\b){eq_esc}(?:[A-Za-z]+)?(?:\s|\(|$)"
            if re.search(eq_pattern, title_clean) or re.search(eq_pattern, cdna_change):
                return True, TIER_EXACT, 100

        # Deletion / insertion query allowing base sequence suffix in title
        if "del" in c_clean or "ins" in c_clean or "dup" in c_clean:
            del_pattern = rf"(?::|\b){escaped}(?:[A-Za-z]+)?(?:\s|\(|$)"
            if re.search(del_pattern, title_clean) or re.search(del_pattern, cdna_change):
                return True, TIER_EXACT, 100

    # 4. Protein consequence verification
    prot_field = raw.get("protein_change", "")
    if protein_change:
        p_clean = protein_change.strip()
        if p_clean in title_clean or (prot_field and prot_field.strip().upper() == p_clean.upper()):
            return True, TIER_EXACT, 100
        p_sub = re.match(r"^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|\*|Ter)$", p_clean)
        if p_sub:
            aa_pos = p_sub.group(2)
            if (
                f"p.Gln{aa_pos}Ter" in title_clean
                or f"Q{aa_pos}*" in title_clean
                or f"Q{aa_pos}*" == prot_field
            ):
                return True, TIER_EXACT, 100

    # 5. Historical aliases check from variation_set record metadata
    record_aliases = [str(a).strip().lower() for a in var_obj.get("aliases", [])]
    if variant_aliases:
        for valias in variant_aliases:
            va_norm = valias.strip().lower()
            if va_norm in record_aliases:
                if c_term and re.search(r"\bc\.\d+", title_clean):
                    c_pos_m = re.search(r"\bc\.(\d+)", c_term)
                    if c_pos_m and f"c.{c_pos_m.group(1)}" in title_clean:
                        return True, TIER_EXACT, 95
                elif not c_term:
                    return True, TIER_EXACT, 95

    # 6. Related variant vs General HBB record
    if re.search(r"c\.[0-9_+-]+[A-Za-z0-9>_delinstup]+", title_clean):
        if c_term:
            sub_m = re.match(r"^c\.(\*?-?\d+)", c_term)
            if sub_m and f"c.{sub_m.group(1)}" in title_clean:
                # Same position in HBB
                return False, TIER_RELATED, 60
        return False, TIER_RELATED, 30

    return False, TIER_GENERAL, 20


def is_exact_match_title(title: str, c_term: Optional[str] = None) -> bool:
    """Backward compatible check for exact variant match from title string."""
    is_exact, _, _ = classify_clinvar_record(title, c_term=c_term)
    return is_exact


async def fetch_clinvar_records(
    query_term: str,
    max_results: int = 8,
    timeout_seconds: float = 8.0,
    transcript_accession: str = "NM_000518.5",
    variant_aliases: Optional[List[str]] = None,
    protein_change: Optional[str] = None,
) -> List[ClinVarRecord]:
    """
    Retrieves and classifies ClinVar records for a genomic variant using NCBI E-utilities.

    Hardened Features:
    - Progressive query strategy (exact transcript HGVS, cDNA Variant Name, protein consequence, aliases, genomic translation)
    - Increased candidate retrieval window (retmax=50) to prevent truncation of true records
    - Deterministic post-retrieval verification comparing coordinate, alleles, and protein consequences
    - Explicit exclusion of compound heterozygotes from exact variant match status
    - Rigorous three-tier evidence classification (EXACT VARIANT MATCH, RELATED HBB RECORD, GENERAL HBB RECORD)
    - Ranking algorithm placing exact single variant records at index 0
    - Graceful empty response when no ClinVar record exists (zero hallucinated records)
    - Verified fixture fallback when NCBI network is unreachable
    """
    clean_term = query_term.strip()
    if not clean_term:
        return []

    # Check for direct Variation ID / VCV accession
    vid_match = re.match(
        r"^(?:VCV0*(\d+)|(\d{4,8}))(?:\s*\[Variation ID\])?$",
        clean_term,
        re.IGNORECASE,
    )
    query_target_id = vid_match.group(1) or vid_match.group(2) if vid_match else None

    # Genomic coordinate translation
    g_mapped_c = translate_genomic_to_cdna(clean_term)

    # Historical alias normalization
    norm_alias_key = clean_term.lower()
    mapped_alias_c = KNOWN_HBB_HISTORICAL_ALIASES.get(norm_alias_key)

    # Extract cDNA term if present
    c_match = re.search(r"(c\.[0-9_+-]+[A-Za-z0-9>_delinstup]+)", clean_term)
    c_term = (
        c_match.group(1)
        if c_match
        else (mapped_alias_c or g_mapped_c or (clean_term if clean_term.startswith("c.") else None))
    )

    # Detect protein query
    p_match = re.search(r"(p\.[A-Za-z0-9*]+)", clean_term)
    active_prot = protein_change or (p_match.group(1) if p_match else None)

    base_url = settings.NCBI_BASE_URL
    id_list: List[str] = []

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        # Tier 1: Direct Variation ID query
        if query_target_id:
            try:
                params_vid = {
                    "db": "clinvar",
                    "term": f"{query_target_id}[Variation ID]",
                    "retmode": "json",
                    "retmax": "10",
                }
                if settings.NCBI_API_KEY:
                    params_vid["api_key"] = settings.NCBI_API_KEY
                if settings.NCBI_EMAIL:
                    params_vid["email"] = settings.NCBI_EMAIL

                resp = await client.get(f"{base_url}/esearch.fcgi", params=params_vid)
                if resp.status_code == 200:
                    id_list = resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as e:
                logger.warning(f"ClinVar Variation ID search failed: {e}")

        # Tier 1: Quoted transcript cDNA query
        if not id_list and c_term:
            queries_tier1 = [
                f'"{c_term}"[Variant Name] AND HBB[Gene Name]',
                f'"{transcript_accession}:{c_term}"',
            ]
            for t_query in queries_tier1:
                try:
                    params_search = {
                        "db": "clinvar",
                        "term": t_query,
                        "retmode": "json",
                        "retmax": "50",
                    }
                    if settings.NCBI_API_KEY:
                        params_search["api_key"] = settings.NCBI_API_KEY
                    if settings.NCBI_EMAIL:
                        params_search["email"] = settings.NCBI_EMAIL

                    resp = await client.get(f"{base_url}/esearch.fcgi", params=params_search)
                    if resp.status_code == 200:
                        ids = resp.json().get("esearchresult", {}).get("idlist", [])
                        if ids:
                            id_list = ids
                            break
                except Exception as e:
                    logger.warning(f"Tier 1 ClinVar esearch failed for '{t_query}': {e}")

        # Tier 2: Protein consequence query
        if not id_list and active_prot:
            try:
                params_prot = {
                    "db": "clinvar",
                    "term": f'"{active_prot}"[Variant Name] AND HBB[Gene Name]',
                    "retmode": "json",
                    "retmax": "50",
                }
                if settings.NCBI_API_KEY:
                    params_prot["api_key"] = settings.NCBI_API_KEY
                if settings.NCBI_EMAIL:
                    params_prot["email"] = settings.NCBI_EMAIL

                resp = await client.get(f"{base_url}/esearch.fcgi", params=params_prot)
                if resp.status_code == 200:
                    id_list = resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as e:
                logger.warning(f"Tier 2 protein esearch failed: {e}")

        # Tier 3: Gene-scoped cDNA query
        if not id_list and c_term:
            try:
                params_c = {
                    "db": "clinvar",
                    "term": f'HBB[Gene Name] AND "{c_term}"',
                    "retmode": "json",
                    "retmax": "50",
                }
                if settings.NCBI_API_KEY:
                    params_c["api_key"] = settings.NCBI_API_KEY
                if settings.NCBI_EMAIL:
                    params_c["email"] = settings.NCBI_EMAIL

                resp = await client.get(f"{base_url}/esearch.fcgi", params=params_c)
                if resp.status_code == 200:
                    id_list = resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as e:
                logger.warning(f"Tier 3 gene-scoped esearch failed: {e}")

        # Tier 4: Canonical equivalents & aliases
        if not id_list and c_term and c_term in CANONICAL_EQUIVALENTS:
            eq_target = CANONICAL_EQUIVALENTS[c_term]
            try:
                params_eq = {
                    "db": "clinvar",
                    "term": f'"{eq_target}"[Variant Name] AND HBB[Gene Name]',
                    "retmode": "json",
                    "retmax": "50",
                }
                if settings.NCBI_API_KEY:
                    params_eq["api_key"] = settings.NCBI_API_KEY
                if settings.NCBI_EMAIL:
                    params_eq["email"] = settings.NCBI_EMAIL

                resp = await client.get(f"{base_url}/esearch.fcgi", params=params_eq)
                if resp.status_code == 200:
                    id_list = resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as e:
                logger.warning(f"Tier 4 canonical esearch failed: {e}")

        # Tier 5: Broad query fallback
        if not id_list:
            search_query = clean_term if "HBB" in clean_term else f"HBB[gene] AND {clean_term}"
            try:
                params_broad = {
                    "db": "clinvar",
                    "term": search_query,
                    "retmode": "json",
                    "retmax": "50",
                }
                if settings.NCBI_API_KEY:
                    params_broad["api_key"] = settings.NCBI_API_KEY
                if settings.NCBI_EMAIL:
                    params_broad["email"] = settings.NCBI_EMAIL

                resp = await client.get(f"{base_url}/esearch.fcgi", params=params_broad)
                if resp.status_code == 200:
                    id_list = resp.json().get("esearchresult", {}).get("idlist", [])
            except Exception as e:
                logger.warning(f"Broad ClinVar esearch failed: {e}")
                return _check_fixture_fallback(
                    clean_term, c_term, transcript_accession, variant_aliases, active_prot
                )

        if not id_list:
            return _check_fixture_fallback(
                clean_term, c_term, transcript_accession, variant_aliases, active_prot
            )

        # Batch summary retrieval for all candidate IDs
        try:
            params_sum = {
                "db": "clinvar",
                "id": ",".join(id_list),
                "retmode": "json",
            }
            if settings.NCBI_API_KEY:
                params_sum["api_key"] = settings.NCBI_API_KEY
            if settings.NCBI_EMAIL:
                params_sum["email"] = settings.NCBI_EMAIL

            sum_resp = await client.get(f"{base_url}/esummary.fcgi", params=params_sum)
            if sum_resp.status_code != 200:
                logger.warning(f"ClinVar esummary failed with status {sum_resp.status_code}")
                return _check_fixture_fallback(
                    clean_term, c_term, transcript_accession, variant_aliases, active_prot
                )

            sum_data = sum_resp.json()
            results_dict = sum_data.get("result", {})
            retrieval_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            evaluated_records: List[Tuple[int, ClinVarRecord]] = []

            for vid in id_list:
                if vid in results_dict:
                    raw = results_dict[vid]
                    if query_target_id:
                        raw["query_target_id"] = query_target_id

                    germline = raw.get("germline_classification", {}) or {}
                    traits_raw = germline.get("trait_set", []) or []
                    conditions = [
                        t.get("trait_name")
                        for t in traits_raw
                        if t and t.get("trait_name") and t.get("trait_name") != "not provided"
                    ]
                    accession_val = raw.get("accession") or f"VCV{int(vid):09d}"
                    title = raw.get("title", f"Variation ID {vid}")

                    is_exact, ev_tier, score = classify_clinvar_record(
                        title=title,
                        c_term=c_term,
                        protein_change=active_prot,
                        variant_aliases=variant_aliases,
                        raw_record=raw,
                    )

                    if score > 0:
                        rec = ClinVarRecord(
                            id=vid,
                            title=title,
                            accession=accession_val,
                            clinical_significance=germline.get("description", "Unknown"),
                            review_status=germline.get("review_status", "no assertion provided"),
                            conditions=conditions[:8],
                            last_evaluated=germline.get("last_evaluated"),
                            variation_id=vid,
                            source="Live NCBI ClinVar",
                            url=f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{vid}/",
                            is_exact_match=is_exact,
                            evidence_type=ev_tier,
                            retrieval_date=retrieval_date_str,
                        )
                        evaluated_records.append((score, rec))

            # Prioritize and sort by score descending
            evaluated_records.sort(key=lambda item: -item[0])
            sorted_records = [rec for _, rec in evaluated_records]
            return sorted_records[:max_results]

        except Exception as exc:
            logger.warning(f"Live ClinVar summary request failed: {exc}")
            return _check_fixture_fallback(
                clean_term, c_term, transcript_accession, variant_aliases, active_prot
            )


def _check_fixture_fallback(
    term: str,
    c_term: Optional[str] = None,
    transcript_accession: str = "NM_000518.5",
    variant_aliases: Optional[List[str]] = None,
    protein_change: Optional[str] = None,
) -> List[ClinVarRecord]:
    """Provides verified fixture data if offline or network error."""
    fixtures = _load_fixtures()
    lookup_key = c_term if c_term else term
    retrieval_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for key, items in fixtures.items():
        if key in lookup_key or lookup_key in key or key in term:
            logger.info(f"Using verified development fixture for ClinVar query: {term}")
            evaluated_records: List[Tuple[int, ClinVarRecord]] = []
            for item in items:
                rec_dict = dict(item)
                title = rec_dict.get("title", "")
                is_exact, ev_tier, score = classify_clinvar_record(
                    title=title,
                    c_term=c_term or key,
                    protein_change=protein_change,
                    variant_aliases=variant_aliases,
                    raw_record={"genes": [{"symbol": "HBB", "geneid": "3043"}]},
                )
                rec = ClinVarRecord(**rec_dict)
                rec.source = "Development Fixture (NCBI ClinVar)"
                rec.is_exact_match = is_exact
                rec.evidence_type = ev_tier
                rec.retrieval_date = retrieval_date_str
                evaluated_records.append((score, rec))

            evaluated_records.sort(key=lambda item: -item[0])
            return [rec for _, rec in evaluated_records]

    return []
