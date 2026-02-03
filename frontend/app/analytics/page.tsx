import AnalyticsCards from "@/components/AnalyticsCards";

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
        <p className="text-muted-foreground text-gray-500">
          Detailed performance metrics of your trading strategy.
        </p>
      </div>
      <AnalyticsCards />
      {/* Future: Add Charts here */}
    </div>
  );
}
