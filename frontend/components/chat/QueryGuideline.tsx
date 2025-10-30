// old - GuidelinesPanel 

import Image from "next/image";
// components/chat/GuidelinesPanel.tsx
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

function ExampleTable() {
  return (
    <div className="mt-3 overflow-x-auto">
      <table className="w-full text-sm border border-gray-200 rounded-xl overflow-hidden">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left">Index</th>
            <th className="px-4 py-2 text-left">uid</th>
            <th className="px-4 py-2 text-left">timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr className="border-t">
            <td className="px-4 py-2">1</td>
            <td className="px-4 py-2">Cu3Tier143jPsyB03</td>
            <td className="px-4 py-2">Sep 12 2025</td>
          </tr>
          <tr className="border-t">
            <td className="px-4 py-2">2</td>
            <td className="px-4 py-2">Cu3Tier143jPsyB03</td>
            <td className="px-4 py-2">1538572954</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default function GuidelinesPanel() {
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
            <span className="">Hi, welcome to ADaS.</span>{" "}
            Here's some information to help you start. Start by uploading your datasets in CSV format. Then specify the header name of unique identifier, and time in your dataset by typing into the chat box.
          </p>
          <p className="mt-6">Tell ADaS what you want to know from your datasets. We accept questions in the following format:</p>
        
          {/* Example chip */}
          <div className="mt-3 rounded-xl bg-violet-50/60 px-4 py-3 text-[14px]">
            <span className="italic">“What are the </span>
            <span className="text-red-500 font-semibold">top 5</span>
            <span className="italic"> anomalies with </span>
            <span className="text-red-500 font-semibold">10</span>
            <span className="italic"> features in the </span>
            <span className="text-red-500 font-semibold">past week</span>
            <span className="italic">?”</span>
          </div>
        </Message>
      </div>

      {/* Message 2: Star icon + purple accent background with table */}
      <div className="flex items-start gap-3">
        <LeadIcon variant="star" />
        <Message variant="accent">
          <p className="">
            For example, you should enter header names like <code>uid</code> and <code>timestamp</code>   
            {" "}for unique identifier, and time respectively as they are the header names in the table:
          </p>
          <ExampleTable />
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
