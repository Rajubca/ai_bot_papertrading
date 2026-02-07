"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

const SYMBOLS = ["RELIANCE", "TCS", "INFY"];

export default function PriceTicker() {
  const [prices, setPrices] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPrices() {
      setLoading(true);
      const results: Record<string, any> = {};

      for (const symbol of SYMBOLS) {
        try {
          // Calls your FastAPI backend which now uses the 0xramm API logic
          const res = await apiFetch(`/api/market/quote?symbol=${symbol}`);
          results[symbol] = res;
        } catch (error) {
          console.error(`Error fetching ${symbol}:`, error);
          // Fallback state if the API fetch fails completely
          results[symbol] = { ltp: null, is_stale: true, status: "error" };
        }
      }

      setPrices(results);
      setLoading(false);
    }

    fetchPrices();
    
    // Optional: Refresh every 5 minutes to match your backend CACHE_EXPIRY
    const interval = setInterval(fetchPrices, 300000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex gap-4 p-4 bg-gray-50 animate-pulse rounded-lg">
        <div className="text-sm text-gray-500">Loading Indian market prices...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-6 border rounded-lg p-4 bg-white shadow-sm">
      {SYMBOLS.map((symbol) => {
        const data = prices[symbol];
        const isStale = data?.is_stale || data?.status === "stale";

        return (
          <div key={symbol} className="min-w-[120px] space-y-1">
            <div className="flex justify-between items-center">
              <span className="font-bold text-gray-700">{symbol}</span>
              {isStale && (
                <span className="text-[10px] font-bold bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded uppercase">
                  Delayed
                </span>
              )}
            </div>

            <div className={`text-xl font-semibold ${isStale ? "text-gray-500" : "text-black"}`}>
              {data?.ltp !== null ? `₹${data.ltp}` : "---"}
            </div>

            {data?.last_updated && (
              <div className="text-[10px] text-gray-400">
                Last: {new Date(data.last_updated * 1000).toLocaleTimeString()}
              </div>
            )}
            
            {!data?.ltp && data?.status === "error" && (
              <div className="text-[10px] text-red-500">
                Data temporarily unavailable
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}