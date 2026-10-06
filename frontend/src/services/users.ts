import { apiFetch } from './http';
import type { Role } from './auth';

export interface ManagedUser {
  id: number;
  username: string;
  role: Role;
  is_active: boolean;
  created_at: string;
}

export interface UserPatch {
  role?: Role;
  is_active?: boolean;
  password?: string;
}

const URL = '/api/users';

async function check(res: Response, fallback: string): Promise<Response> {
  if (res.ok) return res;
  const err = await res.json().catch(() => ({ detail: '' }));
  throw new Error(typeof err.detail === 'string' && err.detail ? err.detail : fallback);
}

export async function listUsers(): Promise<ManagedUser[]> {
  return (await check(await apiFetch(URL), 'Failed to load users')).json();
}

export async function createUser(username: string, password: string, role: Role): Promise<ManagedUser> {
  const res = await apiFetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, role }),
  });
  return (await check(res, 'Failed to create user')).json();
}

export async function updateUser(id: number, patch: UserPatch): Promise<ManagedUser> {
  const res = await apiFetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patch),
  });
  return (await check(res, 'Failed to update user')).json();
}
