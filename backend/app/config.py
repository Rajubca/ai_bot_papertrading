from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict

import os
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    # Core
    DB_URL: str = Field(default="mysql+pymysql://root:root@localhost/ai_trading")
    GROQ_API_KEY: str = Field(default=os.getenv("GROQ_API_KEY")) # Line 19 is now safe!
    JWT_SECRET: str = Field(default="dev-secret")
    

    # Optional (safe defaults)
    APP_ENV: str = "local"
    APP_NAME: str = "papertrade-ai"
    DEBUG: bool = True

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    GROQ_MODEL: str = "llama-3.1-70b"

    MARKET_DATA_PROVIDER: str = "yfinance"
    PRICE_REFRESH_SECONDS: int = 5

    REPORT_OUTPUT_DIR: str = "./reports"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"   # 🔑 THIS FIXES YOUR ERROR
    )


settings = Settings()
