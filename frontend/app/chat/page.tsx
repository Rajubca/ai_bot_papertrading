import ChatPanel from "@/components/ChatPanel";

export default function ChatPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Agent</h1>
        <p className="text-muted-foreground text-gray-500">
          Chat with your AI trading assistant for insights.
        </p>
      </div>
      <ChatPanel />
    </div>
  );
}
