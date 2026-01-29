"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function ChatPanel() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");

  async function send() {
    const res = await apiFetch("/api/agent/chat", {
      method: "POST",
      body: JSON.stringify({ message: input }),
    });

    setMessages([...messages, { role: "user", text: input }, { role: "agent", text: res.summary }]);
    setInput("");
  }

  return (
    <div>
      {messages.map((m, i) => <div key={i}>{m.role}: {m.text}</div>)}
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={send}>Ask AI</button>
    </div>
  );
}
