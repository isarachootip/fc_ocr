from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.api.deps import require_user
from app.config import settings

router = APIRouter(dependencies=[Depends(require_user)])


@router.get("/uploads/{filename}")
def get_upload(filename: str):
    """Serve an uploaded ID card, only to authenticated users."""
    if filename != Path(filename).name or filename.startswith("."):
        raise HTTPException(status_code=400, detail="Invalid filename")
    base = settings.UPLOAD_DIR.resolve()
    target = (base / filename).resolve()
    if target.parent != base or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(target)
