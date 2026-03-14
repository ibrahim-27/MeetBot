"use client";

import { useState } from "react";
import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { Sidebar } from "./Sidebar";
import type { MessageProps } from "./MessageBubble";
import { Menu } from "lucide-react";

export function ChatContainer() {
  const [messages, setMessages] = useState<MessageProps[]>([
    {
      role: "assistant",
      content: "Hello! I am your MeetBot. How can I help you today?"
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async (content: string) => {
    // Add user message immediately
    const userMessage: MessageProps = { role: "user", content };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    
    setIsTyping(true);
    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: updatedMessages.map(msg => ({
            role: msg.role,
            content: msg.content
          }))
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from MeetBot");
      }

      const data = await response.json();
      const assistantMessage: MessageProps = {
        role: "assistant",
        content: data.content,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: MessageProps = {
        role: "assistant",
        content: "Sorry, I'm having trouble connecting right now. Please try again later.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
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
