import re
from pathlib import Path
import fitz  # PyMuPDF
from app.schemas.ocr import IdCardOcrResult
from app.services.address_service import normalize_ocr_address


def extract_text_from_file(file_path: Path) -> str:
    """Extract text from PDF via PyMuPDF or return empty string."""
    text = ""
    if file_path.suffix.lower() == ".pdf":
        doc = fitz.open(str(file_path))
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    return text


def _extract_address_parts(raw_text: str) -> dict:
    """Extract house no, moo, soi, road, subdistrict, district, province from Thai ID text."""
    addr_block_match = re.search(r"(?:ที่)?อยู่\s+([^\n]+(?:\n[^\n]+)?)", raw_text)
    addr_text = addr_block_match.group(1) if addr_block_match else raw_text

    no_match = re.search(r"(?:ที่)?อยู่\s+(\d+[\d\/\-]*)", raw_text)
    moo_match = re.search(r"(?:หมู่ที่|หมู่|ม\.)\s*(\d+)", addr_text)
    soi_match = re.search(
        r"(?:ตรอก|ซอย|ซ\.)\s*([ก-๙A-Za-z0-9\/\-\s]+?)(?=\s+(?:ถ\.|ถนน|ต\.|ตำบล|แขวง|อ\.|อำเภอ|เขต|จ\.|จังหวัด|กรุงเทพ)|$|\n)",
        addr_text,
    )
    road_match = re.search(
        r"(?:ถนน|ถ\.)\s*([ก-๙A-Za-z0-9\/\-\s]+?)(?=\s+(?:ต\.|ตำบล|แขวง|อ\.|อำเภอ|เขต|จ\.|จังหวัด|กรุงเทพ)|$|\n)",
        addr_text,
    )
    sub_match = re.search(r"(?:ต\.|ตำบล|แขวง)\s*([ก-๙]+)", addr_text)
    dist_match = re.search(r"(?:อ\.|อำเภอ|เขต)\s*([ก-๙]+)", addr_text)
    prov_match = re.search(r"(?:จ\.|จังหวัด)\s*([ก-๙]+)", addr_text)

    province = prov_match.group(1) if prov_match else None
    if not province and "กรุงเทพมหานคร" in addr_text:
        province = "กรุงเทพมหานคร"

    return {
        "address_no": no_match.group(1) if no_match else None,
        "address_moo": moo_match.group(1) if moo_match else None,
        "address_soi": soi_match.group(1).strip() if soi_match else None,
        "address_road": road_match.group(1).strip() if road_match else None,
        "address_subdistrict": sub_match.group(1) if sub_match else None,
        "address_district": dist_match.group(1) if dist_match else None,
        "address_province": province,
    }


def parse_id_card_text(raw_text: str) -> IdCardOcrResult:
    """Parse Thai ID card text using pattern matching."""
    tax_id_match = re.search(r"(\d[\s\-]?\d{4}[\s\-]?\d{5}[\s\-]?\d{2}[\s\-]?\d)", raw_text)
    tax_id = re.sub(r"[\s\-]", "", tax_id_match.group(1)) if tax_id_match else ""

    name_th_match = re.search(r"(นาย|นาง|นางสาว)\s+([ก-๙]+)\s+([ก-๙]+)", raw_text)
    if name_th_match:
        title_th, first_th, last_th = name_th_match.groups()
        full_name_th = f"{first_th} {last_th}"
    else:
        title_th, first_th, last_th = None, None, None
        full_name_th = ""

    name_en_match = re.search(
        r"(?:Name\s+)?(Mr\.|Mrs\.|Miss)?\s*([A-Za-z]+)\s+(?:Last\s+name\s+)?([A-Za-z]+)",
        raw_text,
        re.IGNORECASE,
    )
    if name_en_match:
        title_en, first_en, last_en = name_en_match.groups()
        full_name_en = f"{first_en} {last_en}".strip()
    else:
        title_en, first_en, last_en, full_name_en = None, None, None, None

    addr = _extract_address_parts(raw_text)
    dob_match = re.search(r"เกิดวันที่\s+([^\n]+)", raw_text)
    dob_th = dob_match.group(1).strip() if dob_match else None

    result = IdCardOcrResult(
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
        engine_used="LOCAL_OCR",
        **addr,
    )
    return normalize_ocr_address(result)


def scan_id_card_local(file_path: Path) -> IdCardOcrResult:
    """Local OCR fallback handler."""
    text = extract_text_from_file(file_path)
    result = parse_id_card_text(text)
    result.file_path = str(file_path)
    return result
