"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { logout } from "@/lib/auth";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/trade", label: "Trade" },
  { href: "/portfolio", label: "Portfolio" },
  { href: "/analytics", label: "Analytics" },
  { href: "/chat", label: "Agent" },
];

export default function Navbar() {
  const pathname = usePathname();

  // Don't show navbar on login page
  if (pathname === "/login") return null;

  return (
    <nav className="border-b bg-white dark:bg-slate-900 dark:border-slate-800">
      <div className="flex items-center justify-between h-16 px-4 max-w-7xl mx-auto">
        <div className="flex items-center">
          <Link href="/" className="text-xl font-bold mr-8">
            AI Trader
          </Link>
          <div className="hidden md:flex space-x-4">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  pathname === link.href
                    ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800"
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
        <div>
          <Button variant="ghost" onClick={logout} className="text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10">
            Logout
          </Button>
        </div>
      </div>
    </nav>
  );
}
