from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import Optional
import os
import re

app = FastAPI(title="Velora AI Backend", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load dataset once ──────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "argo_sample.csv")
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

# ── Region aliases ─────────────────────────────────────────────────────────────
REGION_ALIASES = {
    "Indian Ocean":   ["indian", "india", "arabian", "bay of bengal"],
    "Pacific Ocean":  ["pacific", "pacific ocean"],
    "Atlantic Ocean": ["atlantic", "atlantic ocean"],
    "Arctic Ocean":   ["arctic", "north pole", "polar", "arct"],
}

def parse_natural_language(question: str) -> dict:
    """
    Rule-based NLP parser.
    Extracts: region, parameter, start_year, end_year from free-form text.
    """
    q = question.lower().strip()

    # ── Region detection ───────────────────────────────────────────────────────
    detected_region = None
    for region, aliases in REGION_ALIASES.items():
        if any(alias in q for alias in aliases):
            detected_region = region
            break

    # ── Parameter detection ────────────────────────────────────────────────────
    if "salin" in q:
        parameter = "salinity"
    else:
        parameter = "temperature"  # default

    # ── Year extraction ────────────────────────────────────────────────────────
    # Matches: "2015", "2015-2020", "2015 to 2020", "from 2015"
    years = re.findall(r"\b(20\d{2})\b", q)
    years = [int(y) for y in years]

    start_year = min(years) if len(years) >= 2 else (years[0] if years else None)
    end_year   = max(years) if len(years) >= 2 else None

    return {
        "region": detected_region,
        "parameter": parameter,
        "start_year": start_year,
        "end_year": end_year,
    }


def build_response(region: str, parameter: str, start_year, end_year, original_question: str = ""):
    """Shared logic: filter df, compute stats & trend, build JSON."""
    filtered = df[df["region"] == region].copy()

    if start_year:
        filtered = filtered[filtered["year"] >= start_year]
    if end_year:
        filtered = filtered[filtered["year"] <= end_year]

    if filtered.empty:
        return {
            "region": region,
            "parameter": parameter,
            "question": original_question,
            "parsed": {"region": region, "parameter": parameter,
                       "start_year": start_year, "end_year": end_year},
            "data": [],
            "stats": {},
            "trend": None,
            "message": f"No data found for region: {region}",
        }

    col = parameter if parameter in ["temperature", "salinity"] else "temperature"

    records = []
    for _, row in filtered.iterrows():
        records.append({
            "date": row["date"].strftime("%Y-%m-%d"),
            "year": int(row["year"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "temperature": float(row["temperature"]),
            "salinity": float(row["salinity"]),
        })

    values = filtered[col].tolist()
    stats = {
        "min":   round(float(np.min(values)), 2),
        "max":   round(float(np.max(values)), 2),
        "mean":  round(float(np.mean(values)), 2),
        "std":   round(float(np.std(values)), 2),
        "count": len(values),
    }

    years_arr = filtered["year"].values
    if len(years_arr) > 1:
        coeffs = np.polyfit(years_arr, filtered[col].values, 1)
        trend_per_year = round(float(coeffs[0]), 4)
    else:
        trend_per_year = 0.0

    return {
        "region": region,
        "parameter": col,
        "question": original_question,
        "parsed": {
            "region": region,
            "parameter": col,
            "start_year": start_year or int(filtered["year"].min()),
            "end_year": end_year or int(filtered["year"].max()),
        },
        "start_year": int(filtered["year"].min()),
        "end_year":   int(filtered["year"].max()),
        "data":  records,
        "stats": stats,
        "trend": {
            "per_year":  trend_per_year,
            "direction": "rising" if trend_per_year > 0 else "falling" if trend_per_year < 0 else "stable",
        },
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Velora AI backend running", "status": "healthy", "version": "1.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "records": len(df)}


@app.get("/regions")
def get_regions():
    return {"regions": sorted(df["region"].unique().tolist())}


@app.post("/query")
def query_natural_language(data: dict):
    """
    POST /query — natural language ocean query.
    Body: { "question": "Show temperature trend in Indian Ocean from 2015 to 2020" }
    """
    question = data.get("question", "").strip()
    if not question:
        return {"error": "Please provide a question."}

    parsed = parse_natural_language(question)

    if not parsed["region"]:
        return {
            "error": "Region not recognized",
            "message": "Try mentioning 'Indian Ocean', 'Pacific Ocean', 'Atlantic Ocean', or 'Arctic Ocean'.",
            "question": question,
            "parsed": parsed,
        }

    return build_response(
        region=parsed["region"],
        parameter=parsed["parameter"],
        start_year=parsed["start_year"],
        end_year=parsed["end_year"],
        original_question=question,
    )


@app.get("/query")
def query_get(
    region: str = Query(...),
    start_year: Optional[int] = Query(None),
    end_year: Optional[int] = Query(None),
    parameter: Optional[str] = Query("temperature"),
):
    """GET /query — kept for direct URL testing."""
    return build_response(region, parameter, start_year, end_year)
