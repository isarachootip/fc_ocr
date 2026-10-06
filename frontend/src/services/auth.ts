import { apiFetch } from './http';

export interface AuthUser {
  username: string;
}

const AUTH_URL = '/api/auth';

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
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '' }));
    throw new Error(err.detail || 'Login failed');
  }
  return res.json();
}

export async function logout(): Promise<void> {
  await apiFetch(`${AUTH_URL}/logout`, { method: 'POST' });
}
