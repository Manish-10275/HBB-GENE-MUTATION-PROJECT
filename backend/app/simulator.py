"""Educational sequence simulator and rule-based screening classifier for HBB variants.

Implements the four classic Indian thalassemia mutations and benchmark variants
with full biological grounding, RefSeq coordinate precision, and educational screening models.
"""

from typing import Any, Dict, List, Optional, Tuple
from app.models import DetectedVariant, ScreeningClassification
from app.reference import reference_manager


def get_available_mutation_presets() -> List[Dict[str, Any]]:
    """Returns curated mutation presets including the 4 Indian mutations and validation cases."""
    indian_dataset = reference_manager.get_indian_mutations().get("mutations", [])
    
    presets = [
        {
            "id": "wild_type",
            "name": "Wild Type Reference (Normal)",
            "subtitle": "NM_000518.5 wild-type human HBB",
            "category": "Normal Control",
            "accession": "NM_000518.5",
            "description": "Standard normal human beta-globin sequence without mutations."
        },
        {
            "id": "c118c_t",
            "name": "c.118C>T (p.Gln40Ter) [Controlled Benchmark]",
            "subtitle": "Exon 2 Nonsense Mutation (CAG -> TAG)",
            "category": "Controlled Validation Case",
            "accession": "NM_000518.5",
            "description": "Nonsense mutation at codon 40 producing a premature stop codon and β0-thalassemia."
        },
        {
            "id": "c20a_t",
            "name": "c.20A>T (p.Glu7Val) [Sickle Cell]",
            "subtitle": "Exon 1 Missense Mutation (GAG -> GTG)",
            "category": "Sickle Cell Disease / Trait",
            "accession": "NM_000518.5",
            "description": "Classic sickle cell mutation substituting valine for glutamic acid at position 7 (historical codon 6)."
        },
        {
            "id": "c19g_a",
            "name": "c.19G>A (p.Glu7Lys) [Hemoglobin C]",
            "subtitle": "Exon 1 Missense Mutation (GAG -> AAG)",
            "category": "Hemoglobin C Trait / Disease",
            "accession": "NM_000518.5",
            "description": "Hemoglobin C variant replacing glutamic acid with lysine at codon 7 (historical codon 6)."
        }
    ]
    
    for m in indian_dataset:
        presets.append({
            "id": m["id"],
            "name": f"{m['common_name']} [Indian Thalassemia]",
            "subtitle": f"{m['region']} {m['mutation_class']}",
            "category": "Indian Thalassemia Panel",
            "accession": m["reference_accession_genomic"] if m["id"] == "ivs1-5" else m["reference_accession_cdna"],
            "description": m["mechanism"]
        })
        
    return presets


