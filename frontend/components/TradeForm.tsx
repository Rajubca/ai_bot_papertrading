"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

const SYMBOLS = [
  "RELIANCE",
  "TCS",
  "INFY",
  "HDFCBANK",
  "ICICIBANK",
];

export default function TradeForm() {
  const [symbol, setSymbol] = useState("RELIANCE");
  const [side, setSide] = useState<"BUY" | "SELL">("BUY");
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState("");

  // price states
  const [price, setPrice] = useState<number | null>(null);
  const [loadingPrice, setLoadingPrice] = useState(false);
  const [stale, setStale] = useState(false);

  // order states
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // ----------------------------
  // FETCH MARKET PRICE
  // ----------------------------
  useEffect(() => {
    async function fetchPrice() {
      setLoadingPrice(true);
      setPrice(null);
      setStale(false);
      setError(null);

      try {
        const res = await apiFetch(
          `/api/market/quote?symbol=${symbol}`
        );

        setPrice(res.ltp ?? null);
        setStale(Boolean(res.stale));
      } catch {
        setPrice(null);
        setStale(true);
      } finally {
        setLoadingPrice(false);
      }
    }

    fetchPrice();
  }, [symbol]);

  // ----------------------------
  // PLACE TRADE
  // ----------------------------
  async function placeTrade() {
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      const res = await apiFetch("/api/trade/execute", {
        method: "POST",
        body: JSON.stringify({
          symbol,
          side,
          quantity,
          trade_notes: notes,
        }),
      });

      setSuccess(
        `${side} ${quantity} ${symbol} @ ₹${res.executed_price}`
      );
      setNotes("");
    } catch (e: any) {
      setError(e.message || "Trade failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm space-y-5">
      {/* SYMBOL */}
      <div>
        <label className="block text-sm font-medium mb-1">
          Symbol
        </label>
        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        >
          {SYMBOLS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      {/* PRICE */}
      <div className="flex justify-between items-center">
        <span className="text-sm text-slate-500">
          Market Price
        </span>

        <div className="text-right">
          {loadingPrice && (
            <span className="text-sm text-slate-400">
              Loading…
            </span>
          )}

          {!loadingPrice && price !== null && (
            <span className="font-semibold text-lg">
              ₹{price}
            </span>
          )}

          {!loadingPrice && price === null && (
            <span className="text-orange-600 text-sm">
              Using last known price
            </span>
          )}


          {stale && (
            <div className="text-xs text-orange-500">
              Delayed / stale price
            </div>
          )}
        </div>
      </div>

      {/* BUY / SELL */}
      <div className="flex gap-4">
        {(["BUY", "SELL"] as const).map((s) => (
          <button
            key={s}
            onClick={() => setSide(s)}
            className={`flex-1 rounded-lg py-2 font-medium transition ${
              side === s
                ? s === "BUY"
                  ? "bg-green-600 text-white"
                  : "bg-red-600 text-white"
                : "border"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* QUANTITY */}
      <div>
        <label className="block text-sm font-medium mb-1">
          Quantity
        </label>
        <input
          type="number"
          min={1}
          value={quantity}
          onChange={(e) =>
            setQuantity(Math.max(1, Number(e.target.value)))
          }
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      {/* NOTES */}
      <div>
        <label className="block text-sm font-medium mb-1">
          Trade Notes
        </label>
        <textarea
          rows={2}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
          placeholder="Optional"
        />
      </div>

      {/* ORDER VALUE */}
      {price !== null && (
        <div className="flex justify-between text-sm text-slate-600">
          <span>Order Value</span>
          <span>
            ₹{(price * quantity).toFixed(2)}
          </span>
        </div>
      )}

      {/* ERROR */}
      {error && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* SUCCESS */}
      {success && (
        <div className="rounded-lg bg-green-50 border border-green-200 px-4 py-2 text-green-700 text-sm">
          {success}
        </div>
      )}

      {/* SUBMIT */}
      <button
        onClick={placeTrade}
        disabled={submitting || loadingPrice}
        className="w-full rounded-lg bg-slate-900 text-white py-2.5 font-medium hover:bg-slate-800 transition disabled:opacity-50"
      >
        {submitting ? "Placing Order…" : "Place Order"}
      </button>
    </div>
  );
}
