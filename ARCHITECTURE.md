# 🌊 Velora AI - Complete Project Structure

## 📁 Full Directory Tree

```
velora-ai/
│
├── 📄 PROJECT_README.md           # Full documentation
├── 📄 QUICKSTART.md               # Quick start guide
├── 📄 SETUP_COMPLETE.md           # Setup completion guide
├── 📄 Readme.md                   # Original readme
│
├── 🚀 start-backend.bat           # Windows backend launcher
├── 🚀 start-backend.sh            # Linux/Mac backend launcher
├── 🚀 start-frontend.bat          # Windows frontend launcher
├── 🚀 start-frontend.sh           # Linux/Mac frontend launcher
│
├── 📂 backend/
│   ├── 📄 main.py                 # FastAPI application
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 .env.example           # Environment template
│   │
│   ├── 📂 ai/
│   │   ├── 📄 __init__.py        # Module init
│   │   ├── 🧠 query_parser.py    # NLP query parser
│   │   ├── 📊 predictor.py       # ML prediction engine
│   │   └── 💡 insight_generator.py # AI insights
│   │
│   ├── 📂 data/
│   │   └── 📄 argo_sample.csv    # Sample ocean data
│   │
│   └── 📂 venv/                   # Python virtual environment
│
└── 📂 frontend/
    ├── 📄 package.json            # Node dependencies
    ├── 📄 vite.config.js         # Vite configuration
    ├── 📄 index.html             # HTML entry point
    │
    ├── 📂 src/
    │   ├── 📄 main.jsx           # React entry point
    │   ├── ⚛️ App.jsx             # Main React component
    │   ├── 🎨 App.css            # Main styles
    │   ├── 🎨 index.css          # Global styles
    │   │
    │   ├── 📂 components/
    │   │   ├── 📈 TrendChart.jsx  # Chart visualization
    │   │   └── 🗺️ MapView.jsx     # Map visualization
    │   │
    │   └── 📂 assets/             # Static assets
    │
    └── 📂 node_modules/           # Installed packages
```

## 🔗 Data Flow Architecture

```
┌─────────────┐
│   User      │
│  Browser    │
└──────┬──────┘
       │ 1. Natural Language Query
       │ "Show temperature in Indian Ocean"
       ▼
┌─────────────────────────────────────────────┐
│          React Frontend (Port 5173)         │
│  ┌────────────┐  ┌────────────┐            │
│  │  App.jsx   │  │ Components │            │
│  │  (Main UI) │  │ - Charts   │            │
│  │            │  │ - Maps     │            │
│  └────────────┘  └────────────┘            │
└──────────────────┬──────────────────────────┘
                   │ 2. HTTP POST /query
                   │ { "query": "..." }
                   ▼
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)         │
│  ┌─────────────────────────────────────┐   │
│  │           main.py                   │   │
│  │  • Receives request                 │   │
│  │  • Validates input                  │   │
│  │  • Coordinates AI modules           │   │
│  └───┬───────────────────────────┬─────┘   │
│      │ 3. Parse Query            │         │
│      ▼                           │         │
│  ┌──────────────────┐            │         │
│  │  query_parser.py │            │         │
│  │  • Extract region │            │         │
│  │  • Extract params │            │         │
│  │  • Extract dates  │            │         │
│  └────────┬─────────┘            │         │
│           │ 4. Filtered Data     │         │
│           ▼                      │         │
│  ┌──────────────────┐            │         │
│  │   Data Loading   │            │         │
│  │  • Read CSV      │            │         │
│  │  • Filter by     │            │         │
│  │    parsed params │            │         │
│  └────────┬─────────┘            │         │
│           │ 5. Process Data      │         │
│           ▼                      │         │
│  ┌──────────────────┐            │         │
│  │   predictor.py   │            │         │
│  │  • Calculate     │            │         │
│  │    statistics    │            │         │
│  │  • Train model   │            │         │
│  │  • Predict trend │            │         │
│  └────────┬─────────┘            │         │
│           │ 6. Generate Insight  │         │
│           ▼                      │         │
│  ┌──────────────────┐            │         │
│  │ insight_gen.py   │            │         │
│  │  • Format data   │            │         │
│  │  • Add context   │            │         │
│  │  • Create summary│            │         │
│  └────────┬─────────┘            │         │
│           │ 7. Return JSON       │         │
└───────────┼──────────────────────┼─────────┘
            │                      │
            ▼                      │
┌─────────────────────────────────────────────┐
│  {                                          │
│    "region": "Indian Ocean",                │
│    "parameter": "temperature",              │
│    "data": [...],                           │
│    "prediction": {...},                     │
│    "insight": "..."                         │
│  }                                          │
└──────────────────┬──────────────────────────┘
                   │ 8. Display Results
                   ▼
          ┌────────────────┐
          │  React UI      │
          │  • Show charts │
          │  • Show maps   │
          │  • Show text   │
          └────────────────┘
```

## 🛠️ Technology Stack Details

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core language |
| **FastAPI** | 0.115.0 | Web framework |
| **Uvicorn** | 0.32.0 | ASGI server |
| **Pandas** | 2.2.3 | Data processing |
| **NumPy** | 2.1.3 | Numerical computing |
| **Scikit-learn** | 1.5.2 | Machine learning |
| **OpenAI** | 1.54.3 | Optional LLM integration |
| **Pydantic** | 2.9.2 | Data validation |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.3.1 | UI framework |
| **Vite** | 7.x | Build tool |
| **Axios** | Latest | HTTP client |
| **Recharts** | Latest | Chart library |
| **Leaflet** | Latest | Map library |
| **React-Leaflet** | Latest | React map bindings |

