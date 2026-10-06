import io
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.models.vendor import Vendor

# Register Thai font (Windows Tahoma, or TLWG fonts on Linux/Docker)
FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/tahoma.ttf"),
    Path("/usr/share/fonts/truetype/tlwg/Loma.ttf"),
    Path("/usr/share/fonts/truetype/tlwg/Garuda.ttf"),
]
FONT_PATH = next((p for p in FONT_CANDIDATES if p.exists()), FONT_CANDIDATES[0])
FONT_NAME = "Helvetica"
if FONT_PATH.exists():
    try:
        pdfmetrics.registerFont(TTFont("ThaiFont", str(FONT_PATH)))
        FONT_NAME = "ThaiFont"
    except Exception:
        pass

def generate_vendor_pdf(vendor: Vendor) -> io.BytesIO:
    """Generate official A4 PDF document for vendor registration."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=25,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        fontName=FONT_NAME,
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor("#1e293b")
    )
    normal_style = ParagraphStyle(
        "NormalStyle",
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    bold_style = ParagraphStyle(
        "BoldStyle",
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )

    elements = []
    # Title
    elements.append(Paragraph("<b>เอกสารการแจ้งเพิ่ม/ปรับปรุงทะเบียนร้านค้า (Vendor Master)</b>", title_style))
    elements.append(Spacer(1, 8))

    # Header Grid (Vendor Code & Request Info)
    hdr_data = [
        [
            Paragraph(f"<b>รหัสร้านค้า:</b> {vendor.vendor_code}", bold_style),
            Paragraph(f"<b>วันที่แจ้ง:</b> {vendor.req_date or '-'}", normal_style),
            Paragraph(f"<b>BU / แผนก:</b> {vendor.req_bu or '-'} / {vendor.req_department or '-'}", normal_style),
        ],
        [
            Paragraph(f"<b>สถานภาพ:</b> {vendor.status_type or '-'}", normal_style),
            Paragraph(f"<b>Oracle Module:</b> {vendor.oracle_module or '-'}", normal_style),
            Paragraph(f"<b>ผู้แจ้ง:</b> {vendor.req_name or '-'} ({vendor.req_phone or '-'})", normal_style),
        ]
    ]
    hdr_table = Table(hdr_data, colWidths=[180, 160, 195])
    hdr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(hdr_table)
    elements.append(Spacer(1, 10))

    # Section 4 & 5: Vendor Info & Tax ID
    tax_formatted = " - ".join(list(vendor.tax_id or ""))
    info_data = [
        [Paragraph("<b>ข้อมูลผู้ประกอบการ / ร้านค้า</b>", bold_style), ""],
        [Paragraph(f"<b>ชื่อภาษาไทย:</b> {vendor.vendor_name_th}", normal_style), Paragraph(f"<b>ชื่อภาษาอังกฤษ:</b> {vendor.vendor_name_en or '-'}", normal_style)],
        [Paragraph(f"<b>เลขประจำตัวผู้เสียภาษี / บัตรประชาชน:</b> {tax_formatted}", bold_style), Paragraph(f"<b>สาขา:</b> {vendor.branch_no or 'สำนักงานใหญ่'}", normal_style)],
        [Paragraph(f"<b>ที่อยู่:</b> เลขที่ {vendor.address_no or '-'} หมู่ {vendor.address_moo or '-'} ต.{vendor.address_subdistrict or '-'} อ.{vendor.address_district or '-'} จ.{vendor.address_province or '-'} {vendor.address_postcode or '-'}", normal_style), ""],
        [Paragraph(f"<b>โทรศัพท์:</b> {vendor.vendor_phone or '-'}", normal_style), Paragraph(f"<b>Email e-Tax:</b> {vendor.email_etax or '-'}", normal_style)],
    ]
    info_table = Table(info_data, colWidths=[270, 265])
    info_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 3), (1, 3)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10))

    # Section 6-12: Commercial & Bank Info
    bank_data = [
        [Paragraph("<b>เงื่อนไขการค้าและการชำระเงิน</b>", bold_style), ""],
        [Paragraph(f"<b>ประเภทภาษี:</b> {vendor.vat_type or '-'} | <b>หัก ณ ที่จ่าย:</b> {vendor.wht_type or '-'} ({vendor.wht_rate or '-'})", normal_style), Paragraph(f"<b>เงื่อนไขชำระ:</b> {vendor.payment_term or '-'} ({vendor.credit_days or '-'} วัน)", normal_style)],
        [Paragraph(f"<b>วิธีการชำระ:</b> {vendor.payment_method or '-'}", normal_style), Paragraph(f"<b>ธนาคาร:</b> {vendor.bank_name or '-'} สาขา {vendor.bank_branch or '-'}", normal_style)],
        [Paragraph(f"<b>ชื่อบัญชี:</b> {vendor.bank_account_name_th or '-'}", normal_style), Paragraph(f"<b>เลขที่บัญชี:</b> {vendor.bank_account_no or '-'}", bold_style)],
    ]
    bank_table = Table(bank_data, colWidths=[270, 265])
    bank_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(bank_table)
    elements.append(Spacer(1, 12))

    # Section 15: Signatures
    sign_data = [
        [Paragraph("ผู้ขอเปิด/เปลี่ยนแปลงหน้าบัญชี", normal_style), Paragraph("ผู้มีอำนาจอนุมัติ", normal_style)],
        [Spacer(1, 25), Spacer(1, 25)],
        [
            Paragraph(f"ลงชื่อ: ...................................................<br/>({vendor.approver_requestor_name or vendor.req_name or 'ผู้ขอเปิด'})<br/>วันที่: {vendor.approver_requestor_date or '-'}", normal_style),
            Paragraph(f"ลงชื่อ: ...................................................<br/>({vendor.approver_manager_name or 'ผู้มีอำนาจอนุมัติ'})<br/>วันที่: {vendor.approver_manager_date or '-'}", normal_style),
        ]
    ]
    sign_table = Table(sign_data, colWidths=[265, 270])
    sign_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(sign_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
