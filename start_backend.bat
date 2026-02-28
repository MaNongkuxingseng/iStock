@echo off
echo Starting iStock Backend API Service...
echo.

cd backend

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.

python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

pause