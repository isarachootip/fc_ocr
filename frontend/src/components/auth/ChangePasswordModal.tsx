import React, { useState } from 'react';
import { X } from 'lucide-react';
import { changePassword } from '../../services/auth';

export const ChangePasswordModal: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [current, setCurrent] = useState('');
  const [next, setNext] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (next !== confirm) {
      setError('รหัสผ่านใหม่ไม่ตรงกัน');
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await changePassword(current, next);
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to change password');
    } finally {
      setBusy(false);
    }
  };

  const input = 'w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500';

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 flex items-center justify-center px-4" role="dialog" aria-modal="true">
      <form onSubmit={submit} className="w-full max-w-sm bg-white rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <h2 className="font-bold text-slate-800 text-sm">เปลี่ยนรหัสผ่าน</h2>
          <button type="button" onClick={onClose} aria-label="ปิด"><X className="w-4 h-4 text-slate-500" /></button>
        </div>
        {done ? (
          <>
            <p role="status" className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg p-3">เปลี่ยนรหัสผ่านเรียบร้อยแล้ว</p>
            <button type="button" onClick={onClose} className="w-full py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold">ปิด</button>
          </>
        ) : (
          <>
            {error && <div role="alert" className="p-2.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs">{error}</div>}
            <label className="block text-xs font-medium text-slate-600">รหัสผ่านปัจจุบัน
              <input className={input} type="password" autoComplete="current-password" required value={current} onChange={(e) => setCurrent(e.target.value)} />
            </label>
            <label className="block text-xs font-medium text-slate-600">รหัสผ่านใหม่ (อย่างน้อย 8 ตัว)
              <input className={input} type="password" autoComplete="new-password" required minLength={8} value={next} onChange={(e) => setNext(e.target.value)} />
            </label>
            <label className="block text-xs font-medium text-slate-600">ยืนยันรหัสผ่านใหม่
              <input className={input} type="password" autoComplete="new-password" required value={confirm} onChange={(e) => setConfirm(e.target.value)} />
            </label>
            <button type="submit" disabled={busy} className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white rounded-lg text-sm font-semibold">
              {busy ? 'กำลังบันทึก...' : 'บันทึก'}
            </button>
          </>
        )}
      </form>
    </div>
  );
};
