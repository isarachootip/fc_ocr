from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

OcrEngine = Literal["AI_GEMINI", "LOCAL_OCR"]
KeySource = Literal["database", "env", "none"]


class GeminiStatus(BaseModel):
    """Public view of the Gemini configuration. Never contains the full key."""
    configured: bool
    source: KeySource
    engine: OcrEngine
    masked: Optional[str] = None
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None


class GeminiKeyUpdate(BaseModel):
    api_key: str = Field(min_length=20, max_length=200)

    @field_validator("api_key", mode="before")
    @classmethod
    def strip_and_reject_spaces(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if any(ch.isspace() for ch in value):
                raise ValueError("API key must not contain whitespace")
        return value
