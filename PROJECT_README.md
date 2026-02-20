# Velora AI - Ocean Intelligence Platform

This project is an AI-powered ocean data analysis platform built for hackathons.

## 🏗 Architecture

- **Frontend**: React (Vite) with Axios, Recharts, and Leaflet
- **Backend**: FastAPI with Python
- **AI Layer**: Query parsing, prediction, and insight generation

## 📂 Project Structure

```
velora-ai/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── data/
│   │   └── argo_sample.csv  # Sample ocean data
│   └── ai/
│       ├── query_parser.py      # NLP query parsing
│       ├── predictor.py         # Time series prediction
│       └── insight_generator.py # AI insight generation
│
└── frontend/
    ├── src/
    │   ├── App.jsx              # Main React app
    │   ├── components/
    │   │   ├── TrendChart.jsx   # Chart visualization
    │   │   └── MapView.jsx      # Map visualization
    │   └── ...
    └── package.json
```

## 🚀 Getting Started

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

Backend will run at: `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies (if not already done):
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 🔧 Configuration

### Optional: OpenAI API (for advanced features)

Create a `.env` file in the `backend` directory:

```
OPENAI_API_KEY=your_api_key_here
```

Without this, the system will use template-based parsing and insights.

## 📊 Usage

1. Start both backend and frontend servers
2. Open `http://localhost:5173` in your browser
3. Enter a natural language query like:
   - "Show temperature trend in Indian Ocean from 2015-2020"
   - "Analyze salinity in Pacific Ocean"
   - "What's the oxygen level in Atlantic Ocean?"

## 🛠 Tech Stack

### Frontend
- React 18
- Vite
- Axios (API calls)
- Recharts (charts)
- Leaflet (maps)

### Backend
- FastAPI
- Pandas (data processing)
- NumPy
- Scikit-learn (predictions)
- OpenAI API (optional)

## ⚡ Features

- Natural language query parsing
- Time series trend analysis
- Predictive modeling
- AI-generated insights
- Interactive visualizations
- Map-based data display

## 📝 Development Notes

This is a hackathon-ready template with:
- ✅ Clean architecture
- ✅ Pre-configured CORS
- ✅ Sample dataset included
- ✅ AI modules ready to extend
- ✅ Professional UI

## 🎯 Next Steps

1. Add more sophisticated LLM integration
2. Expand the ARGO dataset
3. Add more visualization types
4. Implement user authentication
5. Deploy to cloud (Vercel + Render/Railway)

## 📄 License

MIT License - Free for hackathon use