def simulate_mutated_sequence(preset_id: str) -> Dict[str, Any]:
    """
    Simulates a sequence harboring the requested mutation.
    Returns:
    {
        "sequence": str,
        "preset_id": str,
        "name": str,
        "reference_accession": str,
        "coordinate_type": str,
        "description": str
    }
    """
    clean_id = preset_id.lower().strip()
    
    # 1. Wild type
    if clean_id in ("wild_type", "normal", "wt"):
        ref = reference_manager.get_reference("NM_000518.5")
        return {
            "sequence": ref.sequence,
            "preset_id": "wild_type",
            "name": "Wild Type Reference (Normal)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Normal human HBB transcript sequence (628 bp)."
        }
        
    # 2. Benchmark c.118C>T
    if clean_id in ("c118c_t", "c.118c>t", "gln40ter"):
        ref = reference_manager.get_reference("NM_000518.5")
        seq_list = list(ref.sequence)
        # c.118 is at 1-based index 168 (0-based index 167)
        idx = 167
        assert seq_list[idx] == "C", f"Expected C at index {idx}, found {seq_list[idx]}"
        seq_list[idx] = "T"
        return {
            "sequence": "".join(seq_list),
            "preset_id": "c118c_t",
            "name": "NM_000518.5:c.118C>T (p.Gln40Ter)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence containing the c.118C>T nonsense mutation."
        }
        
    # 3. Sickle cell c.20A>T
    if clean_id in ("c20a_t", "c.20a>t", "glu7val", "sickle"):
        ref = reference_manager.get_reference("NM_000518.5")
        seq_list = list(ref.sequence)
        # c.20 is at 1-based index 70 (0-based index 69)
        idx = 69
        assert seq_list[idx] == "A", f"Expected A at index {idx}, found {seq_list[idx]}"
        seq_list[idx] = "T"
        return {
            "sequence": "".join(seq_list),
            "preset_id": "c20a_t",
            "name": "NM_000518.5:c.20A>T (p.Glu7Val)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence containing the c.20A>T sickle mutation."
        }

    # 3b. Hemoglobin C c.19G>A
    if clean_id in ("c19g_a", "c.19g>a", "glu7lys", "hbc"):
        ref = reference_manager.get_reference("NM_000518.5")
        seq_list = list(ref.sequence)
        # c.19 is at 1-based index 69 (0-based index 68)
        idx = 68
        assert seq_list[idx] == "G", f"Expected G at index {idx}, found {seq_list[idx]}"
        seq_list[idx] = "A"
        return {
            "sequence": "".join(seq_list),
            "preset_id": "c19g_a",
            "name": "NM_000518.5:c.19G>A (p.Glu7Lys)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence containing the c.19G>A Hemoglobin C mutation."
        }
        
    # 4. Indian Mutation 1: IVS1-5 (G>C)
    if clean_id in ("ivs1-5", "ivs1-5 (g>c)", "c.92+5g>c"):
        # Intronic mutation requiring genomic reference NG_000007.3 (1608 bp)
        ref = reference_manager.get_reference("NG_000007.3")
        seq_list = list(ref.sequence)
        # Relative position 147 in genomic gene locus (0-based index 146)
        # Exon 1 is 1..142. Intron 1 is 143..272.
        # Position +5 is 142 + 5 = 147 (0-based index 146).
        idx = 146
        assert seq_list[idx] == "G", f"Expected G at index {idx}, found {seq_list[idx]}"
        seq_list[idx] = "C"
        return {
            "sequence": "".join(seq_list),
            "preset_id": "ivs1-5",
            "name": "IVS1-5 (G>C) / c.92+5G>C [Genomic Simulation]",
            "reference_accession": "NG_000007.3",
            "coordinate_type": "Genomic (NG_000007.3 locus)",
            "description": "Simulated HBB genomic sequence (1608 bp) containing the Intron 1 donor splice site mutation IVS1-5 (G>C)."
        }
        
    # 5. Indian Mutation 2: Cd41/42 (-TCTT)
    if clean_id in ("cd41-42", "cd41/42", "c.126_129deltctt", "c.126_129del"):
        ref = reference_manager.get_reference("NM_000518.5")
        # In cDNA: codons 41/42 are at cDNA 121..126. c.126_129 is TCTT.
        # cDNA 126 is at 1-based index 176 (0-based index 175)
        # ref.sequence[175:179] is "TCTT"
        seq = ref.sequence[:175] + ref.sequence[179:]
        return {
            "sequence": seq,
            "preset_id": "cd41-42",
            "name": "Cd41/42 (-TCTT) / c.126_129delTCTT",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence with 4-bp deletion at codons 41/42 producing frameshift p.Phe42fs."
        }
        
    # 6. Indian Mutation 3: Cd8/9 (+G)
    if clean_id in ("cd8-9", "cd8/9", "c.27dup", "c.27_28insg"):
        ref = reference_manager.get_reference("NM_000518.5")
        # In cDNA: codon 8 ends at cDNA 24, codon 9 ends at cDNA 27.
        # c.27 is at 1-based index 77 (0-based index 76). Inserting 'G' after index 76.
        seq = ref.sequence[:77] + "G" + ref.sequence[77:]
        return {
            "sequence": seq,
            "preset_id": "cd8-9",
            "name": "Cd8/9 (+G) / c.27dup (p.Ser10fs)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence with single guanine insertion at codons 8/9 producing frameshift p.Ser10fs."
        }
        
    # 7. Indian Mutation 4: Cd30 (G>C)
    if clean_id in ("cd30", "c.93g>c", "p.arg31ser"):
        ref = reference_manager.get_reference("NM_000518.5")
        seq_list = list(ref.sequence)
        # cDNA 93 is at 1-based index 143 (0-based index 142)
        idx = 142
        assert seq_list[idx] == "G", f"Expected G at index {idx}, found {seq_list[idx]}"
        seq_list[idx] = "C"
        return {
            "sequence": "".join(seq_list),
            "preset_id": "cd30",
            "name": "Cd30 (G>C) / c.93G>C (p.Arg31Ser)",
            "reference_accession": "NM_000518.5",
            "coordinate_type": "Transcript (cDNA)",
            "description": "Simulated HBB cDNA sequence with c.93G>C substitution affecting codon 30/31 and the exon 1 splice junction."
        }
        
    raise ValueError(f"Unknown mutation preset ID: '{preset_id}'")


