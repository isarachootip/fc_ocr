"""Startup tasks: lightweight schema upgrades and first-admin seeding."""
import logging
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine
from app.config import settings
from app.database import SessionLocal
from app.services import user_service

logger = logging.getLogger(__name__)


def ensure_schema(engine: Engine) -> None:
    """Add columns introduced after the first release (create_all never alters tables)."""
    columns = {c["name"] for c in inspect(engine).get_columns("vendors")}
    if "created_by" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE vendors ADD COLUMN created_by VARCHAR(50)"))
        logger.info("Added vendors.created_by column")


def seed_admin() -> None:
    """Create the first admin from ADMIN_USERNAME/ADMIN_PASSWORD when no users exist,
    then the sysadmin from SYSADMIN_USERNAME/SYSADMIN_PASSWORD if that account is missing."""
    db = SessionLocal()
    try:
        if user_service.seed_first_admin(db, settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD):
            logger.warning("Created initial admin user '%s'", settings.ADMIN_USERNAME)
        elif not user_service.list_users(db):
            logger.error("No users exist and ADMIN_PASSWORD is not set: nobody can log in")
        if user_service.seed_sysadmin(db, settings.SYSADMIN_USERNAME, settings.SYSADMIN_PASSWORD):
            logger.warning("Created sysadmin user '%s'", settings.SYSADMIN_USERNAME)
    finally:
        db.close()
