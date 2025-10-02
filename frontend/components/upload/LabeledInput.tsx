"use client";

type Props = {
  label: string;
  placeholder?: string;
  value: string;
  onChange: (v: string) => void;
};
export default function LabeledInput({ label, placeholder, value, onChange }: Props) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-sm text-gray-700">{label}</label>
      <input
        type="text"
        className="px-3 py-2 border rounded-xl outline-none focus:ring-2 focus:ring-violet-300"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
