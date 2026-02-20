# ⚡ START HERE - Velora AI Quick Launch

## 🎯 Fastest Way to Get Running (2 Steps)

### Step 1: Start Backend
Open a terminal and run:

**Windows:**
```cmd
.\start-backend.bat
```

**Mac/Linux:**
```bash
chmod +x start-backend.sh
./start-backend.sh
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Step 2: Start Frontend
Open a **NEW** terminal and run:

**Windows:**
```cmd
.\start-frontend.bat
```

**Mac/Linux:**
```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

Wait for: `Local: http://localhost:5173/`

## ✅ Open Your Browser

Navigate to: **http://localhost:5173**

You should see:
- 🌊 Velora AI header
- Green "Velora AI backend running" status
- Query input box

## 🧪 Try These Queries

1. `Show temperature trend in Indian Ocean from 2015-2020`
2. `Analyze salinity in Pacific Ocean`
3. `What is the oxygen level in Atlantic Ocean?`

## 📚 Need More Help?

- **Quick Setup**: Read `QUICKSTART.md`
- **Full Documentation**: Read `PROJECT_README.md`
- **Architecture Details**: Read `ARCHITECTURE.md`
- **Setup Verification**: Read `SETUP_COMPLETE.md`

## 🐛 Something Not Working?

### Backend won't start?
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend won't start?
```bash
cd frontend
npm install
npm run dev
```

### Port already in use?
- Backend (8000): Stop other apps using port 8000
- Frontend (5173): Vite will auto-select another port

## 🎉 That's It!

You're ready to build your ocean intelligence platform!

Happy Hacking! 🚀🌊
