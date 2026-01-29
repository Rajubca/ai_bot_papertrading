"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function TradeForm() {
  const [form, setForm] = useState({
    symbol: "",
    side: "BUY",
    quantity: 1,
    trade_notes: "",
  });

  async function submitTrade() {
    await apiFetch("/api/trade", {
      method: "POST",
      body: JSON.stringify(form),
    });
    alert("Trade placed");
  }

  return (
    <div>
      <input placeholder="Symbol" onChange={e => setForm({...form, symbol: e.target.value})} />
      <select onChange={e => setForm({...form, side: e.target.value})}>
        <option>BUY</option>
        <option>SELL</option>
      </select>
      <input type="number" onChange={e => setForm({...form, quantity: +e.target.value})} />
      <textarea placeholder="Trade Notes" onChange={e => setForm({...form, trade_notes: e.target.value})} />
      <button onClick={submitTrade}>Execute</button>
    </div>
  );
}
