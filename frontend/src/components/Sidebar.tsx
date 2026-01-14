"use client";

import { API_BASE_URL } from "@/lib/config";
import Link from "next/link";
import React, { useState, useEffect } from "react";
import { LayoutDashboard, Newspaper, Compass, Settings, Bell, MessageSquare, LineChart, Crown, Zap, X, Network, Sparkles, UserCheck, Shield, CalendarDays, Star, Menu } from "lucide-react";
import MarketClock from "./MarketClock";
import { requestPayment } from "@/lib/payment";
import { useAuth } from "@/context/AuthContext";
import LoginModal from "./LoginModal";

const navigation = [
    { name: "대시보드", href: "/", icon: LayoutDashboard },
    { name: "경제/공모주 일정", href: "/schedule", icon: CalendarDays },

    { name: "종목 발굴", href: "/discovery", icon: Compass },
    { name: "이슈 테마", href: "/theme", icon: Sparkles },
    { name: "차트 분석", href: "/pattern", icon: LineChart },
    { name: "AI 코치", href: "/coach", icon: UserCheck },
    { name: "공급망 지도", href: "/supply-chain", icon: Network },
    { name: "상담 챗봇", href: "/chat", icon: MessageSquare },
    { name: "포트폴리오", href: "/portfolio", icon: Shield },
    { name: "MY 관심종목", href: "/watchlist", icon: Star },
    { name: "가격 알림", href: "/alerts", icon: Bell },
    { name: "설정", href: "/settings", icon: Settings },
];

