import json
import os
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

ALERTS_FILE = "alerts.json"
TELEGRAM_TOKEN = "8177986686:AAEk89GeI327ftFLgGN8IZHnUQJK9TiArV0"

def load_alerts():
    if not os.path.exists(ALERTS_FILE):
        return []
    try:
        with open(ALERTS_FILE, "r") as f:
            alerts = json.load(f)
            # Backward compatibility default
            for a in alerts:
                if "type" not in a:
                    a["type"] = "PRICE" 
            return alerts
    except:
        return []

def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

def add_alert(symbol, target_price=0, condition="above", alert_type="PRICE", chat_id=None):
    """
    alert_type: PRICE, RSI_OVERSOLD, GOLDEN_CROSS, PRICE_DROP
    target_price: Required for PRICE type
    condition: Required for PRICE type
    chat_id: Telegram Chat ID
    """
    alerts = load_alerts()
    alert = {
        "id": int(datetime.now().timestamp()), 
        "symbol": symbol.upper(),
        "type": alert_type,
        "target_price": float(target_price) if target_price else 0,
        "condition": condition,
        "chat_id": chat_id,
        "created_at": datetime.now().isoformat(),
        "status": "active" 
    }
    alerts.append(alert)
    save_alerts(alerts)
    return alert

def get_alerts():
    return load_alerts()

def delete_alert(alert_id):
    alerts = load_alerts()
    alerts = [a for a in alerts if a["id"] != int(alert_id)]
    save_alerts(alerts)

