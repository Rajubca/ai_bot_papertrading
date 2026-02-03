"use client";

import RequireAuth from "@/components/RequireAuth";

export default function ProfilePage() {
  return (
    <RequireAuth>
      <h1 className="text-2xl font-bold">Profile</h1>
      <p>User profile details will appear here.</p>
    </RequireAuth>
  );
}
