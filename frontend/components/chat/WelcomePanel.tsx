// Right panel 
import { ChatMessage } from "./ChatMessage";
import { QueryCard } from "./QueryCard";
import { ChatInput } from "./ChatInput";
import { Actor } from "next/font/google";
const actor = Actor({ subsets: ["latin"], weight: "400" });

import Image from "next/image";

interface TableData {
  cols: string[];
  rows: any[][];
}

interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
  tableData?: TableData | null;

}

interface WelcomePanelProps {
  messages: Message[];
  panelWidth: number;
  onQuerySelect: (text: string) => void;
  inputValue: string;
  onInputChange: (value: string) => void;
  onInputSubmit: (e: React.FormEvent) => void;
  isLoading?: boolean;
}

const EXAMPLE_QUERIES = [
  "Tell me the IP address of the top anomalies in the dataset.",
  "What are the anomalies in the past week?",
  "Why was the event associated with IP address x anomalous?",
];

export function WelcomePanel({
  messages,
  panelWidth,
  onQuerySelect,
  inputValue,
  onInputChange,
  onInputSubmit,
  isLoading = false,
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
          alt="ADaS bot"
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
        <div key={message.id} className="space-y-2">
          <ChatMessage
            key={message.id}
            type={message.type}
            content={message.content}
          />
      {/* Pretty scrollable table, only when tableData is present */}
          {message.type === "assistant" && message.tableData && (
            <div className="ml-14"> 
              {/* small indent so it visually groups with the assistant bubble;
                  tweak/remove ml-14 depending on how ChatMessage lays out */}
              <div className="mt-1 max-h-80 overflow-auto rounded-lg border border-gray-200 bg-white shadow-sm">
                <table className="min-w-full text-xs">
                  <thead className="sticky top-0 bg-gray-50">
                    <tr>
                      {message.tableData.cols.map((col) => (
                        <th
                          key={col}
                          className="px-3 py-2 text-left font-semibold border-b border-gray-200"
                        >
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {message.tableData.rows.map((row, idx) => (
                      <tr key={idx} className="odd:bg-white even:bg-gray-50">
                        {row.map((cell, cIdx) => (
                          <td
                            key={cIdx}
                            className="px-3 py-1 border-b border-gray-100 align-top"
                          >
                            {String(cell)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      ))}
      {isLoading && (
        <div className="flex gap-3">
          <div className="w-12 h-12 flex-shrink-0 rounded-full bg-gradient-to-br from-teal-400 to-cyan-400 flex items-center justify-center text-white font-bold">
            A
          </div>
          <div className="flex-1 text-gray-600 italic">Analyzing your dataset...</div>
        </div>
      )}
    </div>
  );

  const widthStyle =
    typeof panelWidth === "number" ? { width: `${panelWidth}%` } : undefined;
  
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
        disabled={isLoading}
      />
    </div>
  );
}
