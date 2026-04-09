from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import psycopg2
import os
from typing import List

app = FastAPI(title="Analytics API")

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": os.getenv("DATABASE_PORT", "5432"),
    "user": os.getenv("DATABASE_USER", "fastapi_user"),
    "password": os.getenv("DATABASE_PASSWORD", "secure_password_123"),
    "database": os.getenv("DATABASE_NAME", "analytics_db")
}

class Event(BaseModel):
    event_type: str
    user_id: str
    value: float

class AnalyticsResponse(BaseModel):
    id: int
    event_type: str
    user_id: str
    value: float
    created_at: datetime

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.on_event("startup")
async def startup():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(100),
            user_id VARCHAR(100),
            value FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/events", response_model=AnalyticsResponse)
async def create_event(event: Event):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO analytics_events (event_type, user_id, value) VALUES (%s, %s, %s) RETURNING id, created_at",
        (event.event_type, event.user_id, event.value)
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return AnalyticsResponse(
        id=result[0],
        event_type=event.event_type,
        user_id=event.user_id,
        value=event.value,
        created_at=result[1]
    )

@app.get("/events", response_model=List[AnalyticsResponse])
async def get_events(limit: int = 100):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, event_type, user_id, value, created_at FROM analytics_events ORDER BY created_at DESC LIMIT %s",
        (limit,)
    )
    events = []
    for row in cur.fetchall():
        events.append(AnalyticsResponse(
            id=row[0],
            event_type=row[1],
            user_id=row[2],
            value=row[3],
            created_at=row[4]
        ))
    cur.close()
    conn.close()
    return events

@app.get("/stats")
async def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            event_type,
            COUNT(*) as count,
            AVG(value) as avg_value,
            SUM(value) as total_value
        FROM analytics_events
        GROUP BY event_type
    """)
    stats = []
    for row in cur.fetchall():
        stats.append({
            "event_type": row[0],
            "count": row[1],
            "avg_value": float(row[2]) if row[2] else 0,
            "total_value": float(row[3]) if row[3] else 0
        })
    cur.close()
    conn.close()
    return stats
