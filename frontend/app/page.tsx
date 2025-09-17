"use client"; 

import Sidebar from "@/components/Sidebar";
import Toolbelt from "@/components/Toolbelt";
import ChatWindow from "@/components/ChatWindow";
import MessageInput from "@/components/MessageInput";

export default function Page() {
  return (
    // <main>Hello </main>
    <main className="grid grid-cols-[300px_1fr] gap-6 p-6 bg-surface-soft min-h-screen">
      <Sidebar />
      <section className="flex flex-col gap-4">
        <Toolbelt />
        <div className="card min-h-[60vh]">
          <ChatWindow />
        </div>
        <MessageInput />
      </section>
    </main>
  );
}
