"use client";

import { useEffect } from "react";
import { useChatStore } from "../../lib/store";
import { Sidebar } from "./Sidebar";
import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { Menu } from "lucide-react";

export function ChatContainer() {
  const { 
    messages, 
    isTyping, 
    sendMessage, 
    currentChatId, 
    clearMessages 
  } = useChatStore();

  // If we're on a new session (currentChatId is null), clear messages
  useEffect(() => {
    if (!currentChatId) {
      clearMessages();
    }
  }, [currentChatId, clearMessages]);

  const handleSendMessage = async (content: string) => {
    await sendMessage(content);
  };

  return (
    <div className="flex h-screen w-full overflow-hidden p-0 bg-white">
      <Sidebar />
      
      <main className="flex-1 flex flex-col relative overflow-hidden bg-white shrink-1 min-w-0">
        {/* Dashboard Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-100">
          <div className="flex items-center gap-4">
            <button className="md:hidden p-2 hover:bg-slate-50 rounded-xl transition-colors text-brand-primary">
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-xl font-black tracking-tight text-brand-text">Discussion Room</h1>
          </div>
          
          <div className="hidden sm:flex items-center gap-2">
            <div className="px-4 py-1.5 rounded-full bg-slate-50 text-brand-primary text-[10px] font-bold uppercase tracking-wider border border-slate-100">
              Live Session
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 w-full overflow-hidden">
          <MessageList messages={messages} isTyping={isTyping} />
        </div>

        {/* Input Area */}
        <div className="w-full max-w-4xl mx-auto px-6 pb-8">
          <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
        </div>
      </main>
    </div>
  );
}
