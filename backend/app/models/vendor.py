from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Index
from app.database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String(50), unique=True, index=True, nullable=False)
    id_card_file_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # 1. ข้อมูลผู้ขอ (Requestor)
    req_date = Column(String(50), nullable=True)
    req_email = Column(String(100), nullable=True)
    req_name = Column(String(100), nullable=True)
    req_department = Column(String(100), nullable=True)
    req_bu = Column(String(50), nullable=True)
    req_phone = Column(String(50), nullable=True)
    req_ext = Column(String(20), nullable=True)

    # 2. ข้อมูลที่ขอเพิ่ม/ปรับปรุง
    status_type = Column(String(50), default="เพิ่มเติม")  # เพิ่มเติม / ปรับปรุง
    oracle_module = Column(String(20), default="AP")       # AP / AR
    purpose = Column(String(100), nullable=True)
    purpose_other = Column(String(100), nullable=True)
    checked_by = Column(String(100), nullable=True)
    check_date = Column(String(50), nullable=True)

    # 3. รายการที่ต้องการปรับปรุง
    update_details = Column(Text, nullable=True)

    # 4. ชื่อและที่อยู่ของร้านค้า
    vendor_name_en = Column(String(255), nullable=True)
    vendor_name_th = Column(String(255), nullable=False)
    address_no = Column(String(50), nullable=True)
    address_moo = Column(String(20), nullable=True)
    address_building = Column(String(100), nullable=True)
    address_floor = Column(String(20), nullable=True)
    address_village = Column(String(100), nullable=True)
    address_soi = Column(String(100), nullable=True)
    address_road = Column(String(100), nullable=True)
    address_subdistrict = Column(String(100), nullable=True)
    address_district = Column(String(100), nullable=True)
    address_province = Column(String(100), nullable=True)
    address_postcode = Column(String(20), nullable=True)
    vendor_phone = Column(String(50), nullable=True)
    vendor_fax = Column(String(50), nullable=True)
    email_remittance = Column(String(255), nullable=True)
    fax_remittance = Column(String(100), nullable=True)
    email_etax = Column(String(255), nullable=True)

    # 5. เลขประจำตัวผู้เสียภาษีอากร / เลขบัตรประชาชน
    tax_id = Column(String(20), index=True, nullable=False)
    branch_no = Column(String(50), default="สำนักงานใหญ่")

    # 6. ผู้ที่สามารถติดต่อได้
    contact_name = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_mobile = Column(String(50), nullable=True)
    contact_email = Column(String(100), nullable=True)

    # 7. รูปแบบการค้า
    business_format = Column(String(100), nullable=True)
    business_format_detail = Column(String(255), nullable=True)

    # 8. ประเภทผู้ประกอบการ
    vat_type = Column(String(50), nullable=True)

    # 9. ภาษีหัก ณ ที่จ่าย
    wht_type = Column(String(50), nullable=True)
    wht_rate = Column(String(20), nullable=True)
    property_billing_dept = Column(String(50), nullable=True)
    is_gov_agency = Column(Boolean, default=False)
    ship_to_address = Column(Text, nullable=True)

    # 10. เงื่อนไขการชำระเงิน
    payment_term = Column(String(50), nullable=True)
    credit_days = Column(String(20), nullable=True)

    # 11. วิธีการชำระเงิน
    payment_method = Column(String(50), nullable=True)

    # 12. รายละเอียดธนาคาร
    bank_name = Column(String(100), nullable=True)
    bank_branch = Column(String(100), nullable=True)
    bank_account_name_th = Column(String(255), nullable=True)
    bank_account_name_en = Column(String(255), nullable=True)
    bank_account_type = Column(String(50), nullable=True)
    bank_account_no = Column(String(50), nullable=True)

    # 13. เอกสารแนบ
    attached_docs = Column(Text, nullable=True)

    # 14. หน่วยงานภายใน FAST
    fast_type = Column(String(50), nullable=True)
    fast_site = Column(String(100), nullable=True)
    fast_terms = Column(String(50), nullable=True)
    fast_pay_group = Column(String(100), nullable=True)
    fast_branch = Column(String(100), nullable=True)
    fast_sub_account = Column(String(100), nullable=True)

    # 15. ลายเซ็นผู้อนุมัติ
    approver_requestor_name = Column(String(100), nullable=True)
    approver_requestor_date = Column(String(50), nullable=True)
    approver_manager_name = Column(String(100), nullable=True)
    approver_manager_date = Column(String(50), nullable=True)

__table_args__ = (
    Index("ix_vendors_search", "vendor_code", "vendor_name_th", "tax_id"),
)
