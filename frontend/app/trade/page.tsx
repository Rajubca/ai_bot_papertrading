import TradeForm from "@/components/TradeForm";

export default function TradePage() {
  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">New Trade</h1>
        <p className="text-muted-foreground text-gray-500">
          Execute manual trades in the market.
        </p>
      </div>
      <TradeForm />
    </div>
  );
}
