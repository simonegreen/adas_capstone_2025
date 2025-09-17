"use client";

export default function Toolbelt({ onNew }: { onNew?: () => void }) {
  return (
    <div className="flex items-center justify-end">
      <button className="btn-primary" onClick={onNew}>
        <svg className="icon-20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
          <path d="M12 5v14m-7-7h14" />
        </svg>
        New Chat
      </button>
    </div>
  );
}
