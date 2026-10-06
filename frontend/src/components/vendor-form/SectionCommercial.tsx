import React from 'react';
import type { VendorFormData } from '../../types/vendor';
import { Landmark } from 'lucide-react';

interface Props {
  data: VendorFormData;
  onChange: (fields: Partial<VendorFormData>) => void;
}

export const SectionCommercial: React.FC<Props> = ({ data, onChange }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-5">
      <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-2">
        <Landmark className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-800 text-sm">
          6-12. ข้อมูลการค้า ภาษี และบัญชีธนาคาร (Commercial & Banking)
        </h3>
      </div>

      {/* Contact & Commercial Format */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">ผู้ประสานงานร้านค้า</label>
          <input
            type="text"
            placeholder="ชื่อผู้ติดต่อ"
            value={data.contact_name || ''}
            onChange={(e) => onChange({ contact_name: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">มือถือผู้ติดต่อ</label>
          <input
            type="text"
            placeholder="08x-xxx-xxxx"
            value={data.contact_mobile || ''}
            onChange={(e) => onChange({ contact_mobile: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">รูปแบบการค้า</label>
          <select
            value={data.business_format || 'ซื้อมาขายไป'}
            onChange={(e) => onChange({ business_format: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="ซื้อมาขายไป">ซื้อมาขายไป / เก็บเงินตามยอดขาย</option>
            <option value="ค่าจ้างทำของ">ค่าจ้างทำของ / บริการ</option>
            <option value="ให้เช่า GUARANTEE">ให้เช่า GUARANTEE</option>
            <option value="ส่วนแบ่งรายได้">ส่วนแบ่งรายได้ (Income Sharing)</option>
            <option value="FAST FOOD">FAST FOOD / FOOD COUPON</option>
          </select>
        </div>
      </div>

      {/* Tax & Payment Method */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4 pt-3 border-t border-slate-100">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">ระบบภาษีมูลค่าเพิ่ม</label>
          <select
            value={data.vat_type || 'ระบบภาษีมูลค่าเพิ่ม 7%'}
            onChange={(e) => onChange({ vat_type: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="ระบบภาษีมูลค่าเพิ่ม 7%">ระบบภาษีมูลค่าเพิ่ม 7%</option>
            <option value="นอกระบบภาษีมูลค่าเพิ่ม">นอกระบบภาษีมูลค่าเพิ่ม</option>
            <option value="ระบบภาษีมูลค่าเพิ่ม 1.5%">ระบบภาษีมูลค่าเพิ่ม 1.5%</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">ประเภทภาษีหัก ณ ที่จ่าย</label>
          <select
            value={data.wht_type || 'ภ.ง.ด. 3'}
            onChange={(e) => onChange({ wht_type: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="ภ.ง.ด. 3">ภ.ง.ด. 3 (บุคคลธรรมดา)</option>
            <option value="ภ.ง.ด. 53">ภ.ง.ด. 53 (นิติบุคคล)</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">อัตราหัก ณ ที่จ่าย</label>
          <select
            value={data.wht_rate || '3%'}
            onChange={(e) => onChange({ wht_rate: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="0%">0%</option>
            <option value="1%">1% (ขนส่ง)</option>
            <option value="2%">2% (โฆษณา)</option>
            <option value="3%">3% (บริการ/จ้างทำของ)</option>
            <option value="5%">5% (ค่าเช่า)</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">เงื่อนไขการชำระเงิน</label>
          <select
            value={data.payment_term || 'โอนผ่านธนาคาร'}
            onChange={(e) => onChange({ payment_term: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="โอนผ่านธนาคาร">โอนผ่านธนาคาร</option>
            <option value="เครดิต 30 วัน">เครดิต 30 วัน</option>
            <option value="เงินสด 7 วัน">เงินสด 7 วัน</option>
            <option value="เงินสด 15 วัน">เงินสด 15 วัน</option>
            <option value="เช็ค">เช็ค</option>
          </select>
        </div>
      </div>

      {/* Bank Account */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-3 border-t border-slate-100">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">ธนาคาร</label>
          <input
            type="text"
            placeholder="เช่น กสิกรไทย / กรุงเทพ"
            value={data.bank_name || ''}
            onChange={(e) => onChange({ bank_name: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">สาขา</label>
          <input
            type="text"
            placeholder="สาขาธนาคาร"
            value={data.bank_branch || ''}
            onChange={(e) => onChange({ bank_branch: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">ชื่อบัญชี (ไทย)</label>
          <input
            type="text"
            placeholder="ชื่อเจ้าของบัญชี"
            value={data.bank_account_name_th || ''}
            onChange={(e) => onChange({ bank_account_name_th: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">เลขที่บัญชีธนาคาร</label>
          <input
            type="text"
            placeholder="xxx-x-xxxxx-x"
            value={data.bank_account_no || ''}
            onChange={(e) => onChange({ bank_account_no: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm font-mono"
          />
        </div>
      </div>
    </div>
  );
};
