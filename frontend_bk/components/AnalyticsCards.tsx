"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function AnalyticsCards() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch("/api/analytics")
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="text-red-600">Analytics error: {error}</div>;
  if (!data) return <div>Loading analytics…</div>;

  return (
    <div className="grid grid-cols-4 gap-4">
      <Card title="Total Trades" value={data.total_trades} />
      <Card title="Win Rate (%)" value={data.win_rate} />
      <Card title="Expectancy" value={data.expectancy} />
      <Card title="Max Win Streak" value={data.max_win_streak} />
    </div>
  );
}

function Card({ title, value }: { title: string; value: any }) {
  return (
    <div className="border rounded p-4">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}
