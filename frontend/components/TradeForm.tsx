"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function TradeForm() {
  const [form, setForm] = useState({
    symbol: "",
    side: "BUY",
    quantity: 1,
    trade_notes: "",
  });
  const [loading, setLoading] = useState(false);

  async function submitTrade() {
    setLoading(true);
    try {
      await apiFetch("/api/trade", {
        method: "POST",
        body: JSON.stringify(form),
      });
      alert("Trade placed successfully");
      setForm({ ...form, symbol: "", quantity: 1, trade_notes: "" });
    } catch (e: any) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Place Order</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-1 block">Symbol</label>
          <Input
            placeholder="e.g. RELIANCE"
            value={form.symbol}
            onChange={e => setForm({...form, symbol: e.target.value.toUpperCase()})}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Side</label>
            <select
              className="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 dark:bg-slate-950 dark:border-slate-800"
              value={form.side}
              onChange={e => setForm({...form, side: e.target.value})}
            >
              <option value="BUY">BUY</option>
              <option value="SELL">SELL</option>
            </select>
          </div>
          <div>
             <label className="text-sm font-medium mb-1 block">Quantity</label>
             <Input
               type="number"
               min="1"
               value={form.quantity}
               onChange={e => setForm({...form, quantity: +e.target.value})}
             />
          </div>
        </div>

        <div>
           <label className="text-sm font-medium mb-1 block">Notes (Strategy)</label>
           <textarea
             className="flex min-h-[80px] w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 dark:bg-slate-950 dark:border-slate-800"
             placeholder="Why are you taking this trade?"
             value={form.trade_notes}
             onChange={e => setForm({...form, trade_notes: e.target.value})}
           />
        </div>

        <Button
          onClick={submitTrade}
          disabled={loading}
          className={`w-full ${form.side === 'BUY' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}
        >
          {loading ? "Executing..." : `${form.side} ${form.symbol || "Stock"}`}
        </Button>
      </CardContent>
    </Card>
  );
}
