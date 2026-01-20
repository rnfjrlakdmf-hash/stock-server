import sqlite3
import os
from datetime import datetime

DB_FILE = "stock_app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # AI 점수 히스토리 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL,
            score INTEGER,
            supply_score INTEGER,
            financial_score INTEGER,
            news_score INTEGER,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Users Table (Google Login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, -- Google ID
            email TEXT,
            name TEXT,
            picture TEXT,
            is_pro BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            free_trial_count INTEGER DEFAULT 2
        )
    ''')
    
    # [Migration] Add free_trial_count if not exists
    try:
        cursor.execute("SELECT free_trial_count FROM users LIMIT 1")
    except sqlite3.OperationalError:
        print("Migrating users table (adding free_trial_count)...")
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN free_trial_count INTEGER DEFAULT 2")
        except Exception as e:
            print(f"Migration Warning: {e}")

    # Watchlist Table (User Specific)
    # Check if watchlist table has user_id column
    try:
        cursor.execute("SELECT user_id FROM watchlist LIMIT 1")
    except sqlite3.OperationalError:
        # Migration: Drop old table and recreate with user_id
        # (Data loss acceptable for dev, or copy if needed. Let's simpler recreate)
        print("Migrating watchlist to multi-user schema...")
        cursor.execute("DROP TABLE IF EXISTS watchlist")
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            user_id TEXT,
            symbol TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, symbol)
        )
    ''')
    
    # Sentiment Battle (User Votes) Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            vote_type TEXT NOT NULL, -- 'UP' or 'DOWN'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user_if_not_exists(user_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_data['id'],))
        row = cursor.fetchone()
        
        if not row:
            cursor.execute('''
                INSERT INTO users (id, email, name, picture, free_trial_count)
                VALUES (?, ?, ?, ?, 2)
            ''', (user_data['id'], user_data['email'], user_data['name'], user_data['picture']))
        else:
            # Update info
            cursor.execute('''
                UPDATE users SET name = ?, picture = ? WHERE id = ?
            ''', (user_data['name'], user_data['picture'], user_data['id']))
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Create User Error: {e}")
        return False
    finally:
        conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Fetch free_trial_count too (added to schema)
        # Note: If accessing old DB file without migration, fetch might fail unless we handled migration in init
        cursor.execute("SELECT id, email, name, picture, is_pro, free_trial_count FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "picture": row[3],
                "is_pro": bool(row[4]),
                "free_trial_count": row[5] if row[5] is not None else 2
            }
        return None
    except Exception as e:
        print(f"Get User Error: {e}")
        return None
    finally:
        conn.close()

def decrement_free_trial(user_id):
    """
    1시간 무료 이용권 사용 (차감)
    Returns: new_count or -1 if failed/already 0
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Decrease only if > 0
        cursor.execute("UPDATE users SET free_trial_count = free_trial_count - 1 WHERE id = ? AND free_trial_count > 0", (user_id,))
        if cursor.rowcount > 0:
            conn.commit()
            # Fetch new count
            cursor.execute("SELECT free_trial_count FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return row[0]
        else:
            return -1 # No change (probably 0 left)
    except Exception as e:
        print(f"Decrement Trial Error: {e}")
        return -1
    finally:
        conn.close()

def save_analysis_result(data):
    """
    AI 분석 결과를 DB에 저장합니다.
    data format matches the return of analyze_stock
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        symbol = data['symbol']
        price = data.get('price', 0)
        # Handle '75,000' string format if necessary, assuming float/int here or cleaning needed
        if isinstance(price, str):
            price = float(price.replace(',', '').replace('$', ''))
            
        score = data.get('score', 0)
        metrics = data.get('metrics', {})
        
        cursor.execute('''
            INSERT INTO score_history (symbol, price, score, supply_score, financial_score, news_score, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            symbol, 
            price, 
            score, 
            metrics.get('supplyDemand', 0), 
            metrics.get('financials', 0), 
            metrics.get('news', 0), 
            data.get('analysis_summary', '')
        ))
        
        conn.commit()
    except Exception as e:
        print(f"DB Save Error: {e}")
    finally:
        conn.close()

def get_score_history(symbol):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT created_at, score, price, supply_score, financial_score, news_score
        FROM score_history
        WHERE symbol = ?
        ORDER BY created_at ASC
        LIMIT 50
    ''', (symbol,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "date": row[0],
            "score": row[1],
            "price": row[2],
            "supply": row[3],
            "financial": row[4],
            "news": row[5]
        })
        
    return history

