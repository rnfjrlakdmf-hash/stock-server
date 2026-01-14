export const FALLBACK_DASHBOARD_DATA = {
    exchange: [
        { name: "미국 USD", price: "1,420.50", change: "5.50", is_up: true },
        { name: "일본 JPY(100엔)", price: "910.20", change: "-2.30", is_up: false },
        { name: "유럽연합 EUR", price: "1,510.10", change: "3.20", is_up: true },
        { name: "중국 CNY", price: "195.40", change: "0.50", is_up: true }
    ],
    world_exchange: [
        { name: "달러 인덱스", price: "104.50", change: "0.20", is_up: true }
    ],
    interest: [
        { name: "CD(91일)", price: "3.50", change: "0.00", is_up: true },
        { name: "국고채(3년)", price: "3.20", change: "-0.01", is_up: false }
    ],
    oil: [
        { name: "WTI", price: "72.40", change: "-0.50", is_up: false }
    ],
    gold: [
        { name: "국제 금", price: "2,040.10", change: "10.00", is_up: true }
    ],
    raw_materials: [
        { name: "구리", price: "8,500.00", change: "50.00", is_up: true }
    ],
    top_sectors: [
        { name: "반도체", percent: "+2.5%" },
        { name: "2차전지", percent: "+1.8%" },
        { name: "제약바이오", percent: "+1.2%" },
        { name: "자동차", percent: "+0.8%" },
        { name: "IT서비스", percent: "-0.5%" }
    ],
    top_themes: [
        { name: "AI 챗봇", percent: "+3.2%" },
        { name: "초전도체", percent: "+2.1%" },
        { name: "리튬", percent: "+1.5%" },
        { name: "로봇", percent: "+1.1%" },
        { name: "클라우드", percent: "+0.9%" }
    ],
    market_summary: {
        kospi: {
            value: "2,650.40",
            change: "15.20",
            percent: "+0.58%",
            direction: "Up",
            chart: "",
            investors: { personal: "-1500", foreigner: "2000", institutional: "-500" }
        },
        kosdaq: {
            value: "870.10",
            change: "-5.30",
            percent: "-0.61%",
            direction: "Down",
            chart: "",
            investors: { personal: "1000", foreigner: "-800", institutional: "-200" }
        }
    },
    investor_items: {
        foreigner_buy: [
            { name: "삼성전자", amount: "500억", change: "1000", is_up: true },
            { name: "SK하이닉스", amount: "300억", change: "2000", is_up: true },
            { name: "현대차", amount: "150억", change: "500", is_up: true }
        ],
        foreigner_sell: [
            { name: "NAVER", amount: "200억", change: "-1000", is_up: false },
            { name: "카카오", amount: "150억", change: "-500", is_up: false }
        ],
        institution_buy: [
            { name: "POSCO홀딩스", amount: "200억", change: "1000", is_up: true },
            { name: "LG에너지솔루션", amount: "150억", change: "3000", is_up: true }
        ],
        institution_sell: [
            { name: "삼성SDI", amount: "100억", change: "-2000", is_up: false }
        ]
    }
};
