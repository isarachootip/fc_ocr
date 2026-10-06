from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings, BASE_DIR
from app.database import engine, Base
from app.models.vendor import Vendor  # ensure models are registered
from app.api import api_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Vendor Master Registration & Thai ID Card OCR API",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static uploads directory for document preview
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

# Serve Frontend SPA if built
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")

