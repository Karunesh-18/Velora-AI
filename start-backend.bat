@echo off
echo ====================================
echo   Starting Velora AI Backend
echo ====================================
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo   Starting FastAPI Server
echo ====================================
echo Backend will run at: http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

uvicorn main:app --reload
