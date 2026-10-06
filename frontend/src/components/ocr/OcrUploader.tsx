import React, { useState, useRef } from 'react';
import { UploadCloud, Loader2, FileText } from 'lucide-react';
import { scanIdCard } from '../../services/api';
import type { IdCardOcrResult } from '../../types/ocr';

interface Props {
  onScanComplete: (result: IdCardOcrResult) => void;
}

export const OcrUploader: React.FC<Props> = ({ onScanComplete }) => {
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    setError(null);
    setFileName(file.name);
    setLoading(true);

    try {
      const result = await scanIdCard(file);
      onScanComplete(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาดในการสแกน');
    } finally {
      setLoading(false);
    }
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-slate-800 text-base flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-indigo-600" />
          สแกนสำเนาบัตรประชาชน (Smart OCR Auto-fill)
        </h3>
        <span className="text-xs px-2.5 py-1 bg-indigo-50 text-indigo-700 font-medium rounded-full">
          รองรับ PDF, JPG, PNG
        </span>
      </div>
      
      <p className="text-xs text-slate-500 mb-4">
        ลากไฟล์สำเนาบัตรประชาชนมาวาง หรือคลิกเพื่ออัปโหลด ระบบ AI จะอ่านเลขบัตร ชื่อ-สกุล และที่อยู่ เพื่อกรอกลงแบบฟอร์มให้อัตโนมัติ
      </p>

      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          loading ? 'border-indigo-400 bg-indigo-50/50' : 'border-slate-300 hover:border-indigo-500 hover:bg-slate-50'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />

        {loading ? (
          <div className="flex flex-col items-center py-2">
            <Loader2 className="w-8 h-8 text-indigo-600 animate-spin mb-2" />
            <span className="text-sm font-medium text-slate-700">กำลังสแกนและวิเคราะห์เอกสาร...</span>
            <span className="text-xs text-slate-400 mt-1">ไฟล์: {fileName}</span>
          </div>
        ) : (
          <div className="flex flex-col items-center py-2">
            <div className="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mb-3">
              <FileText className="w-6 h-6" />
            </div>
            <span className="text-sm font-medium text-slate-700">
              คลิกเพื่อเลือกไฟล์ หรือลากไฟล์มาวางที่นี่
            </span>
            <span className="text-xs text-slate-400 mt-1">
              (เช่น 2.สำเนาบัตรประชาชน.pdf)
            </span>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-3 p-3 bg-red-50 text-red-700 rounded-lg text-xs font-medium">
          {error}
        </div>
      )}
    </div>
  );
};
