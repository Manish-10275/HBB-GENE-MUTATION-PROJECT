"""Pure reference sequence loading and coordinate mapping for NM_000518.5 and NG_000007.3."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.models import AnalysisError, AnalysisErrorCode, Exon


@dataclass(frozen=True)
class ReferenceSequence:
    """Immutable biological reference sequence data."""
    accession: str
    gene: str
    organism: str
    molecule_type: str
    total_length: int
    cds_start: int          # 1-based start (e.g. 51 on NM_000518.5)
    cds_end: int            # 1-based end (e.g. 494 on NM_000518.5)
    cds_length: int         # 444 bp
    protein_id: str         # "NP_000509.1"
    protein_length: int     # 147 aa
    sequence: str           # Full uppercase nucleotide sequence
    cds_sequence: str       # Exact coding sequence (length == cds_length)
    protein_sequence: str   # 147 amino acid translation
    exons: List[Exon] = field(default_factory=list)
    introns: List[Dict[str, Any]] = field(default_factory=list)
    genomic_start: Optional[int] = None
    genomic_end: Optional[int] = None

    def c_pos_to_mrna_pos(self, c_str: str) -> int:
        """
        Converts standard HGVS cDNA c. position to 1-based mRNA nucleotide position.
        
        Raises AnalysisError if position is invalid or out of bounds.
        """
        clean = c_str.replace("c.", "").strip()
        if clean == "0":
            raise AnalysisError(
                AnalysisErrorCode.INVALID_COORDINATE,
                "HGVS nomenclature does not recognize base zero (c.0). Nucleotide preceding c.1 is c.-1."
            )

        if clean.startswith("*"):
            try:
                offset = int(clean[1:])
            except ValueError:
                raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Malformed 3' UTR coordinate '{c_str}'.")
            if offset < 1:
                raise AnalysisError(AnalysisErrorCode.INVALID_COORDINATE, f"Invalid 3' UTR offset '{clean}'.")
            pos = self.cds_end + offset
            if pos > self.total_length:
                raise AnalysisError(
                    AnalysisErrorCode.OUT_OF_BOUNDS,
                    f"Coordinate '{c_str}' (mRNA {pos}) exceeds reference length ({self.total_length} bp)."
                )
            return pos

        try:
            val = int(clean)
        except ValueError:
            raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Non-numeric cDNA coordinate '{c_str}'.")

        if val < 0:
            pos = self.cds_start + val
            if pos < 1:
                raise AnalysisError(
                    AnalysisErrorCode.OUT_OF_BOUNDS,
                    f"Coordinate '{c_str}' (mRNA {pos}) precedes start of transcript (5' UTR length is {self.cds_start - 1} bp)."
                )
            return pos
        else:
            pos = self.cds_start + val - 1
            if pos > self.total_length:
                raise AnalysisError(
                    AnalysisErrorCode.OUT_OF_BOUNDS,
                    f"Coordinate '{c_str}' (mRNA {pos}) exceeds reference transcript length ({self.total_length} bp)."
                )
            return pos

    def mrna_pos_to_c_pos(self, mrna_pos: int) -> str:
        """Converts 1-based mRNA position to standard HGVS cDNA c. position."""
        if mrna_pos < 1 or mrna_pos > self.total_length:
            raise AnalysisError(
                AnalysisErrorCode.OUT_OF_BOUNDS,
                f"mRNA position {mrna_pos} is outside reference length 1..{self.total_length}."
            )
        if mrna_pos < self.cds_start:
            return str(mrna_pos - self.cds_start)
        elif mrna_pos <= self.cds_end:
            return str(mrna_pos - self.cds_start + 1)
        else:
            return f"*{mrna_pos - self.cds_end}"

    def get_region_for_c_pos(self, c_str: str) -> str:
        """Determines the biological region (Exon 1..3, 5' UTR, 3' UTR, etc.) for a cDNA coordinate."""
        clean = c_str.replace("c.", "").strip()
        if clean.startswith("*"):
            return "3' UTR"
        try:
            val = int(clean)
            if val < 0:
                return "5' UTR"
            elif 1 <= val <= 92:
                return "Exon 1"
            elif 93 <= val <= 315:
                return "Exon 2"
            elif 316 <= val <= 444:
                return "Exon 3"
            else:
                return "3' UTR"
        except ValueError:
            if "92+" in clean or "93-" in clean:
                return "Intron 1"
            if "315+" in clean or "316-" in clean:
                return "Intron 2"
            return "Unknown Region"


def map_intronic_cdna_to_genomic(
    c_pos_str: str,
    ng_ref: ReferenceSequence
) -> Tuple[int, int, str]:
    """
    Maps an intronic cDNA notation (e.g. '92+5' or '315+1') to:
    (1-based relative locus position in NG_000007.3, exact genomic coordinate, region_name).
    
    Locus architecture on NG_000007.3 (70545..72152):
    - Exon 1: 1..142 (c.-50..c.92) [70545..70686]
    - Intron 1: 143..272 (c.92+1..c.92+130 / c.93-1..c.93-130) [70687..70816] (130 bp)
    - Exon 2: 273..495 (c.93..c.315) [70817..71039]
    - Intron 2: 496..1345 (c.315+1..c.315+850 / c.316-1..c.316-850) [71040..71889] (850 bp)
    - Exon 3: 1346..1608 (c.316..c.*134) [71890..72152]
    """
    clean = c_pos_str.replace("c.", "").strip()

    # Intron 1 Donor (c.92+N)
    if clean.startswith("92+"):
        try:
            offset = int(clean[3:])
        except ValueError:
            raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Malformed intronic offset in '{c_pos_str}'.")
        if offset < 1 or offset > 130:
            raise AnalysisError(
                AnalysisErrorCode.OUT_OF_BOUNDS,
                f"Intronic coordinate 'c.{clean}' exceeds Intron 1 physical length (130 bp)."
            )
        rel_pos = 142 + offset
        genomic_pos = 70686 + offset
        return rel_pos, genomic_pos, "Intron 1"

    # Intron 1 Acceptor (c.93-N)
    if clean.startswith("93-"):
        try:
            offset = int(clean[3:])
        except ValueError:
            raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Malformed intronic offset in '{c_pos_str}'.")
        if offset < 1 or offset > 130:
            raise AnalysisError(
                AnalysisErrorCode.OUT_OF_BOUNDS,
                f"Intronic coordinate 'c.{clean}' exceeds Intron 1 physical length (130 bp)."
            )
        rel_pos = 273 - offset
        genomic_pos = 70817 - offset
        return rel_pos, genomic_pos, "Intron 1"

    # Intron 2 Donor (c.315+N)
    if clean.startswith("315+"):
        try:
            offset = int(clean[4:])
        except ValueError:
            raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Malformed intronic offset in '{c_pos_str}'.")
        if offset < 1 or offset > 850:
            raise AnalysisError(
                AnalysisErrorCode.OUT_OF_BOUNDS,
                f"Intronic coordinate 'c.{clean}' exceeds Intron 2 physical length (850 bp)."
            )
        rel_pos = 495 + offset
        genomic_pos = 71039 + offset
        return rel_pos, genomic_pos, "Intron 2"

    # Intron 2 Acceptor (c.316-N)
    if clean.startswith("316-"):
        try:
            offset = int(clean[4:])
        except ValueError:
            raise AnalysisError(AnalysisErrorCode.SYNTAX_ERROR, f"Malformed intronic offset in '{c_pos_str}'.")
        if offset < 1 or offset > 850:
            raise AnalysisError(
                AnalysisErrorCode.OUT_OF_BOUNDS,
                f"Intronic coordinate 'c.{clean}' exceeds Intron 2 physical length (850 bp)."
            )
        rel_pos = 1346 - offset
        genomic_pos = 71890 - offset
        return rel_pos, genomic_pos, "Intron 2"

    raise AnalysisError(
        AnalysisErrorCode.OUT_OF_BOUNDS,
        f"Coordinate '{c_pos_str}' does not map to a recognized HBB intronic splice junction."
    )


# Reference Cache & Loader
_REFERENCE_CACHE: Dict[str, ReferenceSequence] = {}


def load_reference(accession: str = "NM_000518.5", ref_dir: Optional[Path] = None) -> ReferenceSequence:
    """Loads and caches reference sequence data from versioned local repository files."""
    if accession in _REFERENCE_CACHE:
        return _REFERENCE_CACHE[accession]

    target_dir = ref_dir or (Path(__file__).resolve().parent.parent.parent.parent / "data" / "reference")
    fasta_path = target_dir / f"{accession}.fasta"
    json_path = target_dir / f"{accession}.json"

    if not fasta_path.exists() or not json_path.exists():
        raise AnalysisError(
            AnalysisErrorCode.EXTERNAL_SOURCE_UNAVAILABLE,
            f"Reference files for '{accession}' not found at {target_dir}."
        )

    with open(json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    with open(fasta_path, "r", encoding="utf-8") as f:
        seq = "".join(l.strip() for l in f if not l.startswith(">")).upper()

    if accession == "NM_000518.5":
        cds_start = meta["cds_start"]
        cds_end = meta["cds_end"]
        cds_seq = seq[cds_start - 1 : cds_end]
        exons = [Exon(number=e["number"], start=e["start"], end=e["end"]) for e in meta.get("exons", [])]
        introns = []
        gen_start = None
        gen_end = None
    else:
        cds_start = meta.get("cds_genomic_start", 70595)
        cds_end = meta.get("cds_genomic_end", 72018)
        cds_seq = ""
        exons = [
            Exon(
                number=e["number"],
                start=e["relative_start"],
                end=e["relative_end"],
                genomic_start=e.get("genomic_start"),
                genomic_end=e.get("genomic_end"),
            )
            for e in meta.get("exons", [])
        ]
        introns = meta.get("introns", [])
        gen_start = meta.get("genomic_locus_start", 70545)
        gen_end = meta.get("genomic_locus_end", 72152)

    ref = ReferenceSequence(
        accession=accession,
        gene=meta.get("gene", "HBB"),
        organism=meta.get("organism", "Homo sapiens"),
        molecule_type=meta.get("molecule_type", "mRNA" if accession.startswith("NM_") else "genomic DNA"),
        total_length=len(seq),
        cds_start=cds_start,
        cds_end=cds_end,
        cds_length=meta.get("cds_length", len(cds_seq)),
        protein_id=meta.get("protein_id", "NP_000509.1"),
        protein_length=meta.get("protein_length", 147),
        sequence=seq,
        cds_sequence=cds_seq,
        protein_sequence=meta.get("protein_sequence", ""),
        exons=exons,
        introns=introns,
        genomic_start=gen_start,
        genomic_end=gen_end,
    )
    _REFERENCE_CACHE[accession] = ref
    return ref
