# Product Demonstration Guide — HBB Mutation Analyzer

**Understand the sequence. Follow the evidence.**

This guide presents the recommended step-by-step demonstration flow for evaluating the scientific capabilities of the **HBB Mutation Analyzer**.

---

## Prerequisites & Launch

### Terminal 1: Launch Backend
```bash
# In project root:
$env:PYTHONPATH="backend"
backend/venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Verify backend health: `http://localhost:8000/health`

### Terminal 2: Launch Frontend
```bash
cd frontend
npm.cmd run dev
```
Open application: `http://localhost:3000`

---

## Core Demonstration Workflows

### Workflow 1: The Controlled Validation Benchmark (`c.118C>T`)
1. **Load Controlled Benchmark:**
   - On the top sequence input strip, click **★ Controlled Validation Case**.
   - Notice the editor automatically populates with the 628 bp synthetic test sequence containing the single nucleotide substitution at $c.118$.
   - Observe live sequence statistics: `628 bp`, `51.9% GC`, `Canonical DNA`.

2. **Execute Deterministic Analysis:**
   - Click **Run Deterministic Analysis**.
   - Observe the overview metrics:
     * **Sequence Identity:** `99.84%`
     * **Alignment Score:** `1253.0`
     * **Detected Variants:** `1`
     * **Retrieved Evidence:** ClinVar records and PubMed papers fetched from NCBI.

3. **Inspect Detected Variants:**
   - Review the Variants Table:
     * **HGVS cDNA:** `NM_000518.5:c.118C>T`
     * **Position:** $c.118$ (mRNA base 168)
     * **Allele Change:** $C \rightarrow T$
     * **Impact:** `Nonsense`
     * **Protein:** `p.Gln40Ter`

4. **Experience the Codon & Protein Visualizer:**
   - Scroll to the Codon Transformation block:
     * **REFERENCE CODON:** `CAG` $\rightarrow$ `Gln` ($Q$)
     * **SAMPLE CODON:** `TAG` $\rightarrow$ `STOP (Ter)` ($*$)
     * Notice the intra-codon highlight on the first base of codon 40 ($C \rightarrow T$).
     * Clearly labeled with the `COMPUTED RESULT` badge.

5. **Examine Pairwise Global Alignment:**
   - Inspect Block #3 (bases 121..180):
     * Reference: `...TGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTGAAGGCTCATGGCAAGAAAGTG...`
     * Sample: Shows the single mismatched position flagged by `.` and highlighted in red.
     * Toggle "Filter to mutated blocks only" to isolate difference windows.

6. **Review External Database Evidence:**
   - Inspect **NCBI ClinVar**:
     * Classification: **Pathogenic**
     * Review Status: *criteria provided, multiple submitters, no conflicts*
     * Associated Conditions: *Beta-thalassemia*, *HBB-related disorder*
   - Inspect **NCBI PubMed**:
     * Live primary literature citations with direct clickable PubMed links.
   - Note the distinct `DATABASE EVIDENCE` badge and provenance metadata.

7. **Engage the AI Research Copilot:**
   - Click one of the suggested inquiry chips:
     * *"Why does this nucleotide change produce a premature stop codon?"*
   - Notice the provenance indicator:
     * `Evidence utilized: Sequence analysis (Deterministic Engine), NCBI ClinVar, NCBI PubMed`.
   - Observe that the response strictly references the deterministic computation and retrieved records without hallucinating outside assertions.

8. **Export the Research Report:**
   - Click **Export Research Report** in the top navigation bar.
   - Review the styled publication-grade preview with full metrics, variant consequences, and disclaimers.
   - Test **Print / Save PDF** (opens standard browser print dialog) or **Download .md**.

---

### Workflow 2: Direct Variant Investigation (No Sequence Upload)
1. In the header bar, click **Direct HGVS Search**.
2. Select the preset chip for `c.20A>T (p.Glu7Val / HbS)`.
3. Click **Search Evidence**.
4. Observe the immediate retrieval of ClinVar and PubMed records for Sickle Cell Disease directly from NCBI.

---

### Workflow 3: Biological Error & Safety Handling
1. Paste invalid text containing RNA Uracil (`ACGAUGAC`) or numbers.
2. Observe immediate live input validation warning explaining that Uracil indicates RNA rather than cDNA/DNA.
3. Observe the "Run Deterministic Analysis" button safely disabling to prevent invalid biological computations.
