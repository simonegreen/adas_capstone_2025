"use client";

import { useRouter } from "next/navigation";
import { Send, Paperclip } from "lucide-react";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function ChatInput({ value = "", onChange, onSubmit }: ChatInputProps) {
  const router = useRouter();
  const handleButtonClick = () => {
    router.push("/");
  };

  return (
    <div className="border-t border-gray-200 bg-gray-50 p-6 flex-shrink-0">
      <form onSubmit={onSubmit} className="flex gap-3">
        <input
          type="text"
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Message..."
          className="flex-1 px-4 py-3 bg-gray-100 rounded-lg border border-gray-200
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
            text-gray-900 placeholder-gray-500 font-normal"
        />
        <button
          type="button"
          onClick={handleButtonClick}
          className="p-3 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Paperclip size={18} className="text-gray-600" />
        </button>
        <button
          type="submit"
          className="p-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
        >
          <Send size={18} className="text-white" />
        </button>
      </form>
    </div>
  );
}