def get_prediction_report():
    """
    과거 AI 예측(점수)과 현재 가격을 비교하여 적중률 리포트를 생성합니다.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 최근 30개의 예측 기록 가져오기 (최신순)
    cursor.execute('''
        SELECT symbol, price, score, created_at
        FROM score_history
        ORDER BY created_at DESC
        LIMIT 30
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    report = {
        "total_count": 0,
        "success_count": 0,
        "success_rate": 0,
        "details": []
    }
    
    import yfinance as yf
    
    # 중복 심볼 제거하고 최신 것만 남기거나, 개별 건으로 처리? 
    # 여기선 개별 건으로 처리하되, 현재가 조회 비용 고려 필요.
    # 데모용으로 심볼별 그룹화하여 최신 1건씩만 검증하자.
    
    unique_checks = {}
    for row in rows:
        sym = row[0]
        if sym not in unique_checks:
            unique_checks[sym] = row
            
    if not unique_checks:
        return report

    try:
        # 현재가 일괄 조회 (yfinance batch)
        symbols = list(unique_checks.keys())
        # market 등 특수 심볼 제외
        symbols = [s for s in symbols if "MARKET" not in s]
        if not symbols: return report
        
        tickers = yf.Tickers(" ".join(symbols))
        
        for sym, row in unique_checks.items():
            if "MARKET" in sym: continue
            
            past_price = row[1]
            score = row[2]
            created_at = row[3]
            
            # 현재가 가져오기
            try:
                # .fast_info.last_price or history
                current_price = tickers.tickers[sym].fast_info.last_price
            except:
                continue
                
            if not current_price: continue
            
            # 수익률
            change_pct = ((current_price - past_price) / past_price) * 100
            
            # 적중 판단
            # Score >= 60 (Bullish) -> Price Up -> Success
            # Score <= 40 (Bearish) -> Price Down -> Success
            # Else (Neutral 41-59) -> Skip or check stability? Let's skip neutrals.
            
            is_correct = False
            prediction = "Neutral"
            
            if score >= 60:
                prediction = "Bullish"
                if change_pct > 0: is_correct = True
            elif score <= 40:
                prediction = "Bearish"
                if change_pct < 0: is_correct = True
            else:
                # 중립은 적중/실패 계산에서 제외 (또는 변동폭 +-1% 이내면 성공 간주 등)
                continue
                
            report["total_count"] += 1
            if is_correct:
                report["success_count"] += 1
                
            report["details"].append({
                "symbol": sym,
                "date": created_at,
                "prediction": prediction,
                "past_price": past_price,
                "current_price": current_price,
                "change_pct": round(change_pct, 2),
                "is_correct": is_correct
            })
            
    except Exception as e:
        print(f"Prediction Report Error: {e}")
        
    if report["total_count"] > 0:
        report["success_rate"] = int((report["success_count"] / report["total_count"]) * 100)
        
    return report

def add_watchlist(user_id, symbol):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO watchlist (user_id, symbol) VALUES (?, ?)", (user_id, symbol))
        conn.commit()
        return True
    except Exception as e:
        print(f"Add Watchlist Error: {e}")
        return False
    finally:
        conn.close()

def remove_watchlist(user_id, symbol):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM watchlist WHERE user_id = ? AND symbol = ?", (user_id, symbol))
        conn.commit()
    finally:
        conn.close()

def clear_watchlist(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM watchlist WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()

def get_watchlist(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM watchlist WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Initialize on module load (or call explicitly)
# Initialize on module load (or call explicitly)
init_db()

def cast_vote(symbol, vote_type):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sentiment_votes (symbol, vote_type) VALUES (?, ?)", (symbol, vote_type))
    conn.commit()
    conn.close()

def get_vote_stats(symbol):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get total counts
    cursor.execute("SELECT vote_type, COUNT(*) FROM sentiment_votes WHERE symbol = ? GROUP BY vote_type", (symbol,))
    rows = cursor.fetchall()
    
    stats = {"UP": 0, "DOWN": 0}
    for row in rows:
        stats[row[0]] = row[1]
    
    total = stats["UP"] + stats["DOWN"]
    if total > 0:
        stats["UP_PERCENT"] = int((stats["UP"] / total) * 100)
        stats["DOWN_PERCENT"] = int((stats["DOWN"] / total) * 100)
    else:
        stats["UP_PERCENT"] = 50
        stats["DOWN_PERCENT"] = 50
        
    conn.close()
    return stats
