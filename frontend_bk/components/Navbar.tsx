"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import ProfileMenu from "@/components/ProfileMenu";

export default function Navbar() {
  const router = useRouter();
  const isLoggedIn = !!getToken();

  return (
    <nav className="border-b px-6 py-3 flex items-center justify-between">
      {/* Left */}
      <div className="flex items-center gap-6">
        <Link href="/" className="font-bold text-lg">
          PaperTrade AI
        </Link>

        {isLoggedIn && (
          <>
            <Link href="/trades">Trades</Link>
            <Link href="/analytics">Analytics</Link>
            <Link href="/chat">AI Chat</Link>
            <Link href="/reports">Reports</Link>
          </>
        )}
      </div>

      {/* Right */}
      <div className="flex gap-4 items-center">
        {!isLoggedIn ? (
          <>
            <Link href="/login">Login</Link>
            <Link href="/register">Register</Link>
          </>
        ) : (
          <ProfileMenu />
        )}
      </div>
    </nav>
  );
}
