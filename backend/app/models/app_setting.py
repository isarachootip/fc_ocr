from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text
from app.database import Base


class AppSetting(Base):
    """Runtime-editable system settings (key/value). Secret values are stored encrypted."""
    __tablename__ = "app_settings"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    updated_by = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
