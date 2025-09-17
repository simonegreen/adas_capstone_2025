import ChatBubble from "./ChatBubble";

export default function ChatWindow() {
  return (
    <div className="flex flex-col gap-4">
      <ChatBubble role="user">Hello! What are the top 5 anomalies with 10 features?</ChatBubble>
      <ChatBubble role="assistant">
        <div className="space-y-2">
          <p>Hi there! Here’s your results, the top 5 anomalies are:</p>
          <ul className="list-disc pl-5 text-sm">
            <li>12345678</li><li>12345678</li><li>12345678</li><li>12345678</li><li>12345678</li>
          </ul>
          <div className="flex items-center gap-3 pt-2">
            <span className="text-text-muted text-sm">You can download the file here:</span>
            <button className="btn-ghost" type="button">📁</button>
            <a className="btn-ghost" href="#" onClick={(e)=>e.preventDefault()}>⬇️</a>
          </div>
        </div>
      </ChatBubble>
      <ChatBubble role="user">Now run it with 12 features.</ChatBubble>
    </div>
  );
}
