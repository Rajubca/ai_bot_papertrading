"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { setToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";

      // Backend expects JSON for login as per current implementation
      const body = JSON.stringify({ email, password });

      const headers = { "Content-Type": "application/json" };

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${endpoint}`, {
        method: "POST",
        headers,
        body,
      });

      if (!res.ok) {
        const errText = await res.json().then(j => j.detail).catch(() => "Authentication failed");
        throw new Error(errText);
      }

      if (isLogin) {
        const data = await res.json();
        setToken(data.access_token);
        router.push("/");
      } else {
         // After register, maybe auto login or ask to login?
         // Current backend register returns {status: "ok"} and doesn't return token.
         setIsLogin(true);
         setError("Registration successful! Please sign in.");
      }

    } catch (err: any) {
        setError(err.message);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 dark:bg-gray-900">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded shadow-md dark:bg-gray-800">
        <h2 className="text-2xl font-bold text-center text-gray-900 dark:text-white">
          {isLogin ? "Sign in to your account" : "Create a new account"}
        </h2>
        {error && (
          <div className={`p-3 text-sm rounded ${error.includes("successful") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {isLogin ? "Sign In" : "Sign Up"}
          </button>
        </form>
        <div className="text-sm text-center">
          <button
            onClick={() => { setIsLogin(!isLogin); setError(""); }}
            className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400"
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
}
