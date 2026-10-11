"""Application configuration settings for HBB Mutation Analyzer."""

from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    REFERENCE_DIR: Path = DATA_DIR / "reference"
    EXAMPLES_DIR: Path = DATA_DIR / "examples"

    # Reference settings
    DEFAULT_REFERENCE_ACCESSION: str = "NM_000518.5"
    DEFAULT_REFERENCE_FILE: Path = REFERENCE_DIR / "NM_000518.5.fasta"
    DEFAULT_METADATA_FILE: Path = REFERENCE_DIR / "NM_000518.5.json"

    # API and CORS
    API_TITLE: str = "HBB Mutation Analyzer API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Genomic research and education API for the human HBB gene"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]

    # External APIs
    NCBI_EMAIL: Optional[str] = "researcher@example.edu"
    NCBI_API_KEY: Optional[str] = None
    NCBI_BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    EVIDENCE_MODE: str = "offline"  # "offline" or "live"

    # Groq configuration (Ultra-fast LLM inference)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_MAX_TOKENS: int = 2500

    @property
    def effective_groq_api_key(self) -> Optional[str]:
        """Returns GROQ_API_KEY if configured."""
        return self.GROQ_API_KEY

    model_config = SettingsConfigDict(
        env_file=(Path(__file__).resolve().parent.parent.parent / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
