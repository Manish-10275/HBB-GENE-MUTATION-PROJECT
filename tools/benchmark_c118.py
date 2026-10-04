"""End-to-End Benchmark & Verification Script for HBB c.118C>T (p.Gln40Ter)."""

import asyncio
import json
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.reference import reference_manager
from app.alignment import align_sequences
from app.variants import detect_variants
from app.clinvar import fetch_clinvar_records
from app.pubmed import fetch_pubmed_records
from app.simulator import classify_screening
from app.evidence import assemble_evidence_packet
from app.ai import synthesize_research_copilot, validate_ai_synthesis
from app.config import settings


async def run_benchmark():
    print("=" * 70)
    print("   HBB MUTATION ANALYZER - BENCHMARK: c.118C>T (p.Gln40Ter)")
    print("=" * 70)

    # 1. Sequence alignment & variant detection
    ref = reference_manager.get_reference("NM_000518.5")
    # c.118 corresponds to index 167 in NM_000518.5
    mut_seq = ref.sequence[:167] + "T" + ref.sequence[168:]

    summary, al_ref, al_query = align_sequences(ref.sequence, mut_seq)
    variants = detect_variants(al_ref, al_query, ref)
    assert len(variants) == 1, "Expected exactly 1 variant"
    v = variants[0]

    print("\n[STEP 1: DETERMINISTIC BIOINFORMATICS]")
    print(f"  • Transcript: {ref.accession} (Gene: {ref.gene})")
    print(f"  • cDNA Variant: {v.hgvs_c}")
    print(f"  • Protein Consequence: {v.hgvs_p}")
    print(f"  • Codon Mutation: Codon {v.codon_change.codon_number}: {v.codon_change.ref_codon} ({v.codon_change.ref_aa}) -> {v.codon_change.sample_codon} ({v.codon_change.sample_aa})")
    print(f"  • Molecular Consequence: {v.functional_impact} (Stop-gain: {v.codon_change.is_stop_gain})")
    print(f"  • Equivalent Aliases: {', '.join(v.equivalent_nomenclature[:6])}...")
    print(f"  • Numbering Note: {v.nomenclature_notes[:100]}...")

    # 2. Database Evidence Retrieval
    c_term = f"c.{v.c_position}{v.ref_allele}>{v.alt_allele}"
    cv_records = await fetch_clinvar_records(c_term)
    pm_records = await fetch_pubmed_records(c_term, variant_aliases=v.equivalent_nomenclature)

    print("\n[STEP 2: DATABASE EVIDENCE RETRIEVAL]")
    print(f"  • ClinVar Records: {len(cv_records)}")
    for c in cv_records[:2]:
        print(f"    - Accession: {c.accession} | VarID: {c.id} | Significance: {c.clinical_significance} | Evidence: {c.evidence_type} | Retrieved: {c.retrieval_date}")
    print(f"  • PubMed Records: {len(pm_records)}")
    for p in pm_records[:3]:
        print(f"    - PMID: {p.pmid} | Classification: {p.evidence_type} | Title: {p.title[:65]}... | Retrieved: {p.retrieval_date}")

    # 3. Evidence Assembly
    screening = classify_screening(variants, zygosity="heterozygous")
    packet = assemble_evidence_packet(
        ref_data=ref,
        alignment_summary=summary,
        variants=variants,
        clinvar_records=cv_records,
        pubmed_records=pm_records,
        screening_classification=screening
    )
    print(f"\n[STEP 3: EVIDENCE PACKET ASSEMBLED] (ID: {packet.analysis_id})")

    # 4. Research Copilot Synthesis
    question = "Why does the CAG to TAG change result in a premature termination codon?"
    print(f"\n[STEP 4: RESEARCH COPILOT INQUIRY]")
    print(f"  Inquiry: \"{question}\"")

    res = await synthesize_research_copilot(question, packet, [])

    print(f"\n[STEP 5: SYNTHESIS STATUS & PROVENANCE]")
    print(f"  • Status: {res.status}")
    print(f"  • Fallback Mode: {res.fallback}")
    print(f"  • Provenance Label: \"{res.provenance_label}\"")
    print(f"  • Provenance Sections: {res.provenance_sections}")
    print(f"  • Evidence Used: {res.evidence_used}")

    print("\n" + "-" * 70)
    print("                 SYNTHESIS OUTPUT")
    print("-" * 70)
    # Print with utf-8 encoding safely
    try:
        print(res.answer)
    except UnicodeEncodeError:
        print(res.answer.encode("ascii", "replace").decode("ascii"))
    print("-" * 70)

    # 5. Validation Check
    is_valid, val_err = validate_ai_synthesis(res.answer, packet)
    print(f"\n[STEP 6: POST-GENERATION VALIDATION INTEGRITY CHECK]")
    print(f"  • Validation Passed: {is_valid}")
    if val_err:
        print(f"  • Validation Note: {val_err}")

    # 6. Compliance assertions
    ans_lower = res.answer.lower()
    assert "cag" in ans_lower, "CAG must be mentioned"
    assert "tag" in ans_lower, "TAG must be mentioned"
    assert "gln40ter" in ans_lower or "q40" in ans_lower or "cd39" in ans_lower or "codon 39" in ans_lower, "Variant must be identified"
    assert res.provenance_label in (
        "Live Groq synthesis grounded in retrieved NCBI evidence",
        "Deterministic synthesis",
        "AI synthesis grounded in retrieved NCBI evidence",
    ), f"Provenance label '{res.provenance_label}' must match requirements"

    print("\n[RESULT: BENCHMARK SUCCEEDED! ALL EVIDENCE & REASONING BOUNDARIES VERIFIED]\n")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
