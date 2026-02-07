"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import ProfileMenu from "@/components/ProfileMenu";

export default function Navbar() {
  const pathname = usePathname();
  const isLoggedIn = !!getToken();

  const linkClass = (path: string) =>
    `text-sm font-medium transition ${
      pathname === path
        ? "text-slate-900"
        : "text-slate-500 hover:text-slate-900"
    }`;

  return (
    <header className="border-b bg-white">
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
        {/* Left */}
        <div className="flex items-center gap-8">
          <Link href="/" className="text-xl font-bold text-slate-900">
            PaperTrade<span className="text-slate-500">AI</span>
          </Link>

          {isLoggedIn && (
            <nav className="flex items-center gap-6">
              <Link href="/portfolio" className={linkClass("/portfolio")}>
                Portfolio
              </Link>
              <Link href="/trades" className={linkClass("/trades")}>
                Trades
              </Link>
              <Link href="/analytics" className={linkClass("/analytics")}>
                Analytics
              </Link>
              <Link href="/chat" className={linkClass("/chat")}>
                AI Assistant
              </Link>
              <Link href="/reports" className={linkClass("/reports")}>
                Reports
              </Link>
            </nav>
          )}
        </div>

        {/* Right */}
        <div className="flex items-center gap-4">
          {!isLoggedIn ? (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-slate-600 hover:text-slate-900"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="rounded-lg bg-slate-900 text-white px-4 py-1.5 text-sm font-medium hover:bg-slate-800 transition"
              >
                Get Started
              </Link>
            </>
          ) : (
            <ProfileMenu />
          )}
        </div>
      </div>
    </header>
  );
}
