from fastapi import FastAPI, Query as QParam
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Optional
import os
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
                   "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load dataset ───────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "argo_sample.csv")
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

predictor = OceanPredictor()


# ── Shared filter + response builder ──────────────────────────────────────────
def build_response(region: str, parameter: str, start_year, end_year,
                   question: str = "", parsed_source: str = "rule-based"):

    col = parameter if parameter in ["temperature", "salinity"] else "temperature"
    filtered = df[df["region"] == region].copy()

    if start_year:
        filtered = filtered[filtered["year"] >= start_year]
    if end_year:
        filtered = filtered[filtered["year"] <= end_year]

    if filtered.empty:
        return {
            "region": region, "parameter": col, "question": question,
            "parsed": {"region": region, "parameter": col,
                       "start_year": start_year, "end_year": end_year,
                       "source": parsed_source},
            "data": [], "stats": {}, "trend": None, "prediction": [],
            "insight": None,
            "message": f"No data found for region: {region}",
        }

    # Records
    records = [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "year": int(row["year"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "temperature": float(row["temperature"]),
            "salinity": float(row["salinity"]),
        }
        for _, row in filtered.iterrows()
    ]

    # Stats
    values = filtered[col].values
    stats = {
        "min":   round(float(np.min(values)),  2),
        "max":   round(float(np.max(values)),  2),
        "mean":  round(float(np.mean(values)), 2),
        "std":   round(float(np.std(values)),  2),
        "count": len(values),
    }

    # Trend
    years_arr = filtered["year"].values
    if len(years_arr) > 1:
        coeffs = np.polyfit(years_arr, values, 1)
        trend_per_year = round(float(coeffs[0]), 4)
    else:
        trend_per_year = 0.0

    trend = {
        "per_year":  trend_per_year,
        "direction": "rising" if trend_per_year > 0 else "falling" if trend_per_year < 0 else "stable",
    }

    # Prediction (5 years ahead)
    pred_result = predictor.predict_trend(filtered, col, future_years=5)
    prediction_points = pred_result.get("predictions", []) if pred_result.get("success") else []

    # AI Insight
    insight = generate_insight(region, col, stats, trend)

    return {
        "region":    region,
        "parameter": col,
        "question":  question,
        "parsed": {
            "region": region, "parameter": col,
            "start_year": start_year or int(filtered["year"].min()),
            "end_year":   end_year   or int(filtered["year"].max()),
            "source": parsed_source,
        },
        "start_year": int(filtered["year"].min()),
        "end_year":   int(filtered["year"].max()),
        "data":       records,
        "stats":      stats,
        "trend":      trend,
        "prediction": prediction_points,   # [{year, value}, ...]
        "insight":    insight,             # {text, source}
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    groq_enabled = bool(os.getenv("GROQ_API_KEY"))
    return {
        "message": "Velora AI backend running",
        "version": "2.0.0",
        "llm": "groq/llama3-70b-8192" if groq_enabled else "rule-based",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "records": len(df)}


@app.get("/regions")
def regions():
    return {"regions": sorted(df["region"].unique().tolist())}


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
