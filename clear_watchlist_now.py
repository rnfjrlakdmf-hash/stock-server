
import sqlite3
import os

DB_FILE = "backend/stock_app.db"

def clear_watchlist():
    if not os.path.exists(DB_FILE):
        print(f"Database file not found at {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM watchlist")
        conn.commit()
        print("Successfully cleared all items from watchlist.")
    except Exception as e:
        print(f"Error clearing watchlist: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_watchlist()
