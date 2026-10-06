from fastapi import APIRouter
from app.api.ocr import router as ocr_router
from app.api.vendors import router as vendors_router
from app.api.exports import router as exports_router

api_router = APIRouter()
api_router.include_router(ocr_router)
api_router.include_router(vendors_router)
api_router.include_router(exports_router)
