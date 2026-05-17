// Lightweight typed API client. When packages/shared-types ships the
// OpenAPI-generated paths, swap `unknown` for the generated `paths` type
// and openapi-fetch will become fully type-safe end-to-end.
import createClient from 'openapi-fetch';

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export const api = createClient<unknown>({ baseUrl });

export function getAuthHeader(): HeadersInit {
  if (typeof window === 'undefined') return {};
  const token = window.localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}
