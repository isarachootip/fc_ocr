import React, { useState } from 'react';
import { Check, X, Sparkles } from 'lucide-react';
import type { IdCardOcrResult } from '../../types/ocr';
import { lookupPostcode } from '../../services/api';

interface Props {
  data: IdCardOcrResult;
  onConfirm: (confirmedData: IdCardOcrResult) => void;
  onClose: () => void;
}

const ADDRESS_FIELDS: Array<{ key: keyof IdCardOcrResult; label: string; triggersPostcode?: boolean }> = [
  { key: 'address_no', label: 'เลขที่' },
  { key: 'address_moo', label: 'หมู่ที่' },
  { key: 'address_soi', label: 'ตรอก / ซอย' },
  { key: 'address_road', label: 'ถนน' },
  { key: 'address_subdistrict', label: 'ตำบล / แขวง', triggersPostcode: true },
  { key: 'address_district', label: 'อำเภอ / เขต', triggersPostcode: true },
  { key: 'address_province', label: 'จังหวัด', triggersPostcode: true },
  { key: 'address_postcode', label: 'รหัสไปรษณีย์' },
];

export const OcrConfirmModal: React.FC<Props> = ({ data, onConfirm, onClose }) => {
  const [formData, setFormData] = useState<IdCardOcrResult>({ ...data });

  const updateField = async (field: keyof IdCardOcrResult, value: string, triggersPostcode?: boolean) => {
    const next = { ...formData, [field]: value };
    setFormData(next);

    if (triggersPostcode) {
      const code = await lookupPostcode(next.address_subdistrict, next.address_district, next.address_province);
      if (code) {
        setFormData((prev) => ({ ...prev, address_postcode: code }));
      }
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in duration-200">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-base">ตรวจสอบข้อมูลบัตรประชาชน (OCR Preview)</h3>
              <p className="text-xs text-slate-500">กรุณาตรวจสอบความถูกต้องของข้อมูลก่อนนำไปกรอกลงฟอร์ม</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <div className="p-6 overflow-y-auto space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className="block text-xs font-semibold text-slate-600 mb-1">เลขประจำตัวประชาชน 13 หลัก *</label>
              <input
                type="text"
                maxLength={13}
                value={formData.tax_id}
                onChange={(e) => updateField('tax_id', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm font-mono tracking-wider focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">ชื่อ-นามสกุล (ภาษาไทย) *</label>
              <input
                type="text"
                value={formData.full_name_th}
                onChange={(e) => updateField('full_name_th', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">ชื่อ-นามสกุล (ภาษาอังกฤษ)</label>
              <input
                type="text"
                value={formData.full_name_en || ''}
                onChange={(e) => updateField('full_name_en', e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="border-t border-slate-100 pt-4">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">ที่อยู่ตามบัตรประชาชน</h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {ADDRESS_FIELDS.map(({ key, label, triggersPostcode }) => (
                <div key={key}>
                  <label className="block text-xs text-slate-500 mb-1">{label}</label>
                  <input
                    type="text"
                    value={(formData[key] as string) || ''}
                    onChange={(e) => updateField(key, e.target.value, triggersPostcode)}
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-slate-300 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-100 transition-colors"
          >
            ยกเลิก
          </button>
          <button
            onClick={() => onConfirm(formData)}
            className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg flex items-center gap-2 shadow-sm transition-colors"
          >
            <Check className="w-4 h-4" />
            ยืนยันและนำข้อมูลเข้าแบบฟอร์ม
          </button>
        </div>
      </div>
    </div>
  );
};
