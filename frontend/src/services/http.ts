type UnauthorizedHandler = () => void;

let unauthorizedHandler: UnauthorizedHandler | null = null;

/** Register a callback fired whenever the API answers 401 (session expired). */
export function setUnauthorizedHandler(handler: UnauthorizedHandler | null): void {
  unauthorizedHandler = handler;
}

/** fetch wrapper: sends the session cookie and reports expired sessions. */
export async function apiFetch(input: string, init: RequestInit = {}): Promise<Response> {
  const res = await fetch(input, { credentials: 'same-origin', ...init });
  if (res.status === 401 && !input.startsWith('/api/auth/')) {
    unauthorizedHandler?.();
  }
  return res;
}
