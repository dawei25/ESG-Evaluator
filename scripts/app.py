from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

class Company(BaseModel):
    id: int
    name: str
    esgScore: float
    environmentalScore: float
    socialScore: float
    governanceScore: float

class ESGTrend(BaseModel):
    date: str
    score: float

@app.get("/api/companies", response_model=List[Company])
async def get_companies():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT c.id, c.name, c.esg_score as "esgScore",
                   e.environmental_score as "environmentalScore",
                   e.social_score as "socialScore",
                   e.governance_score as "governanceScore"
            FROM companies c
            JOIN esg_scores e ON c.id = e.company_id
            WHERE e.date = (SELECT MAX(date) FROM esg_scores WHERE company_id = c.id)
        """)
        companies = cur.fetchall()
        return [Company(**company) for company in companies]
    finally:
        cur.close()
        conn.close()

@app.get("/api/esg-trend/{company_id}", response_model=List[ESGTrend])
async def get_esg_trend(company_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT date::text, total_score as score
            FROM esg_scores
            WHERE company_id = %s
            ORDER BY date
        """, (company_id,))
        trend = cur.fetchall()
        if not trend:
            raise HTTPException(status_code=404, detail="Company not found")
        return [ESGTrend(**data) for data in trend]
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)