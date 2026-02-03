"use client";

import AnalyticsCards from "@/components/AnalyticsCards";
import PortfolioTable from "@/components/PortfolioTable";
import { useEffect, useState } from "react";
import { getCurrentUser } from "@/lib/auth";

export default function Dashboard() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    getCurrentUser().then(setUser);
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground text-gray-500">
          Welcome back, {user?.name || "Trader"}. Here is your overview.
        </p>
      </div>

      <AnalyticsCards />

      <PortfolioTable />
    </div>
  );
}
