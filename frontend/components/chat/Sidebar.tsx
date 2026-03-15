"use client";

import Image from "next/image";
import { MessageSquare, Plus, User, LayoutDashboard, History, Trash } from "lucide-react";
import { cn } from "../../lib/utils";

import { useEffect } from "react";
import { useChatStore } from "../../lib/store";

export function Sidebar() {
  const { 
    sessions, 
    currentChatId, 
    setChatId, 
    fetchSessions, 
    clearMessages,
    isLoadingSessions,
    logout,
    deleteSession,
    showToast
  } = useChatStore();

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  const handleNewSession = () => {
    setChatId(null);
    clearMessages();
  };

  const handleDeleteSession = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    showToast({
      type: 'confirm',
      message: 'Are you sure you want to delete this session? This action cannot be undone.',
      confirmText: 'Delete Session',
      onConfirm: async () => {
        await deleteSession(id);
      }
    });
  };

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
        <button 
          onClick={handleNewSession}
          className="flex items-center gap-3 w-full px-4 py-3 text-sm font-bold transition-all bg-white text-brand-primary rounded-2xl shadow-lg hover:bg-slate-50 group active:scale-95"
        >
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
        
        {isLoadingSessions ? (
          <div className="px-4 py-2 text-xs text-white/40 animate-pulse">Loading history...</div>
        ) : sessions.length === 0 ? (
          <div className="px-4 py-2 text-xs text-white/40 italic">No sessions yet</div>
        ) : (
          sessions.map((chat) => (
            <div
              key={chat.id}
              className={cn(
                "flex items-center gap-3 w-full px-4 py-1 text-sm transition-all rounded-xl group overflow-hidden active:scale-[0.98]",
                currentChatId === chat.id ? "bg-white/20 text-white" : "text-white/80 hover:bg-white/10 hover:text-white"
              )}
            >
              <button
                onClick={() => setChatId(chat.id)}
                className="flex items-center gap-3 flex-1 px-4 py-2 text-left overflow-hidden"
              >
                <MessageSquare className="w-4 h-4 shrink-0 opacity-70 group-hover:opacity-100 transition-opacity" />
                <span className="truncate font-medium">{chat.title}</span>
              </button>
              <button
                onClick={(e) => handleDeleteSession(e, chat.id)}
                className="p-1 mr-2 hover:bg-white/20 rounded-md transition-all opacity-0 group-hover:opacity-100 shrink-0"
              >
                <Trash className="w-3.5 h-3.5" />
              </button>
            </div>
          ))
        )}
      </nav>

      {/* User / Settings Section */}
      <div className="p-4 bg-black/10 border-t border-white/10 space-y-2">
        <div className="flex items-center gap-3 w-full px-4 py-3">
          <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-white border border-white/20">
            <User className="w-5 h-5" />
          </div>
          <div className="flex flex-col items-start overflow-hidden text-left">
            <span className="font-bold text-sm text-white">Admin</span>
            <span className="text-[10px] text-white/80 truncate w-full italic">MeetBot Org</span>
          </div>
        </div>
        
        <button 
          onClick={logout}
          className="flex items-center gap-3 w-full px-4 py-2 text-xs transition-all rounded-xl hover:bg-red-500/20 text-white/60 hover:text-red-300 active:scale-[0.98] font-bold group"
        >
          <div className="w-6 h-6 rounded-md bg-white/5 flex items-center justify-center group-hover:bg-red-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          </div>
          Logout
        </button>
      </div>
    </aside>
  );
}
