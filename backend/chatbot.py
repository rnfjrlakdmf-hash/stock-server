import os
import yfinance as yf
import re
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일 로드 (명시적 경로 설정)
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# 환경 변수에서 Gemini API 키 로드
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"[ERROR] Failed to configure Gemini API in chatbot: {e}")

# 한국어 종목명 매핑 (Frontend와 동기화 필요)
STOCK_KOREAN_MAP = {
    # 미국 주식
    "테슬라": "TSLA", "애플": "AAPL", "마이크로소프트": "MSFT", "엔비디아": "NVDA", "아마존": "AMZN",
    "구글": "GOOGL", "알파벳": "GOOGL", "메타": "META", "페이스북": "META", "넷플릭스": "NFLX",
    "AMD": "AMD", "인텔": "INTC", "쿠팡": "CPNG", "코카콜라": "KO", "펩시": "PEP",
    "스타벅스": "SBUX", "나이키": "NKE", "디즈니": "DIS", "보잉": "BA", "화이자": "PFE",
    "팔란티어": "PLTR", "아이온큐": "IONQ", "유니티": "U", "로블록스": "RBLX", "코인베이스": "COIN",
    "리비안": "RIVN", "루시드": "LCID", "티큐": "TQQQ", "속슬": "SOXL", "슈드": "SCHD",

    # 한국 주식
    "삼성전자": "005930.KS", "삼전": "005930.KS", "에스케이하이닉스": "000660.KS", "하이닉스": "000660.KS", "SK하이닉스": "000660.KS",
    "엘지에너지솔루션": "373220.KS", "엘지엔솔": "373220.KS", "삼성바이오로직스": "207940.KS", "삼바": "207940.KS",
    "현대차": "005380.KS", "현대자동차": "005380.KS", "기아": "000270.KS", "셀트리온": "068270.KS",
    "포스코": "005490.KS", "포스코홀딩스": "005490.KS", "네이버": "035420.KS", "카카오": "035720.KS",
    "삼성에스디아이": "006400.KS", "엘지화학": "051910.KS", "카카오뱅크": "323410.KS", "카뱅": "323410.KS",
    "두산에너빌리티": "034020.KS", "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ", "엘앤에프": "066970.KQ",
    "에이치엘비": "028300.KQ", "알테오젠": "196170.KQ", "펄어비스": "263750.KQ", "하이브": "352820.KS",
    "엔씨소프트": "036570.KS", "크래프톤": "259960.KS", "엘지전자": "066570.KS"
}

def get_market_context(message: str):
    """
    메시지에서 종목 코드를 찾아 기본 시세를 조회합니다.
    """
    # 1. 종목 코드 추출 (대문자 알파벳 2-5자 또는 숫자6자리.KS/KQ)
    # 영어 티커: AAPL, TSLA, BTC-USD (하이픈 포함)
    # 한국 티커: 005930.KS, 035420.KQ
    potential_tickers = re.findall(r'\b[A-Z]{2,5}\b|\b\d{6}\.[A-Z]{2}\b', message.upper())
    
    # 2. 한글 종목명 매핑 확인
    # 메시지에 포함된 한글 단어가 매핑 키에 있는지 확인
    for kor_name, ticker in STOCK_KOREAN_MAP.items():
        if kor_name in message or kor_name in message.replace(" ", ""):
            potential_tickers.append(ticker)

    # 중복 제거
    tickers = set(potential_tickers)
    # 의미 없는 단어 필터링 (간단하게)
    ignore_list = {"THE", "WHO", "HOW", "WHY", "WHAT", "WHEN", "IS", "ARE", "WAS", "WERE", "DO", "DOES", "DID", "CAN", "COULD", "SHOULD", "WOULD", "MAY", "MIGHT", "MUST", "HAVE", "HAS", "HAD", "BUY", "SELL", "HOLD", "YES", "NO"}
    valid_tickers = [t for t in tickers if t not in ignore_list]

    context = ""
    for ticker in valid_tickers:
        try:
            stock = yf.Ticker(ticker)
            # fast_info 사용이 더 빠름
            info = stock.fast_info
            price = info.last_price
            prev_close = info.previous_close
            
            if price and prev_close:
                change = price - prev_close
                pct = (change / prev_close) * 100
                context += f"[{ticker}] Price: {price:.2f}, Change: {change:+.2f} ({pct:+.2f}%)\n"
        except:
            pass
            
    return context

from ai_analysis import analyze_theme

