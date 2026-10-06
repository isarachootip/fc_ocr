import React from 'react';
import type { VendorFormData } from '../../types/vendor';
import { ShieldCheck } from 'lucide-react';

interface Props {
  data: VendorFormData;
  onChange: (fields: Partial<VendorFormData>) => void;
}

export const SectionInternalFast: React.FC<Props> = ({ data, onChange }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-5">
      <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-2">
        <ShieldCheck className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-800 text-sm">
          13-15. เอกสารแนบ ข้อมูลหน่วยงาน FAST และผู้อนุมัติ (Internal & Approvals)
        </h3>
      </div>

      {/* FAST Specifics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">TYPE</label>
          <select
            value={data.fast_type || 'Supplier'}
            onChange={(e) => onChange({ fast_type: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="Supplier">Supplier</option>
            <option value="Employee">Employee</option>
            <option value="Overseas">Overseas</option>
            <option value="Prepayment">Prepayment</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Site</label>
          <input
            type="text"
            placeholder="เช่น สาขา / ไซต์งาน"
            value={data.fast_site || ''}
            onChange={(e) => onChange({ fast_site: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Pay Group</label>
          <input
            type="text"
            placeholder="กลุ่มการจ่าย"
            value={data.fast_pay_group || ''}
            onChange={(e) => onChange({ fast_pay_group: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Branch</label>
          <input
            type="text"
            placeholder="สาขาบัญชี"
            value={data.fast_branch || ''}
            onChange={(e) => onChange({ fast_branch: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>

      {/* Approver Signatures */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-3 border-t border-slate-100">
        <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
          <h4 className="text-xs font-bold text-slate-700 mb-2">15. ผู้ขอเปิด / เปลี่ยนแปลงหน้าบัญชี</h4>
          <div className="space-y-2">
            <div>
              <label className="block text-[11px] text-slate-500 mb-0.5">ชื่อผู้ขอเปิด</label>
              <input
                type="text"
                placeholder="ชื่อ-นามสกุล"
                value={data.approver_requestor_name || data.req_name || ''}
                onChange={(e) => onChange({ approver_requestor_name: e.target.value })}
                className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
              />
            </div>
            <div>
              <label className="block text-[11px] text-slate-500 mb-0.5">วันที่</label>
              <input
                type="text"
                placeholder="วว/ดด/ปปปป"
                value={data.approver_requestor_date || ''}
                onChange={(e) => onChange({ approver_requestor_date: e.target.value })}
                className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
              />
            </div>
          </div>
        </div>

        <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
          <h4 className="text-xs font-bold text-slate-700 mb-2">ผู้มีอำนาจอนุมัติ</h4>
          <div className="space-y-2">
            <div>
              <label className="block text-[11px] text-slate-500 mb-0.5">ชื่อผู้อนุมัติ</label>
              <input
                type="text"
                placeholder="ชื่อ-นามสกุล ผู้จัดการ/ผู้อนุมัติ"
                value={data.approver_manager_name || ''}
                onChange={(e) => onChange({ approver_manager_name: e.target.value })}
                className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
              />
            </div>
            <div>
              <label className="block text-[11px] text-slate-500 mb-0.5">วันที่</label>
              <input
                type="text"
                placeholder="วว/ดด/ปปปป"
                value={data.approver_manager_date || ''}
                onChange={(e) => onChange({ approver_manager_date: e.target.value })}
                className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
