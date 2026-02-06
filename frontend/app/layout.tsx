"use client"; // We need this to check localStorage
import "./globals.css";
import Navbar from "@/components/Navbar";
import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { getToken } from "@/lib/auth";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    const token = getToken();
    const isPublicPage =
      pathname === "/login" || pathname === "/register";

    if (!token && !isPublicPage) {
      router.push("/login");
    } else {
      setAuthorized(true);
    }
  }, [pathname, router]);

  // Prevent flickering while checking auth
  if (!authorized && pathname !== "/login" && pathname !== "/register") {
    return (
      <html lang="en">
        <body className="bg-slate-900 flex items-center justify-center min-h-screen">
          <div className="text-white">
            Loading session...
          </div>
        </body>
      </html>
    );
  }

  return (
    <html lang="en">
      <body className="bg-slate-50 flex flex-col min-h-screen">
        <Navbar />

        {/* Main Content */}
        <main className="flex-1 p-6">
          {children}
        </main>

        {/* Global Disclaimer */}
        <footer className="border-t bg-white">
          <p className="text-xs text-slate-500 text-center py-4 px-4">
            Prices are sourced from Yahoo Finance and may be delayed or stale.
            This platform is for educational paper trading purposes only.
            No real trades are executed.
          </p>
        </footer>
      </body>
    </html>
  );
}
