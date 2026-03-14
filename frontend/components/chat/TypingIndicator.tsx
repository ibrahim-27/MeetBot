import { Bot } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="py-4 px-4 w-full flex flex-col items-start translate-y-[-8px]">
      <div className="max-w-[85%] sm:max-w-2xl px-6 py-4 rounded-3xl bg-brand-surface text-brand-text border border-brand-border rounded-tl-none ml-2 shadow-sm animate-pulse">
        <div className="flex gap-4 items-center">
          <div className="w-8 h-8 rounded-xl bg-brand-primary text-white flex items-center justify-center shrink-0 shadow-inner">
            <Bot className="w-4 h-4" />
          </div>
          <div className="flex gap-1 items-center h-4">
            <span className="w-1.5 h-1.5 bg-brand-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span className="w-1.5 h-1.5 bg-brand-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span className="w-1.5 h-1.5 bg-brand-primary/40 rounded-full animate-bounce"></span>
          </div>
        </div>
      </div>
    </div>
  );
}
