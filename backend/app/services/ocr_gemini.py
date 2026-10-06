import json
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
from app.config import settings
from app.schemas.ocr import IdCardOcrResult

OCR_PROMPT = """
You are an expert OCR AI for Thai National ID Cards.
Analyze the provided Thai ID Card image. Extract the following fields accurately into a JSON object:
{
  "tax_id": "13-digit identification number without spaces or dashes",
  "title_th": "นาย / นาง / นางสาว",
  "first_name_th": "ชื่อภาษาไทย",
  "last_name_th": "นามสกุลภาษาไทย",
  "full_name_th": "ชื่อ-นามสกุลภาษาไทย",
  "title_en": "Mr. / Mrs. / Miss",
  "first_name_en": "First Name in English",
  "last_name_en": "Last Name in English",
  "full_name_en": "Full Name in English",
  "date_of_birth_th": "วันเกิดภาษาไทย เช่น 21 ก.ค. 2507",
  "date_of_birth_en": "Date of Birth English เช่น 21 Jul. 1964",
  "address_raw": "ที่อยู่เต็มตามบัตร",
  "address_no": "บ้านเลขที่",
  "address_moo": "หมู่ที่ (เฉพาะตัวเลข)",
  "address_subdistrict": "ตำบลหรือแขวง (ตัดคำว่า ต. หรือ ตำบล ออก)",
  "address_district": "อำเภอหรือเขต (ตัดคำว่า อ. หรือ อำเภอ ออก)",
  "address_province": "จังหวัด (ตัดคำว่า จ. หรือ จังหวัด ออก)",
  "address_postcode": "รหัสไปรษณีย์ 5 หลัก",
  "issue_date": "วันออกบัตร",
  "expiry_date": "วันหมดอายุ"
}
Ignore any crossed-out signatures or watermark text like "สำเนาถูกต้อง".
Output pure JSON only, without any markdown formatting or explanations.
"""

def get_image_for_gemini(file_path: Path):
    """Load image directly or convert first page of PDF to PIL Image."""
    if file_path.suffix.lower() == ".pdf":
        doc = fitz.open(str(file_path))
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        return img
    return Image.open(str(file_path))

def scan_id_card_gemini(file_path: Path) -> IdCardOcrResult:
    """Scan ID card using Gemini Vision API."""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    img = get_image_for_gemini(file_path)
    response = model.generate_content([OCR_PROMPT, img])
    
    clean_text = response.text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]

    data = json.loads(clean_text.strip())
    data["engine_used"] = "AI_GEMINI"
    data["file_path"] = str(file_path)
    return IdCardOcrResult(**data)
