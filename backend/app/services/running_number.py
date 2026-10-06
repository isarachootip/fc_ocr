from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.vendor import Vendor

def generate_vendor_code(db: Session, target_date: datetime | None = None) -> str:
    """
    Generate running vendor code with format: V + dd + mm + yyyy + xxxx
    Example: V061020260001
    """
    if target_date is None:
        target_date = datetime.now()

    date_prefix = f"V{target_date.strftime('%d%m%Y')}"
    
    # Query highest vendor code for today with this prefix
    last_vendor = db.execute(
        select(Vendor.vendor_code)
        .where(Vendor.vendor_code.like(f"{date_prefix}%"))
        .order_by(Vendor.vendor_code.desc())
        .limit(1)
    ).scalar_one_or_none()

    if not last_vendor:
        next_seq = 1
    else:
        # Extract the sequence suffix (last 4 digits)
        try:
            seq_part = last_vendor[len(date_prefix):]
            next_seq = int(seq_part) + 1
        except (ValueError, IndexError):
            next_seq = 1

    return f"{date_prefix}{next_seq:04d}"
