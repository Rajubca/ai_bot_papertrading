"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function ChatPanel() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState<{ role: string; text: string }[]>([]);

  async function send() {
    if (!input) return;
    setChat((c) => [...c, { role: "You", text: input }]);
    setInput("");

    try {
      const res = await apiFetch("/api/agent/chat", {
        method: "POST",
        body: JSON.stringify({ message: input }),
      });
      setChat((c) => [...c, { role: "AI", text: res.summary ?? JSON.stringify(res) }]);
    } catch (e: any) {
      setChat((c) => [...c, { role: "AI", text: e.message }]);
    }
  }

  return (
    <div className="border rounded p-4 space-y-3">
      <h2 className="font-semibold">AI Assistant</h2>

      <div className="h-40 overflow-auto border p-2">
        {chat.map((m, i) => (
          <div key={i}>
            <b>{m.role}:</b> {m.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Ask about performance, risk…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="border px-3" onClick={send}>
          Send
        </button>
      </div>
    </div>
  );
}
