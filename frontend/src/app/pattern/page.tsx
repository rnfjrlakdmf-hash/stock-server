"use client";

import { useState } from "react";
import Header from "@/components/Header";
import { API_BASE_URL } from "@/lib/config";
import { Search, LineChart, Target, Shield, AlertTriangle, Loader2 } from "lucide-react";
import {
    ResponsiveContainer,
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ReferenceLine
} from "recharts";
import { getTickerFromKorean } from "@/lib/stockMapping";

export default function PatternPage() {
    const [searchInput, setSearchInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const handleSearch = async () => {
        if (!searchInput) return;
        setLoading(true);
        setResult(null);
        try {
            const ticker = getTickerFromKorean(searchInput).toUpperCase();
            const res = await fetch(`${API_BASE_URL}/api/chart/patterns/${ticker}`);
            const json = await res.json();
            if (json.status === "success") {
                setResult(json.data);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen pb-10">
            <Header />

            <div className="p-6 max-w-4xl mx-auto space-y-8">
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-black text-white flex items-center justify-center gap-3">
                        <LineChart className="w-10 h-10 text-emerald-500" />
                        AI 차트 패턴 분석
                    </h1>
                    <p className="text-gray-400 text-lg">
                        복잡한 차트 분석은 AI에게 맡기세요. 패턴, 지지선, 저항선을 자동으로 감지합니다.
                    </p>
                </div>

                <div className="relative max-w-xl mx-auto">
                    <input
                        type="text"
                        value={searchInput}
                        onChange={(e) => setSearchInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        placeholder="티커 또는 한글 종목명 (예: 삼성전자, NVDA)..."
                        className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white text-lg focus:outline-none focus:border-emerald-500/50 transition-colors"
                    />
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 w-6 h-6" />
                    <button
                        onClick={handleSearch}
                        className="absolute right-2 top-1/2 -translate-y-1/2 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl text-sm font-bold transition-colors"
                    >
                        분석
                    </button>
                </div>

                {loading && (
                    <div className="flex flex-col items-center justify-center py-20 text-emerald-500">
                        <Loader2 className="w-12 h-12 animate-spin mb-4" />
                        <p className="animate-pulse text-lg">AI가 지난 60일간의 캔들을 스캔 중입니다...</p>
                    </div>
                )}

                {result && (
                    <div className="animate-in fade-in slide-in-from-bottom-6 duration-700 grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Signal Card with Chart */}
                        <div className="md:col-span-2 rounded-3xl bg-gradient-to-b from-gray-900 to-black border border-white/10 p-8 relative overflow-hidden">
                            <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 z-10 relative">
                                <div>
                                    <span className="text-emerald-400 font-bold tracking-wider text-sm uppercase mb-2 block">
                                        감지된 패턴
                                    </span>
                                    <h2 className="text-4xl font-black text-white mb-2">
                                        {result.pattern}
                                    </h2>
                                    <div className="flex items-center gap-3">
                                        <span className={`px-3 py-1 rounded-full text-sm font-bold ${result.signal === 'Buy' ? 'bg-green-500/20 text-green-400' :
                                            result.signal === 'Sell' ? 'bg-red-500/20 text-red-400' : 'bg-gray-500/20 text-gray-400'
                                            }`}>
                                            {result.signal === 'Buy' ? '매수' : result.signal === 'Sell' ? '매도' : '중립'} 신호
                                        </span>
                                        <span className="text-gray-400 text-sm">
                                            신뢰도: <span className="text-white font-bold">{result.confidence}%</span>
                                        </span>
                                    </div>
                                </div>
                            </div>

                            {/* Interactive Chart */}
                            <div className="h-80 w-full relative z-10">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={result.history}>
                                        <defs>
                                            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                        <XAxis
                                            dataKey="date"
                                            stroke="#666"
                                            tick={{ fill: '#666', fontSize: 10 }}
                                            tickFormatter={(val) => val.slice(5)} // Show MM-DD
                                        />
                                        <YAxis
                                            domain={['auto', 'auto']}
                                            stroke="#666"
                                            tick={{ fill: '#666', fontSize: 10 }}
                                            tickFormatter={(val) => result.currency === '₩' ? val.toLocaleString() : `$${val}`}
                                        />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#111', borderColor: '#333', borderRadius: '8px' }}
                                            itemStyle={{ color: '#fff' }}
                                            formatter={(value: any) => [result.currency === '₩' ? `₩${Number(value).toLocaleString()}` : `$${Number(value)}`, "Price"]}
                                        />
                                        <Area
                                            type="monotone"
                                            dataKey="price"
                                            stroke="#10b981"
                                            fillOpacity={1}
                                            fill="url(#colorPrice)"
                                            strokeWidth={2}
                                        />
                                        {/* Resistance Line */}
                                        <ReferenceLine
                                            y={result.resistance}
                                            stroke="#ef4444"
                                            strokeDasharray="5 5"
                                            label={{
                                                value: `저항선 (${result.currency === '₩' ? '₩' : '$'}${result.resistance?.toLocaleString()})`,
                                                position: 'insideTopRight',
                                                fill: '#ef4444',
                                                fontSize: 12
                                            }}
                                        />
                                        {/* Support Line */}
                                        <ReferenceLine
                                            y={result.support}
                                            stroke="#3b82f6"
                                            strokeDasharray="5 5"
                                            label={{
                                                value: `지지선 (${result.currency === '₩' ? '₩' : '$'}${result.support?.toLocaleString()})`,
                                                position: 'insideBottomRight',
                                                fill: '#3b82f6',
                                                fontSize: 12
                                            }}
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Analysis Detail */}
                        <div className="rounded-3xl bg-white/5 border border-white/10 p-6 backdrop-blur-md">
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <Target className="w-5 h-5 text-purple-400" /> 주요 구간
                            </h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-4 rounded-xl bg-red-500/10 border border-red-500/20">
                                    <span className="text-red-400 font-bold flex items-center gap-2">
                                        <Shield className="w-4 h-4" /> 저항선
                                    </span>
                                    <span className="text-2xl font-bold text-white">
                                        {result.currency || '$'}{Number(result.resistance).toLocaleString()}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
                                    <span className="text-blue-400 font-bold flex items-center gap-2">
                                        <Shield className="w-4 h-4" /> 지지선
                                    </span>
                                    <span className="text-2xl font-bold text-white">
                                        {result.currency || '$'}{Number(result.support).toLocaleString()}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Summary Text */}
                        <div className="rounded-3xl bg-white/5 border border-white/10 p-6 backdrop-blur-md">
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5 text-yellow-400" /> AI 분석 코멘트
                            </h3>
                            <p className="text-gray-300 leading-relaxed text-lg">
                                {result.summary}
                            </p>
                        </div>
                    </div>
                )}
                {/* Beginner Guide Section */}
                <div className="mt-12 border-t border-white/10 pt-8">
                    <h3 className="text-xl font-bold text-gray-400 mb-6 text-center">차트 분석 용어 가이드</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="p-6 rounded-2xl bg-red-900/10 border border-red-500/20">
                            <h4 className="text-red-400 font-bold text-lg mb-2 flex items-center gap-2">
                                <Shield className="w-5 h-5" /> 저항선 (Resistance)
                            </h4>
                            <p className="text-gray-300 text-sm leading-relaxed">
                                주가가 상승하다가 매도세에 부딪혀 <strong>더 이상 오르기 힘든 가격대(천장)</strong>를 의미합니다.
                                이 선을 강하게 뚫고 올라가면 새로운 상승 추세의 시작으로 봅니다.
                            </p>
                        </div>
                        <div className="p-6 rounded-2xl bg-blue-900/10 border border-blue-500/20">
                            <h4 className="text-blue-400 font-bold text-lg mb-2 flex items-center gap-2">
                                <Shield className="w-5 h-5" /> 지지선 (Support)
                            </h4>
                            <p className="text-gray-300 text-sm leading-relaxed">
                                주가가 하락하다가 매수세가 들어와 <strong>반등할 가능성이 높은 가격대(바닥)</strong>를 의미합니다.
                                이 선이 무너지면 추가 하락의 위험이 있습니다.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
