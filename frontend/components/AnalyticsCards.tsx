"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function AnalyticsCards() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    apiFetch("/api/analytics").then(setStats);
  }, []);

  if (!stats) return null;

  return (
    <div className="grid grid-cols-4 gap-4">
      <div>Win Rate: {stats.win_rate}%</div>
      <div>Expectancy: ₹{stats.expectancy}</div>
      <div>Max Win Streak: {stats.max_win_streak}</div>
      <div>Max Loss Streak: {stats.max_loss_streak}</div>
    </div>
  );
}
