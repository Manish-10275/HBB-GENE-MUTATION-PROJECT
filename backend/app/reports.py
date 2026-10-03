"""Generates standardized Markdown and printable HTML Research Reports."""

from datetime import datetime, timezone
from typing import Optional
from app.models import EvidencePacket, ReportResponse


def generate_research_report(
    packet: EvidencePacket,
    copilot_summary: Optional[str] = None
) -> ReportResponse:
    """
    Builds a rigorous scientific research report formatted in both Markdown and
    print-ready styled HTML.
    """
    gen_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    title = f"HBB Genomic Variant Analysis Report — {packet.analysis_id}"

    # Build Markdown report
    md_lines = [
        f"# {title}",
        f"**Generated:** {gen_time}  ",
        f"**Target Gene:** {packet.gene_symbol} (Hemoglobin subunit beta)  ",
        f"**Reference Accession:** {packet.reference_accession} (RefSeq MANE Select)  ",
        "\n---\n",
        "## 1. Sequence & Alignment Metrics",
        f"- **Reference Length:** {packet.summary.get('reference_length_bp', 'N/A')} bp",
        f"- **Sample Query Length:** {packet.summary.get('sample_length_bp', 'N/A')} bp",
        f"- **Sequence Identity:** {packet.summary.get('sequence_identity_pct', 'N/A')}%",
        f"- **Alignment Score:** {packet.summary.get('alignment_score', 'N/A')}",
        f"- **CDS Coordinates:** {packet.summary.get('cds_coordinates', '51..494')} (Length: {packet.summary.get('cds_length_bp', 444)} bp)",
        f"- **Detected Variants:** {packet.summary.get('detected_variants_count', len(packet.variants))}",
        "\n## 2. Detected Variants & Codon Consequences",
    ]

    if not packet.variants:
        md_lines.append("*No sequence variations detected relative to NM_000518.5 reference.*")
    else:
        md_lines.append(
            "| Variant (HGVS c.) | Position | Ref | Alt | Impact | Protein (HGVS p.) | Codon Change |"
        )
        md_lines.append(
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        )
        for v in packet.variants:
            c_change = "N/A"
            if v.codon_change:
                c_change = f"Codon {v.codon_change.codon_number}: {v.codon_change.ref_codon} ({v.codon_change.ref_aa}) → {v.codon_change.sample_codon} ({v.codon_change.sample_aa})"
            md_lines.append(
                f"| `{v.hgvs_c}` | c.{v.c_position} | `{v.ref_allele}` | `{v.alt_allele}` | **{v.functional_impact}** | `{v.hgvs_p or 'None'}` | {c_change} |"
            )

    md_lines.append("\n## 3. External Scientific Evidence")
    md_lines.append("### NCBI ClinVar Annotations")
    if not packet.clinvar_records:
        md_lines.append("*No matching ClinVar records retrieved.*")
    else:
        for c in packet.clinvar_records:
            conds = ", ".join(c.conditions[:4]) if c.conditions else "None listed"
            eval_date = c.last_evaluated or "Not provided"
            md_lines.append(
                f"- **{c.title}**  \n"
                f"  - **Accession:** [{c.accession}]({c.url}) | **Variation ID:** {c.id}  \n"
                f"  - **Clinical Significance:** **{c.clinical_significance}**  \n"
                f"  - **Review Status:** {c.review_status}  \n"
                f"  - **Associated Conditions:** {conds}  \n"
                f"  - **Last Evaluated:** {eval_date}"
            )

    md_lines.append("\n### NCBI PubMed Scientific Literature")
    if not packet.pubmed_records:
        md_lines.append("*No matching PubMed evidence was retrieved.*")
    else:
        for p in packet.pubmed_records:
            authors_str = ", ".join(p.authors) if p.authors else "Authors not listed"
            md_lines.append(
                f"- **[{p.title}]({p.url})**  \n"
                f"  - **PMID:** {p.pmid} | **Journal:** {p.journal} ({p.pub_date})  \n"
                f"  - **Authors:** {authors_str}"
            )

    if copilot_summary:
        md_lines.append("\n## 4. AI Research Synthesis")
        md_lines.append(f"> {copilot_summary}")

    md_lines.append("\n## 5. Evidence Limitations & Constraints")
    for lim in packet.limitations:
        md_lines.append(f"- {lim}")

    md_lines.append("\n---\n")
    md_lines.append("### Safety & Regulatory Disclaimer")
    md_lines.append(
        "**FOR RESEARCH AND EDUCATIONAL USE ONLY.**  \n"
        "This application does not provide a medical diagnosis or treatment recommendation. "
        "All computational findings must be verified against primary empirical lab assays "
        "and certified clinical sequencing workflows before any medical consideration."
    )

    markdown_content = "\n".join(md_lines)

    # Build clean HTML with responsive & printable styling
    html_variants_rows = ""
    for v in packet.variants:
        c_desc = "Non-coding"
        if v.codon_change:
            c_desc = f"Codon {v.codon_change.codon_number}: <code>{v.codon_change.ref_codon}</code> ({v.codon_change.ref_aa}) &rarr; <code>{v.codon_change.sample_codon}</code> ({v.codon_change.sample_aa})"
        html_variants_rows += f"""
        <tr>
            <td><code>{v.hgvs_c}</code></td>
            <td>c.{v.c_position}</td>
            <td><code>{v.ref_allele}</code> &rarr; <code>{v.alt_allele}</code></td>
            <td><span class="badge badge-impact">{v.functional_impact}</span></td>
            <td><code>{v.hgvs_p or 'None'}</code></td>
            <td>{c_desc}</td>
        </tr>
        """

    html_clinvar_items = ""
    if packet.clinvar_records:
        for c in packet.clinvar_records:
            conds = ", ".join(c.conditions[:4]) if c.conditions else "None listed"
            html_clinvar_items += f"""
            <div class="evidence-card">
                <div class="evidence-header">
                    <strong>{c.title}</strong>
                    <span class="badge badge-significance">{c.clinical_significance}</span>
                </div>
                <div class="evidence-meta">
                    <span>Accession: <a href="{c.url}" target="_blank">{c.accession}</a></span>
                    <span>Review: {c.review_status}</span>
                    <span>Conditions: {conds}</span>
                </div>
            </div>
            """
    else:
        html_clinvar_items = "<p class='muted'>No matching ClinVar records retrieved.</p>"

    html_pubmed_items = ""
    if packet.pubmed_records:
        for p in packet.pubmed_records:
            authors_str = ", ".join(p.authors[:3]) if p.authors else "Authors not listed"
            html_pubmed_items += f"""
            <div class="evidence-card">
                <div class="evidence-header">
                    <a href="{p.url}" target="_blank"><strong>{p.title}</strong></a>
                </div>
                <div class="evidence-meta">
                    <span>PMID: <strong>{p.pmid}</strong></span>
                    <span>Journal: {p.journal} ({p.pub_date})</span>
                    <span>Authors: {authors_str}</span>
                </div>
            </div>
            """
    else:
        html_pubmed_items = "<p class='muted'>No matching PubMed evidence was retrieved.</p>"

    copilot_html = ""
    if copilot_summary:
        copilot_html = f"""
        <section class="section">
            <h2>4. AI Research Synthesis</h2>
            <div class="copilot-box">
                <p>{copilot_summary}</p>
            </div>
        </section>
        """

    limitations_html = "".join(f"<li>{lim}</li>" for lim in packet.limitations)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #ffffff;
        }}
        h1, h2, h3 {{ color: #0f172a; font-family: Georgia, serif; }}
        h1 {{ font-size: 26px; border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 16px; }}
        h2 {{ font-size: 18px; margin-top: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        .header-meta {{ font-size: 14px; color: #475569; margin-bottom: 24px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }}
        .metric-card {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px 16px; border-radius: 6px; }}
        .metric-title {{ font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; }}
        .metric-value {{ font-size: 20px; font-weight: 700; color: #0f172a; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background-color: #f1f5f9; font-weight: 600; color: #334155; }}
        code {{ font-family: ui-monospace, Menlo, Monaco, "Cascadia Mono", monospace; background: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-size: 13px; }}
        .badge {{ display: inline-block; padding: 3px 8px; font-size: 12px; font-weight: 600; border-radius: 4px; }}
        .badge-impact {{ background-color: #fee2e2; color: #991b1b; }}
        .badge-significance {{ background-color: #fef3c7; color: #92400e; }}
        .evidence-card {{ border: 1px solid #e2e8f0; background: #f8fafc; padding: 14px 16px; border-radius: 6px; margin-bottom: 10px; }}
        .evidence-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
        .evidence-meta {{ font-size: 13px; color: #64748b; margin-top: 6px; display: flex; flex-direction: column; gap: 2px; }}
        .copilot-box {{ background: #f0fdf4; border-left: 4px solid #16a34a; padding: 14px 18px; border-radius: 4px; }}
        .disclaimer-box {{ margin-top: 40px; padding: 16px; background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; font-size: 13px; color: #92400e; }}
        .muted {{ color: #64748b; font-style: italic; }}
        @media print {{
            body {{ padding: 0; }}
            .disclaimer-box {{ border: 1px solid #000; }}
        }}
    </style>
</head>
<body>
    <h1>HBB Genomic Variant Analysis Report</h1>
    <div class="header-meta">
        <div><strong>Analysis ID:</strong> {packet.analysis_id} | <strong>Date:</strong> {gen_time}</div>
        <div><strong>Target:</strong> {packet.gene_symbol} (Hemoglobin Subunit Beta) | <strong>Reference:</strong> {packet.reference_accession} (RefSeq)</div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-title">Sequence Identity</div>
            <div class="metric-value">{packet.summary.get('sequence_identity_pct', 'N/A')}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Alignment Score</div>
            <div class="metric-value">{packet.summary.get('alignment_score', 'N/A')}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Detected Variants</div>
            <div class="metric-value">{len(packet.variants)}</div>
        </div>
    </div>

    <h2>1. Detected Variants & Codon Consequences</h2>
    <table>
        <thead>
            <tr>
                <th>HGVS c.</th>
                <th>Position</th>
                <th>Ref &rarr; Alt</th>
                <th>Impact</th>
                <th>HGVS p.</th>
                <th>Codon Consequence</th>
            </tr>
        </thead>
        <tbody>
            {html_variants_rows if packet.variants else "<tr><td colspan='6' class='muted'>No variants detected.</td></tr>"}
        </tbody>
    </table>

    <h2>2. NCBI ClinVar Evidence</h2>
    {html_clinvar_items}

    <h2>3. NCBI PubMed Literature</h2>
    {html_pubmed_items}

    {copilot_html}

    <h2>5. Evidence Limitations</h2>
    <ul>
        {limitations_html}
    </ul>

    <div class="disclaimer-box">
        <strong>RESEARCH AND EDUCATIONAL USE ONLY.</strong><br>
        This report does not constitute a diagnostic medical test, clinical interpretation, or medical advice.
        All conclusions are in silico inferences and must be validated through standard diagnostic laboratory protocols.
    </div>
</body>
</html>
    """

    return ReportResponse(
        markdown_content=markdown_content,
        html_content=html_content,
        generated_at=gen_time,
        title=title
    )
