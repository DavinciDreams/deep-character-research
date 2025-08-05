from dataclasses import dataclass
from pathlib import Path
import os
from typing import Optional

@dataclass
class ResearchConfig:
    # Database paths - use user documents folder
    base_data_dir: str = str(Path.home() / "Documents" / "DeepCharacterResearch")
    
    def __post_init__(self):
        # Ensure data directory exists
        Path(self.base_data_dir).mkdir(parents=True, exist_ok=True)
        
        # Set up database paths
        self.vector_db_path = str(Path(self.base_data_dir) / "vector_db")
        self.doc_store_path = str(Path(self.base_data_dir) / "documents.db")

        # AI Provider settings (runtime env loading)
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

        # LM Studio settings
        self.lmstudio_base_url: str = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
        self.lmstudio_model: str = os.getenv("LMSTUDIO_MODEL", "local-model")

        # Default provider and model
        self.default_provider: str = os.getenv("DEFAULT_AI_PROVIDER", "openrouter")
        self.default_model: str = os.getenv("DEFAULT_MODEL", "nvidia/llama-3.1-nemotron-ultra-253b-v1:free")

        # Fallback settings
        self.fallback_enabled: bool = os.getenv("FALLBACK_ENABLED", "true").lower() == "true"

        # Fail early if OpenRouter API key is missing
        if not self.openrouter_api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY environment variable is missing. "
                "Please set it in your environment or .env file."
            )
    
    # Research settings
    max_sources_per_domain: int = 50
    research_timeout: int = 300  # 5 minutes
    
    def get_ai_config(self):
        """Get AI configuration object"""
        from ai_providers import AIConfig
        
        return AIConfig(
            openai_api_key=self.openai_api_key,
            openrouter_api_key=self.openrouter_api_key,
            anthropic_api_key=self.anthropic_api_key,
            lmstudio_base_url=self.lmstudio_base_url,
            lmstudio_model=self.lmstudio_model,
            default_provider=self.default_provider,
            default_model=self.default_model,
            fallback_enabled=self.fallback_enabled
        )