"use client";

type Props = {
  disabled?: boolean;
  loading?: boolean;
};
export default function SubmitButton({ disabled, loading }: Props) {
  return (
    <button
      type="submit"
      disabled={disabled || loading}
      className="w-full rounded-xl bg-violet-600 text-white py-2.5 font-medium
                 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {loading ? "Uploading…" : "Submit"}
    </button>
  );
}
