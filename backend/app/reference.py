"""HBB Reference sequence manager, dual reference architecture (cDNA NM_000518.5 + Genomic NG_000007.3), and coordinate mapping."""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class Exon:
    number: int
    start: int  # 1-based
    end: int    # 1-based
    genomic_start: Optional[int] = None
    genomic_end: Optional[int] = None


@dataclass
class ReferenceData:
    gene: str
    organism: str
    accession: str
    molecule_type: str
    total_length: int
    cds_start: int  # 1-based mRNA or relative start position (e.g., 51)
    cds_end: int    # 1-based position (e.g., 494)
    cds_length: int # e.g., 444 bp
    protein_id: str
    protein_length: int
    source: str
    source_url: str
    description: str
    sequence: str
    cds_sequence: str
    protein_sequence: str
    exons: List[Exon] = field(default_factory=list)
    introns: List[Dict[str, Any]] = field(default_factory=list)
    genomic_start: Optional[int] = None
    genomic_end: Optional[int] = None

    def mrna_pos_to_c_pos(self, mrna_pos: int) -> str:
        """
        Converts 1-based mRNA nucleotide position to standard HGVS cDNA c. position.
        5' UTR: c.-1, c.-2, etc.
        CDS: c.1 to c.444
        3' UTR: c.*1, c.*2, etc.
        """
        if mrna_pos < self.cds_start:
            offset = mrna_pos - self.cds_start  # negative integer
            return str(offset)
        elif mrna_pos <= self.cds_end:
            offset = mrna_pos - self.cds_start + 1
            return str(offset)
        else:
            offset = mrna_pos - self.cds_end
            return f"*{offset}"

    def c_pos_to_mrna_pos(self, c_str: str) -> Optional[int]:
        """
        Converts standard HGVS c. position string to 1-based mRNA position.
        e.g., '118' -> 168
        '-1' -> 50
        '*1' -> 495
        """
        try:
            if c_str.startswith("*"):
                offset = int(c_str[1:])
                if offset <= 0:
                    return None
                return self.cds_end + offset
            val = int(c_str)
            if val < 0:
                return self.cds_start + val
            elif val > 0:
                return self.cds_start + val - 1
            return None
        except ValueError:
            return None


class ReferenceManager:
    """Loads and provides access to official HBB reference data (cDNA and genomic)."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or settings.DATA_DIR
        self.ref_dir = self.data_dir / "reference"
        self._cache: Dict[str, ReferenceData] = {}
        self._indian_mutations_cache: Optional[Dict[str, Any]] = None
        self._load_accession(settings.DEFAULT_REFERENCE_ACCESSION)

    def _load_accession(self, accession: str) -> None:
        fasta_path = self.ref_dir / f"{accession}.fasta"
        json_path = self.ref_dir / f"{accession}.json"

        if not fasta_path.exists() or not json_path.exists():
            raise FileNotFoundError(
                f"Reference files for {accession} not found at {self.ref_dir}."
            )

        with open(json_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        with open(fasta_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            seq = "".join(l.strip() for l in lines if not l.startswith(">")).upper()

        if accession == "NM_000518.5":
            cds_start = meta["cds_start"]
            cds_end = meta["cds_end"]
            cds_sequence = seq[cds_start - 1 : cds_end]
            exons = [
                Exon(number=e["number"], start=e["start"], end=e["end"])
                for e in meta.get("exons", [])
            ]
            introns = []
            gen_start = None
            gen_end = None
            protein_id = meta.get("protein_id", "NP_000509.1")
            protein_len = meta.get("protein_length", 147)
            prot_seq = meta.get("protein_sequence", "")
        else:
            # Genomic NG_000007.3 locus
            cds_start = meta.get("cds_genomic_start", 70595)
            cds_end = meta.get("cds_genomic_end", 72018)
            cds_sequence = ""
            exons = [
                Exon(
                    number=e["number"],
                    start=e["relative_start"],
                    end=e["relative_end"],
                    genomic_start=e.get("genomic_start"),
                    genomic_end=e.get("genomic_end")
                )
                for e in meta.get("exons", [])
            ]
            introns = meta.get("introns", [])
            gen_start = meta.get("genomic_locus_start", 70545)
            gen_end = meta.get("genomic_locus_end", 72152)
            protein_id = "NP_000509.1"
            protein_len = 147
            prot_seq = ""

        ref_data = ReferenceData(
            gene=meta.get("gene", "HBB"),
            organism=meta.get("organism", "Homo sapiens"),
            accession=accession,
            molecule_type=meta.get("molecule_type", "mRNA" if accession.startswith("NM_") else "genomic DNA"),
            total_length=len(seq),
            cds_start=cds_start,
            cds_end=cds_end,
            cds_length=meta.get("cds_length", len(cds_sequence)),
            protein_id=protein_id,
            protein_length=protein_len,
            source=meta.get("source", "NCBI RefSeq"),
            source_url=meta.get("source_url", ""),
            description=meta.get("description", ""),
            sequence=seq,
            cds_sequence=cds_sequence,
            protein_sequence=prot_seq,
            exons=exons,
            introns=introns,
            genomic_start=gen_start,
            genomic_end=gen_end
        )
        self._cache[accession] = ref_data

    def get_reference(self, accession: str = "NM_000518.5") -> ReferenceData:
        if accession not in self._cache:
            try:
                self._load_accession(accession)
            except FileNotFoundError:
                raise KeyError(f"Reference accession '{accession}' is not supported.")
        return self._cache[accession]

    def list_references(self) -> List[Dict[str, Any]]:
        """Lists available reference sequences with metadata."""
        results = []
        for acc in ["NM_000518.5", "NG_000007.3"]:
            try:
                ref = self.get_reference(acc)
                results.append({
                    "accession": ref.accession,
                    "gene": ref.gene,
                    "molecule_type": ref.molecule_type,
                    "total_length": ref.total_length,
                    "description": ref.description,
                    "source": ref.source,
                    "exons_count": len(ref.exons),
                    "introns_count": len(ref.introns)
                })
            except Exception as e:
                logger.warning(f"Failed to load reference {acc}: {e}")
        return results

    def get_indian_mutations(self) -> Dict[str, Any]:
        """Loads and caches the verified 4 Indian thalassemia mutations dataset."""
        if self._indian_mutations_cache is None:
            mut_path = self.ref_dir / "indian_mutations.json"
            if mut_path.exists():
                with open(mut_path, "r", encoding="utf-8") as f:
                    self._indian_mutations_cache = json.load(f)
            else:
                self._indian_mutations_cache = {"mutations": []}
        return self._indian_mutations_cache


# Global instance
reference_manager = ReferenceManager()
