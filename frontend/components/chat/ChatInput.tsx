import { useState, useRef, useEffect } from "react";
import { ArrowUp } from "lucide-react";
import { cn } from "../../lib/utils";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [input]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || disabled) return;
    
    onSendMessage(input.trim());
    setInput("");
    
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full relative group">
      <div className="absolute -inset-0.5 bg-brand-primary rounded-3xl blur opacity-0 group-focus-within:opacity-5 transition-opacity duration-500"></div>
      <form
        onSubmit={handleSubmit}
        className="relative flex items-end gap-3 bg-white border border-slate-200 rounded-[1.75rem] px-4 py-2 transition-all shadow-md group-focus-within:border-brand-primary/30"
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className="flex-1 max-h-[200px] min-h-[52px] bg-transparent resize-none py-4 px-1 focus:outline-none text-brand-text placeholder:text-slate-400 text-base"
          rows={1}
          disabled={disabled}
        />
        
        <button
          type="submit"
          disabled={!input.trim() || disabled}
          className={cn(
            "w-12 h-12 rounded-2xl transition-all flex items-center justify-center shrink-0 mb-1 mr-1",
            input.trim() && !disabled
              ? "bg-brand-primary text-white shadow-lg shadow-teal-500/20 hover:bg-brand-primary-hover"
              : "bg-slate-50 text-slate-300 cursor-not-allowed"
          )}
        >
          <ArrowUp className="w-6 h-6 stroke-[3]" />
        </button>
      </form>
    </div>
  );
}
