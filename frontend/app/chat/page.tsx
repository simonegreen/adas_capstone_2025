"use client";

import TopBanner from "@/components/layout/TopBanner";
import QueryGuideline from "@/components/chat/QueryGuidelinePanel";
import { DraftLeft } from "@/components/chat/DraftLeft";
import { DraggableDivider } from "@/components/chat/DraggableDivider";
import { WelcomePanel } from "@/components/chat/WelcomePanel";
import { useEffect, useRef, useState } from "react";

export const dynamic = "force-dynamic";
interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
}

const defaultMessages: Message[] = [
  {
    id: "1",
    type: "assistant",
    content:
      "Hi, thanks for uploading the dataset to ADaS. Ask me about:\n• Time range\n• Top n anomalies (n is the number of anomalies)\n• Number of features used to identify anomalies.\n  - For example, 6, 8, 10 features. We recommend you to start with 10 features for optimal result. Note, ADaS will run the experiment if you ask it to run with a different number of features. For example, asking 12 features running with 10 features.\n• Explanation\n  You can ask to provide context associated with IP address x",
  },
  {
    id: "2",
    type: "assistant",
    content:
      'You should not query like these bad examples:\n• "Tell me what are the anomalies under feature timestamp"\n  Instead, specify the number of features.\n• "I want to know the output with 10, 1s, and 5s features."\n  Instead, try query with features first, save the result. Query with 12 features.',
  },
  {
    id: "3",
    type: "assistant",
    content: "Now, let's try it yourself. You can start typing on the right.",
  },
];

export default function Page() {
  const [messages, setMessages] = useState<Message[]>(defaultMessages);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [leftPanelWidth, setLeftPanelWidth] = useState(50); // for draggable divider
  const containerRef = useRef<HTMLDivElement>(null); // for draggable divider

  // useEffect(() => {
  //   const handleMouseMove = (e: MouseEvent) => {
  //     if (!containerRef.current) return;

  //     const container = containerRef.current;
  //     const rect = container.getBoundingClientRect();
  //     const newWidth = ((e.clientX - rect.left) / rect.width) * 100;

  //     if (newWidth > 20 && newWidth < 80) {
  //       setLeftPanelWidth(newWidth);
  //     }
  //   };

  //   const handleMouseUp = () => {
  //     document.removeEventListener("mousemove", handleMouseMove);
  //     document.removeEventListener("mouseup", handleMouseUp);
  //   };

  //   const handleDividerMouseDown = () => {
  //     document.addEventListener("mousemove", handleMouseMove);
  //     document.addEventListener("mouseup", handleMouseUp);
  //   };

  //   const divider = containerRef.current?.querySelector('[data-divider]');
  //   if (divider) {
  //     divider.addEventListener("mousedown", handleDividerMouseDown);
  //   }

  //   return () => {
  //     if (divider) {
  //       divider.removeEventListener("mousedown", handleDividerMouseDown);
  //     }
  //   };
  // }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userText = inputValue.trim();
    const userMessage: Message = {
      id: crypto.randomUUID(),
      type: "user",
      content: userText,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
      const resp = await fetch(`${API_BASE}/api/intent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      const data = await resp.json().catch(() => ({}));

      if (!resp.ok || !data.ok) {
        const errorMsg = data?.error || data?.message || "Backend error";
        const assistantMessage: Message = {
          id: crypto.randomUUID(),
          type: "assistant",
          content: `Error: ${errorMsg}`,
        };
        setMessages((prev) => [...prev, assistantMessage]);
        return;
      }

      // Success path
      const summaryText = data.result?.summary || data.message || "Done";
      console.log("anomalies table from backend:", data.result?.table);

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        type: "assistant",
        content: summaryText,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error("Error calling backend:", err);
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        type: "assistant",
        content: "Network error: Could not reach the backend.",
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // const handleNewChat = () => {
  //   setMessages(defaultMessages);
  //   setInputValue("");
  // };
  
  return (
    <main className="min-h-screen bg-white p-6">
      <div className="max-w-6xl mx-auto grid gap-6">
        <TopBanner />
        {/* 2-column content area */}
        <div 
          ref={containerRef} 
          className="grid gap-6"
          style={{
            gridTemplateColumns: `minmax(0, ${leftPanelWidth}%) minmax(0, ${100 - leftPanelWidth}%)`,
          }}
        >
          {/* <QueryGuideline /> */}
          <DraftLeft />
          {/* <DraggableDivider /> */}
          <WelcomePanel
            messages={messages}
            // panelWidth={100 - leftPanelWidth}
            inputValue={inputValue}
            onInputChange={setInputValue}
            onInputSubmit={handleSendMessage}
            onQuerySelect={setInputValue}
            isLoading={isLoading}
          />
        </div>
      </div>
    </main>
  );
}
