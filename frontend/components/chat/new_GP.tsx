// ne

import { ChatMessage } from "./ChatMessage";

interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
}

interface GuidelinesPanelProps {
  messages: Message[];
  panelWidth: number;
}

export function GuidelinesPanel({ messages, panelWidth }: GuidelinesPanelProps) {
  return (
    <div
      style={{ width: `${panelWidth}%` }}
      className="border-r border-gray-200 bg-white flex flex-col overflow-hidden transition-none"
    >
      {/* Section Title */}
      <div className="px-6 py-4 border-b border-gray-200 bg-white flex-shrink-0">
        <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          ADaS User Guidelines
        </p>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            type={message.type}
            content={message.content}
          />
        ))}
      </div>
    </div>
  );
}
