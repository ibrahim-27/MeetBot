"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useChatStore } from "../../lib/store";
import { Lock, User, ArrowRight } from "lucide-react";

function formatLoginError(detail: unknown, status: number): string {
  if (status === 401) {
    return "Incorrect username or password. Check what you typed and try again.";
  }
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) =>
        typeof item === "object" && item !== null && "msg" in item
          ? String((item as { msg: string }).msg)
          : String(item)
      )
      .join(" ");
  }
  return "Something went wrong. Please try again.";
}

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  
  const { login, isAuthenticated, showToast } = useChatStore();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push("/");
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setFormError(null);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        let detail: unknown;
        try {
          detail = (await response.json()).detail;
        } catch {
          detail = undefined;
        }
        const message = formatLoginError(detail, response.status);
        setFormError(message);
        showToast({ type: "error", message });
        return;
      }

      const data = await response.json();
      login(data.access_token);
      showToast({ type: "success", message: "Successfully logged in!" });
      router.push("/");
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Network error. Is the API running?";
      setFormError(message);
      showToast({ type: "error", message });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-white flex items-center justify-center p-6 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-teal-50 via-white to-white">
      <div className="w-full max-w-[440px] animate-in fade-in slide-in-from-bottom-4 duration-1000">
        {/* Brand Header */}
        <div className="flex flex-col items-center mb-10 text-center">
          <div className="relative w-20 h-20 rounded-[2.5rem] overflow-hidden shadow-2xl border-4 border-white bg-white mb-6 rotate-3">
            <img 
              src="/logo.png" 
              alt="MeetBot Logo" 
              className="w-full h-full object-contain p-3"
            />
          </div>
          <h1 className="text-4xl font-black tracking-tighter text-brand-text mb-2">Welcome Back</h1>
          <p className="text-slate-500 font-medium">Log in to your MeetBot organization</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-[2.5rem] p-10 shadow-[0_32px_64px_-16px_rgba(49,164,155,0.15)] border border-slate-100 relative overflow-hidden group">
          {/* Subtle Accent */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-brand-primary/5 rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-110 duration-700"></div>
          
          <form onSubmit={handleSubmit} className="space-y-6 relative z-10">

            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-slate-400 ml-1">Username</label>
              <div className="relative group/input">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within/input:text-brand-primary transition-colors">
                  <User size={18} />
                </div>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-50 border-2 border-transparent focus:border-brand-primary/20 focus:bg-white rounded-2xl py-4 pl-12 pr-4 outline-none transition-all text-brand-text font-medium placeholder:text-slate-300"
                  placeholder="admin"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-slate-400 ml-1">Password</label>
              <div className="relative group/input">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within/input:text-brand-primary transition-colors">
                  <Lock size={18} />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-50 border-2 border-transparent focus:border-brand-primary/20 focus:bg-white rounded-2xl py-4 pl-12 pr-4 outline-none transition-all text-brand-text font-medium placeholder:text-slate-300"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {formError && (
              <p
                className="text-sm text-red-600 font-medium text-center bg-red-50 border border-red-100 rounded-2xl py-3 px-4"
                role="alert"
              >
                {formError}
              </p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-brand-primary py-4 rounded-2xl text-white font-black text-lg shadow-xl shadow-teal-500/30 hover:bg-brand-primary-hover active:scale-[0.98] transition-all flex items-center justify-center gap-3 group/btn"
            >
              {isLoading ? (
                <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Footer info */}
        <p className="mt-12 text-center text-sm text-slate-400 font-medium">
          Secured by <span className="text-brand-primary font-bold">MeetBot Enterprise</span>
        </p>
      </div>
    </div>
  );
}
