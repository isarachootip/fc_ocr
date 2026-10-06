import React from 'react';
import { Printer, X } from 'lucide-react';
import type { VendorRecord } from '../../types/vendor';

interface Props {
  vendor: VendorRecord;
  onClose: () => void;
}

export const A4PrintableView: React.FC<Props> = ({ vendor, onClose }) => {
  const digits = (vendor.tax_id || '').replace(/\D/g, '').padEnd(13, ' ').slice(0, 13).split('');

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 overflow-y-auto p-4 sm:p-8 flex flex-col items-center">
      {/* Action Bar (hidden on print) */}
      <div className="no-print bg-white rounded-xl shadow-lg px-6 py-3 mb-6 w-full max-w-[210mm] flex items-center justify-between">
        <div>
          <h4 className="font-bold text-slate-800 text-sm">แบบพิมพ์ฟอร์ม A4 (Browser Print View)</h4>
          <p className="text-xs text-slate-500">รหัสร้านค้า: {vendor.vendor_code}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 flex items-center gap-1.5 shadow"
          >
            <Printer className="w-4 h-4" /> สั่งพิมพ์ (Print)
          </button>
          <button
            onClick={onClose}
            className="px-3 py-2 border border-slate-300 rounded-lg text-xs font-medium hover:bg-slate-100 flex items-center gap-1"
          >
            <X className="w-4 h-4" /> ปิด
          </button>
        </div>
      </div>

      {/* Printable Sheet */}
      <div className="bg-white w-full max-w-[210mm] min-h-[297mm] p-8 shadow-2xl rounded-sm text-slate-800 text-[11px] leading-relaxed border border-slate-200 print:border-none print:shadow-none print:p-0">
        <h2 className="text-center font-bold text-base border-b-2 border-slate-800 pb-2 mb-3">
          เอกสารการแจ้งเพิ่ม / ปรับปรุงทะเบียนร้านค้า (Vendor Master)
        </h2>

        {/* 1. Requestor */}
        <div className="border border-slate-300 p-2.5 mb-2 bg-slate-50/50">
          <div className="font-bold text-slate-700 mb-1">รายละเอียดข้อมูลผู้ขอ (Requestor)</div>
          <div className="grid grid-cols-3 gap-2">
            <div><b>วันที่แจ้ง:</b> {vendor.req_date || '-'}</div>
            <div><b>ชื่อผู้แจ้ง:</b> {vendor.req_name || '-'}</div>
            <div><b>อีเมล:</b> {vendor.req_email || '-'}</div>
            <div><b>แผนก:</b> {vendor.req_department || '-'}</div>
            <div><b>BU:</b> {vendor.req_bu || '-'}</div>
            <div><b>โทรศัพท์:</b> {vendor.req_phone || '-'} {vendor.req_ext ? `ต่อ ${vendor.req_ext}` : ''}</div>
          </div>
        </div>

        {/* 2. Type & Code */}
        <div className="border border-slate-300 p-2.5 mb-2 flex justify-between items-center">
          <div><b>สถานภาพ:</b> {vendor.status_type || 'เพิ่มเติม'} | <b>Module:</b> {vendor.oracle_module || 'AP'}</div>
          <div className="text-sm font-mono font-bold bg-slate-100 px-3 py-1 border border-slate-300">
            รหัสร้านค้า: {vendor.vendor_code}
          </div>
        </div>

        {/* 4. Name & Address */}
        <div className="border border-slate-300 p-2.5 mb-2">
          <div className="font-bold text-slate-700 mb-1">4. ชื่อและที่อยู่ของร้านค้า</div>
          <div className="mb-1"><b>ชื่อภาษาไทย:</b> {vendor.vendor_name_th}</div>
          <div className="mb-1"><b>ชื่อภาษาอังกฤษ:</b> {vendor.vendor_name_en || '-'}</div>
          <div>
            <b>ที่อยู่:</b> เลขที่ {vendor.address_no || '-'} หมู่ {vendor.address_moo || '-'} 
            ต.{vendor.address_subdistrict || '-'} อ.{vendor.address_district || '-'} 
            จ.{vendor.address_province || '-'} {vendor.address_postcode || '-'} 
            | <b>โทร:</b> {vendor.vendor_phone || '-'} | <b>e-Tax:</b> {vendor.email_etax || '-'}
          </div>
        </div>

        {/* 5. Tax ID Boxes */}
        <div className="border border-slate-300 p-2.5 mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-bold">5. เลขประจำตัว 13 หลัก:</span>
            <div className="flex gap-1 font-mono font-bold">
              {digits.map((d, i) => (
                <span key={i} className="w-5 h-6 border border-slate-400 flex items-center justify-center bg-slate-50">
                  {d}
                </span>
              ))}
            </div>
          </div>
          <div><b>สาขา:</b> {vendor.branch_no || 'สำนักงานใหญ่'}</div>
        </div>

        {/* Commercial & Bank */}
        <div className="border border-slate-300 p-2.5 mb-2 grid grid-cols-2 gap-3">
          <div>
            <div className="font-bold text-slate-700 mb-1">ข้อมูลการค้า & ภาษี</div>
            <div><b>ผู้ติดต่อ:</b> {vendor.contact_name || '-'} ({vendor.contact_mobile || '-'})</div>
            <div><b>รูปแบบการค้า:</b> {vendor.business_format || '-'}</div>
            <div><b>ระบบภาษี:</b> {vendor.vat_type || '-'}</div>
            <div><b>หัก ณ ที่จ่าย:</b> {vendor.wht_type || '-'} ({vendor.wht_rate || '-'})</div>
          </div>
          <div>
            <div className="font-bold text-slate-700 mb-1">เงื่อนไขการเงิน & บัญชีธนาคาร</div>
            <div><b>เงื่อนไขชำระ:</b> {vendor.payment_term || '-'}</div>
            <div><b>ธนาคาร:</b> {vendor.bank_name || '-'} สาขา {vendor.bank_branch || '-'}</div>
            <div><b>ชื่อบัญชี:</b> {vendor.bank_account_name_th || '-'}</div>
            <div><b>เลขที่บัญชี:</b> {vendor.bank_account_no || '-'}</div>
          </div>
        </div>

        {/* Signatures */}
        <div className="border border-slate-300 p-4 mt-6 grid grid-cols-2 gap-8 text-center">
          <div>
            <div className="h-12 border-b border-dashed border-slate-400 flex items-end justify-center pb-1">
              {vendor.approver_requestor_name || vendor.req_name || ''}
            </div>
            <div className="text-[10px] text-slate-500 mt-1">ผู้ขอเปิด / เปลี่ยนแปลงหน้าบัญชี</div>
          </div>
          <div>
            <div className="h-12 border-b border-dashed border-slate-400 flex items-end justify-center pb-1">
              {vendor.approver_manager_name || ''}
            </div>
            <div className="text-[10px] text-slate-500 mt-1">ผู้มีอำนาจอนุมัติ</div>
          </div>
        </div>
      </div>
    </div>
  );
};
