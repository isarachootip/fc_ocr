import React from 'react';
import { Cpu, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import type { GeminiStatus } from '../../services/settings';

interface Props {
  status: GeminiStatus;
}

export const GeminiStatusCard: React.FC<Props> = ({ status }) => {
  const isAi = status.engine === 'AI_GEMINI';
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm mb-6">
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">สถานะระบบ OCR ปัจจุบัน</span>
          <div className="flex items-center gap-2 mt-1">
            {isAi ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                <Sparkles className="w-3.5 h-3.5 text-emerald-600" /> AI_GEMINI (เปิดใช้งาน)
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800">
                <Cpu className="w-3.5 h-3.5 text-amber-600" /> LOCAL_OCR (สำรอง)
              </span>
            )}
            <span className="text-xs text-slate-400">• แหล่งที่มา: {status.source}</span>
          </div>
        </div>

        <div className="text-right text-xs text-slate-500">
          <div>คีย์ปัจจุบัน: <span className="font-mono font-bold text-slate-700">{status.masked || '— ไม่มีคีย์ —'}</span></div>
          {status.updated_by && <div>อัปเดตโดย: {status.updated_by}</div>}
          {status.updated_at && (
            <div>เมื่อ: {new Date(status.updated_at).toLocaleString('th-TH')}</div>
          )}
        </div>
      </div>

      <p className="text-xs text-slate-500 mt-4 border-t border-slate-100 pt-3">
        {isAi ? (
          <span className="flex items-center gap-1.5 text-emerald-700">
            <CheckCircle2 className="w-4 h-4" /> ระบบจะแปลงหน้าแรกของ PDF เป็นภาพแล้วส่งให้ Gemini Vision อ่านบัตรประชาชนอัตโนมัติ
          </span>
        ) : (
          <span className="flex items-center gap-1.5 text-amber-700">
            <AlertCircle className="w-4 h-4" /> ใช้ข้อความที่ฝังใน PDF เท่านั้น — ไฟล์สแกนที่เป็นรูปภาพล้วนจะอ่านไม่ได้จนกว่าจะใส่ Gemini Key
          </span>
        )}
      </p>
    </div>
  );
};
