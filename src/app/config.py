from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Keys
    EXA_API_KEY: str = ""
    JINA_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./market_intelligence.db"
    
    # LLM Configuration
    DEFAULT_LLM_MODEL: str = "gpt-4o"
    DEFAULT_LLM_TEMPERATURE: float = 0.7
    
    # Optional additional configurations
    DEBUG: bool = False
    
    # Use environment files and environment variables
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

def get_settings() -> Settings:
    """
    Retrieve application settings.
    
    Returns:
        Settings: Configured application settings
    """
    return Settings()
