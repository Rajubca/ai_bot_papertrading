"use client";

import { useState } from "react";
import { login, saveToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setError(null);
    try {
      const res = await login(email, password);
      saveToken(res.access_token);
      router.push("/");
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 space-y-4">
      <h1 className="text-2xl font-bold">Login</h1>

      <input
        className="border p-2 w-full"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        className="border p-2 w-full"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button className="border px-4 py-2 w-full" onClick={submit}>
        Login
      </button>

      {error && <div className="text-red-600">{error}</div>}

      <p className="text-sm">
        No account?{" "}
        <a className="underline" href="/register">
          Register
        </a>
      </p>
    </div>
  );
}
