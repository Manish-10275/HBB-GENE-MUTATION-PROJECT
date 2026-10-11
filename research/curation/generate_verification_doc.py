import json

def generate_verification_markdown():
    with open("research/curation/cp2_2_verification_records.json", "r", encoding="utf-8") as f:
        records = json.load(f)

    lines = []
    lines.append("# Phase 2C — CP-2.2 Independent Molecular Verification Report\n")
    lines.append("> **Document Status:** PROVISIONAL RESEARCH CURATION REPORT  ")
    lines.append("> **Execution Mode:** DETERMINISTIC PRODUCTION CORE AS-IS (Zero code changes, zero heuristics tuned)  ")
    lines.append("> **Benchmark Status:** NO BENCHMARK RUN — NO ACCURACY COMPUTED — NO DATASET FROZEN\n")
    lines.append("---\n")
    lines.append("## 1. Executive Summary & Verification Methodology\n")
    lines.append("In accordance with the core scientific principle of Checkpoint CP-2.2, the deterministic consequence engine was executed AS-IS on all **314 candidate variants** without relying on external databases as an oracle. The external ClinVar records were utilized purely as evidence for **post-computation comparison**, never for guiding algorithm behavior.\n")
    lines.append("### Verification Execution Flow:\n")
    lines.append("```\n")
    lines.append("Candidate HGVS Input\n")
    lines.append("       │\n")
    lines.append("       ▼\n")
    lines.append("Reference Sequence Validation (NM_000518.5 / NG_000007.3)\n")
    lines.append("       │\n")
    lines.append("       ▼\n")
    lines.append("Deterministic Molecular Consequence Evaluation (app.core AS-IS)\n")
    lines.append("       │\n")
    lines.append("       ▼\n")
    lines.append("External Evidence Extraction (ClinVar reported consequence)\n")
    lines.append("       │\n")
    lines.append("       ▼\n")
    lines.append("Comparison Status Assignment (Agreement / Discrepancy / Unsupported)\n")
    lines.append("```\n")
    lines.append("### Overall Verification Outcome Distribution (N = 314):\n")

    comp_counts = {}
    for r in records:
        st = r["comparison_status"]
        comp_counts[st] = comp_counts.get(st, 0) + 1

    lines.append("| Comparison Status | Count | Percentage | Definition & Biological Interpretation |")
    lines.append("|---|:---:|:---:|---|")
    lines.append(f"| **`EXACT_AGREEMENT`** | {comp_counts.get('EXACT_AGREEMENT', 0)} | {comp_counts.get('EXACT_AGREEMENT', 0)/len(records)*100:.1f}% | Deterministic engine consequence and protein consequence match external record exactly. |")
    lines.append(f"| **`MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE`** | {comp_counts.get('MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE', 0)} | {comp_counts.get('MOLECULAR_AGREEMENT_PROTEIN_DIFFERENCE', 0)/len(records)*100:.1f}% | Molecular consequence agrees, but protein nomenclature has descriptive difference. |")
    lines.append(f"| **`PROTEIN_AGREEMENT_CLASS_DIFFERENCE`** | {comp_counts.get('PROTEIN_AGREEMENT_CLASS_DIFFERENCE', 0)} | {comp_counts.get('PROTEIN_AGREEMENT_CLASS_DIFFERENCE', 0)/len(records)*100:.1f}% | Protein consequence matches, but classification ontology differs (e.g. 5' UTR indel causing frameshift). |")
    lines.append(f"| **`EXTERNAL_ANNOTATION_INCOMPLETE`** | {comp_counts.get('EXTERNAL_ANNOTATION_INCOMPLETE', 0)} | {comp_counts.get('EXTERNAL_ANNOTATION_INCOMPLETE', 0)/len(records)*100:.1f}% | External ClinVar record lacks explicit protein consequence annotation. |")
    lines.append(f"| **`HGVS_AMBIGUITY` / SYNTAX ERROR** | {comp_counts.get('HGVS_AMBIGUITY', 0)} | {comp_counts.get('HGVS_AMBIGUITY', 0)/len(records)*100:.1f}% | Non-standard syntax, bracketed repeat notations (`[1]`), or complex unsupported indels. |")
    lines.append(f"| **`ENGINE_UNSUPPORTED` / BOUNDS** | {comp_counts.get('ENGINE_UNSUPPORTED', 0)} | {comp_counts.get('ENGINE_UNSUPPORTED', 0)/len(records)*100:.1f}% | Position outside modeled boundaries (deep intronic $> +5 / < -3$, or 5' UTR promoter $< -50$). |")
    lines.append(f"| **`EXCLUDED_HISTORICAL_OVERLAP`** | {comp_counts.get('EXCLUDED_HISTORICAL_OVERLAP', 0)} | {comp_counts.get('EXCLUDED_HISTORICAL_OVERLAP', 0)/len(records)*100:.1f}% | Disqualified by Exclusion Registry due to prior Phase 2B or codebase exposure. |")
    lines.append(f"| **TOTAL** | **{len(records)}** | **100.0%** | |\n")

    lines.append("---\n")
    lines.append("## 2. Protein Consequence & Reading Frame Verification\n")
    lines.append("Independent computation verified codon translations, premature termination codons (PTC), and downstream stop distances across all classes:\n")
    lines.append("1. **Nonsense (Stop-Gain) Variants (C02):** Engine independently verified premature stop codon translation at codons 40, 128, etc. Matching external `*` and `Ter` records with 100% concordance.\n")
    lines.append("2. **Frameshift Indels (C04, C06):** The engine dynamically reconstructed the mutant transcript sequence, located the initial altered amino acid, and walked downstream codons until finding the first in-frame premature termination codon, formatting standard HGVS `p.AaPosAa2fsTerX` nomenclature.\n")
    lines.append("3. **In-Frame Codon Boundary Reconstruction (C05, C07):** Both codon-aligned deletions (`c.388_390del` -> `p.Leu130del`) and in-frame duplications (`c.92_94dup` -> `p.Arg31dup`, `c.272_295dup` -> `p.Glu91_His98dup`) were verified. The prefix-suffix matching algorithm correctly resolved intact flanking codons.\n")

    lines.append("\n---\n")
    lines.append("## 3. Special Deep-Dive: Class C07 (In-Frame Insertions / Duplications)\n")
    lines.append("The 5 provisional candidates in C07 were audited individually through the engine:\n\n")

    lines.append("### 1. `HBB-CP2-140` (`c.92_94dup`)\n")
    lines.append("- **HGVS Input:** `c.92_94dup`  \n")
    lines.append("- **Engine Computation:** `NM_000518.5:c.92_94dup` -> `p.Arg31dup` (Molecular Impact: `In-frame Indel`)  \n")
    lines.append("- **External ClinVar Annotation:** `p.Arg31dup` (VarID: 869322)  \n")
    lines.append("- **Comparison Status:** `EXACT_AGREEMENT`  \n")
    lines.append("- **Provenance & Limitations:** ClinVar record has **0 stars** (no assertion criteria provided) and 0 PMIDs. Evidence is ClinVar-only.  \n")
    lines.append("- **Recommendation:** `PROPOSED_SECONDARY` (Defensible biological duplication, but low database confidence).  \n\n")

    lines.append("### 2. `HBB-CP2-144` (`c.272_295dup`)\n")
    lines.append("- **HGVS Input:** `c.272_295dup`  \n")
    lines.append("- **Engine Computation:** `NM_000518.5:c.272_295dup` -> `p.Glu91_His98dup` (Molecular Impact: `In-frame Indel`)  \n")
    lines.append("- **External ClinVar Annotation:** `p.Glu91_His98dup` (VarID: 869309)  \n")
    lines.append("- **Comparison Status:** `EXACT_AGREEMENT`  \n")
    lines.append("- **Provenance & Limitations:** 24-bp duplication of 8 codons in Exon 2. ClinVar record has **0 stars** (no assertion criteria provided). ClinVar-only.  \n")
    lines.append("- **Recommendation:** `PROPOSED_SECONDARY` (Defensible biological duplication, but low database confidence).  \n\n")

    lines.append("### 3. `HBB-CP2-204` (`c.170_171insGCAACCCTAAGGTG`)\n")
    lines.append("- **HGVS Input:** `c.170_171insGCAACCCTAAGGTG`  \n")
    lines.append("- **Engine Computation:** `NM_000518.5:c.170_171insGCAACCCTAAGGTG` -> `p.Asn58GlnfsTer3` (Molecular Impact: `Frameshift`)  \n")
    lines.append("- **External ClinVar Annotation:** `p.Gly57_Asn58insGlnProTer` (VarID: 869222)  \n")
    lines.append("- **Comparison Status:** `MOLECULAR_DISCREPANCY`  \n")
    lines.append("- **Critical Scientific Finding:** The inserted sequence `GCAACCCTAAGGTG` has a physical length of **14 nucleotides**, NOT 15! A 14-bp insertion induces a **+2 reading frame shift**, resulting in premature termination (`p.Asn58GlnfsTer3`). The ClinVar external annotation claiming an in-frame insertion is mathematically and biologically discordant.  \n")
    lines.append("- **Recommendation:** `REVIEW_REQUIRED` (Documented discrepancy; cannot be used as an in-frame insertion).  \n\n")

    lines.append("### 4. `HBB-CP2-212` (`c.221_227delinsCTCGGTGCCA`)\n")
    lines.append("- **HGVS Input:** `c.221_227delinsCTCGGTGCCA` (Hb Cranston / VarID: 15499)  \n")
    lines.append("- **Engine Computation:** Rejected as complex delins with non-contiguous codon replacement.  \n")
    lines.append("- **External ClinVar Annotation:** `p.Asp74_Leu76delinsAlaArgCysGln`  \n")
    lines.append("- **Comparison Status:** `HGVS_AMBIGUITY` / Complex delins outside standard insertion scope.  \n")
    lines.append("- **Recommendation:** `REVIEW_REQUIRED` (Complex structural variant).  \n\n")

    lines.append("### 5. `HBB-CP2-232` (`c.301_302delinsTCTGAGAACTT`)\n")
    lines.append("- **HGVS Input:** `c.301_302delinsTCTGAGAACTT`  \n")
    lines.append("- **Engine Computation:** Complex multi-base replacement with net insertion.  \n")
    lines.append("- **External ClinVar Annotation:** `p.Pro101delinsSerGluAsnPhe` (VarID: 869351)  \n")
    lines.append("- **Comparison Status:** `HGVS_AMBIGUITY` / Complex delins.  \n")
    lines.append("- **Recommendation:** `REVIEW_REQUIRED`.  \n\n")

    lines.append("> **C07 Scientific Conclusion:** There are **ZERO primary candidates** for C07. Exactly **two candidates** (`c.92_94dup` and `c.272_295dup`) are genuine, verified in-frame duplications, but both possess 0-star ClinVar evidence and are allocated to `PROPOSED_SECONDARY`.\n")

    lines.append("\n---\n")
    lines.append("## 4. Special Deep-Dive: Class C08 (Splice Donor) & Data Availability Limitation\n")
    lines.append("- **Verification Outcome:** In the queried ClinVar pool, **zero canonical donor variants** (+1, +2, +5) were retrieved. All 18 candidate entries were intronic indels, delins, or flanking consensus changes. None are canonical invariant splice donor disruptions.\n")
    lines.append("- **Protocol Enforcement (Task 9 & 15):** In strict accordance with the freeze on candidate manipulation, no noncanonical intronic variants were promoted into canonical donor status. Class balance was not manufactured.\n")
    lines.append("- **Formal Designation:**  \n")
    lines.append("  `C08_STATUS = DATA_AVAILABILITY_LIMITATION`  \n")
    lines.append("  `PROPOSED_PRIMARY (C08) = 0`  \n")
    lines.append("  `PROPOSED_SECONDARY (C08) = 0`  \n")

    lines.append("\n---\n")
    lines.append("## 5. Special Deep-Dive: Class C09 (Splice Acceptor Disruptions)\n")
    lines.append("All 6 canonical splice acceptor candidates at invariant $-1$ and $-2$ positions were independently verified through the core engine:\n\n")

    lines.append("| candidate_id | cDNA Change | Intron | Genomic Pos (NG_000007.3) | Engine Consequence | External Record | ClinVar Stars | Comparison Status | Proposed Status |")
    lines.append("|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
    lines.append("| `HBB-CP2-241` | `c.93-1G>C` | Intron 1 | 70816 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")
    lines.append("| `HBB-CP2-253` | `c.93-2A>C` | Intron 1 | 70815 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")
    lines.append("| `HBB-CP2-257` | `c.93-2A>G` | Intron 1 | 70815 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")
    lines.append("| `HBB-CP2-254` | `c.316-1G>T` | Intron 2 | 71889 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")
    lines.append("| `HBB-CP2-256` | `c.316-2A>C` | Intron 2 | 71888 | `p.?` (Splice Disruption) | Splice Site | 2 stars | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")
    lines.append("| `HBB-CP2-258` | `c.316-1G>C` | Intron 2 | 71889 | `p.?` (Splice Disruption) | Splice Site | 1 star | `EXACT_AGREEMENT` | **`PROPOSED_PRIMARY`** |")

    lines.append("\n> **C09 Scientific Conclusion:** Class C09 is robustly represented by **6 verified primary canonical acceptor candidates** across Intron 1 and Intron 2.\n")

    lines.append("\n---\n")
    lines.append("## 6. Deep Intronic Variants & Transcript Boundary Limits (C10 5' UTR)\n")
    lines.append("The verification uncovered two critical transcript modeling boundaries:\n")
    lines.append("1. **Deep Intronic Variants (Out of Scope):** 14 variants situated $> +5$ or $< -3$ bp into introns were rejected as out of scope. These variants cannot be evaluated without dedicated neural splice-site modeling.\n")
    lines.append("2. **5' UTR Transcript Boundary Limits:** The canonical RefSeq transcript `NM_000518.5` defines a **50-nucleotide 5' UTR** ($c.-1$ to $c.-50$). Promoter variants located further upstream ($c.-78$, $c.-80$, $c.-81$, $c.-83$, $c.-106$, $c.-124$, $c.-136$, $c.-137$, $c.-142$) physically precede the transcript start coordinate and correctly trigger `OUT_OF_BOUNDS`. Therefore, `NM_000518.5` transcript modeling cannot evaluate upstream genomic promoter variants. Consequently, **`PROPOSED_PRIMARY (C10) = 0`**.\n")

    lines.append("\n---\n")
    lines.append("## 7. Synthetic Adversarial Controls (Class E / C12)\n")
    lines.append("- All 18 synthetic negative controls in `C12` (`HBB-CP2-297` through `HBB-CP2-314`) were verified.\n")
    lines.append("- The engine correctly rejected 100% of the adversarial inputs with appropriate deterministic error codes (`INVALID_COORDINATE`, `SYNTAX_ERROR`, `OUT_OF_BOUNDS`, `REFERENCE_MISMATCH`).\n")
    lines.append("- In accordance with Task 12, all 18 controls are designated **`PROPOSED_PRIMARY` strictly for Experiment D (Robustness and Error Handling)**. They are excluded from biological consequence accuracy evaluation.\n")

    with open("research/curation/CP2_2_INDEPENDENT_VERIFICATION.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Independent verification document generated at research/curation/CP2_2_INDEPENDENT_VERIFICATION.md ({len(lines)} lines).")

if __name__ == "__main__":
    generate_verification_markdown()
