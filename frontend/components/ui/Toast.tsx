"use client";

import { useEffect, useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import { useChatStore } from '../../lib/store';
import { cn } from '../../lib/utils';

export function Toast() {
  const { toast, hideToast } = useChatStore();
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    if (toast.isVisible && toast.type !== 'confirm') {
      setProgress(100);
      const duration = 4000;
      const interval = 10;
      const step = (interval / duration) * 100;

      // Progress interval
      const progressTimer = setInterval(() => {
        setProgress((prev) => Math.max(0, prev - step));
      }, interval);

      // Auto-hide timeout
      const hideTimer = setTimeout(() => {
        hideToast();
      }, duration);

      return () => {
        clearInterval(progressTimer);
        clearTimeout(hideTimer);
      };
    }
  }, [toast.isVisible, toast.type, hideToast]);

  if (!toast.isVisible) return null;

  const icons = {
    success: <CheckCircle className="w-5 h-5 text-emerald-500" />,
    error: <XCircle className="w-5 h-5 text-red-500" />,
    info: <Info className="w-5 h-5 text-blue-500" />,
    confirm: <AlertCircle className="w-6 h-6 text-brand-primary" />,
  };

  const bgColors = {
    success: 'bg-emerald-50/90 border-emerald-100',
    error: 'bg-red-50/90 border-red-100',
    info: 'bg-blue-50/90 border-blue-100',
    confirm: 'bg-white/95 border-brand-primary/20 shadow-2xl',
  };

  if (toast.type === 'confirm') {
    return (
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
        <div className={cn(
          "w-full max-w-md p-6 rounded-3xl border shadow-2xl bg-white scale-in-center animate-in zoom-in-95 duration-200",
          bgColors.confirm
        )}>
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center">
              {icons.confirm}
            </div>
            <h3 className="text-xl font-black tracking-tight text-slate-800">Please Confirm</h3>
          </div>
          
          <p className="text-slate-600 mb-8 leading-relaxed font-medium">
            {toast.message}
          </p>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                toast.onConfirm?.();
                hideToast();
              }}
              className="flex-1 py-3 px-6 bg-brand-primary text-white font-bold rounded-2xl hover:bg-brand-primary/90 transition-all active:scale-95 shadow-lg shadow-brand-primary/20"
            >
              {toast.confirmText || 'Confirm'}
            </button>
            <button
              onClick={hideToast}
              className="flex-1 py-3 px-6 bg-slate-100 text-slate-600 font-bold rounded-2xl hover:bg-slate-200 transition-all active:scale-95"
            >
              {toast.cancelText || 'Cancel'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[100] w-full max-w-sm px-4 animate-in slide-in-from-top-4 duration-300">
      <div className={cn(
        "relative flex items-center gap-3 p-4 rounded-2xl border shadow-xl backdrop-blur-md overflow-hidden",
        bgColors[toast.type as keyof typeof bgColors]
      )}>
        {/* Progress bar */}
        <div 
          className="absolute bottom-0 left-0 h-1 bg-brand-primary/20 transition-all duration-100 ease-linear"
          style={{ width: `${progress}%` }}
        />
        
        <div className="shrink-0">{icons[toast.type as keyof typeof icons]}</div>
        
        <p className="flex-1 text-sm font-bold text-slate-700 leading-tight">
          {toast.message}
        </p>

        <button 
          onClick={hideToast}
          className="p-1.5 rounded-lg hover:bg-black/5 transition-colors"
        >
          <X className="w-4 h-4 text-slate-400" />
        </button>
      </div>
    </div>
  );
}
