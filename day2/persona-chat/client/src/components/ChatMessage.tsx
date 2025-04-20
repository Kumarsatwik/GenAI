
import { cn } from "@/lib/utils";

interface ChatMessageProps {
  message: string;
  isAi: boolean;
  avatar?: string;
}

export const ChatMessage = ({ message, isAi, avatar }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex w-full gap-3 p-4",
        isAi ? "bg-slate-50" : "bg-white"
      )}
    >
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow bg-white">
        <span className="text-sm">{isAi ? "🤖" : "👤"}</span>
      </div>
      <div className="flex-1 space-y-2">
        <p className="text-sm text-slate-800">
          {message}
        </p>
      </div>
    </div>
  );
};
