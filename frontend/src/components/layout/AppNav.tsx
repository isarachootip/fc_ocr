import React from 'react';
import { Building2, ListFilter, PlusCircle, LogOut, Users, KeyRound, Settings as SettingsIcon } from 'lucide-react';
import { isAdmin, isSysadmin } from '../../services/roles';
import type { AuthUser } from '../../services/auth';

export type AppTab = 'form' | 'list' | 'users' | 'settings';

interface Props {
  user: AuthUser;
  activeTab: AppTab;
  onSelectTab: (tab: AppTab) => void;
  onOpenChangePassword: () => void;
  onSignOut: () => void;
}

export const AppNav: React.FC<Props> = ({
  user,
  activeTab,
  onSelectTab,
  onOpenChangePassword,
  onSignOut,
}) => {
  const tabBtn = (tab: AppTab, label: string, Icon: React.ComponentType<{ className?: string }>) => (
    <button
      onClick={() => onSelectTab(tab)}
      className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
        activeTab === tab ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
      }`}
    >
      <Icon className="w-4 h-4" /> {label}
    </button>
  );

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold shadow-md shadow-indigo-100">
            <Building2 className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-slate-800 text-base">ระบบลงทะเบียนและจัดการ Vendor Master</h1>
            <p className="text-xs text-slate-500">พร้อมระบบอ่านบัตรประชาชนอัตโนมัติ (AI & Local OCR)</p>
          </div>
        </div>

        <div className="flex bg-slate-100 p-1 rounded-xl">
          {tabBtn('form', 'แบบฟอร์มเปิด Vendor', PlusCircle)}
          {tabBtn('list', 'ทะเบียนผู้ค้า & พิมพ์เอกสาร', ListFilter)}
          {isAdmin(user.role) && tabBtn('users', 'จัดการผู้ใช้', Users)}
          {isSysadmin(user.role) && tabBtn('settings', 'ตั้งค่าระบบ', SettingsIcon)}
        </div>

        <div className="flex items-center gap-1">
          <span className="text-xs text-slate-500 hidden sm:inline mr-2">
            {user.username} {isSysadmin(user.role) && <span className="text-indigo-600 font-bold">(sysadmin)</span>}
          </span>
          <button
            onClick={onOpenChangePassword}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 flex items-center gap-1.5 transition-colors"
          >
            <KeyRound className="w-4 h-4" /> เปลี่ยนรหัสผ่าน
          </button>
          <button
            onClick={onSignOut}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-rose-600 hover:bg-rose-50 flex items-center gap-1.5 transition-colors"
          >
            <LogOut className="w-4 h-4" /> ออกจากระบบ
          </button>
        </div>
      </div>
    </header>
  );
};
