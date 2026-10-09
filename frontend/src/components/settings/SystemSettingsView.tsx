import React, { useEffect, useState } from 'react';
import { KeyRound, Save, Trash2, ShieldCheck, AlertCircle } from 'lucide-react';
import { clearGeminiKey, fetchGeminiStatus, saveGeminiKey, type GeminiStatus } from '../../services/settings';
import { GeminiStatusCard } from './GeminiStatusCard';

export const SystemSettingsView: React.FC = () => {
  const [status, setStatus] = useState<GeminiStatus | null>(null);
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [banner, setBanner] = useState<{ type: 'ok' | 'err'; message: string } | null>(null);

  const load = async () => {
    try {
      setStatus(await fetchGeminiStatus());
    } catch (e) {
      setBanner({ type: 'err', message: e instanceof Error ? e.message : 'โหลดสถานะไม่สำเร็จ' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKey.trim()) return;
    setSaving(true);
    setBanner(null);
    try {
      setStatus(await saveGeminiKey(apiKey));
      setApiKey('');
      setBanner({ type: 'ok', message: 'บันทึก Gemini API Key เรียบร้อยแล้ว (มีผลทันที)' });
    } catch (err) {
      setBanner({ type: 'err', message: err instanceof Error ? err.message : 'บันทึกไม่สำเร็จ' });
    } finally {
      setSaving(false);
    }
  };

  const handleClear = async () => {
    if (!window.confirm('ต้องการลบ Gemini Key ออกจากระบบหรือไม่? ระบบจะกลับไปใช้ Local OCR')) return;
    setSaving(true);
    setBanner(null);
    try {
      setStatus(await clearGeminiKey());
      setBanner({ type: 'ok', message: 'ลบ Gemini Key เรียบร้อยแล้ว' });
    } catch (err) {
      setBanner({ type: 'err', message: err instanceof Error ? err.message : 'ลบไม่สำเร็จ' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-xs text-slate-500">กำลังโหลดการตั้งค่า...</div>;

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-slate-800">ตั้งค่าระบบ (System Settings)</h2>
        <p className="text-xs text-slate-500">เฉพาะผู้ดูแลระบบสูงสุด (Sysadmin) • จัดการ Gemini Vision API Key</p>
      </div>

      {banner && (
        <div className={`mb-5 p-3 rounded-xl text-xs flex items-center gap-2 ${
          banner.type === 'ok' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'
        }`}>
          {banner.type === 'ok' ? <ShieldCheck className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4 text-rose-600" />}
          <span>{banner.message}</span>
        </div>
      )}

      {status && <GeminiStatusCard status={status} />}

      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <KeyRound className="w-4 h-4 text-indigo-600" />
          <h3 className="text-sm font-bold text-slate-800">เปลี่ยน / บันทึก Gemini API Key ใหม่</h3>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Google AI Studio API Key <span className="text-rose-500">*</span>
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="วางคีย์ AIzaSy... ที่ได้จาก Google AI Studio"
              autoComplete="off"
              className="w-full px-3 py-2 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-mono"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              คีย์จะถูกเข้ารหัสก่อนบันทึกลงฐานข้อมูล และระบบจะไม่แสดงคีย์ตัวเต็มกลับมาอีกเพื่อความปลอดภัย
            </p>
          </div>

          <div className="flex items-center justify-between pt-2">
            <button
              type="button"
              onClick={handleClear}
              disabled={saving || !status?.configured}
              className="px-3 py-2 rounded-xl text-xs font-semibold text-rose-600 border border-rose-200 hover:bg-rose-50 disabled:opacity-40 flex items-center gap-1.5 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" /> ลบคีย์ออก
            </button>

            <button
              type="submit"
              disabled={saving || apiKey.trim().length < 20}
              className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-semibold hover:bg-indigo-700 disabled:opacity-50 shadow-md shadow-indigo-100 flex items-center gap-1.5 transition-all"
            >
              <Save className="w-3.5 h-3.5" /> {saving ? 'กำลังบันทึก...' : 'บันทึกคีย์'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
