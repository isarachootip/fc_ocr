from fastapi import APIRouter, Depends
from app.api.deps import require_user
from app.api.auth import router as auth_router
from app.api.ocr import router as ocr_router
from app.api.vendors import router as vendors_router
from app.api.exports import router as exports_router
from app.api.users import router as users_router

api_router = APIRouter()
# Public: login / logout (me and change-password are guarded individually)
api_router.include_router(auth_router)
# Admin only (guard is declared on the router itself)
api_router.include_router(users_router)
# Everything else requires a valid session
_protected = [Depends(require_user)]
api_router.include_router(ocr_router, dependencies=_protected)
api_router.include_router(vendors_router, dependencies=_protected)
api_router.include_router(exports_router, dependencies=_protected)
