// File: app/api/upload/route.ts
// Purpose: API route to handle file uploads from frontend and proxy them to FastAPI backend.
// Author: Aimee Liang
// Created: 2025-10-15
// Last Modified By: Aimee Liang (2025-11-3)

import { NextResponse } from "next/server";

export const runtime = "nodejs";

// Set your backend base URL in .env (Codespaces safe):
// API_BASE_URL=http://localhost:8000
// or something like https://your-backend.example.com
const API_BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000";

export async function POST(req: Request) {
  try {
    const form = await req.formData();
    const file = form.get("file") as File | null;

    if (!file) {
      return NextResponse.json(
        { ok: false, message: "No file received." },
        { status: 400 }
      );
    }

    // Optional: size guard (FastAPI will also enforce its own limits)
    // e.g., block > 200MB
    const MAX_BYTES = 5 * 1024 * 1024 * 1024;
    if (typeof (file as any).size === "number" && (file as any).size > MAX_BYTES) {
      return NextResponse.json(
        { ok: false, message: "File too large." },
        { status: 413 }
      );
    }

    // Build multipart form-data for FastAPI
    const backendForm = new FormData();

    // FastAPI expects the field name "file"
    const arrayBuf = await file.arrayBuffer();
    const filename =
      (file as any).name || "upload.csv"; // name isn't always present in edge cases
    const blob = new Blob([arrayBuf], { type: file.type || "text/csv" });
    backendForm.append("file", blob, filename);

    // If later your backend accepts headers like uidHeader/tsHeader/sceIPHeader, you can send them:
    // const uidHeader = String(form.get("uidHeader") ?? "");
    // const tsHeader  = String(form.get("tsHeader") ?? "");
    // const sceIPHeader  = String(form.get("sceIPHeader") ?? "");

    // backendForm.append("uidHeader", uidHeader);
    // backendForm.append("tsHeader", tsHeader);
    // backendForm.append("sceIPHeader", sceIPHeader);


    const resp = await fetch(`${API_BASE_URL}/add_data/`, {
      method: "POST",
      body: backendForm, // DO NOT set content-type manually; fetch will set multipart boundary.
    });

    // Pass through FastAPI's response cleanly
    const data = await resp.json().catch(() => ({}));

    if (!resp.ok) {
      const detail =
        (data && (data.detail || data.message)) || "Upload failed upstream.";
      return NextResponse.json(
        { ok: false, message: detail },
        { status: resp.status }
      );
    }

    // FastAPI example returns: { status, rows, columns }
    return NextResponse.json({
      ok: true,
      ...data,
    });
  } catch (err) {
    console.error(err);
    return NextResponse.json(
      { ok: false, message: "Server error while proxying upload." },
      { status: 500 }
    );
  }
}
