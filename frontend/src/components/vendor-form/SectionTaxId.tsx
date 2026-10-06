import React from 'react';
import type { VendorFormData } from '../../types/vendor';
import { CreditCard } from 'lucide-react';

interface Props {
  data: VendorFormData;
  onChange: (fields: Partial<VendorFormData>) => void;
}

export const SectionTaxId: React.FC<Props> = ({ data, onChange }) => {
  const digits = (data.tax_id || '').replace(/\D/g, '').padEnd(13, ' ').slice(0, 13).split('');

  const handleDigitChange = (index: number, val: string) => {
    const cleanDigit = val.replace(/\D/g, '').slice(-1);
    const newDigits = [...digits];
    newDigits[index] = cleanDigit || ' ';
    const newTaxId = newDigits.join('').trimEnd();
    onChange({ tax_id: newTaxId });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-5">
      <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-2">
        <CreditCard className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-800 text-sm">
          5. เลขประจำตัวผู้เสียภาษีอากรหรือเลขบัตรประจำตัวประชาชน *
        </h3>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-2">
            เลขประจำตัว 13 หลัก (ระบบจะแยกใส่ช่องแบบฟอร์มให้อัตโนมัติ)
          </label>
          <div className="flex items-center gap-1.5 sm:gap-2">
            {digits.map((digit, i) => (
              <React.Fragment key={i}>
                <input
                  type="text"
                  maxLength={1}
                  value={digit.trim()}
                  onChange={(e) => handleDigitChange(i, e.target.value)}
                  className="w-7 h-9 sm:w-8 sm:h-10 text-center font-mono font-bold text-base border-2 border-slate-300 rounded-lg focus:border-indigo-600 focus:bg-indigo-50/30 transition-all"
                />
                {(i === 0 || i === 4 || i === 9 || i === 11) && (
                  <span className="text-slate-400 font-bold">-</span>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        <div className="w-full sm:w-64">
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            สาขาที่ / สำนักงานใหญ่
          </label>
          <input
            type="text"
            placeholder="เช่น สำนักงานใหญ่ หรือ สาขาที่ 00001"
            value={data.branch_no || 'สำนักงานใหญ่'}
            onChange={(e) => onChange({ branch_no: e.target.value })}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
          />
        </div>
      </div>
    </div>
  );
};
