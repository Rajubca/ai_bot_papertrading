"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, logout } from "@/lib/auth";
import { parseJwt } from "@/lib/user";

export default function ProfileMenu() {
  const router = useRouter();
  const ref = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [user, setUser] = useState<any>({});

  // Load user from JWT
  useEffect(() => {
    const token = getToken();
    const parsed = parseJwt(token);
    setUser(parsed || {});
  }, []);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const displayName = user?.name || user?.email || "Account";
  const initials = displayName
    .split(" ")
    .map((w: string) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div ref={ref} className="relative">
      {/* Trigger */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100 transition"
      >
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-900 text-white text-xs font-semibold">
          {initials}
        </div>
        <span className="hidden sm:block">{displayName}</span>
        <span className="text-xs">▾</span>
      </button>

      {/* Dropdown */}
      {open && (
        <div
          className="
            absolute right-0 mt-2 w-52 rounded-xl border bg-white shadow-lg
            animate-in fade-in slide-in-from-top-2
          "
        >
          {/* Header */}
          <div className="px-4 py-3 border-b">
            <div className="font-semibold text-slate-900">{displayName}</div>
            {user?.email && (
              <div className="text-xs text-slate-500">{user.email}</div>
            )}
          </div>

          {/* Actions */}
          <button
            className="w-full text-left px-4 py-2 text-sm hover:bg-slate-100 transition"
            onClick={() => {
              setOpen(false);
              router.push("/profile");
            }}
          >
            Profile
          </button>

          <button
            className="w-full text-left px-4 py-2 text-sm hover:bg-slate-100 transition"
            onClick={() => {
              setOpen(false);
              router.push("/settings");
            }}
          >
            Settings
          </button>

          <div className="border-t my-1" />

          <button
            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
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
