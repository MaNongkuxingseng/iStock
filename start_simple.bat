@echo off
echo ========================================
echo iStock Simple Development Start
echo ========================================
echo.

echo [1] Install missing dependencies...
pip install uvicorn fastapi sqlalchemy pymysql

echo.
echo [2] Start backend API...
cd backend
start cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo [3] Start frontend development...
cd frontend
start cmd /k "npm start"
cd ..

echo Waiting for frontend to start...
timeout /t 5 /nobreak >nul

echo.
echo [4] Open browser...
start http://localhost:8000/docs
start http://localhost:3000

echo.
echo ========================================
echo Development Started!
echo ========================================
echo.
echo Services:
echo - Backend: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo - Frontend: http://localhost:3000
echo.
echo Start coding now!
echo.
pause