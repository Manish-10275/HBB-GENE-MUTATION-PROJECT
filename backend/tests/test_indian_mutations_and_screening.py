"""Tests for dual-reference architecture, 4 Indian mutations dataset, simulator, and screening engine."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.reference import reference_manager
from app.simulator import (
    classify_screening,
    get_available_mutation_presets,
    simulate_mutated_sequence,
)
from app.models import DetectedVariant


def test_reference_manager_dual_reference():
    """Confirms both cDNA and genomic references are loaded with exact features."""
    nm = reference_manager.get_reference("NM_000518.5")
    assert nm.accession == "NM_000518.5"
    assert nm.total_length == 628
    assert len(nm.exons) == 3
    assert nm.cds_start == 51
    assert nm.cds_end == 494

    ng = reference_manager.get_reference("NG_000007.3")
    assert ng.accession == "NG_000007.3"
    assert ng.total_length == 1608
    assert len(ng.exons) == 3
    assert len(ng.introns) == 2
    assert ng.genomic_start == 70545
    assert ng.genomic_end == 72152

    refs = reference_manager.list_references()
    accessions = [r["accession"] for r in refs]
    assert "NM_000518.5" in accessions
    assert "NG_000007.3" in accessions


def test_indian_mutations_dataset():
    """Confirms the 4 Indian thalassemia mutations dataset is complete and verified."""
    panel = reference_manager.get_indian_mutations()
    muts = panel.get("mutations", [])
    assert len(muts) == 4

    ids = [m["id"] for m in muts]
    assert "ivs1-5" in ids
    assert "cd41-42" in ids
    assert "cd8-9" in ids
    assert "cd30" in ids

    # Check IVS1-5
    ivs = next(m for m in muts if m["id"] == "ivs1-5")
    assert ivs["hgvs_c"] == "c.92+5G>C"
    assert ivs["clinvar_id"] == "15447"
    assert ivs["coordinate_genomic"] == 70691

    # Check Cd41/42
    cd41 = next(m for m in muts if m["id"] == "cd41-42")
    assert "126_129del" in cd41["hgvs_c"]
    assert cd41["clinvar_id"] == "15417"

    # Check Cd8/9
    cd89 = next(m for m in muts if m["id"] == "cd8-9")
    assert cd89["region"] == "Exon 1"
    assert cd89["clinvar_id"] == "36308"

    # Check Cd30
    cd30 = next(m for m in muts if m["id"] == "cd30")
    assert cd30["hgvs_c"] == "c.93G>C"
    assert cd30["clinvar_id"] == "869321"


def test_simulator_generation():
    """Tests sequence simulation for wild-type, benchmark, and Indian mutation presets."""
    wt = simulate_mutated_sequence("wild_type")
    assert len(wt["sequence"]) == 628
    assert wt["reference_accession"] == "NM_000518.5"

    c118 = simulate_mutated_sequence("c118c_t")
    assert len(c118["sequence"]) == 628
    assert c118["sequence"][167] == "T"

    c20 = simulate_mutated_sequence("c20a_t")
    assert len(c20["sequence"]) == 628
    assert c20["sequence"][69] == "T"

    ivs = simulate_mutated_sequence("ivs1-5")
    assert len(ivs["sequence"]) == 1608
    assert ivs["reference_accession"] == "NG_000007.3"
    assert ivs["sequence"][146] == "C"

    cd41 = simulate_mutated_sequence("cd41-42")
    assert len(cd41["sequence"]) == 624  # 4 bp deletion

    cd8 = simulate_mutated_sequence("cd8-9")
    assert len(cd8["sequence"]) == 629  # 1 bp insertion

    cd30 = simulate_mutated_sequence("cd30")
    assert len(cd30["sequence"]) == 628
    assert cd30["sequence"][142] == "C"


def test_screening_classification_rules():
    """Verifies rule-based screening classifications for zygosity combinations."""
    # Wild-type
    res_wt = classify_screening([])
    assert res_wt.severity == "Normal"
    assert "Wild Type" in res_wt.condition_name

    # c.118C>T (Nonsense β0)
    var_c118 = DetectedVariant(
        id="var_1",
        variant_type="substitution",
        ref_position_mrna=168,
        c_position="118",
        ref_allele="C",
        alt_allele="T",
        hgvs_c="NM_000518.5:c.118C>T",
        hgvs_p="p.Gln40Ter",
        functional_impact="Nonsense",
        confidence="Deterministic"
    )
    res_c118_het = classify_screening([var_c118], zygosity="heterozygous")
    assert res_c118_het.severity == "Carrier / Minor"
    assert "β0" in res_c118_het.condition_name
    assert "Carrier" in res_c118_het.condition_name

    res_c118_hom = classify_screening([var_c118], zygosity="homozygous")
    assert res_c118_hom.severity == "Major / Severe"
    assert "Cooley's Anemia" in res_c118_hom.condition_name

    # c.20A>T (Sickle Cell)
    var_sickle = DetectedVariant(
        id="var_2",
        variant_type="substitution",
        ref_position_mrna=70,
        c_position="20",
        ref_allele="A",
        alt_allele="T",
        hgvs_c="NM_000518.5:c.20A>T",
        hgvs_p="p.Glu7Val",
        functional_impact="Missense",
        confidence="Deterministic"
    )
    res_sickle_het = classify_screening([var_sickle], zygosity="heterozygous")
    assert res_sickle_het.severity == "Carrier / Minor"
    assert "Sickle Cell Trait" in res_sickle_het.condition_name

    res_sickle_hom = classify_screening([var_sickle], zygosity="homozygous")
    assert res_sickle_hom.severity == "Major / Severe"
    assert "Sickle Cell Anemia" in res_sickle_hom.condition_name

    # IVS1-5 (Splice β+)
    var_ivs = DetectedVariant(
        id="var_3",
        variant_type="substitution",
        ref_position_mrna=147,
        c_position="92+5",
        ref_allele="G",
        alt_allele="C",
        hgvs_c="NM_000518.5:c.92+5G>C",
        functional_impact="Splice Site Defect",
        confidence="Deterministic"
    )
    res_ivs_het = classify_screening([var_ivs], zygosity="heterozygous")
    assert res_ivs_het.severity == "Carrier / Minor"
    assert "β+" in res_ivs_het.condition_name

    res_ivs_hom = classify_screening([var_ivs], zygosity="homozygous")
    assert "Intermedia" in res_ivs_hom.condition_name


@pytest.mark.asyncio
async def test_api_simulator_and_reference_endpoints():
    """Tests the new HTTP endpoints for references, Indian panel, and simulator."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Reference list
        r_list = await ac.get("/reference/list")
        assert r_list.status_code == 200
        data = r_list.json()
        assert len(data) >= 2

        # Indian panel
        r_panel = await ac.get("/mutations/indian")
        assert r_panel.status_code == 200
        panel = r_panel.json()
        assert len(panel["mutations"]) == 4

        # Simulator presets
        r_presets = await ac.get("/simulator/presets")
        assert r_presets.status_code == 200
        presets = r_presets.json()
        assert len(presets) >= 6

        # Simulator generation
        r_gen = await ac.post("/simulator/generate", json={"preset_id": "ivs1-5"})
        assert r_gen.status_code == 200
        gen_data = r_gen.json()
        assert gen_data["reference_accession"] == "NG_000007.3"
        assert len(gen_data["sequence"]) == 1608

        # Run analysis on simulated IVS1-5
        r_ana = await ac.post("/analyze", json={
            "sequence": gen_data["sequence"],
            "reference_accession": "NG_000007.3",
            "zygosity": "heterozygous"
        })
        assert r_ana.status_code == 200
        ana_res = r_ana.json()
        assert ana_res["success"] is True
        assert len(ana_res["variants"]) == 1
        var = ana_res["variants"][0]
        assert var["c_position"] == "92+5"
        assert "c.92+5G>C" in var["hgvs_c"]
        assert ana_res["screening_classification"] is not None
        assert "Carrier" in ana_res["screening_classification"]["severity"]
