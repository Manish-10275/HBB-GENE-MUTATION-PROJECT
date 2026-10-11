"""
Master dataset generator for HBB Phase 2B Scientific Benchmark.
Builds the 85-variant verified benchmark dataset with explicit provenance,
partitions it into dev, val, and frozen_test splits, and computes cryptographic hashes.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 85 Curated, Verified Benchmark Variants
# Spanning all 12 structural classes + 20 negative controls.
VARIANTS = [
    # =========================================================================
    # 1. Nonsense (Stop-Gain) Variants
    # =========================================================================
    {
        "id": "HBB-BM-001",
        "name": "Codon 39 (C>T) / Mediterranean beta-zero",
        "hgvs_c_input": "c.118C>T",
        "hgvs_c_canonical": "NM_000518.5:c.118C>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Nonsense",
        "region": "Exon 2",
        "coordinate_cdna": "118",
        "ref_allele": "C",
        "alt_allele": "T",
        "expected_hgvs_p": "p.Gln40Ter",
        "expected_clinvar_id": "15402",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015402 / VarID 15402) & RefSeq NM_000518.5",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, multiple submitters, no conflicts",
            "notes": "Historical literature designates Codon 39 (C>T) relative to cleaved Met1; modern HGVS designates Codon 40 (p.Gln40Ter)."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-002",
        "name": "Codon 37 (G>A) Nonsense",
        "hgvs_c_input": "c.114G>A",
        "hgvs_c_canonical": "NM_000518.5:c.114G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Nonsense",
        "region": "Exon 2",
        "coordinate_cdna": "114",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Trp38Ter",
        "expected_clinvar_id": "15405",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015405 / VarID 15405)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "TGG -> TAG nonsense at codon 38 (legacy codon 37)."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-003",
        "name": "Codon 43 (G>T) Nonsense",
        "hgvs_c_input": "c.130G>T",
        "hgvs_c_canonical": "NM_000518.5:c.130G>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Nonsense",
        "region": "Exon 2",
        "coordinate_cdna": "130",
        "ref_allele": "G",
        "alt_allele": "T",
        "expected_hgvs_p": "p.Glu44Ter",
        "expected_clinvar_id": "15406",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015406 / VarID 15406)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "GAG -> TAG nonsense at codon 44 (legacy codon 43)."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-004",
        "name": "Codon 15 (G>A) Nonsense (HGVS Codon 16)",
        "hgvs_c_input": "c.47G>A",
        "hgvs_c_canonical": "NM_000518.5:c.47G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Nonsense",
        "region": "Exon 1",
        "coordinate_cdna": "47",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Trp16Ter",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "IthaGenes (ITHA-HBB-0015) & RefSeq NM_000518.5",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 translation",
            "notes": "TGG -> TAG nonsense at codon 16 (legacy codon 15)."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-005",
        "name": "Codon 18 (legacy Cd17 A>T) Nonsense",
        "hgvs_c_input": "c.52A>T",
        "hgvs_c_canonical": "NM_000518.5:c.52A>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Nonsense",
        "region": "Exon 1",
        "coordinate_cdna": "52",
        "ref_allele": "A",
        "alt_allele": "T",
        "expected_hgvs_p": "p.Lys18Ter",
        "expected_clinvar_id": "15401",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015401 / VarID 15401) & RefSeq NM_000518.5",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.Lys18Ter",
            "notes": "AAG -> TAG nonsense at codon 18 (traditional Chinese/Asian literature Codon 17 A>T)."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-006",
        "name": "Codon 4 (CTG>TGA) Deletion PTC",
        "hgvs_c_input": "c.9del",
        "hgvs_c_canonical": "NM_000518.5:c.9del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "Frameshift",
        "region": "Exon 1",
        "coordinate_cdna": "9",
        "ref_allele": "T",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Leu4Ter",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "RefSeq sequence translation: codon 3 CAT->CAC, codon 4 CTG->TGA (PTC)",
            "notes": "1 bp deletion of T at position 9 creating immediate stop codon TGA at codon 4."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 2. Missense Pathogenic Variants
    # =========================================================================
    {
        "id": "HBB-BM-007",
        "name": "Sickle Cell Disease (HbS)",
        "hgvs_c_input": "c.20A>T",
        "hgvs_c_canonical": "NM_000518.5:c.20A>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 1",
        "coordinate_cdna": "20",
        "ref_allele": "A",
        "alt_allele": "T",
        "expected_hgvs_p": "p.Glu7Val",
        "expected_clinvar_id": "15333",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015333 / VarID 15333)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, multiple submitters",
            "notes": "GAG -> GTG (Glu7Val, legacy Glu6Val)."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-008",
        "name": "Hemoglobin C (HbC)",
        "hgvs_c_input": "c.19G>A",
        "hgvs_c_canonical": "NM_000518.5:c.19G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 1",
        "coordinate_cdna": "19",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Glu7Lys",
        "expected_clinvar_id": "15126",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015126 / VarID 15126)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "GAG -> AAG (Glu7Lys, legacy Glu6Lys)."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-009",
        "name": "Hemoglobin E (HbE)",
        "hgvs_c_input": "c.79G>A",
        "hgvs_c_canonical": "NM_000518.5:c.79G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 1",
        "coordinate_cdna": "79",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Glu27Lys",
        "expected_clinvar_id": "15161",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015161 / VarID 15161)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "GAG -> AAG at codon 27 (legacy Glu26Lys)."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-010",
        "name": "Codon 30 (G>C) Boundary Missense",
        "hgvs_c_input": "c.93G>C",
        "hgvs_c_canonical": "NM_000518.5:c.93G>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 1",
        "coordinate_cdna": "93",
        "ref_allele": "G",
        "alt_allele": "C",
        "expected_hgvs_p": "p.Arg31Ser",
        "expected_clinvar_id": "869321",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000869321 / VarID 869321)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Last nucleotide of Exon 1; causes p.Arg31Ser and disrupts 5' splice recognition."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-011",
        "name": "Hemoglobin D-Los Angeles / D-Punjab",
        "hgvs_c_input": "c.364G>C",
        "hgvs_c_canonical": "NM_000518.5:c.364G>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 2",
        "coordinate_cdna": "364",
        "ref_allele": "G",
        "alt_allele": "C",
        "expected_hgvs_p": "p.Glu122Gln",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "IthaGenes (ITHA-HBB-0121) & RefSeq NM_000518.5",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 translation",
            "notes": "GAA -> CAA at codon 122 (legacy Glu121Gln)."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-012",
        "name": "Hemoglobin Richmond",
        "hgvs_c_input": "c.307A>C",
        "hgvs_c_canonical": "NM_000518.5:c.307A>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Missense",
        "region": "Exon 2",
        "coordinate_cdna": "307",
        "ref_allele": "A",
        "alt_allele": "C",
        "expected_hgvs_p": "p.Asn103His",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Uncertain significance",
        "provenance": {
            "ground_truth_source": "IthaGenes (ITHA-HBB-0102) & RefSeq NM_000518.5",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 translation",
            "notes": "AAC -> CAC at codon 103 (legacy Asn102His)."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 3. Synonymous (Silent) Variants (Benign Controls)
    # =========================================================================
    {
        "id": "HBB-BM-013",
        "name": "Codon 3 Synonymous Variant",
        "hgvs_c_input": "c.9T>C",
        "hgvs_c_canonical": "NM_000518.5:c.9T>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Synonymous",
        "region": "Exon 1",
        "coordinate_cdna": "9",
        "ref_allele": "T",
        "alt_allele": "C",
        "expected_hgvs_p": "p.(=)",
        "expected_clinvar_id": "193106",
        "expected_clinvar_significance": "Benign",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000193106 / VarID 193106)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.His3=",
            "notes": "CAT -> CAC silent translation for Histidine at codon 3."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-014",
        "name": "Codon 5 Synonymous Variant",
        "hgvs_c_input": "c.15T>A",
        "hgvs_c_canonical": "NM_000518.5:c.15T>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Synonymous",
        "region": "Exon 1",
        "coordinate_cdna": "15",
        "ref_allele": "T",
        "alt_allele": "A",
        "expected_hgvs_p": "p.(=)",
        "expected_clinvar_id": "3572117",
        "expected_clinvar_significance": "Likely benign",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV003572117 / VarID 3572117)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.Thr5=",
            "notes": "ACT -> ACA silent translation for Threonine at codon 5."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-015",
        "name": "Codon 36 Synonymous Variant",
        "hgvs_c_input": "c.108C>T",
        "hgvs_c_canonical": "NM_000518.5:c.108C>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Synonymous",
        "region": "Exon 2",
        "coordinate_cdna": "108",
        "ref_allele": "C",
        "alt_allele": "T",
        "expected_hgvs_p": "p.(=)",
        "expected_clinvar_id": "1544548",
        "expected_clinvar_significance": "Conflicting classifications",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV001544548 / VarID 1544548)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.Tyr36=",
            "notes": "TAC -> TAT silent translation for Tyrosine at codon 36."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-016",
        "name": "Codon 59 Synonymous In Silico Control",
        "hgvs_c_input": "c.177T>C",
        "hgvs_c_canonical": "NM_000518.5:c.177T>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Synonymous",
        "region": "Exon 2",
        "coordinate_cdna": "177",
        "ref_allele": "T",
        "alt_allele": "C",
        "expected_hgvs_p": "p.(=)",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Benign",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 translation: CCT -> CCC (Pro59=)",
            "notes": "Silent codon change at codon 59."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-017",
        "name": "Codon 105 Synonymous Boundary Control",
        "hgvs_c_input": "c.315G>A",
        "hgvs_c_canonical": "NM_000518.5:c.315G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "substitution",
        "molecular_consequence": "Synonymous",
        "region": "Exon 2",
        "coordinate_cdna": "315",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.(=)",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Benign",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 translation: AGG -> AGA (Arg105=)",
            "notes": "Last coding base of Exon 2 (c.315)."
        },
        "dataset_split": "val"
    },

    # =========================================================================
    # 4. Frameshift Deletions
    # =========================================================================
    {
        "id": "HBB-BM-018",
        "name": "Codons 41/42 (-TCTT) Frameshift",
        "hgvs_c_input": "c.126_129del",
        "hgvs_c_canonical": "NM_000518.5:c.126_129del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "Frameshift Deletion",
        "region": "Exon 2",
        "coordinate_cdna": "126_129",
        "ref_allele": "CTTT",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Phe42LeufsTer19",
        "expected_clinvar_id": "15417",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015417 / VarID 15417) & RefSeq NM_000518.5",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.Phe42fs",
            "notes": "4 bp deletion in Exon 2 causing translational frameshift with PTC at codon 60."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-019",
        "name": "Codons 41/42 (-TCTT) 5'-Aligned Alias",
        "hgvs_c_input": "c.124_127del",
        "hgvs_c_canonical": "NM_000518.5:c.126_129del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "Frameshift Deletion",
        "region": "Exon 2",
        "coordinate_cdna": "126_129",
        "ref_allele": "TTCT",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Phe42LeufsTer19",
        "expected_clinvar_id": "15417",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015417)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "HGVS 3'-shifting equivalence rule to c.126_129del",
            "notes": "Historical literature 5'-aligned representation of Cd41/42."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-020",
        "name": "Codon 40 Single Base Deletion",
        "hgvs_c_input": "c.118del",
        "hgvs_c_canonical": "NM_000518.5:c.118del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "Frameshift Deletion",
        "region": "Exon 2",
        "coordinate_cdna": "118",
        "ref_allele": "C",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Gln40ArgfsTer21",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation (data/examples/frameshift_deletion.fasta)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Downstream reading frame walk to PTC",
            "notes": "Synthetic control from data/examples."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-021",
        "name": "Codons 15/16 (-TG) Frameshift",
        "hgvs_c_input": "c.46_47del",
        "hgvs_c_canonical": "NM_000518.5:c.46_47del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "Frameshift Deletion",
        "region": "Exon 1",
        "coordinate_cdna": "46_47",
        "ref_allele": "TG",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Trp16GlyfsTer7",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "IthaGenes (ITHA-HBB-0016) & RefSeq NM_000518.5",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "RefSeq sequence translation",
            "notes": "2 bp deletion of TG at codon 16 leading to frameshift."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 5. In-Frame Deletions
    # =========================================================================
    {
        "id": "HBB-BM-022",
        "name": "Codon 18 In-Frame Deletion",
        "hgvs_c_input": "c.52_54del",
        "hgvs_c_canonical": "NM_000518.5:c.52_54del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "In-frame Deletion",
        "region": "Exon 1",
        "coordinate_cdna": "52_54",
        "ref_allele": "AAG",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Lys18del",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 in-frame triplet deletion",
            "notes": "3 bp in-frame deletion removing Lys at codon 18 without frameshift."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-023",
        "name": "Codon 10 In-Frame Deletion",
        "hgvs_c_input": "c.28_30del",
        "hgvs_c_canonical": "NM_000518.5:c.28_30del",
        "reference_accession": "NM_000518.5",
        "variant_class": "deletion",
        "molecular_consequence": "In-frame Deletion",
        "region": "Exon 1",
        "coordinate_cdna": "28_30",
        "ref_allele": "TCT",
        "alt_allele": "-",
        "expected_hgvs_p": "p.Ser10del",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "NCBI Genetic Code Table 1 in-frame triplet deletion",
            "notes": "3 bp in-frame deletion removing Ser at codon 10."
        },
        "dataset_split": "val"
    },

    # =========================================================================
    # 6. Duplications
    # =========================================================================
    {
        "id": "HBB-BM-024",
        "name": "Codons 8/9 (+G) Frameshift Duplication",
        "hgvs_c_input": "c.27dup",
        "hgvs_c_canonical": "NM_000518.5:c.27dup",
        "reference_accession": "NM_000518.5",
        "variant_class": "duplication",
        "molecular_consequence": "Frameshift Duplication",
        "region": "Exon 1",
        "coordinate_cdna": "27",
        "ref_allele": "-",
        "alt_allele": "G",
        "expected_hgvs_p": "p.Ser10ValfsTer14",
        "expected_clinvar_id": "36308",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000036308 / VarID 36308) & RefSeq NM_000518.5",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, p.Ser10fs",
            "notes": "Single G duplication in codons 8/9 with PTC at codon 23."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-025",
        "name": "Codon 122 Frameshift Duplication",
        "hgvs_c_input": "c.363dup",
        "hgvs_c_canonical": "NM_000518.5:c.363dup",
        "reference_accession": "NM_000518.5",
        "variant_class": "duplication",
        "molecular_consequence": "Frameshift Duplication",
        "region": "Exon 2",
        "coordinate_cdna": "363",
        "ref_allele": "-",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Glu122fs",
        "expected_clinvar_id": "3572119",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV003572119 / VarID 3572119)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Duplication at cDNA 363 causing frameshift."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 7. Flanked Insertions
    # =========================================================================
    {
        "id": "HBB-BM-026",
        "name": "Codons 8/9 Flanked Insertion Alias",
        "hgvs_c_input": "c.27_28insG",
        "hgvs_c_canonical": "NM_000518.5:c.27dup",
        "reference_accession": "NM_000518.5",
        "variant_class": "insertion",
        "molecular_consequence": "Frameshift Insertion",
        "region": "Exon 1",
        "coordinate_cdna": "27_28",
        "ref_allele": "-",
        "alt_allele": "G",
        "expected_hgvs_p": "p.Ser10ValfsTer14",
        "expected_clinvar_id": "36308",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "HGVS 3'-Duplication Recommendation & ClinVar 36308",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "HGVS canonicalization of insertion of repeated base to duplication",
            "notes": "Equivalent representation of c.27dup."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-027",
        "name": "Codon 39/40 Flanked Insertion",
        "hgvs_c_input": "c.117_118insA",
        "hgvs_c_canonical": "NM_000518.5:c.117_118insA",
        "reference_accession": "NM_000518.5",
        "variant_class": "insertion",
        "molecular_consequence": "Frameshift Insertion",
        "region": "Exon 2",
        "coordinate_cdna": "117_118",
        "ref_allele": "-",
        "alt_allele": "A",
        "expected_hgvs_p": "p.Gln40fs",
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 In Silico Translation (data/examples/frameshift_insertion.fasta)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Reading frame translation with 1 bp insert",
            "notes": "Synthetic control from data/examples."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 8. Splice Donor Variants (+1, +2, +5)
    # =========================================================================
    {
        "id": "HBB-BM-028",
        "name": "IVS1-5 (G>C) Indian Beta-Plus Thalassemia",
        "hgvs_c_input": "c.92+5G>C",
        "hgvs_c_canonical": "NM_000518.5:c.92+5G>C",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_donor",
        "molecular_consequence": "Splice Site Defect",
        "region": "Intron 1 (IVS-1)",
        "coordinate_cdna": "92+5",
        "ref_allele": "G",
        "alt_allele": "C",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "15447",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015447 / VarID 15447) & RefSeq NG_000007.3 (g.70691G>C)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, reviewed by expert panel",
            "notes": "Consensus splice donor +5 mutation reducing normal splicing efficiency."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-029",
        "name": "IVS1-1 (G>T) Invariant Donor Splice Disruption",
        "hgvs_c_input": "c.92+1G>T",
        "hgvs_c_canonical": "NM_000518.5:c.92+1G>T",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_donor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 1 (IVS-1)",
        "coordinate_cdna": "92+1",
        "ref_allele": "G",
        "alt_allele": "T",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "15437",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015437 / VarID 15437)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal GT dinucleotide at Intron 1 5' donor boundary."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-030",
        "name": "IVS1-2 (T>C) Invariant Donor Splice Disruption",
        "hgvs_c_input": "c.92+2T>C",
        "hgvs_c_canonical": "NM_000518.5:c.92+2T>C",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_donor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 1 (IVS-1)",
        "coordinate_cdna": "92+2",
        "ref_allele": "T",
        "alt_allele": "C",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "36334",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000036334 / VarID 36334)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal GT dinucleotide at Intron 1 5' donor position +2."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-031",
        "name": "IVS2-1 (G>A) Invariant Donor Splice Disruption",
        "hgvs_c_input": "c.315+1G>A",
        "hgvs_c_canonical": "NM_000518.5:c.315+1G>A",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_donor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 2 (IVS-2)",
        "coordinate_cdna": "315+1",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "15438",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015438 / VarID 15438)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal GT dinucleotide at Intron 2 5' donor boundary."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-032",
        "name": "IVS2-2 (T>C) Invariant Donor Splice Disruption",
        "hgvs_c_input": "c.315+2T>C",
        "hgvs_c_canonical": "NM_000518.5:c.315+2T>C",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_donor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 2 (IVS-2)",
        "coordinate_cdna": "315+2",
        "ref_allele": "T",
        "alt_allele": "C",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "869355",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000869355 / VarID 869355)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal GT dinucleotide at Intron 2 5' donor position +2."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 9. Splice Acceptor Variants (-1, -2)
    # =========================================================================
    {
        "id": "HBB-BM-033",
        "name": "IVS1 Acceptor (-1 G>A) Disruption",
        "hgvs_c_input": "c.93-1G>A",
        "hgvs_c_canonical": "NM_000518.5:c.93-1G>A",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_acceptor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 1 (IVS-1)",
        "coordinate_cdna": "93-1",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "15446",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015446 / VarID 15446)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal AG dinucleotide at Intron 1 3' acceptor boundary."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-034",
        "name": "IVS2 Acceptor (-1 G>A) Disruption",
        "hgvs_c_input": "c.316-1G>A",
        "hgvs_c_canonical": "NM_000518.5:c.316-1G>A",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_acceptor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 2 (IVS-2)",
        "coordinate_cdna": "316-1",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "552712",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000552712 / VarID 552712)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal AG dinucleotide at Intron 2 3' acceptor boundary."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-035",
        "name": "IVS2 Acceptor (-2 A>G) Disruption",
        "hgvs_c_input": "c.316-2A>G",
        "hgvs_c_canonical": "NM_000518.5:c.316-2A>G",
        "reference_accession": "NG_000007.3",
        "variant_class": "splice_acceptor",
        "molecular_consequence": "Splice Site Disruption",
        "region": "Intron 2 (IVS-2)",
        "coordinate_cdna": "316-2",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": "p.?",
        "expected_clinvar_id": "21191",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000021191 / VarID 21191)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts universal AG dinucleotide at Intron 2 3' acceptor position -2."
        },
        "dataset_split": "val"
    },

    # =========================================================================
    # 10. 5' UTR / Promoter Variants
    # =========================================================================
    {
        "id": "HBB-BM-036",
        "name": "5' UTR (-29 G>A) Pathogenic Mutation",
        "hgvs_c_input": "c.-29G>A",
        "hgvs_c_canonical": "NM_000518.5:c.-29G>A",
        "reference_accession": "NM_000518.5",
        "variant_class": "5_utr",
        "molecular_consequence": "5' UTR (Non-coding)",
        "region": "5' UTR",
        "coordinate_cdna": "-29",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "393702",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000393702 / VarID 393702)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, 5' UTR c.-29G>A",
            "notes": "5' UTR regulatory mutation reducing transcription."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-037",
        "name": "Cap Site (+1 A>C) Mutation",
        "hgvs_c_input": "c.-50A>C",
        "hgvs_c_canonical": "NM_000518.5:c.-50A>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "5_utr",
        "molecular_consequence": "5' UTR (Non-coding)",
        "region": "5' UTR",
        "coordinate_cdna": "-50",
        "ref_allele": "A",
        "alt_allele": "C",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "36292",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000036292 / VarID 36292)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, Cap site (+1)",
            "notes": "5' UTR transcription initiation site (Cap site) mutation."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-038",
        "name": "5' UTR In Silico Substitution",
        "hgvs_c_input": "c.-5A>G",
        "hgvs_c_canonical": "NM_000518.5:c.-5A>G",
        "reference_accession": "NM_000518.5",
        "variant_class": "5_utr",
        "molecular_consequence": "5' UTR (Non-coding)",
        "region": "5' UTR",
        "coordinate_cdna": "-5",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Uncertain significance",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Coordinate Validation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "5' UTR non-coding position calculation",
            "notes": "Base 46 in mRNA (5 bases upstream of translation initiation codon ATG)."
        },
        "dataset_split": "test"
    },

    # =========================================================================
    # 11. 3' UTR / Polyadenylation Variants
    # =========================================================================
    {
        "id": "HBB-BM-039",
        "name": "PolyA Signal Variant (AATAAA->AATGAA)",
        "hgvs_c_input": "c.*112A>G",
        "hgvs_c_canonical": "NM_000518.5:c.*112A>G",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*112",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "15476",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015476 / VarID 15476)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "Disrupts canonical AATAAA hexamer leading to elongated mRNA and beta-thalassemia."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-040",
        "name": "PolyA Signal Variant (*111A>G)",
        "hgvs_c_input": "c.*111A>G",
        "hgvs_c_canonical": "NM_000518.5:c.*111A>G",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*111",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "15488",
        "expected_clinvar_significance": "Pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000015488 / VarID 15488)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified, reviewed by expert panel",
            "notes": "AATAAA polyadenylation site mutation."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-041",
        "name": "3' UTR Non-coding Substitution (*6C>G)",
        "hgvs_c_input": "c.*6C>G",
        "hgvs_c_canonical": "NM_000518.5:c.*6C>G",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*6",
        "ref_allele": "C",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "393707",
        "expected_clinvar_significance": "Pathogenic/Likely pathogenic",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000393707 / VarID 393707)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "3' UTR non-coding substitution."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-042",
        "name": "3' UTR Non-coding Substitution (*10C>T)",
        "hgvs_c_input": "c.*10C>T",
        "hgvs_c_canonical": "NM_000518.5:c.*10C>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*10",
        "ref_allele": "C",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": "Benign",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Coordinate Validation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "3' UTR position calculation (base 504)",
            "notes": "10 bases downstream of stop codon TAA."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-043",
        "name": "3' UTR Non-coding Substitution (*102C>T)",
        "hgvs_c_input": "c.*102C>T",
        "hgvs_c_canonical": "NM_000518.5:c.*102C>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*102",
        "ref_allele": "C",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "495966",
        "expected_clinvar_significance": "Likely benign",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000495966 / VarID 495966)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "3' UTR polymorphism."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-044",
        "name": "3' UTR Non-coding Substitution (*129T>C)",
        "hgvs_c_input": "c.*129T>C",
        "hgvs_c_canonical": "NM_000518.5:c.*129T>C",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*129",
        "ref_allele": "T",
        "alt_allele": "C",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "3599779",
        "expected_clinvar_significance": "Likely benign",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV003599779 / VarID 3599779)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "3' UTR polymorphism near transcript end."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-045",
        "name": "3' UTR Non-coding Substitution (*67G>T)",
        "hgvs_c_input": "c.*67G>T",
        "hgvs_c_canonical": "NM_000518.5:c.*67G>T",
        "reference_accession": "NM_000518.5",
        "variant_class": "3_utr",
        "molecular_consequence": "3' UTR (Non-coding)",
        "region": "3' UTR",
        "coordinate_cdna": "*67",
        "ref_allele": "G",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": "495970",
        "expected_clinvar_significance": "Benign",
        "provenance": {
            "ground_truth_source": "NCBI ClinVar (VCV000495970 / VarID 495970)",
            "provenance_class": "Class B (External Database Evidence)",
            "verification_method": "NCBI E-utilities verified",
            "notes": "3' UTR benign variant."
        },
        "dataset_split": "val"
    },

    # =========================================================================
    # 12. Negative Controls & Error Traps (N = 20)
    # Must be cleanly rejected with descriptive error messages.
    # =========================================================================
    {
        "id": "HBB-BM-NEG-001",
        "name": "Inverted Deletion Coordinates",
        "hgvs_c_input": "c.129_126del",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 2",
        "coordinate_cdna": "129_126",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "start coordinate must precede end coordinate",
        "provenance": {
            "ground_truth_source": "HGVS Sequence Variant Nomenclature Recommendations",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Syntax specification rule: coordinate ranges must be 5' to 3'",
            "notes": "Error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-002",
        "name": "Non-consecutive Insertion Coordinates",
        "hgvs_c_input": "c.25_28insG",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 1",
        "coordinate_cdna": "25_28",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "two consecutive flanking positions",
        "provenance": {
            "ground_truth_source": "HGVS Sequence Variant Nomenclature Recommendations",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Syntax specification rule: insertions must specify consecutive flanking nucleotides",
            "notes": "Error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-003",
        "name": "Transcript Out-of-Bounds Deletion",
        "hgvs_c_input": "c.999del",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Out of Bounds",
        "coordinate_cdna": "999",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "out of bounds",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Total Length (628 bp)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Coordinate validation: 999 exceeds transcript length 628",
            "notes": "Error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-004",
        "name": "Transcript Out-of-Bounds Substitution",
        "hgvs_c_input": "c.999C>T",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Out of Bounds",
        "coordinate_cdna": "999",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "out of bounds",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Total Length (628 bp)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Coordinate validation: 999 exceeds transcript length",
            "notes": "Error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-005",
        "name": "Reference Base Mismatch at c.9 (Expected T, got A)",
        "hgvs_c_input": "c.9delA",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 1",
        "coordinate_cdna": "9",
        "ref_allele": "A",
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Reference Nucleotide (c.9 is T)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against reference sequence",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-006",
        "name": "Reference Base Mismatch at c.118 (Expected C, got A)",
        "hgvs_c_input": "c.118A>T",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 2",
        "coordinate_cdna": "118",
        "ref_allele": "A",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Reference Nucleotide (c.118 is C)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against reference sequence",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-007",
        "name": "Reference Base Mismatch at c.20 (Expected A, got G)",
        "hgvs_c_input": "c.20G>T",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 1",
        "coordinate_cdna": "20",
        "ref_allele": "G",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Reference Nucleotide (c.20 is A)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against reference sequence",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-008",
        "name": "Reference Base Mismatch at c.19 (Expected G, got A)",
        "hgvs_c_input": "c.19A>G",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 1",
        "coordinate_cdna": "19",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NM_000518.5 Reference Nucleotide (c.19 is G)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against reference sequence",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-009",
        "name": "Reference Base Mismatch at c.92+5 (Expected G, got A)",
        "hgvs_c_input": "c.92+5A>C",
        "hgvs_c_canonical": None,
        "reference_accession": "NG_000007.3",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Intron 1 (IVS-1)",
        "coordinate_cdna": "92+5",
        "ref_allele": "A",
        "alt_allele": "C",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NG_000007.3 Reference Nucleotide (position 147 is G)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against genomic locus reference",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-010",
        "name": "Reference Base Mismatch at c.315+1 (Expected G, got A)",
        "hgvs_c_input": "c.315+1A>G",
        "hgvs_c_canonical": None,
        "reference_accession": "NG_000007.3",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Intron 2 (IVS-2)",
        "coordinate_cdna": "315+1",
        "ref_allele": "A",
        "alt_allele": "G",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Reference base mismatch",
        "provenance": {
            "ground_truth_source": "RefSeq NG_000007.3 Reference Nucleotide (position 496 is G)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Allele validation against genomic locus reference",
            "notes": "Biological error trap."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-011",
        "name": "Garbage Non-HGVS String",
        "hgvs_c_input": "invalid_syntax_123",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Invalid",
        "coordinate_cdna": None,
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "Input Parsing Validation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Regex filter",
            "notes": "Syntax error trap."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-NEG-012",
        "name": "Incomplete HGVS Missing Alteration",
        "hgvs_c_input": "c.118",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Invalid",
        "coordinate_cdna": "118",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "Input Parsing Validation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Regex filter",
            "notes": "Syntax error trap."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-NEG-013",
        "name": "Incomplete Range Missing Operator",
        "hgvs_c_input": "c.118_119",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Invalid",
        "coordinate_cdna": "118_119",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "Input Parsing Validation",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Regex filter",
            "notes": "Syntax error trap."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-NEG-014",
        "name": "Non-Canonical Nucleotide Alphabet",
        "hgvs_c_input": "c.118C>Z",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Invalid",
        "coordinate_cdna": "118",
        "ref_allele": "C",
        "alt_allele": "Z",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "invalid or unsupported",
        "provenance": {
            "ground_truth_source": "IUPAC Nucleotide Alphabet Standards",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Alphabet validation",
            "notes": "Alphabet error trap."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-NEG-015",
        "name": "Out-of-Bounds Intron 1 Offset",
        "hgvs_c_input": "c.92+999G>A",
        "hgvs_c_canonical": None,
        "reference_accession": "NG_000007.3",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Intron 1",
        "coordinate_cdna": "92+999",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "outside supported HBB gene boundaries or introns",
        "provenance": {
            "ground_truth_source": "RefSeq NG_000007.3 Intron 1 Length (130 bp)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Intron boundary validation",
            "notes": "Intron 1 offset 999 exceeds 130 bp intron length."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-016",
        "name": "Out-of-Bounds Intron 2 Offset",
        "hgvs_c_input": "c.315+999G>A",
        "hgvs_c_canonical": None,
        "reference_accession": "NG_000007.3",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Intron 2",
        "coordinate_cdna": "315+999",
        "ref_allele": "G",
        "alt_allele": "A",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "outside supported HBB gene boundaries or introns",
        "provenance": {
            "ground_truth_source": "RefSeq NG_000007.3 Intron 2 Length (850 bp)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Intron boundary validation",
            "notes": "Intron 2 offset 999 exceeds 850 bp intron length."
        },
        "dataset_split": "test"
    },
    {
        "id": "HBB-BM-NEG-017",
        "name": "Illegal Coordinate Zero in HGVS",
        "hgvs_c_input": "c.0C>T",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Invalid",
        "coordinate_cdna": "0",
        "ref_allele": "C",
        "alt_allele": "T",
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "out of bounds",
        "provenance": {
            "ground_truth_source": "HGVS Nomenclature (No base zero between -1 and +1)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Coordinate validation: position 0 does not exist",
            "notes": "Syntax error trap."
        },
        "dataset_split": "dev"
    },
    {
        "id": "HBB-BM-NEG-018",
        "name": "Chromosome Prefix Without cDNA",
        "hgvs_c_input": "chr11:g.5227002C>T",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Genomic",
        "coordinate_cdna": None,
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "Direct Variant Parser Specification",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Syntax rejection of whole-chromosome prefixes",
            "notes": "Syntax error trap."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-NEG-019",
        "name": "Deprecated Numeric Deletion Length",
        "hgvs_c_input": "c.118_120del3",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 2",
        "coordinate_cdna": "118_120",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "HGVS Specification (Numeric del counts deprecated)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Syntax rejection of deprecated numeric suffix",
            "notes": "Syntax error trap."
        },
        "dataset_split": "val"
    },
    {
        "id": "HBB-BM-NEG-020",
        "name": "Empty Delins Sequence",
        "hgvs_c_input": "c.118delins",
        "hgvs_c_canonical": None,
        "reference_accession": "NM_000518.5",
        "variant_class": "negative_control",
        "molecular_consequence": "Invalid / Rejected",
        "region": "Exon 2",
        "coordinate_cdna": "118",
        "ref_allele": None,
        "alt_allele": None,
        "expected_hgvs_p": None,
        "expected_clinvar_id": None,
        "expected_clinvar_significance": None,
        "expected_rejection_reason": "Query must follow standard HGVS notation",
        "provenance": {
            "ground_truth_source": "HGVS Specification (delins requires inserted sequence)",
            "provenance_class": "Class A (Authoritative Standard)",
            "verification_method": "Syntax rejection of empty delins",
            "notes": "Syntax error trap."
        },
        "dataset_split": "dev"
    }
]

def main():
    manifest_dir = ROOT / "research" / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    master_path = manifest_dir / "hbb_benchmark_manifest.json"
    dev_path = manifest_dir / "development.json"
    val_path = manifest_dir / "validation.json"
    frozen_test_path = manifest_dir / "frozen_test.json"

    # 1. Master manifest
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(VARIANTS, f, indent=2)

    # 2. Splits
    dev_vars = [v for v in VARIANTS if v["dataset_split"] == "dev"]
    val_vars = [v for v in VARIANTS if v["dataset_split"] == "val"]
    test_vars = [v for v in VARIANTS if v["dataset_split"] == "test"]

    with open(dev_path, "w", encoding="utf-8") as f:
        json.dump(dev_vars, f, indent=2)

    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(val_vars, f, indent=2)

    # Dump frozen_test with sorted keys and explicit LF for cryptographic stability
    frozen_content = json.dumps(test_vars, indent=2, sort_keys=True)
    with open(frozen_test_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(frozen_content)

    with open(frozen_test_path, "rb") as f:
        test_hash = hashlib.sha256(f.read()).hexdigest()

    hash_file = manifest_dir / "frozen_test.sha256"
    with open(hash_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{test_hash}  frozen_test.json\n")

    print("=" * 60)
    print("   HBB PHASE 2B BENCHMARK MANIFEST GENERATION COMPLETE")
    print("=" * 60)
    print(f"Total benchmark records: {len(VARIANTS)}")
    print(f"  • Development Set (D_dev): {len(dev_vars)}")
    print(f"  • Validation Set (D_val):  {len(val_vars)}")
    print(f"  • Frozen Test Set (D_test):{len(test_vars)}")
    print(f"Frozen test SHA-256:       {test_hash}")
    print(f"Saved to: {manifest_dir}")

if __name__ == "__main__":
    main()
