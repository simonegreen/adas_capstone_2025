"use client";

import { useRouter } from "next/navigation";
import { Send, Paperclip } from "lucide-react";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  disabled?: boolean;
}

export function ChatInput({ value = "", onChange, onSubmit, disabled = false }: ChatInputProps) {
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
          placeholder={disabled ? "Waiting for response..." : "Message..."}
          disabled={disabled}
          className="flex-1 px-4 py-3 bg-gray-100 rounded-lg border border-gray-200
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
            text-gray-900 placeholder-gray-500 font-normal disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="button"
          onClick={handleButtonClick}
          disabled={disabled}
          className="p-3 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Paperclip size={18} className="text-gray-600" />
        </button>
        <button
          type="submit"
          disabled={disabled}
          className="p-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          <Send size={18} className="text-white" />
        </button>
      </form>
    </div>
  );
}
