import React from 'react';
import type { VendorFormData } from '../../types/vendor';
import { MapPin } from 'lucide-react';

interface Props {
  data: VendorFormData;
  onChange: (fields: Partial<VendorFormData>) => void;
}

export const SectionVendorAddress: React.FC<Props> = ({ data, onChange }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-5">
      <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-2">
        <MapPin className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-800 text-sm">
          4. ชื่อและที่อยู่ของร้านค้า (ตรงกับ ภ.พ. หรือบัตรประชาชน)
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            ชื่อร้านค้า / บุคคล (ภาษาไทย) *
          </label>
          <input
            type="text"
            required
            placeholder="เช่น เตียง กันนิกา"
            value={data.vendor_name_th}
            onChange={(e) => onChange({ vendor_name_th: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            ชื่อร้านค้า / บุคคล (ภาษาอังกฤษ)
          </label>
          <input
            type="text"
            placeholder="เช่น Tiang Kannika"
            value={data.vendor_name_en || ''}
            onChange={(e) => onChange({ vendor_name_en: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-4">
        <div>
          <label className="block text-xs text-slate-600 mb-1">เลขที่</label>
          <input
            type="text"
            value={data.address_no || ''}
            onChange={(e) => onChange({ address_no: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">หมู่ที่</label>
          <input
            type="text"
            value={data.address_moo || ''}
            onChange={(e) => onChange({ address_moo: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">อาคาร</label>
          <input
            type="text"
            value={data.address_building || ''}
            onChange={(e) => onChange({ address_building: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">ชั้น</label>
          <input
            type="text"
            value={data.address_floor || ''}
            onChange={(e) => onChange({ address_floor: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">ตรอก/ซอย</label>
          <input
            type="text"
            value={data.address_soi || ''}
            onChange={(e) => onChange({ address_soi: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">ถนน</label>
          <input
            type="text"
            value={data.address_road || ''}
            onChange={(e) => onChange({ address_road: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
        <div>
          <label className="block text-xs text-slate-600 mb-1">ตำบล / แขวง</label>
          <input
            type="text"
            value={data.address_subdistrict || ''}
            onChange={(e) => onChange({ address_subdistrict: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">อำเภอ / เขต</label>
          <input
            type="text"
            value={data.address_district || ''}
            onChange={(e) => onChange({ address_district: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">จังหวัด</label>
          <input
            type="text"
            value={data.address_province || ''}
            onChange={(e) => onChange({ address_province: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">รหัสไปรษณีย์</label>
          <input
            type="text"
            value={data.address_postcode || ''}
            onChange={(e) => onChange({ address_postcode: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-100">
        <div>
          <label className="block text-xs text-slate-600 mb-1">โทรศัพท์ร้านค้า</label>
          <input
            type="text"
            value={data.vendor_phone || ''}
            onChange={(e) => onChange({ vendor_phone: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">โทรสาร (FAX)</label>
          <input
            type="text"
            value={data.vendor_fax || ''}
            onChange={(e) => onChange({ vendor_fax: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-600 mb-1">Email e-Tax</label>
          <input
            type="email"
            value={data.email_etax || ''}
            onChange={(e) => onChange({ email_etax: e.target.value })}
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>
    </div>
  );
};
