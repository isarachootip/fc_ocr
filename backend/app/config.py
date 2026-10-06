import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Vendor Master & OCR System"
    API_V1_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/vendor_db"
    )
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Uploads & Storage
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    TEMPLATE_PATH: Path = BASE_DIR.parent / "1.แบบฟอร์มเปิด vendor.xlsx"

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
