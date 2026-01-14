
"use client";

import { useState, useEffect } from "react";
import { Clock, Globe } from "lucide-react";

interface MarketTime {
    name: string;
    tz: string;
    openHour: number;
    openMinute: number;
    closeHour: number;
    closeMinute: number;
}

const MARKETS: MarketTime[] = [
    { name: "서울 (KRX)", tz: "Asia/Seoul", openHour: 9, openMinute: 0, closeHour: 15, closeMinute: 30 },
    { name: "뉴욕 (NYSE)", tz: "America/New_York", openHour: 9, openMinute: 30, closeHour: 16, closeMinute: 0 },
    { name: "런던 (LSE)", tz: "Europe/London", openHour: 8, openMinute: 0, closeHour: 16, closeMinute: 30 },
];

export default function MarketClock() {
    const [times, setTimes] = useState<Record<string, Date>>({});
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        const updateTime = () => {
            const now = new Date();
            const newTimes: Record<string, Date> = {};

            MARKETS.forEach(m => {
                // Convert current time to target timezone string, then parse it back to a Date object relative to local? 
                // Actually easier way: use Intl.DateTimeFormat to get parts

                const str = new Intl.DateTimeFormat('en-US', {
                    timeZone: m.tz,
                    year: 'numeric', month: 'numeric', day: 'numeric',
                    hour: 'numeric', minute: 'numeric', second: 'numeric',
                    hour12: false
                }).format(now);

                newTimes[m.name] = new Date(str);
            });
            setTimes(newTimes);
        };

        updateTime();
        const interval = setInterval(updateTime, 1000);
        return () => clearInterval(interval);
    }, []);

    if (!mounted) return null;

    return (
        <div className="mb-6 space-y-3">
            <div className="flex items-center gap-2 mb-2 px-1">
                <Globe className="w-4 h-4 text-blue-400" />
                <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">세계 증시 시간</span>
            </div>

            <div className="space-y-3">
                {MARKETS.map((m) => {
                    const localTime = times[m.name];
                    if (!localTime) return null;

                    const hours = localTime.getHours();
                    const minutes = localTime.getMinutes();
                    const totalMinutes = hours * 60 + minutes;
                    const openMinutes = m.openHour * 60 + m.openMinute;
                    const closeMinutes = m.closeHour * 60 + m.closeMinute;

                    const isOpen = totalMinutes >= openMinutes && totalMinutes < closeMinutes;

                    return (
                        <div
                            key={m.name}
                            className={`
                                relative flex justify-between items-center p-3 rounded-xl border transition-all duration-300
                                ${isOpen
                                    ? 'bg-gradient-to-r from-blue-900/30 to-purple-900/10 border-blue-500/30 shadow-lg shadow-blue-900/20'
                                    : 'bg-white/5 border-white/5 opacity-60 hover:opacity-100'}
                            `}
                        >
                            {/* Status Indicator */}
                            {isOpen && (
                                <span className="absolute -top-1 -right-1 flex h-3 w-3">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                                </span>
                            )}

                            <div className="flex flex-col">
                                <span className={`text-xs font-bold mb-0.5 ${isOpen ? 'text-white' : 'text-gray-400'}`}>
                                    {m.name.split(' ')[0]} {/* Show distinct city/exchange name */}
                                    <span className="text-[10px] opacity-70 ml-1 font-normal">{m.name.split(' ')[1]}</span>
                                </span>
                                <span className={`text-[10px] font-bold tracking-wider ${isOpen ? 'text-green-400' : 'text-gray-500'}`}>
                                    {isOpen ? "현재 개장중" : "장 종료"}
                                </span>
                            </div>

                            <div className="text-right flex flex-col items-end">
                                <div className={`font-mono font-bold tracking-tight ${isOpen ? 'text-xl text-white' : 'text-lg text-gray-500'} flex items-baseline justify-end gap-0.5 leading-none`}>
                                    <span>
                                        {localTime.getHours() % 12 || 12}:{localTime.getMinutes().toString().padStart(2, '0')}
                                    </span>
                                    <span className="text-[10px] opacity-60">
                                        :{localTime.getSeconds().toString().padStart(2, '0')}
                                    </span>
                                    <span className="text-[10px] font-sans ml-1 opacity-80 font-medium">
                                        {localTime.getHours() >= 12 ? '오후' : '오전'}
                                    </span>
                                </div>
                                <span className={`text-[10px] font-bold uppercase mt-1 ${isOpen ? 'text-blue-300' : 'text-gray-600'}`}>
                                    {localTime.toLocaleDateString('ko-KR', { weekday: 'long' })}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
