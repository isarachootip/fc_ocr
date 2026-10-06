import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { fetchCurrentUser, logout, type AuthUser } from '../../services/auth';
import { setUnauthorizedHandler } from '../../services/http';
import { AuthContext } from '../../hooks/useAuth';
import { LoginScreen } from './LoginScreen';

type Status = 'loading' | 'anonymous' | 'authenticated';

/** Renders children only for a signed-in user; otherwise shows the login screen. */
export const AuthGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [status, setStatus] = useState<Status>('loading');
  const [user, setUser] = useState<AuthUser | null>(null);
  const [expired, setExpired] = useState(false);

  useEffect(() => {
    fetchCurrentUser()
      .then((u) => {
        setUser(u);
        setStatus(u ? 'authenticated' : 'anonymous');
      })
      .catch(() => setStatus('anonymous'));
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => {
      setUser(null);
      setExpired(true);
      setStatus('anonymous');
    });
    return () => setUnauthorizedHandler(null);
  }, []);

  const signOut = useCallback(async () => {
    await logout().catch(() => undefined);
    setExpired(false);
    setUser(null);
    setStatus('anonymous');
  }, []);

  const value = useMemo(() => (user ? { user, signOut } : null), [user, signOut]);

  if (status === 'loading') {
    return <div className="min-h-screen flex items-center justify-center text-sm text-slate-500">กำลังโหลด...</div>;
  }
  if (status === 'anonymous' || !value) {
    return (
      <LoginScreen
        sessionExpired={expired}
        onLoggedIn={(u) => {
          setUser(u);
          setExpired(false);
          setStatus('authenticated');
        }}
      />
    );
  }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
