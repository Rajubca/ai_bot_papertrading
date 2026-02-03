"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function PriceTicker({ symbol }: { symbol: string }) {
  const [price, setPrice] = useState<number | null>(null);

  useEffect(() => {
    if (!symbol) return;

    // Initial fetch
    apiFetch(`/api/market/quote?symbol=${symbol}`).then(d => setPrice(d.ltp)).catch(() => {});

    const interval = setInterval(async () => {
      try {
        const data = await apiFetch(`/api/market/quote?symbol=${symbol}`);
        setPrice(data.ltp);
      } catch (e) {
        // Ignore errors for ticker
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [symbol]);

  return (
    <div className="text-xl font-mono font-bold text-slate-800 dark:text-slate-200">
      {symbol}: <span className={price ? "text-blue-600" : "text-gray-400"}>₹{price ?? "..."}</span>
    </div>
  );
}
