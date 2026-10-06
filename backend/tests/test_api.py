import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_vendor_create_and_fetch():
    vendor_payload = {
        "vendor_name_th": "บริษัท น่านการเกษตร จำกัด",
        "vendor_name_en": "Nan Agriculture Co., Ltd.",
        "tax_id": "0555567890123",
        "req_name": "สมชาย ใจดี",
        "req_bu": "CTD",
        "address_no": "99",
        "address_district": "เมือง",
        "address_province": "น่าน",
        "bank_name": "กรุงเทพ",
        "bank_account_no": "987-6-54321-0"
    }

    # 1. Create Vendor
    create_res = client.post("/api/vendors", json=vendor_payload)
    assert create_res.status_code == 201, create_res.text
    data = create_res.json()
    assert "vendor_code" in data
    assert data["vendor_code"].startswith("V")
    vendor_id = data["id"]

    # 2. Get Detail
    get_res = client.get(f"/api/vendors/{vendor_id}")
    assert get_res.status_code == 200
    assert get_res.json()["vendor_name_th"] == "บริษัท น่านการเกษตร จำกัด"

    # 3. Search Vendor
    search_res = client.get("/api/vendors?query=น่านการเกษตร")
    assert search_res.status_code == 200
    assert search_res.json()["total"] >= 1

    # 4. Export Excel
    excel_res = client.get(f"/api/vendors/{vendor_id}/export-excel")
    assert excel_res.status_code == 200
    assert len(excel_res.content) > 1000

    # 5. Export PDF
    pdf_res = client.get(f"/api/vendors/{vendor_id}/export-pdf")
    assert pdf_res.status_code == 200
    assert len(pdf_res.content) > 1000
