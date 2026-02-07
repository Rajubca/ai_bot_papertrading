// Define the base URL clearly
const getApiBase = () => {
  return process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
};

export async function apiFetch(
  path: string,
  options: RequestInit = {}
) {
  const API_BASE = getApiBase();

  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${API_BASE}${cleanPath}`;

  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("token")
      : null;

  // ✅ Build headers safely
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  // ✅ Only attach valid token
  if (
    token &&
    token !== "null" &&
    token !== "undefined" &&
    token.trim() !== ""
  ) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // 🔍 Debug (temporary – remove later)
  console.log("API TOKEN:", token);

  const res = await fetch(url, {
    ...options,
    headers,
    cache: "no-store",
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));

    const errorMessage =
      errorData.detail ||
      errorData.message ||
      JSON.stringify(errorData) ||
      `HTTP ${res.status}`;

    console.error(`API Error [${res.status}] ${url}:`, errorMessage);

    // Auto logout
    if (res.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("token");
      window.location.href = "/login?error=expired";
    }

    throw new Error(errorMessage);
  }

  return res.json();
}
