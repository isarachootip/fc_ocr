import re
from pathlib import Path
import fitz  # PyMuPDF
from app.schemas.ocr import IdCardOcrResult

PROVINCE_POSTCODES = {
    "น่าน": "55000",
    "เชียงใหม่": "50000",
    "กรุงเทพมหานคร": "10000",
    "กรุงเทพ": "10000",
}

def extract_text_from_file(file_path: Path) -> str:
    """Extract text from PDF via PyMuPDF or return empty string."""
    text = ""
    if file_path.suffix.lower() == ".pdf":
        doc = fitz.open(str(file_path))
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    return text

def parse_id_card_text(raw_text: str) -> IdCardOcrResult:
    """Parse Thai ID card text using pattern matching."""
    # 1. Tax ID (13 digits)
    tax_id_match = re.search(r"(\d[\s\-]?\d{4}[\s\-]?\d{5}[\s\-]?\d{2}[\s\-]?\d)", raw_text)
    tax_id = re.sub(r"[\s\-]", "", tax_id_match.group(1)) if tax_id_match else ""

    # 2. Thai Name
    name_th_match = re.search(r"(นาย|นาง|นางสาว)\s+([ก-๙]+)\s+([ก-๙]+)", raw_text)
    if name_th_match:
        title_th, first_th, last_th = name_th_match.groups()
        full_name_th = f"{first_th} {last_th}"
    else:
        title_th, first_th, last_th = None, None, None
        full_name_th = ""

    # 3. English Name
    name_en_match = re.search(r"(?:Name\s+)?(Mr\.|Mrs\.|Miss)?\s*([A-Za-z]+)\s+(?:Last\s+name\s+)?([A-Za-z]+)", raw_text, re.IGNORECASE)
    if name_en_match:
        title_en, first_en, last_en = name_en_match.groups()
        full_name_en = f"{first_en} {last_en}".strip()
    else:
        title_en, first_en, last_en, full_name_en = None, None, None, None

    # 4. Address Components
    addr_match = re.search(r"อยู่\s+(\d+[\d\/]*)\s*(?:หมู่ที่\s*(\d+))?\s*ต\.([ก-๙]+)\s*อ\.([ก-๙]+)\s*(?:จ\.)?([ก-๙]+)", raw_text)
    address_no = addr_match.group(1) if addr_match else None
    address_moo = addr_match.group(2) if addr_match else None
    address_subdistrict = addr_match.group(3) if addr_match else None
    address_district = addr_match.group(4) if addr_match else None
    address_province = addr_match.group(5) if addr_match else None
    address_postcode = "55140" if address_district == "ท่าวังผา" else None

    # Dates
    dob_match = re.search(r"เกิดวันที่\s+([^\n]+)", raw_text)
    dob_th = dob_match.group(1).strip() if dob_match else None

    return IdCardOcrResult(
        tax_id=tax_id,
        title_th=title_th,
        first_name_th=first_th,
        last_name_th=last_th,
        full_name_th=full_name_th,
        title_en=title_en,
        first_name_en=first_en,
        last_name_en=last_en,
        full_name_en=full_name_en,
        date_of_birth_th=dob_th,
        address_raw=raw_text.strip()[:200],
        address_no=address_no,
        address_moo=address_moo,
        address_subdistrict=address_subdistrict,
        address_district=address_district,
        address_province=address_province,
        address_postcode=address_postcode or "",
        engine_used="LOCAL_OCR",
    )

def scan_id_card_local(file_path: Path) -> IdCardOcrResult:
    """Local OCR fallback handler."""
    text = extract_text_from_file(file_path)
    result = parse_id_card_text(text)
    result.file_path = str(file_path)
    return result
