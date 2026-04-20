import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";
import { cn } from "../../lib/utils";
import { User, Bot } from "lucide-react";

export interface MessageProps {
  role: "user" | "assistant";
  content: string;
}

export function MessageBubble({ role, content }: MessageProps) {
  const isAssistant = role === "assistant";

  const components: Components = {
    a: ({ href, children }) => (
      <a
        href={href}
        className={cn(
          "underline underline-offset-2 break-all",
          isAssistant ? "text-brand-primary" : "text-white"
        )}
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),
    code: ({ className, children, ...props }) => {
      const isBlock = Boolean(className?.includes("language-"));
      if (isBlock) {
        return (
          <code className={className} {...props}>
            {children}
          </code>
        );
      }
      return (
        <code
          className={cn(
            "rounded px-1 py-0.5 text-[0.9em]",
            isAssistant ? "bg-black/10" : "bg-white/15"
          )}
          {...props}
        >
          {children}
        </code>
      );
    },
    pre: ({ children }) => (
      <pre
        className={cn(
          "overflow-x-auto rounded-lg p-3 my-2 text-[13px]",
          isAssistant ? "bg-black/10 text-brand-text" : "bg-white/10 text-white"
        )}
      >
        {children}
      </pre>
    ),
  };

  return (
    <div className={cn("py-4 px-4 w-full flex flex-col", isAssistant ? "items-start" : "items-end")}>
      <div
        className={cn(
          "max-w-[85%] sm:max-w-2xl px-6 py-5 rounded-3xl animate-in fade-in slide-in-from-bottom-2 duration-300 shadow-sm",
          isAssistant
            ? "bg-brand-surface text-brand-text border border-brand-border rounded-tl-none ml-2"
            : "bg-brand-primary text-white rounded-tr-none mr-2 shadow-lg shadow-teal-900/10"
        )}
      >
        <div className="flex gap-4 items-start">
          <div
            className={cn(
              "w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-0.5",
              isAssistant ? "bg-brand-primary text-white" : "bg-white/10 text-white"
            )}
          >
            {isAssistant ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
          </div>

          <div className="flex-1 min-w-0 py-1">
            <div
              className={cn(
                "text-[15px] leading-relaxed min-w-0 [&_p]:mb-2 [&_p:last-child]:mb-0 [&_ul]:my-2 [&_ol]:my-2 [&_li]:my-0.5 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_blockquote]:border-l-4 [&_blockquote]:border-current/30 [&_blockquote]:pl-3 [&_blockquote]:my-2 [&_h1]:text-xl [&_h2]:text-lg [&_h3]:text-base [&_h1]:font-semibold [&_h2]:font-semibold [&_h3]:font-semibold [&_h1]:mt-3 [&_h2]:mt-3 [&_h3]:mt-2 [&_table]:my-2 [&_table]:w-full [&_table]:text-sm [&_table]:border-collapse [&_th]:border [&_td]:border [&_th]:px-2 [&_td]:px-2 [&_th]:py-1 [&_td]:py-1",
                isAssistant ? "text-brand-text" : "text-white"
              )}
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
                {content}
              </ReactMarkdown>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
