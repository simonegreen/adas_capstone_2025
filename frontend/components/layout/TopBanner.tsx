"use client";

import Image from "next/image";
import Card from "@/components/ui/Card";

export default function TopBanner() {
  return (
    <Card className="rounded-[20px] py-3 px-0 flex items-center justify-between">
      {/* Left: home icon bubble + star logo + title */}
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-3xl border border-neutral-300 bg-white grid place-items-center">
          {/* simple home icon */}
          <svg width="28" height="28" viewBox="0 0 24 24" className="text-zinc-500">
            <path fill="currentColor" d="m4 10 8-6 8 6v10a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1V10z"/>
          </svg>
        </div>

        {/* star+sparkle logo placeholder */}
        <div className="relative w-8 h-8">
          <Image
            src="/Logo.svg"
            alt="star logo"
            fill
            className="rounded-full object-cover"
          />
        </div>

        <div className="text-2xl font-bold leading-9 text-zinc-900">ADaS Chat</div>
      </div>

      {/* Right: New Chat, ?, user avatar */}
      <div className="flex items-center gap-3">
        <button className="px-4 py-2 rounded-3xl bg-indigo-800 text-white text-sm"> +  New Chat</button>
        <button className="px-3 py-2 rounded-3xl border text-sm">?</button>
        <div className="w-11 h-11 rounded-3xl bg-teal-200 overflow-hidden">
          <Image
            src="/user_icon.png"
            alt="user avatar"
            width={44}
            height={44}
          />
        </div>
      </div>
    </Card>
  );
}

// "use client";

// import Image from "next/image";

// export default function TopBanner() {
//   return (
//     // pure white bar, no border/shadow (outline gone), rounded corners
//     <div className="rounded-[20px] bg-white p-3 flex items-center justify-between select-none">
//       {/* Left: home + logo + title */}
//       <div className="flex items-center gap-3">
//         <div className="w-12 h-12 rounded-3xl bg-white grid place-items-center ring-1 ring-zinc-200/0">
//           {/* simple home icon */}
//           <svg width="22" height="22" viewBox="0 0 24 24" className="text-zinc-500">
//             <path fill="currentColor" d="m4 10 8-6 8 6v10a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1V10z"/>
//           </svg>
//         </div>

//         {/* sparkle logo (replace when ready) */}
//         <div className="relative w-8 h-8">
//           <Image
//             src="/Logo.svg"                 // TODO: replace
//             alt="ADaS logo"
//             fill
//             className="object-contain"
//           />
//         </div>

//         <div className="text-zinc-900 text-2xl font-bold leading-9">ADaS Chat</div>
//       </div>

//       {/* Right: actions */}
//       <div className="flex items-center gap-3">
//         <button className="px-4 py-2 rounded-3xl bg-[#5B21B6] text-white text-sm">+ New Chat</button>
//         <button className="px-3 py-2 rounded-3xl border border-zinc-200 text-sm">?</button>
//         <div className="w-11 h-11 rounded-3xl overflow-hidden">
//           <Image src="/user_icon.png" alt="User" width={44} height={44} />
//         </div>
//       </div>
//     </div>
//   );
// }