## 🔌 API Endpoints

### Base URL: `http://127.0.0.1:8000`

#### `GET /`
- **Description**: Health check
- **Response**: `{ "message": "Velora AI backend running" }`

#### `GET /health`
- **Description**: Service health status
- **Response**: `{ "status": "healthy" }`

#### `POST /query`
- **Description**: Process natural language query
- **Request Body**:
  ```json
  {
    "query": "Show temperature trend in Indian Ocean from 2015-2020"
  }
  ```
- **Response**:
  ```json
  {
    "region": "Indian Ocean",
    "parameter": "temperature",
    "start_year": 2015,
    "end_year": 2020,
    "data": [...],
    "prediction": {
      "trend": "increasing",
      "confidence": "high",
      "predictions": [...]
    },
    "insight": "Analysis text..."
  }
  ```

#### `GET /docs`
- **Description**: Interactive API documentation (Swagger UI)
- **Access**: Open in browser when backend is running

## 📊 Sample Data Structure

### ARGO Dataset (CSV)
```csv
year,region,latitude,longitude,temperature,salinity,oxygen,pressure
2015,Indian Ocean,-10.5,75.2,28.5,35.2,220.5,10.2
2016,Indian Ocean,-10.2,75.5,28.7,35.3,219.2,10.3
...
```

### Field Descriptions
- **year**: Measurement year (2015-2020)
- **region**: Ocean region (Indian, Pacific, Atlantic)
- **latitude**: Latitude coordinate
- **longitude**: Longitude coordinate
- **temperature**: Water temperature (°C)
- **salinity**: Salinity (PSU - Practical Salinity Units)
- **oxygen**: Dissolved oxygen (μmol/kg)
- **pressure**: Water pressure (dbar)

## 🎨 Frontend Components

### App.jsx
- Main application container
- Handles API communication
- Manages state
- Displays query interface

### TrendChart.jsx
- Visualizes time series data
- Uses Recharts library
- Shows trends and predictions
- Interactive tooltips

### MapView.jsx
- Displays geographic data
- Uses Leaflet/OpenStreetMap
- Shows data collection points
- Pop-ups with details

## 🧠 AI Modules

### query_parser.py
**Purpose**: Convert natural language to structured queries

**Features**:
- Keyword extraction
- Region detection
- Parameter identification
- Date range parsing
- Optional GPT integration

**Example**:
```python
parser = QueryParser()
result = parser.parse("Show temperature in Indian Ocean from 2015-2020")
# Returns: {
#   "region": "Indian Ocean",
#   "parameter": "temperature",
#   "start_year": 2015,
#   "end_year": 2020
# }
```

### predictor.py
**Purpose**: Perform statistical analysis and predictions

**Features**:
- Linear regression
- Trend detection
- Anomaly detection
- Statistical summaries
- Confidence scoring

**Methods**:
- `predict_trend()`: Future predictions
- `detect_anomalies()`: Outlier detection
- `calculate_statistics()`: Summary stats

### insight_generator.py
**Purpose**: Generate human-readable insights

**Features**:
- Natural language summaries
- Climate context
- Warning detection
- Template-based generation
- Optional GPT enhancement

## 🚦 Startup Sequence

### Correct Order:
1. **Start Backend First** (Port 8000)
2. **Start Frontend Second** (Port 5173)

### Why?
- Frontend checks backend connection on load
- CORS is configured for localhost:5173
- API availability test runs immediately

## 🔐 Environment Variables

### Backend (.env)
```bash
# Optional - for advanced AI features
OPENAI_API_KEY=sk-...

# Server configuration
HOST=127.0.0.1
PORT=8000

# Allowed origins
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend (.env)
```bash
# API endpoint
VITE_API_URL=http://127.0.0.1:8000
```

## 📈 Performance Notes

- **Backend startup**: ~2-3 seconds
- **Frontend startup**: ~500ms (hot reload)
- **Query processing**: 100-500ms
- **Data loading**: <50ms (sample dataset)
- **Prediction**: 10-100ms

## 🎯 Development Workflow

1. **Make backend changes** → Auto-reload with `--reload`
2. **Make frontend changes** → HMR (Hot Module Replacement)
3. **Test API** → http://127.0.0.1:8000/docs
4. **Test UI** → http://localhost:5173
5. **Check console** → Browser DevTools & Terminal

## 📦 Build for Production

### Backend
```bash
# No build needed - Python runs directly
# For deployment, use:
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Creates dist/ folder with optimized files
```

## 🎓 Learning Resources

### FastAPI
- Docs: https://fastapi.tiangolo.com
- Tutorial: /docs endpoint (interactive)

### React
- Docs: https://react.dev
- Vite: https://vite.dev

### Data Science
- Pandas: https://pandas.pydata.org
- Scikit-learn: https://scikit-learn.org

## ✨ Ready to Code!

Everything is set up and ready. Your next steps:

1. Run both servers
2. Test the example queries
3. Start customizing!

Happy coding! 🚀
