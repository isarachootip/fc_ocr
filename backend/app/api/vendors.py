from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.vendor import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    PaginatedVendorResponse,
)
from app.services import vendor_service

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("", response_model=VendorResponse, status_code=201)
def create_vendor(vendor_in: VendorCreate, db: Session = Depends(get_db)):
    return vendor_service.create_vendor(db, vendor_in, vendor_in.id_card_file_path)

@router.get("", response_model=PaginatedVendorResponse)
def list_vendors(
    query: Optional[str] = Query(None, description="Search keyword (code, name, tax id)"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = vendor_service.search_vendors(db, query=query, page=page, limit=limit)
    return PaginatedVendorResponse(items=items, total=total, page=page, limit=limit)

@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor_detail(vendor_id: int, db: Session = Depends(get_db)):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, vendor_in: VendorUpdate, db: Session = Depends(get_db)):
    vendor = vendor_service.update_vendor(db, vendor_id, vendor_in)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    success = vendor_service.delete_vendor(db, vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully", "id": vendor_id}
