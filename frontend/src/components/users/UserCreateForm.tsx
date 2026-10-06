import React, { useState } from 'react';
import { UserPlus } from 'lucide-react';
import { createUser, type ManagedUser } from '../../services/users';
import type { Role } from '../../services/auth';

interface Props {
  onCreated: (user: ManagedUser) => void;
}

const INPUT = 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500';

export const UserCreateForm: React.FC<Props> = ({ onCreated }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<Role>('user');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      onCreated(await createUser(username.trim(), password, role));
      setUsername('');
      setPassword('');
      setRole('user');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create user');
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3">
      <h2 className="font-semibold text-slate-800 text-sm flex items-center gap-2">
        <UserPlus className="w-4 h-4 text-indigo-600" /> เพิ่มผู้ใช้ใหม่
      </h2>
      {error && <div role="alert" className="p-2.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input className={INPUT} placeholder="ชื่อผู้ใช้" aria-label="ชื่อผู้ใช้" autoComplete="off" required
          value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className={INPUT} type="password" placeholder="รหัสผ่าน (อย่างน้อย 8 ตัว)" aria-label="รหัสผ่าน"
          autoComplete="new-password" required minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} />
        <select className={INPUT} aria-label="สิทธิ์" value={role} onChange={(e) => setRole(e.target.value as Role)}>
          <option value="user">ผู้ใช้งานทั่วไป</option>
          <option value="admin">ผู้ดูแลระบบ</option>
        </select>
        <button type="submit" disabled={busy}
          className="py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white rounded-lg text-sm font-semibold">
          {busy ? 'กำลังบันทึก...' : 'เพิ่มผู้ใช้'}
        </button>
      </div>
    </form>
  );
};
