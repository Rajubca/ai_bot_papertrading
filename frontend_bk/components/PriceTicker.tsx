"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function PriceTicker({ symbol }: { symbol: string }) {
  const [price, setPrice] = useState<number | null>(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await apiFetch(`/api/market/quote?symbol=${symbol}`);
      setPrice(data.ltp);
    }, 5000);

    return () => clearInterval(interval);
  }, [symbol]);

  return <span>{symbol}: ₹{price ?? "..."}</span>;
}
