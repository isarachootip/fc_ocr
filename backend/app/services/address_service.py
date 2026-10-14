import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional
from app.schemas.ocr import IdCardOcrResult

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "thai_postcodes.json"

PREFIX_PATTERNS: Dict[str, str] = {
    "moo": r"^(?:หมู่ที่|หมู่|ม\.)\s*",
    "soi": r"^(?:ตรอก/ซอย|ตรอก|ซอย|ซ\.)\s*",
    "road": r"^(?:ถนน|ถ\.)\s*",
    "subdistrict": r"^(?:ตำบล/แขวง|ตำบล|แขวง|ต\.)\s*",
    "district": r"^(?:อำเภอ/เขต|อำเภอ|เขต|อ\.)\s*",
    "province": r"^(?:จังหวัด|จ\.)\s*",
}


@lru_cache(maxsize=1)
def _load_postcode_data() -> Dict[str, Dict[str, str]]:
    if not DATA_PATH.exists():
        return {"districts": {}, "provinces": {}}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_address_prefix(value: Optional[str], kind: str) -> Optional[str]:
    """Strip standard Thai address prefixes (e.g., ถ., ซ., ต., อ., จ.) from extracted values."""
    if not value:
        return None
    cleaned = value.strip()
    pattern = PREFIX_PATTERNS.get(kind)
    if pattern:
        cleaned = re.sub(pattern, "", cleaned).strip()
    if cleaned in ("", "-", "ไม่มี", "null", "None"):
        return None
    return cleaned


def resolve_postcode(
    subdistrict: Optional[str] = None,
    district: Optional[str] = None,
    province: Optional[str] = None,
    fallback_postcode: Optional[str] = None,
) -> str:
    """Resolve 5-digit Thai postal code from subdistrict/district/province or fallback."""
    data = _load_postcode_data()
    districts_map = data.get("districts", {})
    provinces_map = data.get("provinces", {})

    prov = clean_address_prefix(province, "province") or ""
    dist = clean_address_prefix(district, "district") or ""
    sub = clean_address_prefix(subdistrict, "subdistrict") or ""

    if prov in ("กทม", "กทม.", "กรุงเทพ", "กรุงเทพฯ"):
        prov = "กรุงเทพมหานคร"

    # 1. Exact Province + District match
    if prov and dist:
        key = f"{prov}|{dist}"
        if key in districts_map:
            return districts_map[key]
        if dist == "เมือง" and f"{prov}|เมือง{prov}" in districts_map:
            return districts_map[f"{prov}|เมือง{prov}"]
        if dist.startswith("เมือง") and f"{prov}|เมือง{prov}" in districts_map:
            return districts_map[f"{prov}|เมือง{prov}"]

    # 2. Match by District across provinces when province is omitted or slightly OCR-misread
    if dist:
        for k, code in districts_map.items():
            _, d_name = k.split("|", 1)
            if d_name == dist:
                return code

    # 3. Match by Subdistrict if it matches a known district name (e.g., ต.ชะอำ)
    if sub and prov:
        key_sub = f"{prov}|{sub}"
        if key_sub in districts_map:
            return districts_map[key_sub]

    # 4. Fallback to valid 5-digit AI-inferred postcode if provided
    if fallback_postcode:
        digits = re.sub(r"\D", "", fallback_postcode)
        if len(digits) == 5:
            return digits

    # 5. Fallback to Province capital postcode
    if prov and prov in provinces_map:
        return provinces_map[prov]

    return fallback_postcode or ""


def normalize_ocr_address(result: IdCardOcrResult) -> IdCardOcrResult:
    """Clean all address prefixes and populate postcode automatically."""
    result.address_moo = clean_address_prefix(result.address_moo, "moo")
    result.address_soi = clean_address_prefix(result.address_soi, "soi")
    result.address_road = clean_address_prefix(result.address_road, "road")
    result.address_subdistrict = clean_address_prefix(result.address_subdistrict, "subdistrict")
    result.address_district = clean_address_prefix(result.address_district, "district")
    result.address_province = clean_address_prefix(result.address_province, "province")
    result.address_postcode = resolve_postcode(
        subdistrict=result.address_subdistrict,
        district=result.address_district,
        province=result.address_province,
        fallback_postcode=result.address_postcode,
    )
    return result
