import { create } from 'zustand';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface Session {
  id: string;
  title: string;
}

interface ChatState {
  sessions: Session[];
  currentChatId: string | null;
  messages: Message[];
  isTyping: boolean;
  isLoadingSessions: boolean;
  
  // Actions
  setChatId: (id: string | null) => void;
  fetchSessions: () => Promise<void>;
  fetchMessages: (chatId: string) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  addMessage: (message: Message) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  currentChatId: null,
  messages: [],
  isTyping: false,
  isLoadingSessions: false,

  setChatId: (id) => {
    set({ currentChatId: id });
    if (id) {
      get().fetchMessages(id);
    } else {
      get().clearMessages();
    }
  },

  fetchSessions: async () => {
    set({ isLoadingSessions: true });
    try {
      const response = await fetch('http://localhost:8000/api/sessions');
      if (!response.ok) throw new Error('Failed to fetch sessions');
      const data = await response.json();
      set({ sessions: data });
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      set({ isLoadingSessions: false });
    }
  },

  fetchMessages: async (chatId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${chatId}/messages`);
      if (!response.ok) throw new Error('Failed to fetch messages');
      const data = await response.json();
      set({ messages: data });
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  },

  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),

  clearMessages: () => set({ messages: [] }),

  sendMessage: async (content: string) => {
    const { currentChatId, addMessage } = get();
    
    // 1. Add user message to UI immediately
    const userMessage: Message = { role: 'user', content };
    addMessage(userMessage);
    set({ isTyping: true });

    try {
      // 2. Post to API
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...get().messages], // Send full context if needed or just new one
          chat_id: currentChatId
        }),
      });

      if (!response.ok) throw new Error('Failed to send message');
      
      const data = await response.json();

      // 3. Add assistant message to UI
      const assistantMessage: Message = { 
        role: 'assistant', 
        content: data.content 
      };
      addMessage(assistantMessage);
      
      // 4. Refresh sessions to get potential new title/ID
      await get().fetchSessions();
      
      // 5. If it's a new session, we should ideally get the ID from the response
      // For now, let's assume the API returns it or we manage it
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({ role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' });
    } finally {
      set({ isTyping: false });
    }
  },
}));
