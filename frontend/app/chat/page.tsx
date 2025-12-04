"use client";

import TopBanner from "@/components/layout/TopBanner";
import QueryGuideline from "@/components/chat/QueryGuidelinePanel";
import { DraftLeft } from "@/components/chat/DraftLeft";
import { DraggableDivider } from "@/components/chat/DraggableDivider";
import { WelcomePanel } from "@/components/chat/WelcomePanel";
import { useEffect, useRef, useState } from "react";

export const dynamic = "force-dynamic";

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

interface BackendResult {
  explain?: string;
  vt_lookups?: Record<string, any> | null;
  anomalies?: { cols: string[]; rows: any[][] } | null;
  csv?: string | null;
  [k: string]: any;
}

interface BackendResponse {
  ok: boolean;
  action?: string;
  result?: BackendResult;
  message?: string;
  error?: string;
  [k: string]: any;
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

    /** Helper: trigger CSV download of the full backend result */
  const triggerCsvDownload = (csv: string) => {
    if (typeof window === "undefined") return;

    try {
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      link.href = url;
      link.setAttribute("download", `adas_anomalies_${timestamp}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error("Failed to trigger CSV download", e);
    }
  };

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

      const data: BackendResponse = await resp.json().catch(() => ({} as BackendResponse));

      // Debug logging (temporary)
      console.log("Full backend data:", data);
      console.log("Result:", data.result);
      console.log("Explain:", data.result?.explain);
      console.log("VT lookups:", data.result?.vt_lookups);
      console.log("Anomalies:", data.result?.anomalies);
      console.log("CSV:", data.result?.csv);

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

      // Success path: expand result into multiple assistant messages
      const result = data.result as BackendResult | undefined;

      const newMessages: Message[] = [];

      if (result?.explain) {
        newMessages.push({
          id: crypto.randomUUID(),
          type: "assistant",
          content: `Explanation:\n${result.explain}`,
        });
      }

      if (result?.vt_lookups && Object.keys(result.vt_lookups).length > 0) {
        newMessages.push({
          id: crypto.randomUUID(),
          type: "assistant",
          content: `Lookups:\n${JSON.stringify(result.vt_lookups, null, 2)}`,
        });
      }

            // ---------- PRETTY TABLE FOR ANOMALIES ----------
      if (result?.anomalies) {
        const an = result.anomalies as { cols: string[]; rows: any[][] };
        if (an.cols && an.rows) {
          const limitedRows = an.rows.slice(0, 100); // show up to 100 in-table

          newMessages.push({
            id: crypto.randomUUID(),
            type: "assistant",
            content:
              "Anomalies (table preview): Top rows from the result. Full CSV downloaded to your device.",
            tableData: {
              cols: an.cols,
              rows: limitedRows,
            },
          });
        } else {
          newMessages.push({
            id: crypto.randomUUID(),
            type: "assistant",
            content: `Anomalies:\n${JSON.stringify(result.anomalies, null, 2)}`,
          });
        }
      }

      // ---------- CSV PREVIEW + AUTO-DOWNLOAD ----------
      if (result?.csv) {
        const csvString =
          typeof result.csv === "string"
            ? result.csv
            : JSON.stringify(result.csv, null, 2);

        const csvPreview =
          typeof csvString === "string"
            ? csvString.slice(0, 200)
            : String(csvString);

        newMessages.push({
          id: crypto.randomUUID(),
          type: "assistant",
          content: `CSV preview:\n${csvPreview}${
            typeof csvString === "string" && csvString.length > 200
              ? "\n... (truncated)"
              : ""
          }`,
        });

        // Trigger browser download of the full CSV
        if (typeof result.csv === "string") {
          triggerCsvDownload(result.csv);
        }
      }

      // If nothing was produced above, fall back to a simple message
      if (newMessages.length === 0) {
        const fallback = data.message || "Done";
        newMessages.push({
          id: crypto.randomUUID(),
          type: "assistant",
          content: fallback,
        });
      }

      setMessages((prev) => [...prev, ...newMessages]);
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
          <DraftLeft />
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
