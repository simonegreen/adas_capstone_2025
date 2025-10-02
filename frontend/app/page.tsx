import TopBanner from "@/components/layout/TopBanner";
import GuidelinesPanel from "@/components/chat/GuidelinesPanel";
import UploadCard from "@/components/upload/UploadCard";

export default function Page() {
  return (
    <main className="min-h-screen bg-white p-6">
      <div className="max-w-6xl mx-auto grid gap-6">
        <TopBanner />

        {/* 2-column content area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GuidelinesPanel />
          <UploadCard />
        </div>
      </div>
    </main>
  );
}
