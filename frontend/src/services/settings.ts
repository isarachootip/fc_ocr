import { apiFetch } from './http';

export type OcrEngine = 'AI_GEMINI' | 'LOCAL_OCR';
export type KeySource = 'database' | 'env' | 'none';

export interface GeminiStatus {
  configured: boolean;
  source: KeySource;
  engine: OcrEngine;
  masked: string | null;
  updated_by: string | null;
  updated_at: string | null;
}

const URL = '/api/settings/gemini';

async function check(res: Response, fallback: string): Promise<Response> {
  if (res.ok) return res;
  const err = await res.json().catch(() => ({ detail: '' }));
  throw new Error(typeof err.detail === 'string' && err.detail ? err.detail : fallback);
}

export async function fetchGeminiStatus(): Promise<GeminiStatus> {
  return (await check(await apiFetch(URL), 'Failed to fetch Gemini status')).json();
}

export async function saveGeminiKey(apiKey: string): Promise<GeminiStatus> {
  const res = await apiFetch(URL, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: apiKey }),
  });
  return (await check(res, 'Failed to save Gemini key')).json();
}

export async function clearGeminiKey(): Promise<GeminiStatus> {
  const res = await apiFetch(URL, { method: 'DELETE' });
  return (await check(res, 'Failed to remove Gemini key')).json();
}
