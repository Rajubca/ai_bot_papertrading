export default function ReportsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
        <p className="text-muted-foreground text-gray-500">
          View and download your trading reports.
        </p>
      </div>
      <div className="p-4 border rounded-md bg-white dark:bg-slate-800">
        <p>No reports available yet.</p>
      </div>
    </div>
  );
}
