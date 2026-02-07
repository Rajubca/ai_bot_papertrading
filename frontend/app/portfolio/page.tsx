"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function PortfolioPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function load() {
      const res = await apiFetch("/api/portfolio/");
      setData(res);
    }

    load();
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div className="p-6 space-y-4">

      <h1 className="text-2xl font-bold">Portfolio</h1>

      <div className="text-lg">
        Balance: ₹{data.balance}
      </div>

      <table className="w-full border mt-4">
        <thead>
          <tr className="bg-gray-100">
            <th>Symbol</th>
            <th>Qty</th>
            <th>Avg Price</th>
          </tr>
        </thead>

        <tbody>
          {data.positions.map((p: any) => (
            <tr key={p.symbol} className="text-center border-t">
              <td>{p.symbol}</td>
              <td
                className={
                  p.quantity < 0 ? "text-red-600" : "text-green-600"
                }
              >
                {p.quantity}
              </td>
              <td>₹{p.avg_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
