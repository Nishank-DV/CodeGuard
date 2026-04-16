import { getApiKey } from './auth';

export const API_BASE = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');

export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers || {});
  headers.set('X-API-Key', getApiKey());
  try {
    return await fetch(`${API_BASE}${path}`, { ...init, headers });
  } catch (error) {
    const reason = error instanceof Error ? error.message : 'unknown network error';
    throw new Error(`Cannot reach backend API at ${API_BASE} (${reason}). Ensure backend is running.`);
  }
}

async function tryReadJsonBody<T>(response: Response): Promise<T | null> {
  const text = await response.text();
  if (!text.trim()) return null;

  try {
    return JSON.parse(text) as T;
  } catch {
    return null;
  }
}

export async function readApiJson<T>(response: Response, emptyBodyMessage = 'API returned an empty response body'): Promise<T> {
  const data = await tryReadJsonBody<T>(response);
  if (data === null) {
    throw new Error(emptyBodyMessage);
  }
  return data;
}

export async function readApiError(response: Response, fallbackMessage: string): Promise<string> {
  const payload = await tryReadJsonBody<Record<string, unknown>>(response);
  const candidate = payload?.detail ?? payload?.message ?? payload?.error;
  if (typeof candidate === 'string' && candidate.trim()) {
    return candidate;
  }
  return `${fallbackMessage} (HTTP ${response.status})`;
}

export function reportDownloadUrl(scanId: string, format: 'json' | 'md'): string {
  const key = encodeURIComponent(getApiKey());
  return `${API_BASE}/scans/${scanId}/report?format=${format}&api_key=${key}`;
}
