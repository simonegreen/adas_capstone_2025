
// Right panel - Query suggestion card

interface QueryCardProps {
  text: string;
  onClick: (text: string) => void;
}

export function QueryCard({ text, onClick }: QueryCardProps) {
  return (
    <div
      onClick={() => onClick(text)}
      className="p-4 bg-white rounded-lg hover:bg-gray-100 cursor-pointer transition-colors
        text-gray-600
        text-[18px] leading-[28px] font-normal
        border border-gray-200"
    >
      {text}
    </div>
  );
}
