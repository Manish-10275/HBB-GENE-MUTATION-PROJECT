"""Application configuration settings for HBB Mutation Analyzer."""

import json
from pathlib import Path
from typing import Any, List, Optional, Union
from pydantic import field_validator
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
    FRONTEND_ORIGIN: Optional[str] = None
    FRONTEND_URL: Optional[str] = None
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    CORS_ORIGIN_REGEX: Optional[str] = r"https?://(localhost|127\.0\.0\.1)(:\d+)?"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(i).strip() for i in parsed if str(i).strip() and str(i).strip() != "*"]
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip() and i.strip() != "*"]
        elif isinstance(v, (list, tuple, set)):
            return [str(i).strip() for i in v if str(i).strip() and str(i).strip() != "*"]
        return []

    @property
    def effective_cors_origins(self) -> List[str]:
        """Consolidates allowed origins ensuring dev origins and configured frontend origins are present.

        Strictly rejects arbitrary wildcard origins ('*').
        """
        origins: List[str] = []

        default_dev = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
        for dev_url in default_dev:
            if dev_url not in origins:
                origins.append(dev_url)

        if isinstance(self.CORS_ORIGINS, list):
            for o in self.CORS_ORIGINS:
                cleaned = o.strip().rstrip("/")
                if cleaned and cleaned != "*" and cleaned not in origins:
                    origins.append(cleaned)
        elif isinstance(self.CORS_ORIGINS, str):
            for part in self.CORS_ORIGINS.split(","):
                cleaned = part.strip().rstrip("/")
                if cleaned and cleaned != "*" and cleaned not in origins:
                    origins.append(cleaned)

        for candidate in (self.FRONTEND_ORIGIN, self.FRONTEND_URL):
            if candidate:
                for part in candidate.split(","):
                    cleaned = part.strip().rstrip("/")
                    if cleaned and cleaned != "*" and cleaned not in origins:
                        origins.append(cleaned)

        return origins

    # External APIs
    NCBI_EMAIL: Optional[str] = "researcher@example.edu"
    NCBI_API_KEY: Optional[str] = None
    NCBI_BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

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
