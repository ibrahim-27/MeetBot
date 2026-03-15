import { create } from 'zustand';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export type ToastType = 'success' | 'error' | 'info' | 'confirm';

export interface ToastState {
  isVisible: boolean;
  message: string;
  type: ToastType;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

interface ChatState {
  // Auth State
  token: string | null;
  isAuthenticated: boolean;
  
  // UI State
  toast: ToastState;

  // Chat State
  sessions: Session[];
  currentChatId: string | null;
  messages: Message[];
  isTyping: boolean;
  isLoadingSessions: boolean;
  isLoadingMessages: boolean;
  
  // Actions
  login: (token: string) => void;
  logout: () => void;
  deleteSession: (id: string) => Promise<void>;
  setChatId: (id: string | null) => void;
  fetchSessions: () => Promise<void>;
  fetchMessages: (chatId: string) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  showToast: (options: Omit<ToastState, 'isVisible'>) => void;
  hideToast: () => void;
  handleAuthError: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  // Auth State
  token: typeof window !== 'undefined' ? localStorage.getItem('meetbot_token') : null,
  isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('meetbot_token') : false,

  // UI State
  toast: {
    isVisible: false,
    message: '',
    type: 'info',
  },

  // Chat State
  sessions: [],
  currentChatId: null,
  messages: [],
  isTyping: false,
  isLoadingSessions: false,
  isLoadingMessages: false,

  // UI Actions
  showToast: (options: Omit<ToastState, 'isVisible'>) => {
    set({ toast: { ...options, isVisible: true } });
  },
  hideToast: () => {
    set((state) => ({ toast: { ...state.toast, isVisible: false } }));
  },

  handleAuthError: () => {
    get().logout();
    get().showToast({ 
      type: 'error', 
      message: 'Your session has expired. Please log in again.' 
    });
  },

  // Auth Actions
  login: (token) => {
    localStorage.setItem('meetbot_token', token);
    set({ token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('meetbot_token');
    set({ token: null, isAuthenticated: false, sessions: [], messages: [], currentChatId: null });
  },

  deleteSession: async (id: string) => {
    const { token, currentChatId, fetchSessions } = get();
    if (!token) return;

    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete session');
      }

      // If deleted session was the active one, clear state
      if (currentChatId === id) {
        set({ currentChatId: null, messages: [] });
      }

      // Refresh session list
      await fetchSessions();
      get().showToast({ type: 'success', message: 'Session deleted successfully' });
    } catch (error: any) {
      console.error('Error deleting session:', error);
      get().showToast({ type: 'error', message: error.message });
    }
  },

  setChatId: (id) => {
    set({ currentChatId: id });
    if (id) {
      get().fetchMessages(id);
    } else {
      get().clearMessages();
    }
  },

  fetchSessions: async () => {
    const { token } = get();
    if (!token) return;

    set({ isLoadingSessions: true });
    try {
      const response = await fetch('http://localhost:8000/api/sessions', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        if (response.status === 401) {
          get().handleAuthError();
          return;
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to fetch sessions (${response.status})`);
      }
      const data = await response.json();
      set({ sessions: data });
    } catch (error: any) {
      console.error('Error fetching sessions:', error);
      get().showToast({ type: 'error', message: error.message });
    } finally {
      set({ isLoadingSessions: false });
    }
  },

  fetchMessages: async (chatId: string) => {
    const { token } = get();
    if (!token) return;

    set({ isLoadingMessages: true });
    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${chatId}/messages`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        if (response.status === 401) {
          get().handleAuthError();
          return;
        }
        throw new Error('Failed to fetch messages');
      }
      const data = await response.json();
      set({ messages: data });
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      set({ isLoadingMessages: false });
    }
  },

  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),

  clearMessages: () => set({ messages: [] }),

  sendMessage: async (content: string) => {
    const { currentChatId, addMessage, token } = get();
    if (!token) return;
    
    // 1. Add user message to UI immediately
    const userMessage: Message = { role: 'user', content };
    addMessage(userMessage);
    set({ isTyping: true });

    try {
      // 2. Post to API
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          messages: [...get().messages],
          chat_id: currentChatId
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          get().handleAuthError();
          return;
        }
        throw new Error('Failed to send message');
      }
      
      const data = await response.json();
      
      // If this was a new session, capture the returned chat ID
      if (!currentChatId && data.chat_id) {
        set({ currentChatId: data.chat_id });
      }

      // 3. Add assistant message to UI
      const assistantMessage: Message = { 
        role: 'assistant', 
        content: data.content 
      };
      addMessage(assistantMessage);
      
      // 4. Refresh sessions to get potential new title/ID
      await get().fetchSessions();
      
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({ role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' });
    } finally {
      set({ isTyping: false });
    }
  },
}));
