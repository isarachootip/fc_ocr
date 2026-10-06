import React, { useState } from 'react';
import { KeyRound, ShieldCheck, UserCheck, UserX } from 'lucide-react';
import { updateUser, type ManagedUser, type UserPatch } from '../../services/users';
import type { Role } from '../../services/auth';

interface Props {
  users: ManagedUser[];
  currentUsername: string;
  onChanged: (user: ManagedUser) => void;
  onError: (message: string) => void;
}

export const UsersTable: React.FC<Props> = ({ users, currentUsername, onChanged, onError }) => {
  const [busyId, setBusyId] = useState<number | null>(null);

  const apply = async (u: ManagedUser, patch: UserPatch) => {
    setBusyId(u.id);
    try {
      onChanged(await updateUser(u.id, patch));
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Update failed');
    } finally {
      setBusyId(null);
    }
  };

  const resetPassword = (u: ManagedUser) => {
    const password = window.prompt(`ตั้งรหัสผ่านใหม่ให้ ${u.username} (อย่างน้อย 8 ตัวอักษร)`);
    if (password) void apply(u, { password });
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl overflow-x-auto">
      <table className="w-full text-left text-xs">
        <thead>
          <tr className="border-b border-slate-200 bg-slate-100/70 text-slate-600 font-semibold">
            <th className="py-3 px-4">ชื่อผู้ใช้</th>
            <th className="py-3 px-4">สิทธิ์</th>
            <th className="py-3 px-4">สถานะ</th>
            <th className="py-3 px-4">สร้างเมื่อ</th>
            <th className="py-3 px-4 text-center">จัดการ</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 text-slate-700">
          {users.map((u) => {
            const self = u.username === currentUsername;
            const btn = 'px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-50 flex items-center gap-1';
            return (
              <tr key={u.id} className={u.is_active ? '' : 'bg-slate-50 text-slate-400'}>
                <td className="py-3 px-4 font-medium">{u.username}{self && ' (คุณ)'}</td>
                <td className="py-3 px-4">
                  <select aria-label={`สิทธิ์ของ ${u.username}`} value={u.role} disabled={busyId === u.id || self}
                    onChange={(e) => void apply(u, { role: e.target.value as Role })}
                    className="border border-slate-200 rounded-lg px-2 py-1 bg-white">
                    <option value="user">ผู้ใช้งานทั่วไป</option>
                    <option value="admin">ผู้ดูแลระบบ</option>
                  </select>
                </td>
                <td className="py-3 px-4">
                  {u.is_active ? <span className="text-emerald-600 flex items-center gap-1"><ShieldCheck className="w-3.5 h-3.5" />ใช้งานได้</span> : 'ถูกระงับ'}
                </td>
                <td className="py-3 px-4">{new Date(u.created_at).toLocaleDateString('th-TH')}</td>
                <td className="py-3 px-4">
                  <div className="flex justify-center gap-1.5">
                    <button className={btn} disabled={busyId === u.id} onClick={() => resetPassword(u)}>
                      <KeyRound className="w-3.5 h-3.5" /> รีเซ็ตรหัสผ่าน
                    </button>
                    {!self && (
                      <button className={btn} disabled={busyId === u.id} onClick={() => void apply(u, { is_active: !u.is_active })}>
                        {u.is_active ? <><UserX className="w-3.5 h-3.5" /> ระงับ</> : <><UserCheck className="w-3.5 h-3.5" /> เปิดใช้งาน</>}
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
