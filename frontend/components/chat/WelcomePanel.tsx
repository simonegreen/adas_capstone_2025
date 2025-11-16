// Right panel 
import { ChatMessage } from "./ChatMessage";
import { QueryCard } from "./QueryCard";
import { ChatInput } from "./ChatInput";
import { Actor } from "next/font/google";
const actor = Actor({ subsets: ["latin"], weight: "400" });

import Image from "next/image";

interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
}

interface WelcomePanelProps {
  messages: Message[];
  // panelWidth: number;
  onQuerySelect: (text: string) => void;
  inputValue: string;
  onInputChange: (value: string) => void;
  onInputSubmit: (e: React.FormEvent) => void;
}

const EXAMPLE_QUERIES = [
  "Tell me the IP address of the top anomalies in the dataset.",
  "What are the anomalies in the past week?",
  "Why was the event associated with IP address x anomalous?",
];

export function WelcomePanel({
  messages,
  // panelWidth,
  onQuerySelect,
  inputValue,
  onInputChange,
  onInputSubmit,
}: WelcomePanelProps) {
  // Check if user has started chatting
  const hasUserMessage = messages.some((m) => m.type === "user");

  // Once the user has spoken, show the entire conversation (user + assistant).
  const userInitiatedMessages = messages.slice(3);

  const messagesArea = userInitiatedMessages.length === 0 ? (
    <div className="flex-1 flex flex-col items-center justify-center p-8 overflow-y-auto">
      {/* Mascot Icon */}
      <div className="self-center pt-[2px] shrink-0 h-36 w-24 grid place-items-center rounded-full">
        <Image
          src={"/bot.png"}
          width={150}
          height={150}
          className="object-contain"
          priority={false}
        />
      </div>

      {/* Title and Description */}
      <h2 className="text-3xl font-semibold text-gray-900 mb-3 text-center ">
        ADaS
      </h2>
      <p className="text-gray-600 text-center mb-8 max-w-sm leading-[28px] text-[18px]">
        I'm your cybersecurity analyst ready to identify the anomalies and
        save your time.
      </p>

      {/* Example Queries */}
      <div className="space-y-3 w-full max-w-sm">
        {EXAMPLE_QUERIES.map((query, index) => (
          <QueryCard key={index} text={query} onClick={onQuerySelect} />
        ))}
      </div>
    </div>
  ) : (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {userInitiatedMessages.map((message) => (
        <ChatMessage
          key={message.id}
          type={message.type}
          content={message.content}
        />
      ))}
    </div>
  );

  return (
    <div
      style={{ width: `${panelWidth}%` }}
      className={`${actor.className} text-[16px] leading-[26px] font-normal bg-gray-50 flex flex-col overflow-hidden transition-none`}
    >
      {messagesArea}
      {/* Chat Input (always visible) */}
      <ChatInput
        value={inputValue}
        onChange={onInputChange}
        onSubmit={onInputSubmit}
      />
    </div>
  );
}
