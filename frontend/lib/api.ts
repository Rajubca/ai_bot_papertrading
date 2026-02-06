// Fallback to local address if the environment variable is missing
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function apiFetch(
  path: string,
  options: RequestInit = {}
) {
  // Ensure the path starts with a slash
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${API_BASE}${cleanPath}`;

  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("token")
      : null;

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    // Attempt to parse error detail from FastAPI
    const errorData = await res.json().catch(() => ({}));
    const errorMessage = errorData.detail || `HTTP ${res.status}`;
    
    console.error(`API Error [${res.status}] ${url}:`, errorMessage);
    throw new Error(errorMessage);
  }

  return res.json();
}