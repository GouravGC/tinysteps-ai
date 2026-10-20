import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemma-3-4b-it:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    default_provider: str = "Local Gemma (Ollama)"
    request_timeout: int = 90

    @classmethod
    def from_env(cls):
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"),
            ollama_model=os.getenv("OLLAMA_MODEL", "gemma3:4b"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
            openrouter_model=os.getenv("OPENROUTER_MODEL", "google/gemma-3-4b-it:free"),
            openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/"),
            default_provider=os.getenv("DEFAULT_PROVIDER", "Local Gemma (Ollama)"),
            request_timeout=int(os.getenv("AI_REQUEST_TIMEOUT", "90")),
        )
