export default function ChatBubble({
  role,
  children
}: { role: "user" | "assistant"; children: React.ReactNode }) {
  const align = role === "user" ? "items-end" : "items-start";
  return (
    <div className={`flex ${align}`}>
      <div className="bubble max-w-[640px]">{children}</div>
    </div>
  );
}
