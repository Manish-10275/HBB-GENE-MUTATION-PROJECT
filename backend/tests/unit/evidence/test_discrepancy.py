"""Unit tests verifying ClinVar evidence does not overwrite deterministic consequence."""

from app.core.consequences import evaluate_consequence
from app.core.hgvs import parse_hgvs
from app.core.reference import load_reference
from app.evidence.clinvar_offline import OfflineClinVarProvider


def test_clinvar_does_not_overwrite_deterministic_consequence():
    ref = load_reference("NM_000518.5")
    # 1. Deterministic core interpretation
    variant = parse_hgvs("c.118C>T", ref_seq=ref)
    consequence = evaluate_consequence(variant, ref)

    assert consequence.hgvs_p == "p.Gln40Ter"
    assert consequence.molecular_impact.value == "Nonsense"

    # 2. Retrieve offline ClinVar evidence with a hypothetical differing consequence
    provider = OfflineClinVarProvider()
    evidence_res = provider.search_variant(
        "c.118C>T",
        normalized_variant=variant,
        deterministic_consequence="p.Gln39Ter",  # simulate mature protein notation discrepancy
    )

    # 3. Discrepancy is explicitly recorded
    assert len(evidence_res.discrepancies) == 1
    disc = evidence_res.discrepancies[0]
    assert disc.field_name == "protein_consequence"
    assert disc.deterministic_value == "p.Gln39Ter"
    assert disc.evidence_value == "p.Gln40Ter"

    # 4. The deterministic consequence itself was not altered or overwritten
    assert consequence.hgvs_p == "p.Gln40Ter"
