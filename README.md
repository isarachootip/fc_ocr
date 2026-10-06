# Vendor Master Registration & Citizen ID OCR System

ระบบลงทะเบียนและจัดการทะเบียนผู้ค้า (Vendor Master) พร้อมระบบอ่านสำเนาบัตรประชาชนอัตโนมัติ (AI & Local OCR) บันทึกลงฐานข้อมูล PostgreSQL และพิมพ์/ส่งออกเอกสารได้ครบทุกรูปแบบ

---

## ฟีเจอร์หลัก (Key Features)

1. **Smart ID Card OCR with Review Modal**:
   - รองรับการสแกนสำเนาบัตรประชาชนทั้งไฟล์ **PDF** และ **รูปภาพ (JPG/PNG)**
   - สกัดเลขบัตร 13 หลัก, ชื่อ-สกุล (ไทย-อังกฤษ), วันเกิด, และที่อยู่แยกหมวดหมู่ (บ้านเลขที่, หมู่, ตำบล, อำเภอ, จังหวัด, รหัสไปรษณีย์)
   - หน้าต่าง **OCR Preview & Confirm Modal** ให้ผู้ใช้ตรวจสอบ/แก้ไขข้อมูลก่อนนำเข้าสู่ฟอร์มจริง
   - รองรับ **Gemini Vision AI** เป็นหลัก และมี **Local OCR (PyMuPDF/EasyOCR)** สำรองอัตโนมัติ

2. **บันทึกข้อมูลครบ 15 ส่วนตามแบบฟอร์มบริษัท**:
   - ส่วนที่ 1-3: ข้อมูลผู้ขอ (Requestor), สถานะคำขอ (เพิ่มใหม่/ปรับปรุง), Oracle Module (AP/AR), จุดประสงค์
   - ส่วนที่ 4: ชื่อและที่อยู่ร้านค้า (ภาษาไทย-อังกฤษ, ที่อยู่แยกย่อย 10 ฟิลด์, e-Tax)
   - ส่วนที่ 5: เลขประจำตัว 13 หลัก พร้อมกล่องแยก 13 ช่อง และสาขา
   - ส่วนที่ 6-12: ผู้ติดต่อ, รูปแบบการค้า, ประเภท VAT, ภาษีหัก ณ ที่จ่าย ภ.ง.ด., และบัญชีธนาคาร
   - ส่วนที่ 13-15: เอกสารแนบ, ข้อมูลเฉพาะ FAST, และลายมือชื่อผู้อนุมัติ

3. **Running Number อัตโนมัติ**:
   - รูปแบบ `V` + `dd` + `mm` + `yyyy` + `xxxx` เช่น `V061020260001`

4. **พิมพ์และส่งออกเอกสารได้ 3 รูปแบบ (All-in-One Export)**:
   - **Excel (.xlsx)**: หยอดค่าลงในแม่แบบทางการ `1.แบบฟอร์มเปิด vendor.xlsx` ตามพิกัดช่องเดิมเป๊ะ
   - **PDF (.pdf)**: สร้างเอกสาร A4 พร้อมตารางและข้อมูลครบถ้วนสำหรับเซ็นอนุมัติ
   - **Browser Print (A4)**: หน้าจอสำหรับสั่งพิมพ์ผ่านเบราว์เซอร์ พร้อม CSS `@media print` สำหรับกระดาษ A4

5. **สืบค้นและจัดการ (Search & Management)**:
   - ค้นหาได้แบบ Real-time ด้วยรหัส Vendor, ชื่อร้านค้า, หรือเลขบัตรประชาชน 13 หลัก
   - จัดเก็บไฟล์สำเนาบัตรประชาชนต้นฉบับไว้ในโฟลเดอร์ `/uploads` พร้อมเชื่อมโยงกับฐานข้อมูล

---

## วิธีเริ่มใช้งาน (Quick Start)

### วิธีที่ 1: ดับเบิ้ลคลิกไฟล์รันอัตโนมัติ
ดับเบิ้ลคลิกที่ไฟล์:
```
start.bat
```
ระบบจะเปิด Web Application ที่ `http://localhost:8000` ให้อัตโนมัติ

### วิธีที่ 2: รันผ่าน Terminal

1. **รัน Backend & Web App (FastAPI):**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
เข้าใช้งานได้ที่: **http://localhost:8000** (หรือ API Documentation ที่ http://localhost:8000/docs)

2. **(ตัวเลือกเสริม) รัน Frontend Dev Server:**
```bash
cd frontend
npm run dev
```
เข้าใช้งาน Dev Mode ได้ที่: **http://localhost:5173**

---

## การตั้งค่า Environment Variables (`backend/.env`)

| ตัวแปร | คำอธิบาย | ค่าเริ่มต้น |
|---|---|---|
| `DATABASE_URL` | PostgreSQL Connection String | `postgresql://postgres:postgres@localhost:5432/vendor_db` |
| `GEMINI_API_KEY` | API Key ของ Google Gemini Vision (ถ้าไม่ใส่จะใช้ Local OCR อัตโนมัติ) | *(เว้นว่าง)* |
