"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface Position {
  symbol: string;
  net_quantity: number;
  avg_price: number;
  unrealized_pnl: number;
}

export default function PortfolioTable() {
  const [positions, setPositions] = useState<Position[]>([]);
  const [balance, setBalance] = useState(0);

  async function fetchPortfolio() {
    try {
      const data = await apiFetch("/api/portfolio");
      setPositions(data.positions);
      setBalance(data.balance);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    fetchPortfolio();
    const interval = setInterval(fetchPortfolio, 5000); // Polling update
    return () => clearInterval(interval);
  }, []);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Open Positions</CardTitle>
        <div className="text-lg font-semibold text-green-600">
            Balance: ₹{balance.toLocaleString()}
        </div>
      </CardHeader>
      <CardContent>
        {positions.length === 0 ? (
          <div className="text-center text-gray-500 py-8">No open positions</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Symbol</TableHead>
                <TableHead>Qty</TableHead>
                <TableHead>Avg Price</TableHead>
                <TableHead>P&L</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {positions.map((p) => (
                <TableRow key={p.symbol}>
                  <TableCell className="font-medium">{p.symbol}</TableCell>
                  <TableCell>{p.net_quantity}</TableCell>
                  <TableCell>₹{p.avg_price.toFixed(2)}</TableCell>
                  <TableCell className={p.unrealized_pnl >= 0 ? "text-green-600" : "text-red-600"}>
                    ₹{p.unrealized_pnl.toFixed(2)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
