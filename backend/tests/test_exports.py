import pytest
from app.models.vendor import Vendor
from app.services.excel_export import export_vendor_to_excel
from app.services.pdf_export import generate_vendor_pdf

def test_export_excel_and_pdf():
    mock_vendor = Vendor(
        id=1,
        vendor_code="V061020260001",
        vendor_name_th="เตียง กันนิกา",
        vendor_name_en="Tiang Kannika",
        tax_id="3550600242471",
        address_no="21",
        address_moo="8",
        address_subdistrict="ศรีภูมิ",
        address_district="ท่าวังผา",
        address_province="น่าน",
        address_postcode="55140",
        req_name="สุนิษา ช้างแก้ว",
        req_phone="02-103-3333",
        req_ext="53464",
        req_date="13/07/2569",
        req_bu="CTD",
        bank_name="กสิกรไทย",
        bank_account_no="123-4-56789-0"
    )

    # Test Excel Export
    excel_buf = export_vendor_to_excel(mock_vendor)
    excel_bytes = excel_buf.getvalue()
    assert len(excel_bytes) > 1000, "Excel output should not be empty"

    # Test PDF Export
    pdf_buf = generate_vendor_pdf(mock_vendor)
    pdf_bytes = pdf_buf.getvalue()
    assert len(pdf_bytes) > 1000, "PDF output should not be empty"
    assert pdf_bytes.startswith(b"%PDF"), "Valid PDF header expected"
