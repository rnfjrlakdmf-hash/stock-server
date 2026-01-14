
import uvicorn
import os

if __name__ == "__main__":
    print("Starting backend...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
