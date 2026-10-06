import React, { useState } from 'react';
import { Save, AlertCircle, RotateCcw } from 'lucide-react';
import type { VendorFormData, VendorRecord } from '../../types/vendor';
import { createVendor } from '../../services/api';
import { SectionRequestor } from './SectionRequestor';
import { SectionVendorAddress } from './SectionVendorAddress';
import { SectionTaxId } from './SectionTaxId';
import { SectionCommercial } from './SectionCommercial';
import { SectionInternalFast } from './SectionInternalFast';

interface Props {
  formData: VendorFormData;
  setFormData: React.Dispatch<React.SetStateAction<VendorFormData>>;
  onSaveSuccess: (vendor: VendorRecord) => void;
  onReset: () => void;
}

export const VendorFormView: React.FC<Props> = ({
  formData,
  setFormData,
  onSaveSuccess,
  onReset,
}) => {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateFields = (fields: Partial<VendorFormData>) => {
    setFormData((prev) => ({ ...prev, ...fields }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.vendor_name_th.trim()) {
      setError('กรุณาระบุชื่อร้านค้า / บุคคลภาษาไทย');
      return;
    }
    if (!formData.tax_id.trim() || formData.tax_id.replace(/\D/g, '').length < 13) {
      setError('กรุณาระบุเลขประจำตัวผู้เสียภาษี / บัตรประชาชน ให้ครบ 13 หลัก');
      return;
    }

    setSaving(true);
    setError(null);
    try {
      const created = await createVendor(formData);
      onSaveSuccess(created);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาดในการบันทึกข้อมูล');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <SectionRequestor data={formData} onChange={updateFields} />
      <SectionVendorAddress data={formData} onChange={updateFields} />
      <SectionTaxId data={formData} onChange={updateFields} />
      <SectionCommercial data={formData} onChange={updateFields} />
      <SectionInternalFast data={formData} onChange={updateFields} />

      <div className="flex items-center justify-end gap-3 pt-2">
        <button
          type="button"
          onClick={onReset}
          className="px-4 py-2.5 border border-slate-300 text-slate-700 text-sm font-medium rounded-xl hover:bg-slate-100 flex items-center gap-2 transition-colors"
        >
          <RotateCcw className="w-4 h-4" />
          ล้างฟอร์ม
        </button>
        <button
          type="submit"
          disabled={saving}
          className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-xl flex items-center gap-2 shadow-sm disabled:opacity-50 transition-colors"
        >
          <Save className="w-4 h-4" />
          {saving ? 'กำลังบันทึกลงระบบ...' : 'บันทึกเปิด Vendor (Save to DB)'}
        </button>
      </div>
    </form>
  );
};
