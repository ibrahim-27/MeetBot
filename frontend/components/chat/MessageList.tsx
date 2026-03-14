import { useEffect, useRef } from "react";
import { MessageBubble, type MessageProps } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";

interface MessageListProps {
  messages: MessageProps[];
  isTyping?: boolean;
  isLoadingMessages?: boolean;
}

export function MessageList({ messages, isTyping, isLoadingMessages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="h-full overflow-y-auto custom-scrollbar flex flex-col pt-4">
      {/* Loading Overlay or Bar */}
      {isLoadingMessages && (
        <div className="absolute top-0 left-0 w-full h-1 z-20">
          <div className="h-full bg-brand-primary animate-[loading_1.5s_infinite] origin-left"></div>
        </div>
      )}

      <div className="flex-1">
        {messages.length === 0 && !isLoadingMessages ? (
          <div className="h-full flex flex-col items-center justify-center opacity-40 mt-[10vh]">
            <div className="w-24 h-24 rounded-[2rem] bg-brand-primary/5 border-2 border-brand-primary/20 flex items-center justify-center mb-6 rotate-3 shadow-sm">
              <span className="text-5xl font-black text-brand-primary italic -rotate-6">M</span>
            </div>
            <h2 className="text-2xl font-black tracking-tight text-brand-primary mb-2">Welcome Back</h2>
            <p className="text-sm font-medium opacity-60">Ready to boost your productivity today?</p>
          </div>
        ) : (
          <>
            {!isLoadingMessages && messages.map((message, index) => (
              <MessageBubble key={index} role={message.role} content={message.content} />
            ))}
            {isTyping && <TypingIndicator />}
          </>
        )}
      </div>
      <div ref={bottomRef} className="h-12 shrink-0" />
    </div>
  );
}
