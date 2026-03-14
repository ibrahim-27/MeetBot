"use client";

import Image from "next/image";
import { MessageSquare, Plus, User, LayoutDashboard, History } from "lucide-react";
import { cn } from "../../lib/utils";

interface Conversation {
  id: string;
  title: string;
}

const HARDCODED_CONVERSATIONS: Conversation[] = [
  { id: "1", title: "Meeting Notes Summary" },
  { id: "2", title: "Project Brainstorming" },
  { id: "3", title: "Client Call Follow-up" },
  { id: "4", title: "Technical Architecture" },
];

export function Sidebar() {
  return (
    <aside className="hidden md:flex flex-col w-[280px] h-full bg-brand-primary text-white shrink-0">
      {/* Brand Header */}
      <div className="p-6 flex items-center gap-3">
        <div className="relative w-10 h-10 rounded-xl overflow-hidden shadow-lg border border-white/10 bg-white">
          <Image 
            src="/logo.png" 
            alt="MeetBot Logo" 
            fill
            className="object-contain p-1.5"
          />
        </div>
        <span className="font-bold text-xl tracking-tight text-white/95">MeetBot</span>
      </div>

      {/* Primary Actions */}
      <div className="px-4 mb-6">
        <button className="flex items-center gap-3 w-full px-4 py-3 text-sm font-bold transition-all bg-white text-brand-primary rounded-2xl shadow-lg hover:bg-slate-50 group">
          <Plus className="w-4 h-4" />
          <span>New Session</span>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-4 py-2 space-y-1 custom-scrollbar">
        <div className="flex items-center gap-2 px-4 py-2 mb-2 text-[10px] font-bold text-white/60 uppercase tracking-[2px]">
          <History className="w-3 h-3" />
          <span>Recent History</span>
        </div>
        
        {HARDCODED_CONVERSATIONS.map((chat) => (
          <button
            key={chat.id}
            className="flex items-center gap-3 w-full px-4 py-3 text-sm transition-all rounded-xl hover:bg-white/20 text-left group overflow-hidden text-white hover:text-white active:scale-[0.98]"
          >
            <MessageSquare className="w-4 h-4 shrink-0 opacity-70 group-hover:opacity-100 transition-opacity" />
            <span className="truncate font-medium">{chat.title}</span>
          </button>
        ))}
      </nav>

      {/* User / Settings Section */}
      <div className="p-4 bg-black/10 border-t border-white/10">
        <button className="flex items-center gap-3 w-full px-4 py-3 text-sm transition-all rounded-xl hover:bg-white/20 text-white hover:text-white active:scale-[0.98]">
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center text-white border border-white/20">
            <User className="w-5 h-5" />
          </div>
          <div className="flex flex-col items-start overflow-hidden text-left">
            <span className="font-bold text-sm text-white">John Doe</span>
            <span className="text-[10px] text-white/80 truncate w-full italic">Premium Member</span>
          </div>
        </button>
      </div>
    </aside>
  );
}