export default function Sidebar() {
    const { user, logout } = useAuth();
    const [showLoginModal, setShowLoginModal] = useState(false);
    const [showProModal, setShowProModal] = useState(false);
    const [exchangeRate, setExchangeRate] = useState<number>(1450); // Default fallback

    useEffect(() => {
        fetch(`${API_BASE_URL}/api/market/status`)
            .then(res => res.json())
            .then(data => {
                if (data.status === "success" && data.data.details?.usd) {
                    const rate = parseFloat(data.data.details.usd.replace(/,/g, ''));
                    if (!isNaN(rate)) setExchangeRate(rate);
                }
            })
            .catch(err => console.error(err));
    }, []);

    const proPriceUsd = 3.5;
    const proPriceKrw = Math.floor(proPriceUsd * exchangeRate / 10) * 10; // 10원 단위 절사
    const [isMobileOpen, setIsMobileOpen] = useState(false);

    return (
        <>
            {/* Mobile Toggle Button */}
            <button
                onClick={() => setIsMobileOpen(true)}
                className="md:hidden fixed top-8 left-4 z-[100] p-2 rounded-lg bg-black/80 text-white border border-white/20 hover:bg-white/10 backdrop-blur-md shadow-xl"
            >
                <Menu className="h-6 w-6" />
            </button>

            {/* Mobile Overlay */}
            {isMobileOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black/80 backdrop-blur-sm md:hidden"
                    onClick={() => setIsMobileOpen(false)}
                />
            )}

            <div className={`
                fixed inset-y-0 left-0 z-50 h-full w-80 flex flex-col justify-between border-r border-white/10 bg-[#050505] md:bg-black/40 backdrop-blur-xl text-white p-4 transition-transform duration-300 ease-in-out
                md:relative md:translate-x-0 md:flex
                ${isMobileOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full md:translate-x-0'}
            `}>
                {/* Mobile Close Button */}
                <button
                    onClick={() => setIsMobileOpen(false)}
                    className="absolute top-2 right-2 p-2 text-gray-400 hover:text-white md:hidden z-10"
                >
                    <X className="h-6 w-6" />
                </button>
                <div className="flex-1 overflow-y-auto custom-scrollbar no-scrollbar pb-4">
                    <div className="flex items-center gap-2 px-2 py-4 mb-8">
                        <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 animate-pulse" />
                        <span className="text-xl font-bold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                            STOCK AI
                        </span>
                    </div>

                    <nav className="space-y-2">
                        {navigation.map((item) => (
                            <Link
                                key={item.name}
                                href={item.href}
                                className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-bold text-gray-200 transition-all hover:bg-white/10 hover:text-white hover:scale-105 active:scale-95 group"
                            >
                                <item.icon className="h-5 w-5 transition-colors group-hover:text-blue-400" />
                                {item.name}
                            </Link>
                        ))}
                    </nav>
                </div>
                <div className="mt-auto space-y-4">
                    {/* API Debug Info */}
                    <div className="text-[9px] text-gray-500 text-center font-mono break-all bg-white/5 rounded py-1">API: {API_BASE_URL}</div>
                    {user ? (
                        <div className="rounded-xl bg-white/5 p-4 border border-white/5 flex items-center gap-3">
                            <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center font-bold text-white text-lg">
                                {user.name[0]}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-bold text-white truncate">{user.name}</p>
                                <p className="text-xs text-gray-400 truncate">{user.email}</p>
                            </div>
                            <button onClick={logout} className="p-2 text-gray-400 hover:text-white transition-colors">
                                <span className="text-xs">로그아웃</span>
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={() => setShowLoginModal(true)}
                            className="w-full rounded-xl bg-white/10 py-3 text-sm font-bold text-white hover:bg-white/20 transition-colors flex items-center justify-center gap-2"
                        >
                            <UserCheck className="w-4 h-4" />
                            로그인
                        </button>
                    )}

                    {!user?.is_pro && (
                        <>
                            <MarketClock />
                            <div className="rounded-xl bg-gradient-to-br from-blue-900/50 to-purple-900/50 p-4 border border-white/5">
                                <p className="text-xs font-semibold text-blue-200 mb-1">PRO 요금제</p>
                                <p className="text-[10px] text-gray-400 mb-3">
                                    월 ${proPriceUsd} (약 ₩{proPriceKrw.toLocaleString()})<br />
                                    고급 AI 인사이트를 받아보세요
                                </p>
                                <button
                                    onClick={() => setShowProModal(true)}
                                    className="w-full rounded-lg bg-blue-600 py-2 text-xs font-bold text-white hover:bg-blue-500 transition-colors"
                                >
                                    업그레이드
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>

            <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />

            {showProModal && (
                <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
                    <div className="relative bg-[#111] border border-white/20 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl">
                        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-600/20 to-transparent" />

                        <div className="p-8 relative">
                            <button
                                onClick={() => setShowProModal(false)}
                                className="absolute top-4 right-4 p-2 text-gray-400 hover:text-white transition-colors"
                            >
                                <X size={20} />
                            </button>

                            <div className="text-center mb-6">
                                <div className="inline-block bg-gradient-to-r from-yellow-400 to-orange-500 text-black text-xs font-black px-3 py-1 rounded-full mb-4 animate-bounce">
                                    🚀 GRAND LAUNCH SPECIAL
                                </div>
                                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 mb-4 shadow-lg shadow-blue-500/30">
                                    <Crown className="w-8 h-8 text-white" />
                                </div>
                                <h2 className="text-2xl font-bold text-white mb-2">PRO 멤버십 혜택</h2>
                                <p className="text-gray-400 text-sm">상위 1% 투자자를 위한 프리미엄 기능을 잠금 해제하세요.</p>
                            </div>

                            <div className="space-y-4 mb-8">
                                <BenefitItem
                                    icon={<Zap className="w-5 h-5 text-yellow-400" />}
                                    title="무제한 AI 분석 & 진단"
                                    desc="하루 제한 없이 종목 발굴과 포트폴리오 진단을 이용하세요."
                                />
                                <BenefitItem
                                    icon={<LineChart className="w-5 h-5 text-green-400" />}
                                    title="실시간 스나이퍼 알림"
                                    desc="RSI 과매도, 골든크로스 등 매수 타이밍을 놓치지 마세요."
                                />
                                <BenefitItem
                                    icon={<Newspaper className="w-5 h-5 text-blue-400" />}
                                    title="심층 리포트 & 공급망 분석"
                                    desc="기업의 숨겨진 리스크와 공급망 관계를 한눈에 파악하세요."
                                />
                            </div>

                            <button
                                onClick={async () => {
                                    try {
                                        await requestPayment(() => {
                                            localStorage.setItem("isPro", "true");
                                            alert("결제가 완료되었습니다! 프로 기능이 활성화됩니다.");
                                            setShowProModal(false);
                                            window.location.reload();
                                        });
                                    } catch (e: any) {
                                        alert("결제 요청 실패: " + e.message);
                                    }
                                }}
                                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 py-4 rounded-xl font-bold text-white text-lg transition-all hover:scale-[1.02] shadow-lg shadow-blue-600/30 flex flex-col items-center justify-center gap-1"
                            >
                                <span className="text-blue-200 text-xs font-normal line-through">$10.00/mo</span>
                                <span>월 ${proPriceUsd} (약 ₩{proPriceKrw.toLocaleString()})으로 시작하기</span>
                            </button>
                            <p className="text-center text-xs text-gray-500 mt-4">
                                * 실시간 환율({exchangeRate.toLocaleString()}원/$) 적용
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

function BenefitItem({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
    return (
        <div className="flex items-start gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
            <div className="mt-1">{icon}</div>
            <div>
                <h4 className="font-bold text-white text-sm mb-1">{title}</h4>
                <p className="text-xs text-gray-400 leading-relaxed">{desc}</p>
            </div>
        </div>
    );
}
