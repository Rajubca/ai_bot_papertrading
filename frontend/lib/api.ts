const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function apiFetch(endpoint: string, options = {}) {
  const token = localStorage.getItem("token");

  return fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options as any).headers,
    },
  }).then(res => res.json());
}
