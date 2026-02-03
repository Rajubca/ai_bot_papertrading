"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function TradeForm() {
  const [symbol, setSymbol] = useState("");
  const [side, setSide] = useState("BUY");
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  async function submit() {
    setMsg(null);
    try {
      const res = await apiFetch("/api/trade", {
        method: "POST",
        body: JSON.stringify({
          symbol,
          side,
          quantity,
          trade_notes: notes,
        }),
      });
      setMsg(`Trade success @ ${res.executed_price}`);
    } catch (e: any) {
      setMsg(e.message);
    }
  }

  return (
    <div className="border rounded p-4 space-y-3">
      <h2 className="font-semibold">Place Trade</h2>

      <div className="flex gap-2">
        <input
          className="border p-2"
          placeholder="Symbol (RELIANCE)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <select
          className="border p-2"
          value={side}
          onChange={(e) => setSide(e.target.value)}
        >
          <option>BUY</option>
          <option>SELL</option>
        </select>
        <input
          className="border p-2 w-24"
          type="number"
          min={1}
          value={quantity}
          onChange={(e) => setQuantity(+e.target.value)}
        />
      </div>

      <textarea
        className="border p-2 w-full"
        placeholder="Trade notes"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />

      <button className="border px-4 py-2" onClick={submit}>
        Execute
      </button>

      {msg && <div className="text-sm">{msg}</div>}
    </div>
  );
}
