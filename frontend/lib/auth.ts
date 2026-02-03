import { apiFetch } from "./api";

export const setToken = (token: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("token", token);
  }
};

export const getToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token");
  }
  return null;
};

export const removeToken = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
  }
};

export const isAuthenticated = () => {
  return !!getToken();
};

export const logout = () => {
  removeToken();
  if (typeof window !== "undefined") {
    window.location.href = "/login";
  }
};

export async function getCurrentUser() {
  try {
    return await apiFetch("/api/auth/me");
  } catch (error) {
    return null;
  }
}
