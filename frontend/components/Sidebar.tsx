export default function Sidebar() {
  return (
    <aside className="sidebar h-fit">
      <h2 className="text-lg font-semibold mb-2">ADaS User Guidelines</h2>
      <p className="text-text-muted mb-4">
        Start by uploading your datasets in CSV format. Then ask what you want to know.
      </p>
      <div className="card">
        <p className="text-sm">
          Example: “What are the top <span className="text-brand-500 font-semibold">5</span> anomalies with
          <span className="text-brand-500 font-semibold"> 10</span> features in the
          <span className="text-brand-500 font-semibold"> past week</span>?”
        </p>
      </div>
    </aside>
  );
}
