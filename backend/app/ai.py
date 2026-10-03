"""AI Research Copilot module for evidence-grounded synthesis."""

import json
import logging
from typing import List, Tuple
from app.config import settings
from app.models import CopilotChatMessage, CopilotResponse, EvidencePacket

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the AI Research Copilot for the HBB Mutation Analyzer, a scientific research and educational platform.

STRICT OPERATIONAL DIRECTIVES:
1. ONLY utilize the supplied deterministic analysis and retrieved database evidence provided in the EVIDENCE PACKET.
2. Under NO circumstances invent facts, ClinVar records, PubMed papers, PMIDs, clinical significance, citations, or biological mechanisms.
3. If evidence is missing, sparse, or unavailable in the packet, explicitly state that evidence is unavailable.
4. VISIBLY DISTINGUISH:
   - COMPUTED RESULT (from deterministic bioinformatics engine: nucleotide position, codon change, amino acid consequence, HGVS).
   - DATABASE EVIDENCE (from NCBI ClinVar and PubMed: assertions, submitters, accession numbers, PMIDs).
   - AI SYNTHESIS (your structured explanation connecting the computed consequence to the retrieved literature).
5. DO NOT provide medical diagnoses or treatment recommendations.
6. DO NOT claim that a variant is pathogenic unless that classification is explicitly present in the supplied ClinVar evidence and clearly attributed to NCBI ClinVar.
7. Always maintain a calm, precise, scientific editorial tone. Keep answers structured and informative.
"""


def _generate_offline_synthesis(packet: EvidencePacket, question: str) -> CopilotResponse:
    """
    Generates a deterministic summary when OpenAI API key is not configured.
    Ensures zero hallucination and full utility in offline/no-key mode.
    """
    var_descriptions: List[str] = []
    evidence_used: List[str] = ["Sequence analysis (Deterministic Engine)"]

    for v in packet.variants:
        desc = f"• **{v.hgvs_c}**"
        if v.hgvs_p:
            desc += f" ({v.hgvs_p})"
        desc += f" — Impact: {v.functional_impact}"
        if v.codon_change:
            desc += f" (Codon {v.codon_change.codon_number}: {v.codon_change.ref_codon} [{v.codon_change.ref_aa}] → {v.codon_change.sample_codon} [{v.codon_change.sample_aa}])"
        var_descriptions.append(desc)

    clinvar_summaries: List[str] = []
    if packet.clinvar_records:
        evidence_used.append("NCBI ClinVar Database")
        for c in packet.clinvar_records:
            conds = ", ".join(c.conditions[:3]) if c.conditions else "None listed"
            clinvar_summaries.append(
                f"• Accession {c.accession} (VarID {c.id}): Classification **{c.clinical_significance}** "
                f"(Review: {c.review_status}; Conditions: {conds})"
            )

    pubmed_summaries: List[str] = []
    if packet.pubmed_records:
        evidence_used.append("NCBI PubMed Database")
        for p in packet.pubmed_records:
            pubmed_summaries.append(f"• PMID {p.pmid}: \"{p.title}\" ({p.journal}, {p.pub_date})")

    answer_parts = [
        "### Deterministic Evidence Summary *(AI API Key Not Configured)*\n",
        "> **Note:** To enable live natural-language synthesis with the AI Research Copilot, set `OPENAI_API_KEY` in your `.env` file. "
        "Below is the exact, unhallucinated scientific evidence packet assembled from deterministic bioinformatics and NCBI databases.\n\n",
        "#### Computed Variants:",
        "\n".join(var_descriptions) if var_descriptions else "No variants detected (100% identity to NM_000518.5 reference).",
        "\n\n#### Database Evidence (ClinVar):",
        "\n".join(clinvar_summaries) if clinvar_summaries else "No ClinVar records retrieved for this query.",
        "\n\n#### Database Evidence (PubMed):",
        "\n".join(pubmed_summaries) if pubmed_summaries else "No matching PubMed literature retrieved for this query.",
        f"\n\n#### Response to question: *\"{question}\"*",
        "The deterministic analysis above directly documents the molecular consequence and retrieved evidence. For customized reasoning and narrative synthesis, configure your `OPENAI_API_KEY`."
    ]

    return CopilotResponse(
        answer="".join(answer_parts),
        evidence_used=evidence_used,
        limitations_cited=packet.limitations[:3],
        status="no_key"
    )


async def synthesize_research_copilot(
    question: str,
    evidence_packet: EvidencePacket,
    conversation_history: List[CopilotChatMessage]
) -> CopilotResponse:
    """
    Coordinates LLM research synthesis strictly bounded by the supplied evidence packet.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return _generate_offline_synthesis(evidence_packet, question)

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=api_key)

        evidence_json = evidence_packet.model_dump_json(indent=2)
        user_prompt = f"""EVIDENCE PACKET:
```json
{evidence_json}
```

RESEARCH QUESTION:
{question}

Provide an evidence-grounded scientific explanation answering the research question.
Explicitly cite the provenance (Computed Result vs. ClinVar vs. PubMed) for every statement.
"""

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Append recent history (up to last 6 messages)
        for msg in conversation_history[-6:]:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": user_prompt})

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=1000
        )

        answer_text = response.choices[0].message.content or ""

        # Identify evidence sources utilized
        evidence_used = ["Sequence analysis (Deterministic Engine)"]
        if evidence_packet.clinvar_records and ("clinvar" in answer_text.lower() or "vcv" in answer_text.lower()):
            evidence_used.append("NCBI ClinVar")
        if evidence_packet.pubmed_records and ("pubmed" in answer_text.lower() or "pmid" in answer_text.lower()):
            evidence_used.append("NCBI PubMed")

        return CopilotResponse(
            answer=answer_text,
            evidence_used=evidence_used,
            limitations_cited=evidence_packet.limitations,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error during AI synthesis: {e}")
        # Graceful fallback to deterministic summary
        fallback = _generate_offline_synthesis(evidence_packet, question)
        fallback.status = "error"
        fallback.answer = (
            f"**Error contacting OpenAI API:** `{str(e)}`\n\n"
            + fallback.answer
        )
        return fallback
