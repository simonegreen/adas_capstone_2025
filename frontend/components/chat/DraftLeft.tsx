// /components/chat/draft.tsx
// Left Panel (draggable width) with QueryGuidelinesPanel styling

import Image from "next/image";
import { Actor } from "next/font/google";
const actor = Actor({ subsets: ["latin"], weight: "400" });

// Keep the prop shape so DraggableDivider/layout code still works
interface GuidelinesPanelProps {
  // messages prop is ignored now (static guidelines panel)
  messages?: Array<{ id: string; type: "user" | "assistant"; content: string }>;
  panelWidth: number;
}

// Simple lead icon bubble
function LeadIcon({ variant }: { variant: "adas" | "star" }) {
  const src = variant === "star" ? "/Logo.svg" : "/bot.png";
  return (
    <div className="self-centre pt-[2px] shrink-0 h-14 w-12 grid place-items-center rounded-full">
      <Image
        src={src}
        alt={`${variant} icon`}
        width={100}
        height={100}
        className="object-contain"
        priority={false}
      />
    </div>
  );
}

// Message bubble container
function Message({
  children,
  variant = "plain",
}: {
  children: React.ReactNode;
  variant?: "plain" | "accent";
}) {
  const base = "flex-1 rounded-[16px] px-4 py-3";
  const styles = variant === "accent" ? `${base} bg-violet-50/60` : `${base} bg-white`;
  return <div className={styles}>{children}</div>;
}

export function DraftLeft({ panelWidth }: GuidelinesPanelProps) {
  return (
    <div
      style={{ width: `${panelWidth}%` }}
      className={`${actor.className} text-[#171A1F] text-[16px] leading-[26px] font-normal
                  bg-white flex flex-col overflow-hidden transition-none`}
    >
      {/* Inline label sitting on white, not inside a box */}
      <div className="px-6 py-4 border-b border-gray-200 bg-white flex-shrink-0">
        <div className="text-gray-500 text-base">ADaS User Guidelines</div>
      </div>

      {/* Scrollable messages column */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {/* Message 1: ADaS (green) leading the convo */}
        <div className="flex items-start gap-3">
          <LeadIcon variant="adas" />
          <Message>
            <p className="text-[17px] leading-7">
              <span>Hi, thanks for uploading the dataset to ADaS. Ask me about:</span>
            </p>
            <ul className="mt-3 list-disc pl-6 space-y-1">
              <li>Time range</li>
              <li>
                Top <span className="font-semibold">n</span> anomalies (
                <span className="font-semibold">n</span> is the number of anomalies)
              </li>
              <li>
                Number of features used to identify anomalies.
                <div className="mt-2 text-[16px] leading-6">
                  For example, 6, 8, 10 features. We recommend you to start with 10 features
                  for optimal result. Note, ADaS will rerun the experiment if you ask to run
                  with a different number of features. For example, asking 12 features after
                  running with 10 features.
                </div>
              </li>
              <li>Explanation</li>
              <li>
                You can ask to provide context associated with IP address{" "}
                <span className="font-mono">x</span>
              </li>
            </ul>
          </Message>
        </div>

        {/* Message 2: Bad examples and corrections */}
        <div className="flex items-start gap-3">
          <LeadIcon variant="adas" />
          <Message variant="accent">
            <p className="font-semibold">You should not query like these bad examples:</p>
            <ul className="mt-2 list-disc pl-6 space-y-2">
              <li>
                <span className="italic">“Tell me what are the anomalies under the </span>
                <span className="text-red-500 font-semibold">feature timestamp</span>
                <span className="italic">?”</span>
                <div className="mt-1">
                  Instead, specify the <span className="font-semibold">number of features</span>.
                </div>
              </li>
              <li>
                <span className="italic">“I want to know the output with </span>
                <span className="text-red-500 font-semibold">10</span>
                <span className="italic">, </span>
                <span className="text-red-500 font-semibold">12</span>
                <span className="italic">, and </span>
                <span className="text-red-500 font-semibold">14</span>
                <span className="italic"> features.”</span>
                <div className="mt-1">
                  Instead, try a query with <span className="font-semibold">10</span> features
                  first, save the result, then query with{" "}
                  <span className="font-semibold">12</span> features.
                </div>
              </li>
            </ul>
          </Message>
        </div>

        {/* Message 3: ADaS follow-up hint */}
        <div className="flex items-start gap-3">
          <LeadIcon variant="adas" />
          <Message>
            <p>Now, try it yourself—use the uploader on the right.</p>
          </Message>
        </div>
      </div>
    </div>
  );
}
