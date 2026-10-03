"""HBB Reference sequence manager and genomic coordinate mapping."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from app.config import settings


@dataclass
class Exon:
    number: int
    start: int  # 1-based mRNA
    end: int    # 1-based mRNA


@dataclass
class ReferenceData:
    gene: str
    organism: str
    accession: str
    molecule_type: str
    total_length: int
    cds_start: int  # 1-based mRNA position (e.g., 51)
    cds_end: int    # 1-based mRNA position (e.g., 494)
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
    """Loads and provides access to official HBB reference data."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or settings.DATA_DIR
        self.ref_dir = self.data_dir / "reference"
        self._cache: Dict[str, ReferenceData] = {}
        self._load_default()

    def _load_default(self) -> None:
        accession = settings.DEFAULT_REFERENCE_ACCESSION
        fasta_path = self.ref_dir / f"{accession}.fasta"
        json_path = self.ref_dir / f"{accession}.json"

        if not fasta_path.exists() or not json_path.exists():
            raise FileNotFoundError(
                f"Reference files for {accession} not found at {self.ref_dir}. "
                "Ensure data/reference/NM_000518.5.fasta and NM_000518.5.json exist."
            )

        with open(json_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        with open(fasta_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            seq = "".join(l.strip() for l in lines if not l.startswith(">")).upper()

        cds_start = meta["cds_start"]
        cds_end = meta["cds_end"]
        # In Python 0-based slicing: cds_start-1 to cds_end
        cds_sequence = seq[cds_start - 1 : cds_end]

        exons = [
            Exon(number=e["number"], start=e["start"], end=e["end"])
            for e in meta.get("exons", [])
        ]

        ref_data = ReferenceData(
            gene=meta.get("gene", "HBB"),
            organism=meta.get("organism", "Homo sapiens"),
            accession=accession,
            molecule_type=meta.get("molecule_type", "mRNA"),
            total_length=len(seq),
            cds_start=cds_start,
            cds_end=cds_end,
            cds_length=len(cds_sequence),
            protein_id=meta.get("protein_id", "NP_000509.1"),
            protein_length=meta.get("protein_length", 147),
            source=meta.get("source", "NCBI RefSeq MANE Select"),
            source_url=meta.get("source_url", ""),
            description=meta.get("description", ""),
            sequence=seq,
            cds_sequence=cds_sequence,
            protein_sequence=meta.get("protein_sequence", ""),
            exons=exons
        )
        self._cache[accession] = ref_data

    def get_reference(self, accession: str = "NM_000518.5") -> ReferenceData:
        if accession not in self._cache:
            if accession == settings.DEFAULT_REFERENCE_ACCESSION:
                self._load_default()
            else:
                raise KeyError(f"Reference accession '{accession}' is not supported.")
        return self._cache[accession]


# Global instance
reference_manager = ReferenceManager()
