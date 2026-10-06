import { apiFetch } from './http';

export type Role = 'admin' | 'user';

export interface AuthUser {
  username: string;
  role: Role;
}

const AUTH_URL = '/api/auth';

async function errorMessage(res: Response, fallback: string): Promise<string> {
  const err = await res.json().catch(() => ({ detail: '' }));
  return typeof err.detail === 'string' && err.detail ? err.detail : fallback;
}

export async function fetchCurrentUser(): Promise<AuthUser | null> {
  const res = await apiFetch(`${AUTH_URL}/me`);
  if (!res.ok) return null;
  return res.json();
}

export async function login(username: string, password: string): Promise<AuthUser> {
  const res = await apiFetch(`${AUTH_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error(await errorMessage(res, 'Login failed'));
  return res.json();
}

export async function logout(): Promise<void> {
  await apiFetch(`${AUTH_URL}/logout`, { method: 'POST' });
}

export async function changePassword(currentPassword: string, newPassword: string): Promise<void> {
  const res = await apiFetch(`${AUTH_URL}/change-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
  });
  if (!res.ok) throw new Error(await errorMessage(res, 'Failed to change password'));
}
