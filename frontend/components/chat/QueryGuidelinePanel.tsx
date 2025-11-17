// Left Panel - Based off the old - GuidelinesPanel 

import Image from "next/image";
import { Actor } from "next/font/google";
const actor = Actor({ subsets: ["latin"], weight: "400" });


// Simple lead icon bubble
function LeadIcon({ variant }: { variant: "adas" | "star" }) {
  const src = variant === "star" ? "/Logo.svg" : "/bot.png";
  const bg  = variant === "adas" ? "bg-emerald-500/10" : "bg-indigo-600/10";

  return (
    <div className="self-start pt-[2px] shrink-0 h-14 w-12 grid place-items-center rounded-full">
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
function Message({ children, variant = "plain" as "plain" | "accent" }) {
  const base =
    "flex-1 rounded-[16px] px-4 py-3";
  const styles = variant === "accent" ? `${base} bg-violet-50/60` : `${base} bg-white`;
  return <div className={styles}>{children}</div>;
}


export default function QueryGuidelinesPanel() {
  return (
    <section
      className={`${actor.className} text-[#171A1F] text-[16px] leading-[26px] font-normal space-y-4`}
    >
      {/* Inline label sitting on white, not inside a box */}
      <div className="text-gray-500 text-base">ADaS User Guidelines</div>

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
            Top <span className="font-semibold">n</span> anomalies (<span className="font-semibold">n</span> is the number of anomalies)
            </li>
            <li>
            Number of features used to identify anomalies.
            <div className="mt-2 text-[16px] leading-6">
            For example, 6, 8, 10 features. We recommend you to start with 10 features for optimal result. Note, ADaS will rerun the experiment if you ask to run with a different number of features. For example, asking 12 features after running with 10 features.
            </div>
            </li>
            <li>Explanation</li>
            <li>
            You can ask to provide context associated with IP address <span className="font-mono">x</span>
            </li>
            </ul>
          
        </Message>
      </div>

      {/* Message 2: Star icon + purple accent background with table */}
      <div className="flex items-start gap-3">
        <LeadIcon variant="adas" />
        <Message variant="accent">
          <p className="font-semibold">You should not query like these bad examples:</p>
            <ul className="mt-2 list-disc pl-6 space-y-2">
            <li>
            <span className="italic">“Tell me what are the anomalies under the </span>
            <span className="text-red-500 font-semibold">feature timestamp</span>
            <span className="italic">?”</span>
            <div className="mt-1">Instead, specify the <span className="font-semibold">number of features</span>.</div>
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
            Instead, try a query with <span className="font-semibold">10</span> features first, save the result, then query with <span className="font-semibold">12</span> features.
            </div>
            </li>
            </ul>
        </Message>
      </div>

      {/* Message 3: ADaS follow-up hint */}
      <div className="flex items-start gap-3">
        <LeadIcon variant="adas" />
        <Message>
          <p className="">
            Now, try it yourself—use the uploader on the right.
          </p>
        </Message>
      </div>
    </section>
  );
}
