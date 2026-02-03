"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function AnalyticsCards() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    // This will work once we fix the backend router in step 6
    apiFetch("/api/analytics")
      .then(setStats)
      .catch(err => console.error("Failed to fetch analytics", err));
  }, []);

  if (!stats) return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 animate-pulse">
        {[1,2,3,4].map(i => <div key={i} className="h-32 bg-gray-200 rounded-lg dark:bg-gray-800"></div>)}
    </div>
  );

  const items = [
    { label: "Win Rate", value: `${stats.win_rate || 0}%`, color: "text-blue-600" },
    { label: "Expectancy", value: `₹${stats.expectancy || 0}`, color: "text-green-600" },
    { label: "Max Win Streak", value: stats.max_win_streak || 0, color: "text-indigo-600" },
    { label: "Max Loss Streak", value: stats.max_loss_streak || 0, color: "text-red-600" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {items.map((item) => (
        <Card key={item.label}>
          <CardContent className="pt-6">
             <div className="text-sm font-medium text-gray-500">{item.label}</div>
             <div className={`text-3xl font-bold ${item.color}`}>{item.value}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
