import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

export const runtime = "nodejs";

export async function POST(req: Request) {
  try {
    const form = await req.formData();
    const file = form.get("file") as File | null;
    const uidHeader = String(form.get("uidHeader") ?? "");
    const tsHeader = String(form.get("tsHeader") ?? "");

    if (!file) {
      return NextResponse.json({ ok: false, message: "No file received." }, { status: 400 });
    }

    const arrayBuf = await file.arrayBuffer();
    const buf = Buffer.from(arrayBuf);
    const dest = path.join("/tmp", file.name);
    await fs.writeFile(dest, buf);

    let inferredHeaders: string[] | undefined;
    if (file.type.includes("csv") || file.name.endsWith(".csv")) {
      const firstChunk = buf.toString("utf8").split(/\r?\n/)[0] ?? "";
      inferredHeaders = firstChunk.split(",").map(s => s.trim());
    }

    // Friendly echo to help you debug integrations
    const message = `Uploaded ${file.name}. UID header: "${uidHeader || "(not set)"}", Timestamp header: "${tsHeader || "(not set)"}".` +
      (inferredHeaders?.length ? ` CSV headers detected: ${inferredHeaders.join(" | ")}` : "");

    return NextResponse.json({ ok: true, message, inferredHeaders });
  } catch (err) {
    console.error(err);
    return NextResponse.json({ ok: false, message: "Server error while uploading." }, { status: 500 });
  }
}
