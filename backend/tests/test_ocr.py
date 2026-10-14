import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.services.ocr_service import process_id_card
from app.services.ocr_local import parse_id_card_text
from app.services.address_service import clean_address_prefix, resolve_postcode

client = TestClient(app)


def test_ocr_with_real_pdf():
    pdf_path = Path("C:/atgv/fc_ocr/2.สำเนาบัตรประชาชน.pdf")
    assert pdf_path.exists(), "Target test file not found"

    result = process_id_card(pdf_path)
    assert result.tax_id == "3550600242471"
    assert "เตียง" in result.full_name_th
    assert "กันนิกา" in result.full_name_th
    assert result.address_district == "ท่าวังผา"
    assert result.address_province == "น่าน"
    assert result.address_no == "21"
    assert result.address_postcode == "55140"


def test_clean_address_prefix():
    assert clean_address_prefix("ถ.บ้านบนตลาด", "road") == "บ้านบนตลาด"
    assert clean_address_prefix("ถนนเพชรเกษม", "road") == "เพชรเกษม"
    assert clean_address_prefix("ซ.สุขุมวิท 10", "soi") == "สุขุมวิท 10"
    assert clean_address_prefix("ซอย 5", "soi") == "5"
    assert clean_address_prefix("ตรอกวัดจันทร์", "soi") == "วัดจันทร์"
    assert clean_address_prefix("ต.ชะอำ", "subdistrict") == "ชะอำ"
    assert clean_address_prefix("แขวงคลองเตย", "subdistrict") == "คลองเตย"
    assert clean_address_prefix("อ.ชะอำ", "district") == "ชะอำ"
    assert clean_address_prefix("เขตคลองเตย", "district") == "คลองเตย"
    assert clean_address_prefix("จ.เพชรบุรี", "province") == "เพชรบุรี"


def test_resolve_postcode():
    assert resolve_postcode("ชะอำ", "ชะอำ", "เพชรบุรี") == "76120"
    assert resolve_postcode("ศรีภูมิ", "ท่าวังผา", "น่าน") == "55140"
    assert resolve_postcode("คลองเตย", "คลองเตย", "กรุงเทพมหานคร") == "10110"
    assert resolve_postcode("ไม่ทราบ", "ไม่ทราบ", "ไม่ทราบ", "99999") == "99999"


def test_parse_id_card_with_road_and_soi():
    raw_cha_am = (
        "เลขประจำตัวประชาชน 1 7698 00065 46 8\n"
        "ชื่อตัวและชื่อสกุล นาย รณพีร์ ฉิมทอง\n"
        "Name Mr. Ronnapee\n"
        "Last name Chimtung\n"
        "เกิดวันที่ 19 ก.ค. 2538\n"
        "ที่อยู่ 1175/6 ถ.บ้านบนตลาด ต.ชะอำ\n"
        "อ.ชะอำ จ.เพชรบุรี\n"
    )
    res1 = parse_id_card_text(raw_cha_am)
    assert res1.tax_id == "1769800065468"
    assert res1.address_no == "1175/6"
    assert res1.address_road == "บ้านบนตลาด"
    assert res1.address_soi is None
    assert res1.address_subdistrict == "ชะอำ"
    assert res1.address_district == "ชะอำ"
    assert res1.address_province == "เพชรบุรี"
    assert res1.address_postcode == "76120"

    raw_bkk = (
        "เลขประจำตัวประชาชน 1 1004 00123 45 6\n"
        "ชื่อตัวและชื่อสกุล นางสาว สมหญิง ใจดี\n"
        "ที่อยู่ 99/12 หมู่ที่ 3 ซ.สุขุมวิท 10 ถ.สุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร\n"
    )
    res2 = parse_id_card_text(raw_bkk)
    assert res2.address_no == "99/12"
    assert res2.address_moo == "3"
    assert res2.address_soi == "สุขุมวิท 10"
    assert res2.address_road == "สุขุมวิท"
    assert res2.address_subdistrict == "คลองเตย"
    assert res2.address_district == "คลองเตย"
    assert res2.address_province == "กรุงเทพมหานคร"
    assert res2.address_postcode == "10110"


def test_postcode_lookup_endpoint():
    login_res = client.post("/api/auth/login", json={"username": "t_admin", "password": "s3cret-pass"})
    assert login_res.status_code == 200
    resp = client.get("/api/ocr/postcode", params={"subdistrict": "ชะอำ", "district": "ชะอำ", "province": "เพชรบุรี"})
    assert resp.status_code == 200
    assert resp.json() == {"postcode": "76120"}
    client.cookies.clear()

