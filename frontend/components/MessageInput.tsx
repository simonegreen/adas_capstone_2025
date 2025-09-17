"use client";

export default function MessageInput() {
  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const msg = form.get("message");
    console.log("Submit message:", msg);
    e.currentTarget.reset();
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2">
      <textarea
        name="message"
        className="textarea"
        rows={2}
        placeholder="Message"
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            (e.currentTarget.form as HTMLFormElement)?.requestSubmit();
          }
        }}
      />
      <button type="submit" className="btn-primary">Send</button>
    </form>
  );
}
