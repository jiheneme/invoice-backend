from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    invoice_agent_url: str
    invoice_mcp_server_url: str
    
    env: str = "dev"

    model_config = SettingsConfigDict(
        env_file=".env",  # Used only by Pydantic, overridden manually with dotenv
        env_file_encoding="utf-8",
    )

def get_settings() -> Settings:
    env = os.getenv("ENV", "dev")
    base_env_path = Path(".env")
    env_path = Path(f".env.{env}")

    # Load base environment variables first
    if base_env_path.exists():
        load_dotenv(dotenv_path=base_env_path, override=False)

    # Then override with environment-specific variables (dev, rec, prod)
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)

    return Settings()
