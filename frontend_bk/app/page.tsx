"use client";

import { useEffect } from "react";
import { getToken } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { logout } from "@/lib/auth";
import AnalyticsCards from "@/components/AnalyticsCards";
import TradeForm from "@/components/TradeForm";
import ChatPanel from "@/components/ChatPanel";

export default function Page() {
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
    }
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">AI Paper Trading Dashboard</h1>

      <AnalyticsCards />
      <TradeForm />
      <ChatPanel />
    </div>
    <button onClick={() => { logout(); location.href = "/login"; }}>
        Logout
    </button>
  );
}
