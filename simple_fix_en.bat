@echo off
echo ========================================
echo iStock Quick Fix and Start
echo ========================================
echo.

echo [1] Check frontend directory...
if exist "frontend\src\App.js" (
    echo OK: Frontend directory exists
    dir /s /b frontend\*.* 2>nul | find /c /v "" >nul && (
        for /f %%i in ('dir /s /b frontend\*.* 2^>nul ^| find /c /v ""') do echo   Files: %%i
    )
) else (
    echo ERROR: Frontend key files missing
    echo Creating basic frontend structure...
    
    if not exist "frontend" mkdir frontend
    if not exist "frontend\src" mkdir frontend\src
    if not exist "frontend\public" mkdir frontend\public
    
    echo Creating package.json...
    echo { > frontend\package.json
    echo   "name": "istock-frontend", >> frontend\package.json
    echo   "version": "0.1.0", >> frontend\package.json
    echo   "private": true, >> frontend\package.json
    echo   "dependencies": { >> frontend\package.json
    echo     "react": "^18.2.0", >> frontend\package.json
    echo     "react-dom": "^18.2.0", >> frontend\package.json
    echo     "react-scripts": "5.0.1", >> frontend\package.json
    echo     "axios": "^1.6.2" >> frontend\package.json
    echo   }, >> frontend\package.json
    echo   "scripts": { >> frontend\package.json
    echo     "start": "react-scripts start", >> frontend\package.json
    echo     "build": "react-scripts build", >> frontend\package.json
    echo     "test": "react-scripts test", >> frontend\package.json
    echo     "eject": "react-scripts eject" >> frontend\package.json
    echo   } >> frontend\package.json
    echo } >> frontend\package.json
)

echo.
echo [2] Configure MySQL database...
if exist "configure_mysql.bat" (
    echo Running MySQL configuration...
    call configure_mysql.bat
) else (
    echo WARNING: MySQL config script not found
)

echo.
echo [3] Install backend dependencies...
if exist "backend\requirements.txt" (
    echo Installing Python dependencies...
    pip install -r backend\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if errorlevel 1 (
        echo Installing basic dependencies...
        pip install fastapi uvicorn sqlalchemy pymysql pydantic
    )
) else (
    echo ERROR: requirements.txt not found
)

echo.
echo [4] Install frontend dependencies...
cd frontend
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install --registry=https://registry.npmmirror.com
    
    if errorlevel 1 (
        echo Cleaning cache and retrying...
        npm cache clean --force
        del package-lock.json 2>nul
        rmdir /s /q node_modules 2>nul
        npm install --registry=https://registry.npmmirror.com
    )
) else (
    echo OK: node_modules exists
    echo Checking dependencies...
    npm list --depth=0 2>nul | findstr "react"
)
cd ..

echo.
echo [5] Fix missing backend code...
if not exist "backend\src\main.py" (
    echo Creating backend main file...
    if not exist "backend\src" mkdir backend\src
    
    echo from fastapi import FastAPI > backend\src\main.py
    echo from fastapi.middleware.cors import CORSMiddleware >> backend\src\main.py
    echo. >> backend\src\main.py
    echo app = FastAPI(title="iStock API", version="1.0.0") >> backend\src\main.py
    echo. >> backend\src\main.py
    echo # CORS configuration >> backend\src\main.py
    echo app.add_middleware( >> backend\src\main.py
    echo     CORSMiddleware, >> backend\src\main.py
    echo     allow_origins=["*"], >> backend\src\main.py
    echo     allow_credentials=True, >> backend\src\main.py
    echo     allow_methods=["*"], >> backend\src\main.py
    echo     allow_headers=["*"], >> backend\src\main.py
    echo ) >> backend\src\main.py
    echo. >> backend\src\main.py
    echo @app.get("/") >> backend\src\main.py
    echo async def root(): >> backend\src\main.py
    echo     return {"message": "iStock API is running"} >> backend\src\main.py
    echo. >> backend\src\main.py
    echo @app.get("/health") >> backend\src\main.py
    echo async def health_check(): >> backend\src\main.py
    echo     return {"status": "healthy", "service": "iStock API"} >> backend\src\main.py
    
    echo OK: Created backend\src\main.py
)

echo.
echo [6] Create startup script...
echo @echo off > start_services.bat
echo echo Starting iStock services... >> start_services.bat
echo echo. >> start_services.bat
echo echo [1] Starting backend API (port 8000)... >> start_services.bat
echo cd backend >> start_services.bat
echo start "iStock Backend" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload" >> start_services.bat
echo cd .. >> start_services.bat
echo timeout /t 5 /nobreak >nul >> start_services.bat
echo echo. >> start_services.bat
echo echo [2] Starting frontend dev server (port 3000)... >> start_services.bat
echo cd frontend >> start_services.bat
echo start "iStock Frontend" cmd /k "npm start" >> start_services.bat
echo cd .. >> start_services.bat
echo timeout /t 5 /nobreak >nul >> start_services.bat
echo echo. >> start_services.bat
echo echo [3] Opening browser... >> start_services.bat
echo start http://localhost:8000/docs >> start_services.bat
echo start http://localhost:3000 >> start_services.bat
echo echo. >> start_services.bat
echo echo === Services started === >> start_services.bat
echo echo Backend API: http://localhost:8000 >> start_services.bat
echo echo API docs: http://localhost:8000/docs >> start_services.bat
echo echo Frontend app: http://localhost:3000 >> start_services.bat
echo echo. >> start_services.bat
echo echo Press any key to check service status... >> start_services.bat
echo pause >nul >> start_services.bat
echo curl http://localhost:8000/health 2^>nul >> start_services.bat
echo echo. >> start_services.bat
echo echo Press any key to exit... >> start_services.bat
echo pause >nul >> start_services.bat

echo OK: Created start_services.bat

echo.
echo ========================================
echo QUICK FIX COMPLETED
echo ========================================
echo.
echo Next steps:
echo 1. Run start_services.bat to start all services
echo 2. Check backend: http://localhost:8000/health
echo 3. Check frontend: http://localhost:3000
echo 4. Check API docs: http://localhost:8000/docs
echo.
echo If services don't start:
echo - Check Python dependencies: pip list | findstr fastapi
echo - Check Node.js: node --version
echo - Check MySQL: configure_mysql.bat
echo.
pause