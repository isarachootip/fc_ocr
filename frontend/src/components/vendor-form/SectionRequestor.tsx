import React from 'react';
import type { VendorFormData } from '../../types/vendor';
import { UserCheck } from 'lucide-react';

interface Props {
  data: VendorFormData;
  onChange: (fields: Partial<VendorFormData>) => void;
}

export const SectionRequestor: React.FC<Props> = ({ data, onChange }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-5">
      <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-2">
        <UserCheck className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-800 text-sm">
          1-3. รายละเอียดข้อมูลผู้ขอ และสถานะคำขอ (Requestor & Request Type)
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">วันที่แจ้ง</label>
          <input
            type="text"
            placeholder="เช่น 13/07/2569"
            value={data.req_date || ''}
            onChange={(e) => onChange({ req_date: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">ชื่อผู้แจ้ง</label>
          <input
            type="text"
            placeholder="ชื่อ-นามสกุล ผู้แจ้ง"
            value={data.req_name || ''}
            onChange={(e) => onChange({ req_name: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">อีเมลผู้แจ้ง</label>
          <input
            type="email"
            placeholder="user@company.com"
            value={data.req_email || ''}
            onChange={(e) => onChange({ req_email: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">แผนก</label>
          <input
            type="text"
            placeholder="เช่น HWS Account AR"
            value={data.req_department || ''}
            onChange={(e) => onChange({ req_department: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">BU</label>
          <input
            type="text"
            placeholder="เช่น CTD"
            value={data.req_bu || ''}
            onChange={(e) => onChange({ req_bu: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">โทรศัพท์</label>
          <input
            type="text"
            placeholder="02-xxx-xxxx"
            value={data.req_phone || ''}
            onChange={(e) => onChange({ req_phone: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">เบอร์ต่อ</label>
          <input
            type="text"
            placeholder="53464"
            value={data.req_ext || ''}
            onChange={(e) => onChange({ req_ext: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t border-slate-100">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">สถานภาพ</label>
          <select
            value={data.status_type || 'เพิ่มเติม'}
            onChange={(e) => onChange({ status_type: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="เพิ่มเติม">เพิ่มเติม (เพิ่มใหม่)</option>
            <option value="ปรับปรุง">ปรับปรุง (แก้ไขข้อมูลเดิม)</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Oracle Module</label>
          <select
            value={data.oracle_module || 'AP'}
            onChange={(e) => onChange({ oracle_module: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm bg-white"
          >
            <option value="AP">AP (เจ้าหนี้)</option>
            <option value="AR">AR (ลูกหนี้)</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">จุดประสงค์</label>
          <input
            type="text"
            placeholder="เช่น เพิ่มร้านค้าใหม่ / ปลด Inactive"
            value={data.purpose || ''}
            onChange={(e) => onChange({ purpose: e.target.value })}
            className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>
    </div>
  );
};