def classify_screening(
    detected_variants: List[DetectedVariant],
    zygosity: str = "heterozygous"
) -> ScreeningClassification:
    """
    Evaluates detected HBB variants and assigned zygosity to generate
    an educational screening classification with biological phenotype predictions.
    """
    is_homozygous = zygosity.lower() in ("homozygous", "homo", "hom")
    zyg_display = "Homozygous" if is_homozygous else "Heterozygous"
    
    if not detected_variants:
        return ScreeningClassification(
            zygosity="N/A",
            condition_name="Normal HBB Sequence (Wild Type)",
            severity="Normal",
            thalassemia_type="None",
            clinical_summary=(
                "No nucleotide differences detected compared to the reference sequence. "
                "Normal adult beta-globin chain synthesis is expected."
            ),
            laboratory_correlations=[
                "Normal adult hemoglobin pattern: HbA >96-97%",
                "Normal HbA2: 2.5-3.2%",
                "Normal HbF: <1.0%",
                "Normal red cell indices (MCV >80 fL, MCH >27 pg)"
            ]
        )

    # Check primary variant
    primary = detected_variants[0]
    hgvs_c = primary.hgvs_c.lower()
    hgvs_p = (primary.hgvs_p or "").lower()
    impact = primary.functional_impact.lower()

    # Case 1: Sickle Cell Mutation (c.20A>T / p.Glu7Val)
    if "c.20a>t" in hgvs_c or "glu7val" in hgvs_p or "glu6val" in hgvs_p:
        if is_homozygous:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Sickle Cell Anemia / Disease (Hb SS) [Educational Model]",
                severity="Major / Severe",
                thalassemia_type="Sickle Disease (HbSS)",
                clinical_summary=(
                    "Homozygous inheritance of the sickle cell mutation (c.20A>T, p.Glu7Val). "
                    "Causes abnormal hemoglobin S polymerization upon deoxygenation, resulting in "
                    "sickle-shaped erythrocytes, severe chronic hemolytic anemia, and recurrent vaso-occlusive crises."
                ),
                laboratory_correlations=[
                    "Hemoglobin electrophoresis / HPLC: HbS >85-90%, HbF 2-15%, complete absence of HbA",
                    "Blood smear: Sickle cells (drepanocytes), target cells, Howell-Jolly bodies",
                    "Chronic severe normocytic anemia (Hb 6-9 g/dL)"
                ]
            )
        else:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Sickle Cell Trait / Carrier (Hb AS) [Educational Model]",
                severity="Carrier / Minor",
                thalassemia_type="Sickle Trait (HbAS Carrier)",
                clinical_summary=(
                    "Heterozygous carrier state for the sickle mutation. Individuals produce both normal HbA "
                    "and abnormal HbS. Generally asymptomatic with normal life expectancy, but confers protective "
                    "resistance against severe Plasmodium falciparum malaria."
                ),
                laboratory_correlations=[
                    "Hemoglobin electrophoresis / HPLC: HbA ~55-60%, HbS ~35-40%, normal HbA2",
                    "Normal complete blood count indices under ordinary atmospheric conditions"
                ]
            )

    # Case 2: Hemoglobin C Mutation (c.19G>A / p.Glu7Lys)
    if "c.19g>a" in hgvs_c or "glu7lys" in hgvs_p:
        if is_homozygous:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Hemoglobin C Disease (Hb CC) [Educational Model]",
                severity="Mild Chronic Anemia",
                thalassemia_type="Hemoglobin C Disease (HbCC)",
                clinical_summary=(
                    "Homozygous inheritance of the hemoglobin C mutation (c.19G>A, p.Glu7Lys). "
                    "Results in reduced hemoglobin solubility and intracellular crystal formation, "
                    "causing mild to moderate chronic hemolytic anemia and splenomegaly."
                ),
                laboratory_correlations=[
                    "Hemoglobin electrophoresis / HPLC: HbC >90%, HbA 0% (absent), HbF normal to slightly elevated",
                    "Blood smear: Numerous target cells (codocytes), microspherocytes, intracellular HbC crystals",
                    "Mild normocytic to microcytic anemia"
                ]
            )
        else:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Hemoglobin C Trait / Carrier (Hb AC) [Educational Model]",
                severity="Carrier / Minor",
                thalassemia_type="Hemoglobin C Trait (HbAC Carrier)",
                clinical_summary=(
                    "Heterozygous carrier state for the hemoglobin C mutation. Individuals produce both normal HbA "
                    "and abnormal HbC. Asymptomatic carrier state without significant anemia."
                ),
                laboratory_correlations=[
                    "Hemoglobin electrophoresis / HPLC: HbA ~60-70%, HbC ~30-40%",
                    "Blood smear: Frequent target cells (codocytes), otherwise normal indices"
                ]
            )

    # Case 3: Beta-zero (β0) mutations (nonsense c.118C>T, frameshift cd41-42, cd8-9)
    is_beta_zero = (
        "nonsense" in impact or
        "c.118c>t" in hgvs_c or
        "gln40ter" in hgvs_p or
        "cd41" in hgvs_c or
        "126_129del" in hgvs_c or
        "cd8" in hgvs_c or
        "27dup" in hgvs_c or
        "frameshift" in impact
    )

    if is_beta_zero:
        if is_homozygous:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Beta-Thalassemia Major (Cooley's Anemia, β0/β0) [Educational Model]",
                severity="Major / Severe",
                thalassemia_type="β0 Thalassemia Major",
                clinical_summary=(
                    "Homozygous inheritance of null beta-globin alleles (β0/β0). Results in complete absence "
                    "of beta-globin chain synthesis and severe excess of unpaired alpha-globin chains. "
                    "Presents in early infancy with severe transfusion-dependent hemolytic anemia, failure to thrive, "
                    "and extramedullary hematopoiesis."
                ),
                laboratory_correlations=[
                    "Severe microcytic hypochromic anemia (Hb 2-6 g/dL, MCV 50-70 fL)",
                    "HPLC / Electrophoresis: HbF >90-95%, HbA2 variable (2-5%), HbA 0% (absent)",
                    "Peripheral smear: Marked anisopoikilocytosis, severe hypochromia, nucleated red blood cells"
                ]
            )
        else:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Beta-Thalassemia Minor / Carrier (β0 / β trait) [Educational Model]",
                severity="Carrier / Minor",
                thalassemia_type="β0 Thalassemia Trait",
                clinical_summary=(
                    "Heterozygous carrier for a beta-zero null allele. Typically asymptomatic or causes mild "
                    "asymptomatic microcytic anemia. Clinically significant for prenatal counseling and partner screening."
                ),
                laboratory_correlations=[
                    "HPLC / Electrophoresis: Elevated HbA2 (>3.5-5.5%), normal or slightly elevated HbF (1-3%)",
                    "CBC: Low MCV (<75 fL), low MCH (<25 pg), borderline normal to slightly reduced Hb",
                    "Normal to elevated red blood cell count (RBC >5.0 x 10^12/L)"
                ]
            )

    # Case 3: Beta-plus (β+) / Splicing mutations (IVS1-5 c.92+5G>C, Cd30 c.93G>C)
    is_splice_or_beta_plus = (
        "ivs1-5" in hgvs_c or
        "92+5" in hgvs_c or
        "c.93g>c" in hgvs_c or
        "splice" in impact
    )

    if is_splice_or_beta_plus:
        if is_homozygous:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Beta-Thalassemia Intermedia / Major (β+/β+) [Educational Model]",
                severity="Intermediate to Major",
                thalassemia_type="β+ Thalassemia",
                clinical_summary=(
                    "Homozygous inheritance of partially defective beta-globin alleles (β+/β+). Splicing efficiency "
                    "is severely reduced but residual beta-globin is produced. Clinical severity ranges from "
                    "non-transfusion-dependent thalassemia intermedia (NTDT) to transfusion-dependent thalassemia major."
                ),
                laboratory_correlations=[
                    "Moderate to severe microcytic anemia (Hb 6-9 g/dL in intermedia)",
                    "HPLC / Electrophoresis: HbF 60-90%, HbA markedly reduced (5-30%), elevated HbA2",
                    "Elevated reticulocyte count reflecting active erythroid marrow compensation"
                ]
            )
        else:
            return ScreeningClassification(
                zygosity=zyg_display,
                condition_name="Beta-Thalassemia Minor / Carrier (β+ / β trait) [Educational Model]",
                severity="Carrier / Minor",
                thalassemia_type="β+ Thalassemia Trait",
                clinical_summary=(
                    "Heterozygous carrier for a beta-plus hypomorphic allele. Mildly diminished beta-chain synthesis. "
                    "Asymptomatic carrier state identifiable primarily through red cell indices and hemoglobin chromatography."
                ),
                laboratory_correlations=[
                    "HPLC / Electrophoresis: Elevated HbA2 (>3.5%), normal to mild HbF elevation",
                    "CBC: Microcytosis (MCV <78 fL), hypochromia (MCH <26 pg)"
                ]
            )

    # Generic or other detected variant fallback
    return ScreeningClassification(
        zygosity=zyg_display,
        condition_name=f"HBB Variant Carrier ({primary.functional_impact}) [Educational Model]",
        severity="Carrier / Variant",
        thalassemia_type="Variant of Unknown Significance / Other",
        clinical_summary=(
            f"Detected {primary.variant_type} variant ({primary.hgvs_c}) resulting in predicted {primary.functional_impact} effect. "
            "Phenotypic expression depends on residual chain stability and co-inherited globin modifiers."
        ),
        laboratory_correlations=[
            "Hemoglobin HPLC and complete blood count recommended for phenotypic characterization"
        ]
    )
