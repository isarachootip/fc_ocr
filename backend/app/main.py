from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings, BASE_DIR
from app.database import engine, Base
from app.models.vendor import Vendor  # ensure models are registered
from app.models.user import User  # noqa: F401  (ensure model is registered)
from app.models.app_setting import AppSetting  # noqa: F401  (ensure model is registered)
from app.api import api_router
from app.api.uploads import router as uploads_router
from app.db_init import ensure_schema, seed_admin

# Create DB tables, upgrade older schemas, seed the first admin
Base.metadata.create_all(bind=engine)
ensure_schema(engine)
seed_admin()

app = FastAPI(
    title=settings.APP_NAME,
    description="Vendor Master Registration & Thai ID Card OCR API",
    version="1.0.0"
)

# CORS: the SPA is served same-origin in production; only the Vite dev server needs it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protected uploads (ID card previews) - requires login
app.include_router(uploads_router)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

# Serve Frontend SPA if built
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")

