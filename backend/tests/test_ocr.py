import pytest
from pathlib import Path
from app.services.ocr_service import process_id_card

def test_ocr_with_real_pdf():
    pdf_path = Path("C:/atgv/fc_ocr/2.สำเนาบัตรประชาชน.pdf")
    assert pdf_path.exists(), "Target test file not found"

    result = process_id_card(pdf_path)
    # Assert critical Thai ID card fields
    assert result.tax_id == "3550600242471"
    assert "เตียง" in result.full_name_th
    assert "กันนิกา" in result.full_name_th
    assert result.address_district == "ท่าวังผา"
    assert result.address_province == "น่าน"
    assert result.address_no == "21"