def calculate_technical_signals(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        
        # Fetch history for indicators
        hist = ticker.history(period="3mo")
        if len(hist) < 20: 
            return None
            
        # 1. RSI (14)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # 2. Moving Averages (Golden Cross)
        ma5 = hist['Close'].rolling(window=5).mean()
        ma20 = hist['Close'].rolling(window=20).mean()
        
        # Current and Previous for Crossover check
        curr_ma5 = ma5.iloc[-1]
        curr_ma20 = ma20.iloc[-1]
        prev_ma5 = ma5.iloc[-2]
        prev_ma20 = ma20.iloc[-2]
        
        # 3. Daily Change
        prev_close = hist['Close'].iloc[-2]
        current_close = hist['Close'].iloc[-1]
        change_pct = ((current_close - prev_close) / prev_close) * 100
        
        return {
            "price": price,
            "rsi": current_rsi,
            "ma5": curr_ma5,
            "ma20": curr_ma20,
            "prev_ma5": prev_ma5,
            "prev_ma20": prev_ma20,
            "change_pct": change_pct
        }
    except Exception as e:
        print(f"Tech calc failed for {symbol}: {e}")
        return None

def check_alerts():
    alerts = load_alerts()
    active_alerts = [a for a in alerts if a["status"] == "active"]
    
    if not active_alerts:
        return []

    triggered = []
    updated = False
    
    # Cache technical data to avoid re-fetching for same symbol multiple times
    tech_cache = {} 
    
    for alert in alerts:
        if alert["status"] != "active":
            continue
            
        symbol = alert["symbol"]
        
        try:
            # --- Type: PRICE ALERT ---
            if alert["type"] == "PRICE":
                if symbol not in tech_cache:
                    ticker = yf.Ticker(symbol)
                    p = ticker.fast_info.last_price
                    if p: tech_cache[symbol] = {"price": p}
                
                current_price = tech_cache.get(symbol, {}).get("price")
                if not current_price: continue
                
                condition_met = False
                if alert["condition"] == "above" and current_price >= alert["target_price"]:
                    condition_met = True
                elif alert["condition"] == "below" and current_price <= alert["target_price"]:
                    condition_met = True
                    
                if condition_met:
                    trigger_alert(alert, current_price, triggered)
                    updated = True

            # --- Type: SNIPER ALERTS ---
            else:
                if symbol not in tech_cache:
                    tech_data = calculate_technical_signals(symbol)
                    if tech_data: tech_cache[symbol] = tech_data
                
                data = tech_cache.get(symbol)
                if not data: continue
                
                current_price = data["price"]
                condition_met = False
                msg_suffix = ""

                if alert["type"] == "RSI_OVERSOLD":
                    # RSI < 30
                    if data["rsi"] < 30:
                        condition_met = True
                        msg_suffix = f"(RSI: {data['rsi']:.1f} 진입)"
                        
                elif alert["type"] == "RSI_OVERBOUGHT":
                    # RSI > 70
                    if data["rsi"] > 70:
                        condition_met = True
                        msg_suffix = f"(RSI: {data['rsi']:.1f} 과열)"

                elif alert["type"] == "GOLDEN_CROSS":
                    # MA5 crosses above MA20
                    if data["prev_ma5"] <= data["prev_ma20"] and data["ma5"] > data["ma20"]:
                        condition_met = True
                        msg_suffix = "(5일선이 20일선 돌파)"

                elif alert["type"] == "PRICE_DROP":
                    # -3% Drop
                    if data["change_pct"] <= -3.0:
                        condition_met = True
                        msg_suffix = f"(변동률: {data['change_pct']:.2f}%)"

                if condition_met:
                    trigger_alert(alert, current_price, triggered, msg_suffix)
                    updated = True

        except Exception as e:
            print(f"Alert check failed for {alert['symbol']}: {e}")
            
    if updated:
        save_alerts(alerts)
        
    return triggered

def trigger_alert(alert, price, triggered_list, extra_msg=""):
    alert["status"] = "triggered"
    alert["triggered_at"] = datetime.now().isoformat()
    alert["triggered_price"] = price
    triggered_list.append(alert)
    
    # Telegram
    if alert.get("chat_id"):
        send_telegram_message(alert, price, extra_msg)


def send_telegram_message(alert, current_price, extra_msg=""):
    """
    알림 유형에 따라 메시지 포맷을 다르게 전송
    """
    symbol = alert["symbol"]
    chat_id = alert["chat_id"]
    
    if alert["type"] == "PRICE":
        cond_str = "이상" if alert["condition"] == 'above' else "이하"
        title = "📢 *가격 도달 알림*"
        body = f"📈 *{symbol}* 목표가 도달!\n\n현재가: *{current_price}*\n목표가: {alert['target_price']} ({cond_str})"
    
    elif alert["type"] == "RSI_OVERSOLD":
        title = "💎 *스나이퍼 포착 (과매도)*"
        body = f"📉 *{symbol}* RSI 침체 구간 진입!\n\n현재가: *{current_price}*\n{extra_msg}\n반등 가능성이 높은 구간입니다."
        
    elif alert["type"] == "RSI_OVERBOUGHT":
        title = "⚠️ *스나이퍼 경고 (과매수)*"
        body = f"📈 *{symbol}* RSI 과열 구간!\n\n현재가: *{current_price}*\n{extra_msg}\n조정이 올 수 있습니다."
        
    elif alert["type"] == "GOLDEN_CROSS":
        title = "🚀 *스나이퍼 포착 (골든크로스)*"
        body = f"💹 *{symbol}* 골든크로스 발생!\n\n현재가: *{current_price}*\n단기 이평선이 장기 이평선을 돌파했습니다."
        
    elif alert["type"] == "PRICE_DROP":
        title = "📉 *급락 발생 경고*"
        body = f"🔻 *{symbol}* -3% 이상 급락!\n\n현재가: *{current_price}*\n{extra_msg}\n리스크 관리가 필요합니다."
    
    else:
        title = "🔔 *알림*"
        body = f"*{symbol}* 알림 조건 충족\n현재가: {current_price}"

    message = f"{title}\n\n{body}\n\n[StockAI App에서 확인하기]"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_recent_telegram_users():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        users = []
        if data.get("ok"):
            for update in reversed(data.get("result", [])):
                msg = update.get("message", {})
                chat = msg.get("chat", {})
                if chat.get("id"):
                    if not any(u['id'] == str(chat['id']) for u in users):
                        users.append({
                            "id": str(chat['id']),
                            "name": chat.get("first_name", "Unknown"),
                            "date": msg.get("date")
                        })
            return users[:5]
        return []
    except:
        return []
