"use client";

import { DragEvent, useRef, useState } from "react";
import Image from "next/image";


export default function FileDropzone({ onFile }: { onFile: (f: File | null) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  const [name, setName] = useState("");

  const pick = () => inputRef.current?.click();

  const setFile = (f: File | null) => {
    if (f) setName(`${f.name} (${(f.size / 1024).toFixed(1)} KB)`);
    onFile(f);
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    setFile(e.dataTransfer.files?.[0] ?? null);
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={onDrop}
      className={`rounded-[12px] p-8 text-center transition
       ${dragOver ? "border-violet-400 bg-violet-50" : "border-zinc-300"}`}
      onClick={pick}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv,.zip,text/csv,application/zip"
        className="hidden"
        onChange={() => setFile(inputRef.current?.files?.[0] ?? null)}
      />

      {/* Cloud icon (simple SVG) */}
      <div className="mx-auto mb-3 h-8 w-8 text-indigo-700" aria-hidden>
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 18a4 4 0 0 1 0-8 5 5 0 0 1 9.58-1.65A4 4 0 1 1 18 18H6zm5-6v4m-2-2h4"/></svg>
      </div>

      <div className="text-sm text-zinc-700">
        Drag and drop your file here,<br /> or click to browse
      </div>
      <div className="mt-1 text-xs text-gray-400">Only one CSV file or ZIP file supported</div>

      {/* Small “Browse Files” chip like the comp */}
      <button
        type="button"
        onClick={pick}
        className="mt-3 inline-flex h-10 w-28 items-center justify-center rounded-md bg-white border border-zinc-200"
      >
        Browse Files
      </button>

      {name && <div className="mt-3 text-xs text-gray-700">{name}</div>}
    </div>
  );
}
