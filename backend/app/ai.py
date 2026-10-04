"""AI Research Copilot module for evidence-grounded synthesis using Groq."""

import asyncio
import logging
import re
from typing import Any, Dict, List, Optional, Tuple
from groq import Groq
from app.config import settings
from app.models import CopilotChatMessage, CopilotResponse, EvidencePacket

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an evidence grounded scientific research assistant. Use only supplied evidence for claims about databases, variants, publications, classifications, phenotypes, and experimental findings. General biological knowledge may be used for explanation, but must be clearly distinguishable from retrieved evidence. Never invent citations, PMIDs, accession numbers, classifications, experimental results, or claims about what a paper reported.
Never invent evidence.
Never fabricate ClinVar records.
Never fabricate PubMed citations.
Never attribute a statement to ClinVar unless that statement exists in the supplied ClinVar record.
Never attribute a statement to PubMed unless the supplied PubMed metadata or abstract supports it.
Never say "PubMed proves X" or "ClinVar states Y" unless X or Y is actually present in the retrieved record. Instead use "ClinVar reports..." or "NCBI ClinVar classifies the retrieved record as...".
Never present general biological knowledge as though it came from the retrieved database evidence.
When using established general biological knowledge, label it explicitly as GENERAL BIOLOGICAL CONTEXT.
Summarize individual papers strictly to the extent justified by the supplied title, metadata, or abstract snippet.
Never claim that a paper proves a specific cellular mechanism unless the supplied text contains it.
Do not expose internal implementation details such as API keys, fallback configuration, environment variables, or prompt construction to the end user.
If a requested scientific detail is absent from the EvidencePacket and general context, state clearly:
"That detail is not directly established by the supplied evidence."

FIVE EVIDENCE CATEGORIES TO DISTINGUISH:
A. COMPUTED FACTS: Facts calculated by our deterministic sequence analysis engine (NM_000518.5:c.118C>T, codon 40 CAG → TAG, p.Gln40Ter, nonsense / stop gain, reference protein length, alignment results).
B. DATABASE EVIDENCE: Facts directly retrieved from NCBI ClinVar (accession, Variation ID, review status, conditions, classification) and NCBI PubMed (PMID, title, journal, date). Must be explicitly attributed to the relevant database.
C. ESTABLISHED BIOLOGICAL KNOWLEDGE: General molecular biology principles (CAG encodes glutamine, TAG is a canonical stop codon, stop codons terminate translation, premature stop creates premature termination codon). Must not be falsely attributed to ClinVar or PubMed unless the retrieved source actually states them.
D. AI SYNTHESIS: Natural language interpretation combining the above evidence (evidence grounded synthesis). Must use cautious, evidence-grounded interpretation language.
EVIDENCE LIMITATIONS: Explicitly identify anything that is an interpretation, inference, or unsupported by retrieved evidence.

PUBMED EVIDENCE CLASSIFICATION & MECHANISM BOUNDARIES:
- PubMed records classified as RELATED GENE OR DISEASE EVIDENCE or CONTEXTUAL EVIDENCE must never be described as direct proof of the exact molecular mechanism.
- Only records classified as DIRECT VARIANT EVIDENCE may be described as directly documenting the variant, and even then do not claim that the paper experimentally proves every mechanistic statement unless the retrieved article evidence actually supports it.

NOMENCLATURE DISTINCTION (HBB c.118C>T / p.Gln40Ter):
For the HBB variant NM_000518.5:c.118C>T, p.Gln40Ter, clearly distinguish:
- HGVS reference nomenclature: NM_000518.5:c.118C>T, p.Gln40Ter
- Historical nomenclature: CD39 C>T, Q39*, Gln39Ter, Codon 39 C>T
Explain that the numbering difference results from historical mature beta globin protein numbering after removal of the initiator methionine, whereas HGVS transcript based numbering includes the initiating methionine. Do not present these as separate variants.

CAG TO TAG EXPLANATION:
"CAG encodes glutamine. The C to T substitution changes CAG at codon 40 into TAG, which is a canonical translation termination codon. The ribosome therefore terminates translation at this newly created stop signal, producing a 39 amino acid peptide rather than the full length beta globin protein. This is classified as a nonsense or stop gain variant, p.Gln40Ter."
Do not overstate structural consequences unless directly supported.

NONSENSE MEDIATED DECAY (NMD) LANGUAGE:
Do not state the exact exon junction distance or the 50 to 55 nucleotide rule as a computed fact unless the application has actually calculated the relevant exon and exon junction coordinates from the reference transcript.
Use conservative wording:
"Because this is an early premature termination codon, nonsense mediated decay may contribute to reduced mutant transcript abundance. This is a biological interpretation and is not directly established by the codon calculation."

STRICT SCIENTIFIC CLAIM BOUNDARIES:
- The model must NOT state as experimentally established:
  * "The mutant protein is definitely produced."
  * "The truncated protein definitely folds incorrectly."
  * "The protein definitely lacks the heme pocket."
  * "NMD definitely occurs."
  * "The mutation definitely causes degradation of the transcript."
