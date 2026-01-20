#!/bin/bash
pkill -f uvicorn
cd ~/StockTrendProgram/backend
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "Server restarted successfully."
