export type DemoRole = 'admin' | 'analyst' | 'viewer';

const ROLE_KEY = 'codeguard_role';
const API_KEY_KEY = 'codeguard_api_key';

const defaults: Record<DemoRole, string> = {
  admin: 'dev-admin-key',
  analyst: 'dev-analyst-key',
  viewer: 'dev-viewer-key',
};

export function getRole(): DemoRole | null {
  const value = localStorage.getItem(ROLE_KEY);
  if (value === 'admin' || value === 'analyst' || value === 'viewer') return value;
  return null;
}

export function getApiKey(): string {
  return localStorage.getItem(API_KEY_KEY) || import.meta.env.VITE_API_KEY || defaults.analyst;
}

export function isAuthenticated(): boolean {
  return Boolean(getApiKey());
}

export function setAuth(role: DemoRole, apiKey?: string): void {
  localStorage.setItem(ROLE_KEY, role);
  localStorage.setItem(API_KEY_KEY, (apiKey || defaults[role]).trim());
}

export function clearAuth(): void {
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(API_KEY_KEY);
}

export function defaultKeyForRole(role: DemoRole): string {
  return defaults[role];
}