- Instead use scientifically appropriate wording:
  * "is expected to substantially truncate the encoded protein"
  * "may contribute to reduced mutant transcript abundance"
  * "is consistent with a loss of functional beta-globin"
  * "represents a biological interpretation rather than an experimentally established fact in this analysis"
- Never turn a general biological possibility into a database supported fact.

CANONICAL SECTION STRUCTURE (EACH HEADING AT MOST ONCE):
You must structure your response using exactly these sections in order, using level-2 headings (##) and without duplicate headers:

## DIRECT SCIENTIFIC ANSWER
Provide the concise, direct scientific answer upfront. For premature termination inquiries, state:
"CAG encodes glutamine. The C to T substitution changes codon 40 from CAG to TAG. TAG is a canonical stop codon, so the ribosome terminates translation at that position. Because this occurs before the normal end of the beta globin coding sequence, the variant is a premature termination or nonsense variant, annotated as p.Gln40Ter."

## A. COMPUTED FACTS
State deterministic engine calculations: coordinates, codon 40 CAG to TAG, p.Gln40Ter nonsense consequence, 147 canonical codons.
Distinguish HGVS reference nomenclature (NM_000518.5:c.118C>T, p.Gln40Ter) from historical nomenclature (CD39 C>T, Q39*, Gln39Ter) and explain initiator methionine numbering.

## B. DATABASE EVIDENCE
State retrieved NCBI ClinVar records and NCBI PubMed literature. Do not use nested ## or ### headings.

## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
Explain universal molecular biology mechanisms: universal genetic code, codon recognition by aminoacyl-tRNAs vs release factors, ribosomal translation termination.

## D. AI SYNTHESIS
Provide a scientific synthesis tying together computed and retrieved facts using cautious, evidence-grounded interpretation language.

## EVIDENCE LIMITATIONS
Explicitly state biological interpretations (such as NMD) vs directly established facts, stating what is not established.
"""


def format_structured_evidence_context(packet: EvidencePacket) -> str:
    """
    Builds a structured, unambiguous evidence context distinguishing:
    - 1. COMPUTED RESULT (DETERMINISTIC BIOINFORMATICS) / A. COMPUTED BIOINFORMATICS RESULT
    - 2. NCBI CLINVAR DATABASE EVIDENCE / B. DATABASE EVIDENCE
    - 3. NCBI PUBMED SCIENTIFIC LITERATURE EVIDENCE
    - SCIENTIFIC LIMITATIONS & PIPELINE CONSTRAINTS
    """
    sections: List[str] = []

    # A. Computed Result
    ref_info = (
        f"Accession: {packet.reference_accession} (RefSeq MANE Select, CCDS7753.1)\n"
        f"Gene Symbol: {packet.gene_symbol}\n"
        f"Total Length: {packet.summary.get('reference_length_bp', 628)} bp\n"
        f"CDS Coordinates: {packet.summary.get('cds_coordinates', '51..494')} ({packet.summary.get('cds_length_bp', 444)} bp coding sequence, 147 codons)\n"
        f"Sequence Identity: {packet.summary.get('sequence_identity_pct', 100.0)}%"
    )

    var_lines = []
    for idx, v in enumerate(packet.variants, 1):
        lines = [
            f"- Variant #{idx}:",
            f"  - Canonical HGVS cDNA: {v.hgvs_c}",
            f"  - DNA Change: c.{v.c_position}{v.ref_allele}>{v.alt_allele} (mRNA pos {v.ref_position_mrna})",
            f"  - Canonical HGVS Protein: {v.hgvs_p or 'None'}",
            f"  - Molecular Consequence: {v.functional_impact}",
        ]
        if v.codon_change:
            lines.extend([
                f"  - Codon Number: {v.codon_change.codon_number} (of 147 canonical codons)",
                f"  - Reference Codon: {v.codon_change.ref_codon} (encodes {v.codon_change.ref_aa} / {v.codon_change.ref_aa_single} - Glutamine)",
                f"  - Altered Sample Codon: {v.codon_change.sample_codon} (encodes {v.codon_change.sample_aa} / {v.codon_change.sample_aa_single} - Stop / Ter)",
                f"  - Premature Termination (Stop-gain): {'Yes (Nonsense)' if v.codon_change.is_stop_gain else 'No'}",
            ])
        if getattr(v, "equivalent_nomenclature", None):
            aliases_str = ", ".join(v.equivalent_nomenclature)
            lines.append(f"  - Historical & Equivalent Nomenclature: {aliases_str}")
        if getattr(v, "nomenclature_notes", None):
            lines.append(f"  - Nomenclature Note (Mature vs. Reference Numbering): {v.nomenclature_notes}")
        var_lines.append("\n".join(lines))

    comp_body = f"Reference Transcript:\n{ref_info}\n\nDetected Variants & Consequences:\n"
    if var_lines:
        comp_body += "\n\n".join(var_lines)
    else:
        comp_body += "No sequence variants detected (100% identity to reference NM_000518.5)."

    sections.append(f"### 1. COMPUTED RESULT (DETERMINISTIC BIOINFORMATICS)\n{comp_body}")

    # B. ClinVar Database Evidence
    cv_lines = []
    for c in packet.clinvar_records:
        conds = ", ".join(c.conditions) if c.conditions else "None listed"
        ev_type = getattr(c, "evidence_type", "DIRECT VARIANT EVIDENCE" if getattr(c, "is_exact_match", False) else "RELATED GENE OR DISEASE EVIDENCE")
        ret_date = getattr(c, "retrieval_date", "Today")
        cv_lines.append(
            f"- Accession: {c.accession} | Variation ID: {c.id}\n"
            f"  Relevance Level: {ev_type}\n"
            f"  Evidence Classification: {ev_type}\n"
            f"  Title: {c.title}\n"
            f"  Clinical Significance (Database Record): {c.clinical_significance}\n"
            f"  Review Status: {c.review_status}\n"
            f"  Associated Conditions in Record: {conds}\n"
            f"  Retrieval Date: {ret_date}\n"
            f"  Database URL: {c.url}"
        )
    cv_sec = "### 2. NCBI CLINVAR DATABASE EVIDENCE\n" + ("\n\n".join(cv_lines) if cv_lines else "No matching ClinVar records retrieved for this query.")

    # B. PubMed Scientific Literature Evidence
    pm_lines = []
    for p in packet.pubmed_records:
        auths = ", ".join(p.authors[:4]) if p.authors else "Authors not listed"
        ev_type = getattr(p, "evidence_type", "DIRECT VARIANT EVIDENCE" if getattr(p, "is_exact_match", False) else "RELATED GENE OR DISEASE EVIDENCE")
        ret_date = getattr(p, "retrieval_date", "Today")
        abstract_desc = f"\n  Abstract / Snippet: {p.abstract_snippet}" if p.abstract_snippet else "\n  Abstract / Snippet: Not supplied in retrieval packet (Title & metadata only)"
        pm_lines.append(
            f"- PMID: {p.pmid}\n"
            f"  Relevance Level: {ev_type}\n"
            f"  Evidence Classification: {ev_type}\n"
            f"  Title: \"{p.title}\"\n"
            f"  Authors: {auths}\n"
            f"  Journal: {p.journal} ({p.pub_date})\n"
            f"  Retrieval Date: {ret_date}{abstract_desc}\n"
            f"  URL: {p.url}"
        )
    pm_sec = f"### 3. NCBI PUBMED SCIENTIFIC LITERATURE EVIDENCE ({len(packet.pubmed_records)} retrieved records):\n" + ("\n\n".join(pm_lines) if pm_lines else "No matching PubMed literature retrieved for this query.")

    sections.append(f"### B. DATABASE EVIDENCE (RETRIEVED NCBI EVIDENCE)\n{cv_sec}\n\n{pm_sec}")

    # Limitations
    if packet.limitations:
        lims = "\n".join(f"- {lim}" for lim in packet.limitations)
        sections.append(f"### SCIENTIFIC LIMITATIONS & PIPELINE CONSTRAINTS\n{lims}")

    return "\n\n".join(sections)


def validate_ai_synthesis(
    answer_text: str,
    packet: EvidencePacket
) -> Tuple[bool, Optional[str]]:
    """
    Post-generation verification layer enforcing provenance integrity:
    1. Rejects empty responses.
    2. Validates gene name consistency ("HBB").
    3. Validates active variant presence (cDNA, protein, or equivalent alias).
    4. Validates consequence consistency (nonsense / premature stop / termination).
    5. Preserves ClinVar classification (rejects contradictory benign claims for pathogenic records).
    6. Strict PMID provenance check: every cited PMID in the text MUST exist in packet.pubmed_records.
    """
    if not answer_text or not answer_text.strip():
        return False, "empty_answer"

    text = answer_text.strip()
    text_lower = text.lower()

    # 0. Secret / API key leakage prevention
    if re.search(r"gsk_[a-zA-Z0-9]{20,}", text):
        return False, "api_key_leakage_detected: output contains Groq API key pattern"
    if "api_key" in text_lower and ("sk-" in text_lower or "bearer" in text_lower or "gsk" in text_lower):
        return False, "credential_leakage_detected: credential pattern found in output"

    # 1. Gene name consistency
    if packet.variants and packet.gene_symbol:
        gene_terms = [packet.gene_symbol.lower(), "beta-globin", "beta globin", "globin", "thalassemia", "cd39", "hemoglobin"]
        if not any(k in text_lower for k in gene_terms):
            return False, f"gene_name_missing: expected {packet.gene_symbol}"

    # 2. Active variant presence
    if packet.variants:
        v = packet.variants[0]
        # Build list of valid identifiers for this variant
        valid_terms = [
            v.hgvs_c.lower(),
            f"c.{v.c_position}".lower(),
            f"{v.c_position}{v.ref_allele}>{v.alt_allele}".lower(),
        ]
        if v.hgvs_p:
            valid_terms.append(v.hgvs_p.lower())
            valid_terms.append(v.hgvs_p.replace("p.", "").lower())
        if getattr(v, "equivalent_nomenclature", None):
            for alias in v.equivalent_nomenclature:
                valid_terms.append(alias.lower())

        found_variant = any(term in text_lower for term in valid_terms if term)
        if not found_variant:
            return False, f"active_variant_missing: neither {v.hgvs_c} nor equivalent nomenclature found"

        # 3. Consequence consistency
        if v.functional_impact == "Nonsense" or (v.codon_change and v.codon_change.is_stop_gain):
            stop_keywords = ["nonsense", "stop", "termination", "terminat", "truncated", "truncation"]
            if not any(k in text_lower for k in stop_keywords):
                return False, "consequence_inconsistent: nonsense/stop-gain consequence not acknowledged"

    # 4. ClinVar classification preservation
    if packet.clinvar_records:
        for c in packet.clinvar_records:
            sig = c.clinical_significance.lower()
            if "pathogenic" in sig and "conflict" not in sig:
                # Ensure the synthesis doesn't falsely claim the variant is benign
                if re.search(r"\b(classified as|is|deemed|considered)\s+(benign|likely benign)\b", text_lower):
                    return False, f"clinvar_contradiction: variant with ClinVar {c.clinical_significance} claimed as benign"

    # 5. Strict PMID provenance check
    # Find all cited PMIDs in answer_text
    cited_pmid_matches = re.findall(r"\bPMID[:\s#]*([0-9]{5,9})\b", text, re.IGNORECASE)
    pubmed_matches = re.findall(r"\bPubMed\s*(?:ID|record|paper)?[:\s#]*([0-9]{5,9})\b", text, re.IGNORECASE)
    all_cited_pmids = set(cited_pmid_matches + pubmed_matches)

    valid_pmids = {p.pmid.strip() for p in packet.pubmed_records if p.pmid}

    for cited in all_cited_pmids:
        if cited not in valid_pmids:
            return False, f"hallucinated_pmid: {cited} cited in synthesis but not present in retrieved EvidencePacket"

    return True, None


def normalize_canonical_sections(text: str) -> str:
    """
    Guarantees that generated AI or fallback responses contain each canonical
    provenance section at most once, in canonical scientific order:
    1. ## DIRECT SCIENTIFIC ANSWER
    2. ## A. COMPUTED FACTS
    3. ## B. DATABASE EVIDENCE
    4. ## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
    5. ## D. AI SYNTHESIS
    6. ## EVIDENCE LIMITATIONS
    Merges duplicate sections and strips internal heading echoes.
    """
    if not text or not text.strip():
        return text

    d_title = "D. DETERMINISTIC SYNTHESIS" if ("deterministic synthesis" in text.lower()) else "D. AI SYNTHESIS"

    canonical_order = [
        "DIRECT SCIENTIFIC ANSWER",
        "A. COMPUTED FACTS",
        "B. DATABASE EVIDENCE",
        "C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
        d_title,
        "EVIDENCE LIMITATIONS",
    ]

    canonical_pattern = re.compile(
        r"^(?:#{1,3}\s+)?(?:"
        r"DIRECT\s+SCIENTIFIC\s+ANSWER|"
        r"[A-D]\.\s+(?:COMPUTED|DATABASE|ESTABLISHED|AI|DETERMINISTIC)|"
        r"EVIDENCE\s+LIMITATIONS)",
        re.IGNORECASE,
    )

    lines = text.splitlines()
    has_canonical_structure = any(canonical_pattern.match(l.strip()) for l in lines)
    if not has_canonical_structure:
        return text

    def get_canonical_category(header: str) -> Optional[str]:
        h = header.lower().strip()
        h = re.sub(r"^[#\s\*\-]+|[#\s\*\-]+$", "", h).strip()
        if not h:
            return None
        if re.search(r"\bdirect\s+(?:scientific\s+)?answer\b", h):
            return "DIRECT SCIENTIFIC ANSWER"
        if re.search(r"\bdatabase\s+evidence\b|\bclinvar\b|\bpubmed\b|\bretrieved\s+ncbi\b", h):
            return "B. DATABASE EVIDENCE"
        if re.search(r"\bcomputed\s+(?:facts|analysis|bioinformatics)\b|^a\.\s*computed", h):
            return "A. COMPUTED FACTS"
        if re.search(r"\bestablished\b|\bgeneral\s+biological\b|\bbiological\s+context\b|\bbiological\s+knowledge\b", h):
            return "C. ESTABLISHED BIOLOGICAL KNOWLEDGE"
        if re.search(r"\b(?:ai|scientific|deterministic)\s+synthesis\b|\blive\s+groq\b", h):
            return d_title
        if re.search(r"\blimitation", h):
            return "EVIDENCE LIMITATIONS"
        return None

    sections: Dict[str, List[str]] = {title: [] for title in canonical_order}
    current_sec = "DIRECT SCIENTIFIC ANSWER"
    notice_banner: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> **Notice:"):
            notice_banner = stripped
            continue

        header_candidate = stripped
        inline_body = ""
        if ":" in stripped and not stripped.startswith("#"):
            prefix, _, suffix = stripped.partition(":")
            if canonical_pattern.match(prefix.strip()):
                header_candidate = prefix.strip()
                inline_body = suffix.strip()

        is_heading = stripped.startswith("#") or bool(canonical_pattern.match(header_candidate))
        cat = get_canonical_category(header_candidate) if is_heading else None

        if cat:
            current_sec = cat
            if inline_body:
                sections[current_sec].append(inline_body)
        else:
            if not (stripped.startswith("#") and get_canonical_category(stripped)):
                sections[current_sec].append(line)

    output_parts: List[str] = []
    for title in canonical_order:
        body = "\n".join(sections[title]).strip()
        if body:
            output_parts.append(f"## {title}\n{body}")
            if title == "DIRECT SCIENTIFIC ANSWER" and notice_banner:
                output_parts.append(notice_banner)

    return "\n\n".join(output_parts)


def _generate_offline_synthesis(
    packet: EvidencePacket,
    question: str,
    reason: str = "no_key",
    error_message: Optional[str] = None
) -> CopilotResponse:
    """
    Generates an authoritative, unhallucinated deterministic summary when Groq
    API key is missing, when an error occurs, or when validation rejects an output.
    Separates findings into canonical categories with zero duplicated headings:
    ## DIRECT SCIENTIFIC ANSWER
    ## A. COMPUTED FACTS
    ## B. DATABASE EVIDENCE
    ## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
    ## D. AI SYNTHESIS
    ## EVIDENCE LIMITATIONS
    """
    evidence_used: List[str] = ["Deterministic Sequence Engine"]
    primary_v = packet.variants[0] if packet.variants else None

    # Determine direct question-first answer
    q_lower = question.lower()
    if primary_v and primary_v.codon_change and primary_v.codon_change.is_stop_gain:
        cc = primary_v.codon_change
        if "why" in q_lower or "premature" in q_lower or "stop" in q_lower or "termination" in q_lower or "cag" in q_lower:
            direct_answer = (
                "CAG encodes glutamine, whereas TAG is a termination codon. "
                "The C to T substitution therefore converts codon 40 from a sense codon into a stop codon, producing p.Gln40Ter. "
                "TAG is a canonical stop codon, so the ribosome terminates translation at that position. "
                "Because this occurs before the normal end of the beta globin coding sequence, "
                "the variant is a premature termination or nonsense variant, annotated as p.Gln40Ter."
            )
        elif "clinvar" in q_lower:
            cv_sig = packet.clinvar_records[0].clinical_significance if packet.clinvar_records else "No ClinVar record"
            cv_varid = packet.clinvar_records[0].id if packet.clinvar_records else "N/A"
            direct_answer = (
                f"The retrieved ClinVar database records classify the active variant {primary_v.hgvs_c} "
                f"({primary_v.hgvs_p}, Variation ID {cv_varid}) as {cv_sig} for Beta thalassemia."
            )
        elif "pubmed" in q_lower or "literature" in q_lower or "paper" in q_lower:
            direct_answer = (
                "The system retrieved relevant PubMed literature associated with the variant or HBB/beta thalassemia context "
                "(including publications reporting the CD39 C>T pathogenic variant). These records represent retrieved "
                "literature rather than independent experimental validations conducted by this tool."
            )
        elif "mean" in q_lower or "what does" in q_lower:
            direct_answer = (
                f"{primary_v.hgvs_p} indicates that codon {cc.codon_number} of the HBB translation product, which normally encodes "
                f"glutamine ({cc.ref_aa}), is converted into a termination codon ({cc.sample_aa} / *). "
                f"This causes premature translation termination and is expected to produce a truncated {cc.codon_number - 1}-amino-acid polypeptide chain "
                f"instead of the full 147-amino-acid beta-globin protein."
            )
        else:
            direct_answer = (
                f"Deterministic bioinformatics analysis confirms that {primary_v.hgvs_c} produces {primary_v.hgvs_p} "
                f"at codon {cc.codon_number} of HBB (NM_000518.5), creating a premature translation termination codon."
            )
    else:
        direct_answer = (
            "Deterministic bioinformatics analysis confirms sequence coordinates and consequence for the active variant in HBB (NM_000518.5). "
            "Below is the authoritative evidence packet answering the research inquiry."
        )

    # Section A: Computed Facts
    var_descriptions: List[str] = []
    if packet.variants:
        for v in packet.variants:
            desc_lines = [
                "• **HGVS Reference Nomenclature**:",
                f"  - HGVS cDNA: {v.hgvs_c}",
                f"  - HGVS Protein: {v.hgvs_p or 'None'}",
                f"  - Molecular Consequence: {v.functional_impact}",
            ]
            if v.codon_change:
                desc_lines.append(
                    f"  - Codon Analysis: Codon {v.codon_change.codon_number} of 147 canonical codons "
                    f"({v.codon_change.ref_codon} [{v.codon_change.ref_aa}] → {v.codon_change.sample_codon} [{v.codon_change.sample_aa}]) "
                    f"({'Premature Stop-gain / Nonsense' if v.codon_change.is_stop_gain else v.codon_change.consequence})"
                )
            if getattr(v, "equivalent_nomenclature", None):
                equiv = ", ".join(v.equivalent_nomenclature)
                desc_lines.extend([
                    "• **Historical Literature Nomenclature**:",
                    f"  - Historical Aliases: {equiv}",
                ])
            if v.c_position == "118" or (v.codon_change and v.codon_change.codon_number == 40):
                desc_lines.append(
                    "  - Numbering Explanation: The numbering difference results from historical mature beta globin protein "
                    "numbering after removal of the initiator methionine, whereas HGVS transcript based numbering "
                    "includes the initiating methionine. Do not present these as separate variants."
                )
            elif getattr(v, "nomenclature_notes", None):
                desc_lines.append(
                    f"  - Numbering Explanation: {v.nomenclature_notes} "
                    "These refer to the identical mutation and are not separate variants."
                )
            var_descriptions.append("\n".join(desc_lines))
    else:
        var_descriptions.append("No sequence variants detected (100% identity to NM_000518.5 reference).")

    # Section B: Database Evidence
    clinvar_summaries: List[str] = []
    if packet.clinvar_records:
        evidence_used.append("NCBI ClinVar")
        for c in packet.clinvar_records:
            conds = ", ".join(c.conditions[:3]) if c.conditions else "None listed"
            ev_type = getattr(c, "evidence_type", "DIRECT VARIANT EVIDENCE")
            ret_d = getattr(c, "retrieval_date", "Today")
            clinvar_summaries.append(
                f"• Accession {c.accession} (Variation ID {c.id}) [{ev_type}]: "
                f"Classification **{c.clinical_significance}** (Review: {c.review_status}; Conditions: {conds}; Retrieved: {ret_d})"
            )

    pubmed_summaries: List[str] = []
    if packet.pubmed_records:
        evidence_used.append("NCBI PubMed")
        for p in packet.pubmed_records:
            ev_type = getattr(p, "evidence_type", "RELATED GENE OR DISEASE EVIDENCE")
            ret_d = getattr(p, "retrieval_date", "Today")
            pubmed_summaries.append(
                f"• PMID {p.pmid} [{ev_type}]: \"{p.title}\" ({p.journal}, {p.pub_date}; Retrieved: {ret_d})"
            )

    if reason == "no_key":
        header_banner = (
            "> **Notice: Live AI synthesis is unavailable.** `GROQ_API_KEY` is not configured in your environment. "
            "Deterministic evidence remains authoritative (Deterministic Evidence Summary active).\n\n"
        )
    elif reason in ("api_error", "quota_exceeded", "rate_limit"):
        header_banner = (
            "> **Notice: Live AI synthesis is temporarily unavailable. Deterministic evidence remains authoritative.** "
            "(Deterministic Evidence Summary active)\n\n"
        )
    elif reason == "validation_failed":
        header_banner = (
            f"> **Notice: Live AI synthesis is temporarily unavailable. Deterministic evidence remains authoritative.** "
            f"(Validation fallback: {error_message or 'unsupported claims'})\n\n"
        )
    else:
        header_banner = (
            "> **Notice: Live AI synthesis is temporarily unavailable. Deterministic evidence remains authoritative.** "
            "(Deterministic Evidence Summary active)\n\n"
        )

    # Biological explanation for Section D
    if primary_v and primary_v.codon_change and primary_v.codon_change.is_stop_gain:
        cc = primary_v.codon_change
        bio_explanation = (
            "1. **Codon Mutation & Termination**: CAG encodes glutamine. The C to T substitution changes CAG at codon 40 into TAG, "
            "which is a canonical translation termination codon. The ribosome therefore terminates translation at this newly created stop signal, "
            "producing a 39 amino acid peptide rather than the full length beta globin protein. This is classified as a nonsense or stop gain variant, p.Gln40Ter.\n"
            "2. **Functional & Structural Impact**: Translation terminates at codon 40, producing a peptide containing the 39 amino acids encoded before the premature stop. "
            f"This leaves the remaining {147 - cc.codon_number} canonical codons untranslated, "
            "substantially truncating the encoded protein and consistent with a loss of functional beta-globin.\n"
            "3. **Transcript Fate (NMD)**: Because this is an early premature termination codon, nonsense mediated decay may contribute to reduced mutant transcript abundance. "
            "This is a biological interpretation and is not directly established by the codon calculation.\n"
            "4. **Nomenclature Concordance**: Historical literature designates this mutation as CD39 C>T, Q39*, or Gln39Ter because mature circulating beta-globin was historically numbered "
            "after post-translational removal of initiator Met1. HGVS reference sequence NM_000518.5 numbers from the initiating methionine as codon 40. These describe the identical mutation."
        )
    else:
        bio_explanation = (
            f"Inquiry: \"{question}\"\n"
            "The deterministic sequence calculations and database records above provide the complete verified evidence packet."
        )

    cv_text = ("\n".join(clinvar_summaries)) if clinvar_summaries else "No matching ClinVar records were retrieved."
    pubmed_intro = "These PubMed records were retrieved as relevant literature associated with the variant or HBB/beta thalassemia context:\n" if pubmed_summaries else ""
    pm_text = f"{pubmed_intro}" + ("\n".join(pubmed_summaries)) if pubmed_summaries else "No matching PubMed literature was retrieved."

    db_evidence_content = (
        "**NCBI ClinVar Evidence**:\n"
        f"{cv_text}\n\n"
        "**NCBI PubMed Literature**:\n"
        f"{pm_text}"
    )

    limitations_content = (
        "• **Biological Interpretations**: Nonsense mediated decay is a mechanistic interpretation and was not directly demonstrated by this sequence analysis. "
        "Polypeptide instability and degradation also represent biological interpretations rather than directly observed experimental findings.\n"
        "• **Literature Scope**: PubMed records classified as RELATED GENE OR DISEASE EVIDENCE or CONTEXTUAL EVIDENCE provide background disease context and do not constitute direct proof of the exact molecular mechanism for this specific variant.\n"
        "• **Evidence Boundaries**: Additional biological mechanisms beyond the computed sequence consequence and retrieved database records are not directly established by the supplied evidence."
    )

    answer_parts = [
        f"## DIRECT SCIENTIFIC ANSWER\n{direct_answer}\n\n",
        header_banner,
        "## A. COMPUTED FACTS\n",
        "\n".join(var_descriptions),
        "\n\n## B. DATABASE EVIDENCE\n",
        db_evidence_content,
        "\n\n## C. ESTABLISHED BIOLOGICAL KNOWLEDGE\n",
        "In the universal genetic code, 61 sense codons specify amino acids (CAG specifies glutamine) while UAG/TAG, UAA/TAA, and UGA/TGA function as translation termination codons. When a single-base substitution converts a sense codon to a stop codon, release factors recognize the stop codon and ribosomal translation terminates prematurely.",
        "\n\n## D. DETERMINISTIC SYNTHESIS\n",
        bio_explanation,
        "\n\n## EVIDENCE LIMITATIONS\n",
        limitations_content,
    ]

    provenance_sections = [
        "DIRECT SCIENTIFIC ANSWER",
        "A. COMPUTED FACTS",
        "B. DATABASE EVIDENCE",
        "C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
        "D. DETERMINISTIC SYNTHESIS",
        "EVIDENCE LIMITATIONS",
    ]

    return CopilotResponse(
        answer=normalize_canonical_sections("".join(answer_parts)),
        evidence_used=evidence_used,
        limitations_cited=packet.limitations[:3],
        status="no_key" if reason == "no_key" else "error",
        provider="groq",
        model=settings.GROQ_MODEL,
        fallback=True,
        provenance_sections=provenance_sections,
        provenance_label="Deterministic synthesis"
    )


async def synthesize_research_copilot(
    question: str,
    evidence_packet: EvidencePacket,
    conversation_history: List[CopilotChatMessage]
) -> CopilotResponse:
    """
    Coordinates Groq LLM research synthesis strictly bounded by the supplied evidence packet.
    Implements automatic retry for transient errors, reasoning token exhaustion detection,
    post-generation validation with strict provenance checks, and graceful deterministic fallback.
    """
    if not settings.GROQ_API_KEY:
        logger.warning(
            "AI provider: Groq | GROQ_API_KEY not configured | Fallback: true | Reason: Missing GROQ_API_KEY"
        )
        return _generate_offline_synthesis(evidence_packet, question, reason="no_key")

    try:
        logger.info("AI synthesis started | Provider: Groq | Model: %s", settings.GROQ_MODEL)
        client = Groq(api_key=settings.GROQ_API_KEY)

        structured_evidence = format_structured_evidence_context(evidence_packet)
        user_prompt = f"""=== AUTHORITATIVE EVIDENCE PACKET ===
{structured_evidence}

=== RESEARCH QUESTION ===
{question}

Provide an evidence-grounded scientific explanation answering the research question.
Strictly adhere to the following canonical section structure without repeating any headers:
## DIRECT SCIENTIFIC ANSWER
## A. COMPUTED FACTS
## B. DATABASE EVIDENCE
## C. ESTABLISHED BIOLOGICAL KNOWLEDGE
## D. AI SYNTHESIS
## EVIDENCE LIMITATIONS
"""

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        # Append recent history (up to last 6 messages)
        for msg in conversation_history[-6:]:
            role = "assistant" if msg.role in ("assistant", "model") else "user"
            messages.append({"role": role, "content": msg.content})

        messages.append({"role": "user", "content": user_prompt})

        # Call Groq with transient error retry (up to 3 retries for rate limit or timeouts)
        max_retries = 3
        chat_completion = None
        for attempt in range(max_retries + 1):
            try:
                chat_completion = await asyncio.to_thread(
                    client.chat.completions.create,
                    model=settings.GROQ_MODEL,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=settings.GROQ_MAX_TOKENS,
                )
                break
            except Exception as exc:
                err_str = str(exc).lower()
                is_daily_limit = "tokens per day" in err_str or "tpd" in err_str
                if is_daily_limit:
                    logger.warning("Groq daily token limit (TPD) reached. Activating deterministic fallback immediately.")
                    raise exc

                is_transient = any(kw in err_str for kw in ("rate limit", "timeout", "connection", "503", "429"))
                if is_transient and attempt < max_retries:
                    retry_match = re.search(r"try again in ([\d\.]+)s", err_str)
                    if retry_match:
                        wait_time = float(retry_match.group(1)) + 1.0
                    else:
                        wait_time = 4.0 * (attempt + 1)
                    logger.warning(
                        "Groq transient error (%s). Retrying in %.1fs (attempt %d/%d)...",
                        type(exc).__name__,
                        wait_time,
                        attempt + 1,
                        max_retries,
                    )
                    await asyncio.sleep(wait_time)
                else:
                    raise exc

        choice = chat_completion.choices[0]
        answer_text = (choice.message.content or "").strip()

        if not answer_text:
            reasoning = getattr(choice.message, "reasoning", None)
            if reasoning:
                raise ValueError(
                    f"Groq model '{settings.GROQ_MODEL}' consumed the entire token budget "
                    f"({settings.GROQ_MAX_TOKENS} tokens) on reasoning without producing visible content. "
                    f"Increase GROQ_MAX_TOKENS to accommodate reasoning tokens."
                )
            raise ValueError(f"Groq model '{settings.GROQ_MODEL}' returned empty completion content.")

        # Normalize canonical sections to guarantee each heading appears at most once
        normalized_answer = normalize_canonical_sections(answer_text)

        # Post-generation verification layer
        is_valid, validation_err = validate_ai_synthesis(normalized_answer, evidence_packet)
        if not is_valid:
            logger.warning(
                "AI synthesis rejected by validation layer: %s. Falling back to deterministic synthesis.",
                validation_err
            )
            return _generate_offline_synthesis(
                evidence_packet,
                question,
                reason="validation_failed",
                error_message=f"Validation error: {validation_err}"
            )

        # Identify evidence sources utilized in answer
        evidence_used = ["Deterministic Sequence Engine"]
        ans_lower = normalized_answer.lower()
        if evidence_packet.clinvar_records and ("clinvar" in ans_lower or "vcv" in ans_lower):
            evidence_used.append("NCBI ClinVar")
        if evidence_packet.pubmed_records and ("pubmed" in ans_lower or "pmid" in ans_lower):
            evidence_used.append("NCBI PubMed")

        provenance_sections = []
        if "direct" in ans_lower:
            provenance_sections.append("DIRECT SCIENTIFIC ANSWER")
        if "computed" in ans_lower or "a. computed" in ans_lower:
            provenance_sections.append("A. COMPUTED FACTS")
        if "database" in ans_lower or "b. database" in ans_lower or "clinvar" in ans_lower or "pubmed" in ans_lower:
            provenance_sections.append("B. DATABASE EVIDENCE")
        if "established" in ans_lower or "general biological" in ans_lower or "c. established" in ans_lower:
            provenance_sections.append("C. ESTABLISHED BIOLOGICAL KNOWLEDGE")
        if "ai synthesis" in ans_lower or "grounded synthesis" in ans_lower or "d. ai" in ans_lower or "d. evidence" in ans_lower or "synthesis" in ans_lower:
            provenance_sections.append("D. AI SYNTHESIS")
        if "limitation" in ans_lower or "boundary" in ans_lower or "evidence limitations" in ans_lower:
            provenance_sections.append("EVIDENCE LIMITATIONS")

        if not provenance_sections:
            provenance_sections = [
                "DIRECT SCIENTIFIC ANSWER",
                "A. COMPUTED FACTS",
                "B. DATABASE EVIDENCE",
                "C. ESTABLISHED BIOLOGICAL KNOWLEDGE",
                "D. AI SYNTHESIS",
                "EVIDENCE LIMITATIONS",
            ]

        logger.info(
            "AI synthesis succeeded | Provider: Groq | Model: %s | Tokens: %d | Evidence sources: %s | Provenance sections: %s | Fallback: false",
            settings.GROQ_MODEL,
            settings.GROQ_MAX_TOKENS,
            ", ".join(evidence_used),
            ", ".join(provenance_sections)
        )

        return CopilotResponse(
            answer=normalized_answer,
            evidence_used=evidence_used,
            limitations_cited=evidence_packet.limitations,
            status="success",
            provider="groq",
            model=settings.GROQ_MODEL,
            fallback=False,
            provenance_sections=provenance_sections,
            provenance_label="Live Groq synthesis"
        )

    except Exception as e:
        safe_error = type(e).__name__ + (f": {str(e)[:120]}" if str(e) else "")
        logger.error(
            "AI synthesis failed: %s | Fallback activated | Provider: Groq | Model: %s",
            safe_error,
            settings.GROQ_MODEL
        )
        return _generate_offline_synthesis(
            evidence_packet,
            question,
            reason="api_error",
            error_message=safe_error
        )
