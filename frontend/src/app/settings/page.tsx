"use client";

import { useState, useEffect } from "react";
import Header from "@/components/Header";
import { Settings, Key, Bell, Moon, Shield, Save, Crown } from "lucide-react";
import { API_BASE_URL } from "@/lib/config";

export default function SettingsPage() {
    const [isPro, setIsPro] = useState(false);
    const [secretCount, setSecretCount] = useState(0);

    // [New] Telegram Config State
    const [telegramId, setTelegramId] = useState("");
    const [loadingConfig, setLoadingConfig] = useState(false);
    const [configError, setConfigError] = useState("");

    // [New] Market Close Briefing State
    const [isSummaryEnabled, setIsSummaryEnabled] = useState(false);

    useEffect(() => {
        const saved = localStorage.getItem("isPro");
        if (saved === "true") setIsPro(true);

        const savedTg = localStorage.getItem("telegramId");
        if (savedTg) setTelegramId(savedTg);

        // Fetch Alert Status
        const fetchAlertStatus = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/alerts`);
                const json = await res.json();
                if (json.status === "success") {
                    // Check if WATCHLIST_SUMMARY exists for "guest" (or current user logic if we had auth)
                    // Since we don't have robust auth on frontend yet for this specific logic, we assume backend filtering works or we just check type.
                    // Ideally we match user_id but local storage user might not match exactly if we use "guest".
                    // Let's just check if ANY WATCHLIST_SUMMARY alert exists for now as a simple toggle state.
                    const hasSummary = json.data.some((a: any) => a.type === "WATCHLIST_SUMMARY");
                    setIsSummaryEnabled(hasSummary);
                }
            } catch (e) {
                console.error("Failed to fetch alerts", e);
            }
        };
        fetchAlertStatus();
    }, []);

    const findMyTelegramId = async () => {
        setLoadingConfig(true);
        setConfigError("");
        try {
            const res = await fetch(`${API_BASE_URL}/api/telegram/recent-users`);
            const json = await res.json();
            if (json.status === "success" && json.data.length > 0) {
                // 가장 최근 사용자 (첫번째) 선택
                const user = json.data[0];
                setTelegramId(user.id);
                localStorage.setItem("telegramId", user.id);
                alert(`ID found! Connected as ${user.name}`);
            } else {
                setConfigError("최근 메시지를 찾을 수 없습니다. 봇에게 메시지를 보냈는지 확인하세요.");
            }
        } catch (e) {
            setConfigError("서버 연결 실패");
        } finally {
            setLoadingConfig(false);
        }
    };

    const handleSummaryToggle = async () => {
        if (!telegramId) {
            alert("먼저 텔레그램 Chat ID를 설정해주세요.");
            return;
        }

        const newState = !isSummaryEnabled;
        setIsSummaryEnabled(newState);

        try {
            if (newState) {
                // Subscribe
                await fetch(`${API_BASE_URL}/api/alerts/summary`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ chat_id: telegramId })
                });
            } else {
                // Unsubscribe
                await fetch(`${API_BASE_URL}/api/alerts/summary`, {
                    method: "DELETE"
                });
            }
        } catch (e) {
            console.error(e);
            setIsSummaryEnabled(!newState); // Revert on error
            alert("설정 변경에 실패했습니다.");
        }
    };

    const togglePro = () => {
        const newVal = !isPro;
        setIsPro(newVal);
        localStorage.setItem("isPro", String(newVal));
    };

    const handleSecretTap = () => {
        const newCount = secretCount + 1;
        setSecretCount(newCount);

        if (newCount === 7) {
            const newVal = !isPro;
            setIsPro(newVal);
            localStorage.setItem("isPro", String(newVal));
            alert(newVal ? "👑 Developer Mode Activated! (Ads Removed)" : "Developer Mode Disabled.");
            setSecretCount(0);
        }
    };

    return (
        <div className="min-h-screen pb-10 text-white">
            <Header title="Settings" subtitle="Configure your AI preferences and API keys" />

            <div className="p-6 max-w-4xl mx-auto space-y-8">

                {/* Developer Mode Card (Only visible if ALREADY Pro, so admin can toggle off) */}
                {isPro && (
                    <div className="rounded-3xl bg-gradient-to-r from-gray-900 to-black border border-white/10 p-8 relative overflow-hidden animate-in fade-in slide-in-from-top-4 duration-500">
                        <div className="absolute top-0 right-0 p-6 opacity-20">
                            <Crown className="w-24 h-24 text-yellow-500" />
                        </div>
                        <div className="relative z-10 flex items-center justify-between">
                            <div>
                                <h3 className="text-xl font-bold mb-2 flex items-center gap-2 text-yellow-400">
                                    <Crown className="w-5 h-5 fill-yellow-400" /> Developer Mode (Pro)
                                </h3>
                                <p className="text-gray-400 text-sm max-w-md">
                                    현재 <strong>운영자 권한</strong>이 활성화되었습니다. 모든 광고가 제거됩니다.
                                </p>
                            </div>
                            <button
                                onClick={togglePro}
                                className="px-6 py-3 rounded-xl font-bold bg-yellow-500 text-black hover:bg-yellow-400 transition-all shadow-lg shadow-yellow-500/20"
                            >
                                ACTIVATED
                            </button>
                        </div>
                    </div>
                )}

                {/* API Configuration */}
                <div className="rounded-3xl bg-black/20 border border-white/10 p-8">
                    <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                        <Key className="w-5 h-5 text-blue-400" /> API Connections
                    </h3>

                    <div className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">OpenAI API Key (for Analysis)</label>
                            <div className="relative">
                                <input type="password" value="sk-xxxxxxxxxxxxxxxxxxxxxxxx" disabled className="w-full h-12 rounded-xl bg-white/5 border border-white/10 px-4 text-gray-400 font-mono text-sm opacity-50" />
                                <button className="absolute right-3 top-1/2 -translate-y-1/2 text-xs bg-blue-600 px-3 py-1 rounded-lg hover:bg-blue-500">Edit</button>
                            </div>
                            <p className="text-xs text-gray-500">Used to generate daily briefings and sentiment analysis.</p>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">Brokerage API (Korea Investment / Kiwoom)</label>
                            <div className="relative">
                                <input type="password" value="APP-xxxxxxxx-xxxx" disabled className="w-full h-12 rounded-xl bg-white/5 border border-white/10 px-4 text-gray-400 font-mono text-sm opacity-50" />
                                <button className="absolute right-3 top-1/2 -translate-y-1/2 text-xs bg-blue-600 px-3 py-1 rounded-lg hover:bg-blue-500">Edit</button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Mobile Notification Setup */}
                <div className="rounded-3xl bg-black/20 border border-white/10 p-8">
                    <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                        <Bell className="w-5 h-5 text-green-400" /> Mobile Notification (Telegram)
                    </h3>
                    <div className="space-y-6">
                        <div className="bg-white/5 p-4 rounded-xl border border-white/10 text-sm text-gray-300 leading-relaxed">
                            <p className="mb-2"><strong className="text-white">1단계:</strong> 텔레그램 앱에서 <strong className="text-yellow-400">@rnfjrlAlarm_bot</strong> 을 검색하세요.</p>
                            <p className="mb-2"><strong className="text-white">2단계:</strong> 봇에게 아무 메시지나 보내세요. (예: &quot;hello&quot;)</p>
                            <p><strong className="text-white">3단계:</strong> 아래 <strong className="text-blue-400">&apos;내 ID 찾기&apos;</strong> 버튼을 누르면 자동으로 ID가 입력됩니다.</p>
                        </div>

                        <div className="flex gap-3">
                            <div className="relative flex-1">
                                <input
                                    type="text"
                                    value={telegramId}
                                    onChange={(e) => {
                                        setTelegramId(e.target.value);
                                        localStorage.setItem("telegramId", e.target.value);
                                    }}
                                    placeholder="Telegram Chat ID (숫자)"
                                    className="w-full h-12 rounded-xl bg-white/5 border border-white/10 px-4 text-white font-mono text-sm focus:ring-2 focus:ring-green-500 outline-none"
                                />
                                {telegramId && (
                                    <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500 flex items-center gap-1 text-xs font-bold">
                                        <Shield className="w-3 h-3" /> Connected
                                    </div>
                                )}
                            </div>
                            <button
                                onClick={findMyTelegramId}
                                disabled={loadingConfig}
                                className="bg-green-600 hover:bg-green-500 text-white px-6 rounded-xl font-bold text-sm transition-colors disabled:opacity-50 whitespace-nowrap"
                            >
                                {loadingConfig ? "찾는 중..." : "내 ID 찾기"}
                            </button>
                        </div>
                        {configError && <p className="text-red-400 text-xs">{configError}</p>}

                        {/* Summary Toggle */}
                        {telegramId && (
                            <div className="pt-4 border-t border-white/10 flex items-center justify-between">
                                <div>
                                    <h4 className="font-bold text-white mb-1">장 마감 브리핑 받기</h4>
                                    <p className="text-xs text-gray-400">관심종목의 마감 시세를 매일 자동으로 받아봅니다. (15:40)</p>
                                </div>
                                <button
                                    onClick={handleSummaryToggle}
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${isSummaryEnabled ? 'bg-green-500' : 'bg-gray-700'}`}
                                >
                                    <span
                                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${isSummaryEnabled ? 'translate-x-6' : 'translate-x-1'}`}
                                    />
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* Preferences */}
                <div className="rounded-3xl bg-black/20 border border-white/10 p-8">
                    <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                        <Settings className="w-5 h-5 text-purple-400" /> Preferences
                    </h3>

                    <div className="space-y-4">
                        {[
                            { icon: Bell, title: "Price Alerts", desc: "Push notifications for sudden price drops" },
                            { icon: Shield, title: "Risk Auto-Check", desc: "Daily automatic portfolio health scan" },
                            { icon: Moon, title: "Dark Mode", desc: "Always use dark theme (System default)" },
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-transparent hover:border-white/10 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="p-2 rounded-lg bg-white/10 text-gray-300">
                                        <item.icon className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-sm">{item.title}</h4>
                                        <p className="text-xs text-gray-500">{item.desc}</p>
                                    </div>
                                </div>
                                <div className="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-600 cursor-pointer">
                                    <span className="inline-block h-4 w-4 transform translate-x-6 rounded-full bg-white transition" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Save Button */}
                <div className="flex justify-end pt-4">
                    <button className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-4 rounded-xl font-bold hover:shadow-lg hover:shadow-blue-500/20 transition-all active:scale-95">
                        <Save className="w-5 h-5" /> Save Changes
                    </button>
                </div>

                {/* Secret Trigger Area */}
                <div
                    onClick={handleSecretTap}
                    className="mt-10 py-10 text-center text-gray-800 hover:text-gray-700 transition-colors cursor-default select-none text-xs font-mono"
                >
                    ANTIGRAVITY v1.1.0 (Build 20251231)
                </div>

            </div>
        </div>
    );
}
