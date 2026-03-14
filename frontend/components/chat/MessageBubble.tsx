import { cn } from "../../lib/utils";
import { User, Bot } from "lucide-react";

export interface MessageProps {
  role: "user" | "assistant";
  content: string;
}

export function MessageBubble({ role, content }: MessageProps) {
  const isAssistant = role === "assistant";

  return (
    <div className={cn("py-4 px-4 w-full flex flex-col", isAssistant ? "items-start" : "items-end")}>
      <div className={cn(
        "max-w-[85%] sm:max-w-2xl px-6 py-5 rounded-3xl animate-in fade-in slide-in-from-bottom-2 duration-300 shadow-sm",
        isAssistant 
          ? "bg-brand-surface text-brand-text border border-brand-border rounded-tl-none ml-2" 
          : "bg-brand-primary text-white rounded-tr-none mr-2 shadow-lg shadow-teal-900/10"
      )}>
        <div className="flex gap-4 items-start">
          <div className={cn(
            "w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-0.5",
            isAssistant ? "bg-brand-primary text-white" : "bg-white/10 text-white"
          )}>
            {isAssistant ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
          </div>
          
          <div className="flex-1 min-w-0 py-1">
            <div className={cn(
              "text-[15px] leading-relaxed whitespace-pre-wrap",
              isAssistant ? "text-brand-text" : "text-white"
            )}>
              {content}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
