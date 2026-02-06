"use client";

import RequireAuth from "@/components/RequireAuth";
import TradeForm from "@/components/TradeForm";

export default function TradesPage() {
  return (
    <RequireAuth>
      <div className="max-w-3xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-slate-900">
          Place Trade
        </h1>
        <TradeForm />
      </div>
    </RequireAuth>
  );
}
