"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, logout } from "@/lib/auth";
import { parseJwt } from "@/lib/user";

export default function ProfileMenu() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = getToken();
    const parsed = parseJwt(token);
    setUser(parsed || {}); // 👈 NEVER null
  }, []);

  const displayName =
    user?.name || user?.email || "Account";

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="border px-3 py-1 rounded flex items-center gap-2"
      >
        <span className="font-medium">{displayName}</span>
        <span>▾</span>
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 border bg-white rounded shadow">
          <div className="px-4 py-2 border-b">
            <div className="font-semibold">{displayName}</div>
          </div>

          <button
            className="w-full text-left px-4 py-2 hover:bg-gray-100"
            onClick={() => {
              setOpen(false);
              router.push("/profile");
            }}
          >
            Profile
          </button>

          <button
            className="w-full text-left px-4 py-2 hover:bg-gray-100"
            onClick={() => {
              setOpen(false);
              router.push("/settings");
            }}
          >
            Settings
          </button>

          <button
            className="w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100"
            onClick={() => {
              logout();
              router.push("/login");
            }}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
