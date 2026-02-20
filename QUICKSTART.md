# Velora AI - Quick Start Guide

## 🚀 Quick Setup (15 minutes)

### Option 1: Using Startup Scripts (Recommended)

**Windows:**
1. Open two terminal windows
2. In terminal 1: Double-click `start-backend.bat` or run:
   ```
   .\start-backend.bat
   ```
3. In terminal 2: Double-click `start-frontend.bat` or run:
   ```
   .\start-frontend.bat
   ```

**Mac/Linux:**
1. Make scripts executable:
   ```bash
   chmod +x start-backend.sh start-frontend.sh
   ```
2. Open two terminals
3. In terminal 1: `./start-backend.sh`
4. In terminal 2: `./start-frontend.sh`

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 🧪 Test Queries

Try these example queries in the app:

1. "Show temperature trend in Indian Ocean from 2015-2020"
2. "Analyze salinity in Pacific Ocean"
3. "What is the oxygen level in Atlantic Ocean?"

## ✅ Verification Checklist

- [ ] Backend running at port 8000
- [ ] Frontend running at port 5173
- [ ] Frontend shows "Velora AI backend running" status
- [ ] Can submit a query and see results

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 8000 is already in use
- Try: `pip install --upgrade pip`

### Frontend won't start
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is already in use

### CORS errors
- Make sure backend is running before frontend
- Check backend console for errors

## 📦 Dependencies

**Backend:**
- Python 3.8+
- FastAPI, uvicorn, pandas, numpy, scikit-learn

**Frontend:**
- Node.js 16+
- React, Vite, Axios, Recharts, Leaflet

## 🎯 Next Steps

1. Explore the AI modules in `backend/ai/`
2. Customize the frontend components in `frontend/src/components/`
3. Add your own ARGO data to `backend/data/`
4. Integrate OpenAI API for advanced features

## 📚 Documentation

- Full documentation: `PROJECT_README.md`
- API documentation: http://127.0.0.1:8000/docs (when backend is running)
