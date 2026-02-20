from fastapi import FastAPI, Query as QParam
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Optional
import os
import sqlite3
from dotenv import load_dotenv

# Load env before importing AI modules
load_dotenv()

from ai.query_parser import parse_query
from ai.insight_generator import generate_insight
from ai.predictor import OceanPredictor

app = FastAPI(title="Velora AI Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173",
                   "http://localhost:5174", "http://127.0.0.1:5174",
                   "http://localhost", "http://127.0.0.1",
                   "http://192.168.137.29:5173", "http://192.168.137.29:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database connection ──────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "argo.db")
RAW_PREVIEW_LIMIT = 100

def get_db_connection():
    """Get SQLite connection with row factory for dict-like access"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA temp_store = MEMORY")
    conn.execute("PRAGMA cache_size = -64000")
    return conn

predictor = OceanPredictor()

# Region geographic bounds (lon_min, lon_max, lat_min, lat_max)
REGION_BOUNDS = {
    "Indian Ocean": (20, 120, -60, 23),
    "Pacific Ocean": (120, 180, -60, 60),
    "Atlantic Ocean": (-100, 0, -60, 60),
    "Arctic Ocean": (-180, 180, 60, 90),
}

def clean_nans(obj):
    """Recursively replace NaN/Inf values with None or 0"""
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(v) for v in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return 0.0 if np.isnan(obj) else None
        return obj
    return obj

# ── Shared filter + response builder ──────────────────────────────────────────
def build_response(region: str, parameter: str, start_year, end_year,
                   question: str = "", parsed_source: str = "rule-based"):

    # Ensure parameter is valid
    col = parameter if parameter in ["temperature", "salinity"] else "temperature"
    
    # Check region validity
    if region not in REGION_BOUNDS:
        return {
            "region": region, "parameter": col, "question": question,
            "parsed": {"region": region, "parameter": col,
                       "start_year": start_year, "end_year": end_year,
                       "source": parsed_source},
            "data": [], "stats": {}, "trend": None, "prediction": [],
            "insight": None,
            "message": f"Region not recognized: {region}",
        }
    
    # Query database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Build SQL query with filters
    where_clauses = []
    params = []
    
    # Add region filter (geographic bounds)
    lon_min, lon_max, lat_min, lat_max = REGION_BOUNDS[region]
    where_clauses.append("longitude >= ? AND longitude <= ? AND latitude >= ? AND latitude <= ?")
    params.extend([lon_min, lon_max, lat_min, lat_max])
    
    # Add year filters
    if start_year:
        where_clauses.append("substr(time, 1, 4) >= ?")
        params.append(str(start_year))
    if end_year:
        where_clauses.append("substr(time, 1, 4) <= ?")
        params.append(str(end_year))
    
    # Build the WHERE clause
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get column name to query
    col_name = "temperature" if col == "temperature" else "salinity"
    
    stats_query = f"""
        SELECT
            COUNT({col_name}) AS count,
            MIN({col_name}) AS min_val,
            MAX({col_name}) AS max_val,
            AVG({col_name}) AS mean_val,
            (AVG({col_name} * {col_name}) - AVG({col_name}) * AVG({col_name})) AS variance
        FROM argo_data
        WHERE {where_sql} AND {col_name} IS NOT NULL
    """
    cur.execute(stats_query, params)
    stats_row = cur.fetchone()

    total_count = int(stats_row["count"] or 0)
    if total_count == 0:
        conn.close()
        return {
            "region": region, "parameter": col, "question": question,
            "parsed": {"region": region, "parameter": col,
                       "start_year": start_year, "end_year": end_year,
                       "source": parsed_source},
            "data": [], "stats": {}, "trend": None, "prediction": [],
            "insight": None,
            "message": f"No data found for region: {region}",
        }

    preview_query = f"""
        SELECT time, latitude, longitude, temperature, salinity
        FROM argo_data
        WHERE {where_sql}
        ORDER BY time DESC
        LIMIT {RAW_PREVIEW_LIMIT}
    """
    cur.execute(preview_query, params)
    preview_rows = cur.fetchall()

    records = [
        {
            "date": row["time"],
            "year": int(str(row["time"])[:4]) if row["time"] else None,
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "temperature": float(row["temperature"]) if pd.notna(row["temperature"]) else None,
            "salinity": float(row["salinity"]) if pd.notna(row["salinity"]) else None,
        }
        for row in preview_rows
    ]

    mean_val = float(stats_row["mean_val"]) if stats_row["mean_val"] is not None else 0.0
    variance = float(stats_row["variance"]) if stats_row["variance"] is not None else 0.0
    std_val = float(np.sqrt(max(variance, 0.0)))

    stats = {
        "min": round(float(stats_row["min_val"]) if stats_row["min_val"] is not None else 0.0, 2),
        "max": round(float(stats_row["max_val"]) if stats_row["max_val"] is not None else 0.0, 2),
        "mean": round(mean_val, 2),
        "std": round(std_val, 2),
        "count": total_count,
    }

    yearly_query = f"""
        SELECT CAST(substr(time, 1, 4) AS INTEGER) AS year, AVG({col_name}) AS avg_value
        FROM argo_data
        WHERE {where_sql} AND {col_name} IS NOT NULL
        GROUP BY CAST(substr(time, 1, 4) AS INTEGER)
        ORDER BY year ASC
    """
    cur.execute(yearly_query, params)
    yearly_rows = cur.fetchall()

    years_arr = np.array([int(row["year"]) for row in yearly_rows], dtype=float)
    yearly_values = np.array([float(row["avg_value"]) for row in yearly_rows], dtype=float)

    yearly_data = [
        {"year": int(year), "value": round(float(value), 2)}
        for year, value in zip(years_arr, yearly_values)
    ]

    if len(years_arr) > 1:
        try:
            coeffs = np.polyfit(years_arr, yearly_values, 1)
            trend_per_year = round(float(coeffs[0]), 4)
            if np.isnan(trend_per_year):
                trend_per_year = 0.0
        except:
            trend_per_year = 0.0
    else:
        trend_per_year = 0.0

    trend = {
        "per_year":  trend_per_year,
        "direction": "rising" if trend_per_year > 0 else "falling" if trend_per_year < 0 else "stable",
    }

    # Prediction (5 years ahead)
    prediction_df = pd.DataFrame({
        "year": years_arr.astype(int),
        col_name: yearly_values,
    })
    pred_result = predictor.predict_trend(prediction_df, col_name, future_years=5)
    prediction_points = pred_result.get("predictions", []) if pred_result.get("success") else []

    # AI Insight
    insight = generate_insight(region, col_name, stats, trend)
    
    conn.close()

    response = {
        "region":    region,
        "parameter": col,
        "question":  question,
        "parsed": {
            "region": region, "parameter": col,
            "start_year": start_year or int(years_arr.min()),
            "end_year":   end_year   or int(years_arr.max()),
            "source": parsed_source,
        },
        "start_year": int(years_arr.min()),
        "end_year":   int(years_arr.max()),
        "raw_limit":  RAW_PREVIEW_LIMIT,
        "data":       records,
        "yearly_data": yearly_data,
        "stats":      stats,
        "trend":      trend,
        "prediction": prediction_points,   # [{year, value}, ...]
        "insight":    insight,             # {text, source}
    }
    
    return clean_nans(response)


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    groq_enabled = bool(os.getenv("GROQ_API_KEY"))
    return {
        "message": "Velora AI backend running",
        "version": "2.0.0",
        "llm": "groq/llama3-70b-8192" if groq_enabled else "rule-based",
        "data": "ARGO Real Dataset (25M+ records)",
    }


@app.get("/health")
def health():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM argo_data")
    count = cur.fetchone()[0]
    conn.close()
    return {"status": "healthy", "records": count}


@app.get("/regions")
def regions():
    return {"regions": list(REGION_BOUNDS.keys())}


@app.post("/query")
def query_nl(data: dict):
    """
    POST /query
    Body: { "question": "Show salinity in Atlantic Ocean from 2018 to 2021" }
    """
    question = data.get("question", "").strip()
    if not question:
        return {"error": "Please provide a question."}

    # LLM (or rule-based) parsing
    parsed = parse_query(question)

    if not parsed.get("region"):
        return {
            "error": "Region not recognised",
            "message": "Try mentioning Indian Ocean, Pacific Ocean, Atlantic Ocean, or Arctic Ocean.",
            "question": question,
            "parsed": parsed,
        }

    return build_response(
        region=parsed["region"],
        parameter=parsed.get("parameter", "temperature"),
        start_year=parsed.get("start_year"),
        end_year=parsed.get("end_year"),
        question=question,
        parsed_source=parsed.get("source", "rule-based"),
    )


@app.get("/query")
def query_get(
    region: str = QParam(...),
    start_year: Optional[int] = QParam(None),
    end_year:   Optional[int] = QParam(None),
    parameter:  Optional[str] = QParam("temperature"),
):
    """GET /query — for direct URL testing."""
    return build_response(region, parameter, start_year, end_year)
