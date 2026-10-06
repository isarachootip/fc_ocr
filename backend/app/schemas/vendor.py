from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class VendorBase(BaseModel):
    # 1. ข้อมูลผู้ขอ
    req_date: Optional[str] = None
    req_email: Optional[str] = None
    req_name: Optional[str] = None
    req_department: Optional[str] = None
    req_bu: Optional[str] = None
    req_phone: Optional[str] = None
    req_ext: Optional[str] = None

    # 2. ข้อมูลที่ขอเพิ่ม/ปรับปรุง
    status_type: Optional[str] = "เพิ่มเติม"
    oracle_module: Optional[str] = "AP"
    purpose: Optional[str] = None
    purpose_other: Optional[str] = None
    checked_by: Optional[str] = None
    check_date: Optional[str] = None

    # 3. รายการที่ต้องการปรับปรุง
    update_details: Optional[str] = None

    # 4. ชื่อและที่อยู่ของร้านค้า
    vendor_name_en: Optional[str] = None
    vendor_name_th: str = Field(..., min_length=1, description="ชื่อร้านค้าหรือบุคคลภาษาไทย")
    address_no: Optional[str] = None
    address_moo: Optional[str] = None
    address_building: Optional[str] = None
    address_floor: Optional[str] = None
    address_village: Optional[str] = None
    address_soi: Optional[str] = None
    address_road: Optional[str] = None
    address_subdistrict: Optional[str] = None
    address_district: Optional[str] = None
    address_province: Optional[str] = None
    address_postcode: Optional[str] = None
    vendor_phone: Optional[str] = None
    vendor_fax: Optional[str] = None
    email_remittance: Optional[str] = None
    fax_remittance: Optional[str] = None
    email_etax: Optional[str] = None

    # 5. เลขประจำตัวผู้เสียภาษี / เลขบัตรประชาชน
    tax_id: str = Field(..., min_length=10, max_length=20, description="เลขประจำตัว 13 หลัก")
    branch_no: Optional[str] = "สำนักงานใหญ่"

    # 6. ผู้ที่สามารถติดต่อได้
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_mobile: Optional[str] = None
    contact_email: Optional[str] = None

    # 7. รูปแบบการค้า
    business_format: Optional[str] = None
    business_format_detail: Optional[str] = None

    # 8. ประเภทผู้ประกอบการ
    vat_type: Optional[str] = None

    # 9. ภาษีหัก ณ ที่จ่าย
    wht_type: Optional[str] = None
    wht_rate: Optional[str] = None
    property_billing_dept: Optional[str] = None
    is_gov_agency: Optional[bool] = False
    ship_to_address: Optional[str] = None

    # 10. เงื่อนไขการชำระเงิน
    payment_term: Optional[str] = None
    credit_days: Optional[str] = None

    # 11. วิธีการชำระเงิน
    payment_method: Optional[str] = None

    # 12. รายละเอียดธนาคาร
    bank_name: Optional[str] = None
    bank_branch: Optional[str] = None
    bank_account_name_th: Optional[str] = None
    bank_account_name_en: Optional[str] = None
    bank_account_type: Optional[str] = None
    bank_account_no: Optional[str] = None

    # 13. เอกสารแนบ
    attached_docs: Optional[str] = None

    # 14. หน่วยงานภายใน FAST
    fast_type: Optional[str] = None
    fast_site: Optional[str] = None
    fast_terms: Optional[str] = None
    fast_pay_group: Optional[str] = None
    fast_branch: Optional[str] = None
    fast_sub_account: Optional[str] = None

    # 15. ลายเซ็นผู้อนุมัติ
    approver_requestor_name: Optional[str] = None
    approver_requestor_date: Optional[str] = None
    approver_manager_name: Optional[str] = None
    approver_manager_date: Optional[str] = None

    # เอกสารประกอบ
    id_card_file_path: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(VendorBase):
    vendor_name_th: Optional[str] = None
    tax_id: Optional[str] = None

class VendorResponse(VendorBase):
    id: int
    vendor_code: str
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VendorListItem(BaseModel):
    id: int
    vendor_code: str
    vendor_name_th: str
    vendor_name_en: Optional[str] = None
    tax_id: str
    status_type: Optional[str] = None
    oracle_module: Optional[str] = None
    created_at: datetime
    created_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedVendorResponse(BaseModel):
    items: List[VendorListItem]
    total: int
    page: int
    limit: int
