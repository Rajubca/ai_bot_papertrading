"use client";

import AnalyticsCards from "@/components/AnalyticsCards";
import TradeForm from "@/components/TradeForm";
import ChatPanel from "@/components/ChatPanel";
import { logout } from "@/lib/auth";
import PriceTicker from "@/components/PriceTicker";

export default function Page() {
  return (
    <div className="p-6 space-y-6">
      <PriceTicker />
      <AnalyticsCards />
      <TradeForm />
      <ChatPanel />

      <button
        onClick={() => {
          logout();
          window.location.href = "/login";
        }}
        className="rounded-lg bg-red-600 text-white px-4 py-2"
      >
        Logout
      </button>
    </div>
  );
}
