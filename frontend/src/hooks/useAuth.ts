import { createContext, useContext } from 'react';
import type { AuthUser } from '../services/auth';

interface AuthContextValue {
  user: AuthUser;
  signOut: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthGate>');
  return ctx;
}
