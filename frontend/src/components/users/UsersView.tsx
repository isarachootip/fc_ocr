import React, { useCallback, useEffect, useState } from 'react';
import { listUsers, type ManagedUser } from '../../services/users';
import { useAuth } from '../../hooks/useAuth';
import { UserCreateForm } from './UserCreateForm';
import { UsersTable } from './UsersTable';

export const UsersView: React.FC = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState<ManagedUser[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    listUsers().then(setUsers).catch((e: Error) => setError(e.message));
  }, []);

  useEffect(load, [load]);

  const upsert = (saved: ManagedUser) => {
    setError(null);
    setUsers((prev) =>
      prev.some((u) => u.id === saved.id) ? prev.map((u) => (u.id === saved.id ? saved : u)) : [...prev, saved],
    );
  };

  return (
    <div className="space-y-5">
      <UserCreateForm currentUserRole={user.role} onCreated={upsert} />
      {error && (
        <div role="alert" className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
          {error}
        </div>
      )}
      <UsersTable
        users={users}
        currentUsername={user.username}
        currentUserRole={user.role}
        onChanged={upsert}
        onError={setError}
      />
    </div>
  );
};
