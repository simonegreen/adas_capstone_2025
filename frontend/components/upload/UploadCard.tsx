"use client";

import { useState } from "react";
import FileDropzone from "./FileDropzone";

type UploadResponse = { ok: boolean; status?: string; rows?: number; columns?: number; message?: string };

export default function UploadCard() {
  const [file, setFile] = useState<File | null>(null);
  const [uidHeader, setUidHeader] = useState("");
  const [tsHeader, setTsHeader] = useState("");
  const [loading, setLoading] = useState(false);
  const [serverMsg, setServerMsg] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setServerMsg(null);
    if (!file) return setServerMsg("Please select a CSV or ZIP file first.");
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      fd.append("uidHeader", uidHeader);
      fd.append("tsHeader", tsHeader);
      const r = await fetch("/api/upload", { method: "POST", body: fd });
      const data = (await r.json()) as UploadResponse;
      setServerMsg(
        data.ok ? `✅ Uploaded. Rows: ${data.rows ?? "?"}, Cols: ${data.columns ?? "?"}` : `❌ ${data.message}`
      );
    } catch {
      setServerMsg("❌ Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    // Outer gray container (the big rounded box)
    <div className="rounded-[24px] bg-gray-100 p-4 shadow-[0_3px_6px_rgba(18,15,40,0.12)]">
      {/* Inner white panel with border + soft shadow */}
      <div className="rounded-[18px] bg-white p-8 border border-gray-200 shadow-[0_4px_9px_rgba(23,26,31,0.19),0_0_2px_rgba(23,26,31,0.20)]">
        <h2 className="text-center text-3xl font-bold text-zinc-900">Dataset Upload</h2>
        <p className="mt-2 text-center text-gray-600">
          Upload your CSV file and specify column headers for unique identifiers and timestamps.
        </p>

        <form onSubmit={handleSubmit} className="mt-6">
          {/* Dropzone with dashed border */}
          <div className="rounded-[12px] border-2 border-dashed border-zinc-200 p-6">
            <FileDropzone onFile={setFile} />
            {/* <div className="mt-2 text-center text-gray-400 text-sm">Only one CSV file or ZIP file supported</div> */}
          </div>

          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-xs text-zinc-900 mb-2">Unique Identifier Column Header</label>
              <input
                className="w-full h-11 px-3 rounded-md border border-zinc-200 focus:outline-none focus:ring-2 focus:ring-violet-300"
                placeholder="e.g., customer_id, transaction_uuid"
                value={uidHeader}
                onChange={(e) => setUidHeader(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs text-zinc-900 mb-2">Timestamp Column Header</label>
              <input
                className="w-full h-11 px-3 rounded-md border border-zinc-200 focus:outline-none focus:ring-2 focus:ring-violet-300"
                placeholder="e.g., event_timestamp, created_at"
                value={tsHeader}
                onChange={(e) => setTsHeader(e.target.value)}
              />
            </div>
          </div>

          <div className="mt-6 flex justify-end">
            <button
              type="submit"
              disabled={loading || !file}
              className="min-w-[128px] h-10 px-4 rounded-md bg-[#5B21B6] text-white text-base disabled:opacity-50"
            >
              {loading ? "Uploading…" : "Submit"}
            </button>
          </div>

          {serverMsg && (
            <div className="mt-3 text-sm rounded-md border bg-gray-50 px-3 py-2 text-gray-700">{serverMsg}</div>
          )}
        </form>
      </div>
    </div>
  );
}
