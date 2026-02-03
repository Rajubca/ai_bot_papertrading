"use client";

import RequireAuth from "@/components/RequireAuth";

export default function SettingsPage() {
  return (
    <RequireAuth>
      <h1 className="text-2xl font-bold">Settings</h1>
      <p>Preferences and risk settings go here.</p>
    </RequireAuth>
  );
}
