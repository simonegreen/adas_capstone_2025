// ne

import { QueryCard } from "./QueryCard";
import { ChatInput } from "./ChatInput";

interface WelcomePanelProps {
  panelWidth: number;
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
  panelWidth,
  onQuerySelect,
  inputValue,
  onInputChange,
  onInputSubmit,
}: WelcomePanelProps) {
  return (
    <div
      style={{ width: `${panelWidth}%` }}
      className="bg-gray-50 flex flex-col overflow-hidden transition-none"
    >
      {/* Welcome State */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 overflow-y-auto">
        {/* Mascot Icon */}
        <div className="w-40 h-40 bg-gradient-to-br from-teal-400 to-cyan-400 rounded-3xl flex items-center justify-center mb-8 flex-shrink-0">
          <svg
            viewBox="0 0 120 120"
            className="w-full h-full text-white p-4"
            fill="currentColor"
          >
            <circle cx="60" cy="45" r="22" />
            <circle cx="52" cy="38" r="4" fill="white" />
            <circle cx="68" cy="38" r="4" fill="white" />
            <path
              d="M 52 52 Q 60 58 68 52"
              stroke="white"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
            />
            <rect x="45" y="70" width="30" height="40" rx="4" />
            <circle cx="53" cy="85" r="3" fill="white" />
            <circle cx="67" cy="85" r="3" fill="white" />
          </svg>
        </div>

        {/* Title and Description */}
        <h2 className="text-2xl font-semibold text-gray-900 mb-3 text-center">
          ADaS
        </h2>
        <p className="text-gray-600 text-center mb-8 max-w-sm text-sm leading-relaxed">
          I'm your cybersecurity analyst ready to identify the anomalies and
          save your time.
        </p>

        {/* Example Queries */}
        <div className="space-y-3 w-full max-w-sm">
          {EXAMPLE_QUERIES.map((query, index) => (
            <QueryCard
              key={index}
              text={query}
              onClick={onQuerySelect}
            />
          ))}
        </div>
      </div>

      {/* Chat Input */}
      <ChatInput
        value={inputValue}
        onChange={onInputChange}
        onSubmit={onInputSubmit}
      />
    </div>
  );
}
