import React from "react";

type Props = React.PropsWithChildren<{ className?: string }>;
export default function Card({ className = "", children }: Props) {
  return (
    <div className={`rounded-2xl shadow-sm bg-white ${className}`}>
      {children}
    </div>
  );
}
