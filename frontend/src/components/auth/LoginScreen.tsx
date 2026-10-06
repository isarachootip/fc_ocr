import React, { useState } from 'react';
import { Building2, Lock, LogIn, User } from 'lucide-react';
import { login, type AuthUser } from '../../services/auth';

interface Props {
  onLoggedIn: (user: AuthUser) => void;
  sessionExpired?: boolean;
}

export const LoginScreen: React.FC<Props> = ({ onLoggedIn, sessionExpired }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      onLoggedIn(await login(username.trim(), password));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      setPassword('');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm bg-white border border-slate-200 rounded-2xl shadow-sm p-8 space-y-5"
      >
        <div className="flex flex-col items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-md shadow-indigo-100">
            <Building2 className="w-6 h-6" />
          </div>
          <div className="text-center">
            <h1 className="font-bold text-slate-800">ระบบลงทะเบียน Vendor Master</h1>
            <p className="text-xs text-slate-500">กรุณาเข้าสู่ระบบเพื่อใช้งาน</p>
          </div>
        </div>

        {sessionExpired && !error && (
          <div role="status" className="p-3 bg-amber-50 border border-amber-200 text-amber-800 rounded-lg text-xs">
            เซสชันหมดอายุ กรุณาเข้าสู่ระบบอีกครั้ง
          </div>
        )}
        {error && (
          <div role="alert" className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs">
            {error}
          </div>
        )}

        <label className="block text-xs font-medium text-slate-600">
          ชื่อผู้ใช้
          <div className="mt-1 relative">
            <User className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              autoComplete="username"
              autoFocus
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </label>

        <label className="block text-xs font-medium text-slate-600">
          รหัสผ่าน
          <div className="mt-1 relative">
            <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </label>

        <button
          type="submit"
          disabled={busy}
          className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-colors"
        >
          <LogIn className="w-4 h-4" /> {busy ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ'}
        </button>
      </form>
    </div>
  );
};
