import PortfolioTable from "@/components/PortfolioTable";

export default function PortfolioPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Portfolio</h1>
        <p className="text-muted-foreground text-gray-500">
          View your open positions and current balance.
        </p>
      </div>
      <PortfolioTable />
    </div>
  );
}
