#!/usr/bin/env bash
set -e

echo "Setting up DB"

python - << 'py'
import os
import time
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise SystemExit("No DATABASE_URL")

engine = create_engine(db_url, future=True)

for i in range(30):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database ready")
        break
    except Exception as e:
        print(f"DB not ready ({e}), retrying...")
        time.sleep(2)
else:
    raise SystemExit("DB not ready in time")
py

echo "Running ETL"
python /app/etl.py

echo "Starting FastAPI with Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000