def chat_with_ai(message: str) -> str:
    if not API_KEY:
        return "죄송합니다. Gemini API 키가 설정되지 않아 답변할 수 없습니다. .env 파일을 확인해주세요."

    # 1. 텍스트에서 종목 정보 조회 (Context Injection)
    market_context = get_market_context(message)
    
    # [New] 종목 코드가 없고 '관련주/테마' 질문인 경우 처리
    if not market_context and any(k in message for k in ["관련주", "테마", "수혜주", "대장주", "어떤 종목", "알려줘"]):
        print(f"Detecting theme in message: {message}")
        try:
            # AI에게 테마 종목 추출 요청
            theme_result = analyze_theme(message)
            if theme_result:
                related_items = []
                # Leaders와 Followers에서 심볼 추출
                for item in theme_result.get("leaders", []) + theme_result.get("followers", []):
                    symbol = item.get("symbol")
                    name = item.get("name", "Unknown")
                    if symbol:
                        # 미국 주식은 그대로, 한국 주식은 .KS/.KQ 보정 필요할 수 있음
                        # AI가 보통 "012340" 처럼 숫자만 줄 수도 있음 -> 한국 주식으로 가정하고 .KS 시도
                        if symbol.isdigit(): 
                            final_symbol = f"{symbol}.KS" # 일단 KS로 시도 (KQ일수도 있지만)
                        else:
                            final_symbol = symbol
                        related_items.append({"symbol": final_symbol, "name": name})
                
                # 추출된 종목들의 현재가 조회
                if related_items:
                    print(f"Found related items: {related_items}")
                    context_list = []
                    for item in related_items[:5]: # 최대 5개만 조회
                        ticker = item['symbol']
                        name = item['name']
                        try:
                            stock = yf.Ticker(ticker)
                            # info = stock.fast_info (fast_info가 가끔 불안정하면 history 사용)
                            price = stock.fast_info.last_price
                            if price:
                                # 종목명과 티커를 같이 표기
                                context_list.append(f"[{name}({ticker})] {price:,.0f} (AI 추천 관련주)")
                        except:
                            pass
                    
                    if context_list:
                        market_context = "\n".join(context_list)
                        market_context += f"\n(AI가 분석한 '{message}' 관련 테마주 실시간 시세입니다)"
        except Exception as e:
            print(f"Theme lookup failed: {e}")

    # [New] 종합 시장 데이터 조회 (질문이 광범위하거나 시장 전반을 물을 때)
    # 키워드: 증시, 시장, 오늘, 지수, 환율, 브리핑, 상황, 어때
    general_keywords = ["증시", "시장", "오늘", "지수", "환율", "브리핑", "상황", "어때", "흐름", "경제"]
    if any(k in message for k in general_keywords) or not market_context:
        try:
            from stock_data import get_all_assets
            from korea_data import get_live_investor_estimates
            
            # 1. 자산 시세 (지수, 환율 등)
            assets = get_all_assets()
            market_summary = []
            
            if assets.get("Indices"):
                market_summary.append("== 주요 지수 ==")
                for idx in assets["Indices"][:5]: # Top 5 Indices
                    market_summary.append(f"{idx['name']}: {idx['price']} ({idx['change']})")
            
            if assets.get("Forex"):
                market_summary.append("\n== 주요 환율 ==")
                for fx in assets["Forex"][:3]: # Top 3 Forex
                    market_summary.append(f"{fx['name']}: {fx['price']} ({fx['change']})")

            # 2. 투자자 동향 (한국 시장 장중인 경우)
            # 삼성전자 예시로 투자자 동향을 볼 수도 있지만, 전체 시장 동향은 별도 API 필요.
            # 여기서는 대표적으로 '삼성전자'의 투자자 동향을 참고용으로만 가져오거나(대장주니까), 생략.
            # get_live_investor_estimates('005930.KS') 활용 가능.
            
            if market_summary:
                briefing = "\n".join(market_summary)
                market_context += f"\n\n[실시간 시장 브리핑 데이터]\n{briefing}\n(사용자가 증시 전반을 물어보면 이 데이터를 브리핑해주세요)"
        except Exception as e:
            print(f"Market Summary fetch failed: {e}")

    # 2. 시스템 프롬프트 구성
    system_prompt = f"""
    당신은 월스트리트 출신의 전설적인 트레이더이자 'AI 주식 상담사'입니다.
    사용자는 당신을 믿고 의지하는 투자자입니다. 
    단순한 답변보다는 시장의 흐름과 통찰력(Insight)이 담긴 답변을 제공하세요.
    모든 데이터는 '실시간' 기준이며, 당신은 이 모든 정보를 이미 알고 있다고 가정하고 자연스럽게 이야기하세요.
    
    [실시간 시장 데이터 (Fact)]
    {market_context}

    지침:
    1. 시장 데이터가 있다면 구체적인 수치(지수, 등락률)를 언급하며 분석하세요. (예: "오늘 코스피는 0.5% 상승하며 좋은 흐름이네요.")
    2. 데이터가 없다면 "현재 실시간 데이터를 가져오는 중 통신이 원활하지 않지만..." 하고 일반적인 뷰를 제시하세요.
    3. 매수/매도 추천은 "제 개인적인 의견으로는..."이라는 뉘앙스로 조심스럽게 하되, 명확한 근거(재무, 수급 등)를 대세요.
    4. 답변은 친절하고 전문적인 '해요체'를 사용하세요. 가독성을 위해 불릿 포인트나 줄바꿈을 적절히 쓰세요.
    5. 사용자가 특정 종목을 물어보면 그 종목에 집중하고, 시장 전체를 물어보면 지수와 환율을 종합적으로 브리핑하세요.
    """

    try:
        # 모델 설정 (Gemini Flash 사용)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # 채팅 세션 시작 (히스토리는 유지하지 않음, 단발성 질문 처리)
        # 만약 히스토리가 필요하면 chat = model.start_chat() 사용
        # 여기선 간단히 generate_content 사용
        
        full_prompt = f"{system_prompt}\n\n사용자 질문: {message}"
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return f"죄송합니다. 잠시 생각할 시간이 필요해요. (오류: {str(e)})"
