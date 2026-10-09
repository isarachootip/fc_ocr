import type { Role } from './auth';

export const isSysadmin = (role: Role | string): boolean => role === 'sysadmin';

export const isAdmin = (role: Role | string): boolean => role === 'admin' || role === 'sysadmin';

export const roleLabel = (role: Role | string): string => {
  switch (role) {
    case 'sysadmin':
      return 'ผู้ดูแลระบบสูงสุด (Sysadmin)';
    case 'admin':
      return 'ผู้ดูแลระบบ (Admin)';
    case 'user':
    default:
      return 'ผู้ใช้งานทั่วไป';
  }
};
