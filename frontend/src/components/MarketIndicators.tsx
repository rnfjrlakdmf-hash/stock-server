
"use client";

import React, { useState, useEffect } from 'react';
import { BarChart3, DollarSign, RefreshCw, Droplet } from 'lucide-react';
import { Loader2 } from 'lucide-react';
import { API_BASE_URL } from "@/lib/config";

interface MarketItem {
    name: string;
    price: string;
    change: string;
    is_up: boolean;
}

interface MarketListProps {
    title: string;
    icon: React.ReactNode;
    items: MarketItem[];
}

export const MarketList = ({ title, icon, items }: MarketListProps) => (
    <div className="bg-white/5 rounded-2xl p-5 border border-white/5 flex flex-col h-full">
        <h4 className="text-white font-bold mb-4 flex items-center gap-2 flex-shrink-0">
            {icon} {title}
        </h4>
        <div className="space-y-3 overflow-y-auto max-h-[400px] pr-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
            {items && items.length > 0 ? (
                items.map((item, i) => (
                    <div key={i} className="flex justify-between items-center group">
                        <span className="text-gray-400 group-hover:text-white transition-colors text-sm">{item.name}</span>
                        <div className="text-right">
                            <div className="text-white font-mono text-sm font-bold">{item.price}</div>
                            <div className={`text-xs ${item.is_up ? 'text-red-400' : 'text-blue-400'}`}>
                                {item.is_up ? '+' : ''}{item.change}
                            </div>
                        </div>
                    </div>
                ))
            ) : (
                <div className="text-center text-gray-600 text-xs py-4">데이터 로딩중...</div>
            )}
        </div>
    </div>
);

interface MarketIndicatorsProps {
    limit?: number; // Optional limit for items to display (default: all or 10)
}

export default function MarketIndicators({ limit }: MarketIndicatorsProps) {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const fetchAssets = async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/api/assets`);
            const json = await res.json();
            if (json.status === "success") {
                setData(json.data);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAssets();
        const interval = setInterval(fetchAssets, 5000); // 5초 갱신
        return () => clearInterval(interval);
    }, []);

    // Helper to process /api/assets data into MarketItem format with Korean translation
    function processAssets(items: any[] | undefined, type: 'indices' | 'crypto' | 'forex' | 'commodity'): MarketItem[] {
        if (!items || items.length === 0) return [];

        return items.map(item => {
            let name = item.name;
            // Korean Translation Mapping
            if (type === 'indices') {
                if (name === 'S&P 500') name = 'S&P 500 (미국)';
                else if (name === 'Nasdaq') name = '나스닥 (미국)';
                else if (name === 'Dow Jones') name = '다우존스 (미국)';
                else if (name === 'Russell 2000') name = '러셀 2000';
                else if (name === 'VIX') name = 'VIX (공포지수)';
                else if (name === 'KOSPI') name = '코스피 (한국)';
                else if (name === 'KOSDAQ') name = '코스닥 (한국)';
                else if (name === 'Nikkei 225') name = '니케이 225 (일본)';
                else if (name === 'Euro Stoxx 50') name = '유로스톡스 50';
                else if (name === 'Shanghai Composite') name = '상해종합 (중국)';
            } else if (type === 'crypto') {
                if (name === 'Bitcoin') name = '비트코인';
                else if (name === 'Ethereum') name = '이더리움';
                else if (name === 'Ripple') name = '리플';
                else if (name === 'Solana') name = '솔라나';
                else if (name === 'Dogecoin') name = '도지코인';
                else if (name === 'Cardano') name = '에이다';
                else if (name === 'BNB') name = '바이낸스';
                else if (name === 'Tron') name = '트론';
                else if (name === 'Avalanche') name = '아발란체';
                else if (name === 'Chainlink') name = '체인링크';
            } else if (type === 'forex') {
                if (name.includes('USD/KRW')) name = '달러/원 (USD)';
                else if (name.includes('JPY/KRW')) name = '엔/원 (JPY)';
                else if (name.includes('EUR/KRW')) name = '유로/원 (EUR)';
                else if (name.includes('CNY/KRW')) name = '위안/원 (CNY)';
                else if (name.includes('GBP/KRW')) name = '파운드/원 (GBP)';
                else if (name.includes('AUD/KRW')) name = '호주달러/원';
                else if (name.includes('CAD/KRW')) name = '캐나다달러/원';
                else if (name.includes('CHF/KRW')) name = '스위스프랑/원';
                else if (name.includes('HKD/KRW')) name = '홍콩달러/원';
                else if (name.includes('NZD/KRW')) name = '뉴질랜드달러/원';
            } else if (type === 'commodity') {
                if (name === 'Gold') name = '국제 금';
                else if (name === 'Silver') name = '국제 은';
                else if (name === 'Crude Oil') name = 'WTI 원유';
                else if (name === 'Natural Gas') name = '천연가스';
                else if (name === 'Copper') name = '구리';
                else if (name === 'Corn') name = '옥수수';
                else if (name === 'Platinum') name = '백금';
                else if (name === 'Palladium') name = '팔라듐';
                else if (name === 'Wheat') name = '소맥 (밀)';
                else if (name === 'Soybean') name = '대두 (콩)';
            }

            // Safety check for price
            let priceStr = "0.00";
            if (typeof item.price === 'number') {
                priceStr = item.price.toLocaleString(undefined, { maximumFractionDigits: 2 });
            } else if (typeof item.price === 'string') {
                priceStr = item.price;
            }

            const changeVal = item.change || 0;
            const is_up = changeVal >= 0;
            const changeStr = `${Math.abs(changeVal).toFixed(2)}%`;

            return {
                name: name,
                price: type === 'crypto' ? `₩${priceStr}` : priceStr, // Coins in KRW (Upbit)
                change: changeStr,
                is_up: is_up
            };
        });
    }

    if (loading && !data) return <div className="p-8 text-center text-gray-500"><Loader2 className="w-6 h-6 animate-spin mx-auto" /></div>;
    if (!data) return null;

    const displayLimit = limit || 10;
    const titleSuffix = limit ? `(Top ${limit})` : '(10)';

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <MarketList
                title={`글로벌 주요 지수 ${titleSuffix}`}
                icon={<BarChart3 className="text-blue-400" />}
                items={processAssets(data.Indices, 'indices').slice(0, displayLimit)}
            />
            <MarketList
                title={`암호화폐 ${titleSuffix}`}
                icon={<DollarSign className="text-yellow-400" />}
                items={processAssets(data.Crypto, 'crypto').slice(0, displayLimit)}
            />
            <MarketList
                title={`주요 환율 ${titleSuffix}`}
                icon={<RefreshCw className="text-green-400" />}
                items={processAssets(data.Forex, 'forex').slice(0, displayLimit)}
            />
            <MarketList
                title={`원자재 ${titleSuffix}`}
                icon={<Droplet className="text-orange-400" />}
                items={processAssets(data.Commodity, 'commodity').slice(0, displayLimit)}
            />
        </div>
    );
}
