
// ne

interface ChatMessageProps {
  type: "user" | "assistant";
  content: string;
}

export function ChatMessage({ type, content }: ChatMessageProps) {
  if (type === "assistant") {
    return (
      <div className="flex gap-3">
        <div className="w-8 h-8 flex-shrink-0 rounded-full bg-gradient-to-br from-teal-400 to-cyan-400 flex items-center justify-center text-white font-bold text-sm">
          A
        </div>
        <div className="flex-1 text-sm text-gray-700 leading-relaxed">
          {content.split("\n").map((line, i) => {
            const isHighlighted =
              line.includes("feature timestamp") ||
              line.includes("features under") ||
              line.includes("1s, and");

            return (
              <div key={i} className="mb-1">
                {isHighlighted ? (
                  <span className="text-red-500 font-medium">{line}</span>
                ) : (
                  <span>{line}</span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-3 justify-end">
      <div className="max-w-xs bg-blue-600 text-white rounded-lg p-3 text-sm leading-relaxed">
        {content}
      </div>
    </div>
  );
}
