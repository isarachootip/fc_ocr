from typing import Optional
from pydantic import BaseModel, Field

class IdCardOcrResult(BaseModel):
    tax_id: str = Field(..., description="เลขประจำตัวประชาชน 13 หลัก")
    title_th: Optional[str] = Field(None, description="คำนำหน้าชื่อไทย เช่น นาย / นาง / นางสาว")
    first_name_th: Optional[str] = Field(None, description="ชื่อตัวไทย")
    last_name_th: Optional[str] = Field(None, description="ชื่อสกุลไทย")
    full_name_th: str = Field(..., description="ชื่อ-นามสกุล ภาษาไทย")
    
    title_en: Optional[str] = Field(None, description="คำนำหน้าอังกฤษ เช่น Mr. / Mrs. / Miss")
    first_name_en: Optional[str] = Field(None, description="First Name EN")
    last_name_en: Optional[str] = Field(None, description="Last Name EN")
    full_name_en: Optional[str] = Field(None, description="Full Name EN")
    
    date_of_birth_th: Optional[str] = Field(None, description="วันเกิด พ.ศ.")
    date_of_birth_en: Optional[str] = Field(None, description="Date of birth")
    
    # Address breakdown
    address_raw: Optional[str] = Field(None, description="ที่อยู่เต็ม")
    address_no: Optional[str] = Field(None, description="บ้านเลขที่")
    address_moo: Optional[str] = Field(None, description="หมู่ที่")
    address_subdistrict: Optional[str] = Field(None, description="ตำบล / แขวง")
    address_district: Optional[str] = Field(None, description="อำเภอ / เขต")
    address_province: Optional[str] = Field(None, description="จังหวัด")
    address_postcode: Optional[str] = Field(None, description="รหัสไปรษณีย์")
    
    # Additional info
    issue_date: Optional[str] = Field(None, description="วันออกบัตร")
    expiry_date: Optional[str] = Field(None, description="วันบัตรหมดอายุ")
    file_path: Optional[str] = Field(None, description="Path ของไฟล์ที่อัปโหลด")
    engine_used: Optional[str] = Field(None, description="AI_GEMINI หรือ LOCAL_OCR")
