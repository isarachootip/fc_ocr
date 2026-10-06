from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, select, func
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate
from app.services.running_number import generate_vendor_code

def create_vendor(
    db: Session,
    vendor_in: VendorCreate,
    file_path: Optional[str] = None,
    created_by: Optional[str] = None,
) -> Vendor:
    """Create a new vendor with an automatic running code."""
    vendor_code = generate_vendor_code(db)
    vendor_data = vendor_in.model_dump()
    
    if file_path:
        vendor_data["id_card_file_path"] = file_path

    vendor = Vendor(vendor_code=vendor_code, created_by=created_by, **vendor_data)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor

def get_vendor(db: Session, vendor_id: int) -> Optional[Vendor]:
    return db.get(Vendor, vendor_id)

def update_vendor(db: Session, vendor_id: int, vendor_in: VendorUpdate) -> Optional[Vendor]:
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        return None

    update_data = vendor_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vendor, field, value)

    db.commit()
    db.refresh(vendor)
    return vendor

def delete_vendor(db: Session, vendor_id: int) -> bool:
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        return False
    db.delete(vendor)
    db.commit()
    return True

def search_vendors(
    db: Session,
    query: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> Tuple[List[Vendor], int]:
    stmt = select(Vendor)
    count_stmt = select(func.count(Vendor.id))

    if query:
        search_filter = or_(
            Vendor.vendor_code.ilike(f"%{query}%"),
            Vendor.vendor_name_th.ilike(f"%{query}%"),
            Vendor.tax_id.ilike(f"%{query}%"),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    offset = (page - 1) * limit
    items = db.execute(
        stmt.order_by(Vendor.id.desc()).offset(offset).limit(limit)
    ).scalars().all()

    return list(items), total
