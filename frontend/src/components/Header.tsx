"use client";

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { Search, Bell, User, BarChart2, ShieldAlert, Sparkles, LineChart, UserCheck, Users } from "lucide-react";
import { useEffect, useRef } from 'react';
import { API_BASE_URL } from "@/lib/config";
import { useAuth } from "@/context/AuthContext";

interface HeaderProps {
    title?: string;
    subtitle?: string;
    onSearch?: (term: string) => void;
}

export default function Header({ title = "대시보드", subtitle = "환영합니다, 투자자님", onSearch }: HeaderProps) {
    const pathname = usePathname();
    const { user } = useAuth();

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && onSearch) {
            onSearch(e.currentTarget.value);
        }
    };

    // [New] Real-time Alert Polling
    useEffect(() => {
        const checkAlerts = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/alerts`);
                const json = await res.json();
                if (json.status === "success") {
                    const triggered = json.data.filter((a: any) => a.status === "triggered");

                    // Check local storage to see if we already notified this specific trigger
                    // Trigger ID usually is timestamp, but triggered_at is better unique key for the event
                    const lastSeen = JSON.parse(localStorage.getItem("seenAlerts") || "[]");
                    const newTriggers = triggered.filter((a: any) => !lastSeen.includes(a.id + "_" + a.triggered_at));

                    if (newTriggers.length > 0) {
                        // Play Alert Sound
                        try {
                            const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
                            const osc = ctx.createOscillator();
                            const gain = ctx.createGain();
                            osc.connect(gain);
                            gain.connect(ctx.destination);

                            // Ding-Dong effect
                            osc.frequency.setValueAtTime(880, ctx.currentTime); // High
                            osc.frequency.exponentialRampToValueAtTime(500, ctx.currentTime + 0.5); // Low
                            gain.gain.setValueAtTime(0.5, ctx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);

                            osc.start();
                            osc.stop(ctx.currentTime + 0.6);
                        } catch (e) {
                            console.error("Audio block", e);
                        }

                        // Browser Notification (Toast style via window.alert for now, simplest to force attention)
                        // In a real app we would use a Toast component, but alert() is effective for forcing user to see it.
                        // Or we can just log it if we want to be less intrusive, but user asked for ALERTS.

                        // Let's use simple alert for v1
                        const msg = `🚨 [가격 알림] ${newTriggers[0].symbol} 목표가 도달!\n현재가: ${newTriggers[0].triggered_price}\n목표가: ${newTriggers[0].target_price}`;
                        // We use setTimeout to let UI render/sound play before blocking with alert
                        setTimeout(() => alert(msg), 100);

                        // Mark as seen
                        const updatedSeen = [...lastSeen, ...newTriggers.map((a: any) => a.id + "_" + a.triggered_at)];
                        localStorage.setItem("seenAlerts", JSON.stringify(updatedSeen));
                    }
                }
            } catch (e) {
                // Ignore fetch errors
            }
        };

        const interval = setInterval(checkAlerts, 10000); // Check every 10s
        checkAlerts(); // Run immediately on mount
        return () => clearInterval(interval);
    }, []);

    return (
        <header className="flex flex-col md:flex-row items-center justify-between p-6 border-b border-white/5 bg-black/40 backdrop-blur-md sticky top-0 z-50 transition-all duration-200">
            <div className="flex items-center gap-8 w-full md:w-auto mb-4 md:mb-0">
                <div>
                    <h1 className="text-2xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                        ANTIGRAVITY
                    </h1>
                    <p className="text-xs text-gray-400 font-mono tracking-widest uppercase">AI Stock Analyst</p>
                </div>

                {/* Navigation moved to Sidebar */}
            </div>

            <div className="flex items-center gap-4 w-full md:w-auto">
                <div className="relative group w-full md:w-auto">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 group-focus-within:text-blue-400 transition-colors" />
                    <input
                        type="text"
                        placeholder="종목 검색 (예: AAPL)..."
                        onKeyDown={handleKeyDown}
                        className="h-10 w-full md:w-64 rounded-xl bg-white/5 pl-10 pr-4 text-sm outline-none ring-1 ring-white/10 transition-all focus:ring-2 focus:ring-blue-500/50 focus:bg-white/10 text-gray-200 placeholder-gray-500"
                    />
                </div>

                <div className="flex items-center gap-2">
                    <button className="relative rounded-xl bg-white/5 p-2.5 transition-colors hover:bg-white/10 hover:text-blue-400 border border-white/5">
                        <Bell className="h-5 w-5 text-gray-400" />
                        <span className="absolute right-2.5 top-2.5 h-2 w-2 rounded-full bg-red-500 animate-pulse ring-2 ring-black" />
                    </button>
                    <button className="rounded-xl border border-white/5 bg-white/5 p-1 flex items-center gap-2 pr-3 hover:bg-white/10 transition-colors">
                        {user ? (
                            <>
                                {user.picture ? (
                                    <img
                                        src={user.picture}
                                        alt={user.name}
                                        className="h-8 w-8 rounded-lg object-cover border border-white/10"
                                    />
                                ) : (
                                    <div className="rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 p-1.5">
                                        <User className="h-4 w-4 text-white" />
                                    </div>
                                )}
                                <span className="text-sm font-medium text-gray-300 hidden md:block">{user.name}</span>
                            </>
                        ) : (
                            <>
                                <div className="rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 p-1.5">
                                    <User className="h-4 w-4 text-white" />
                                </div>
                                <span className="text-sm font-medium text-gray-300 hidden md:block">투자자</span>
                            </>
                        )}
                    </button>
                </div>
            </div>
        </header>
    );
}
