@echo off
echo ========================================
echo iStock IMMEDIATE DEVELOPMENT START
echo ========================================
echo.

echo [PHASE 1] Git Commit Current Work
echo.

echo Checking Git status...
git status

echo.
echo Adding all files...
git add .

echo.
echo Committing with Chinese message...
git commit -m "feat: 立即开始iStock开发 - 修复前端目录和配置MySQL"

echo.
echo Pushing to GitHub...
git push origin develop

echo.
echo [PHASE 2] Start Development Services
echo.

echo Starting backend API...
cd backend
start "iStock Backend" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting frontend development server...
cd frontend
start "iStock Frontend" cmd /k "npm start"
cd ..

echo Waiting 5 seconds for frontend to start...
timeout /t 5 /nobreak >nul

echo.
echo [PHASE 3] Open Development Tools
echo.

echo Opening browser tabs...
start http://localhost:8000/docs
start http://localhost:3000

echo.
echo [PHASE 4] Create Development Tasks
echo.

echo Creating development task list...
echo # iStock开发任务清单 > DEV_TASKS.md
echo. >> DEV_TASKS.md
echo ## 立即执行的任务 >> DEV_TASKS.md
echo. >> DEV_TASKS.md
echo - [ ] 验证后端API运行: http://localhost:8000/health >> DEV_TASKS.md
echo - [ ] 验证前端运行: http://localhost:3000 >> DEV_TASKS.md
echo - [ ] 测试MySQL数据库连接 >> DEV_TASKS.md
echo - [ ] 创建基础数据表 >> DEV_TASKS.md
echo - [ ] 实现股票数据API >> DEV_TASKS.md
echo - [ ] 实现用户认证API >> DEV_TASKS.md
echo - [ ] 创建前端股票列表组件 >> DEV_TASKS.md
echo - [ ] 创建前端仪表板 >> DEV_TASKS.md
echo. >> DEV_TASKS.md
echo ## 今日目标 >> DEV_TASKS.md
echo. >> DEV_TASKS.md
echo 1. 完成基础API开发 >> DEV_TASKS.md
echo 2. 完成前端基础界面 >> DEV_TASKS.md
echo 3. 实现数据库操作 >> DEV_TASKS.md
echo 4. 测试完整流程 >> DEV_TASKS.md

echo.
echo [PHASE 5] Start Coding
echo.

echo Creating first API endpoint...
if not exist "backend\src\api" mkdir backend\src\api

echo Creating stocks API...
echo from fastapi import APIRouter, HTTPException > backend\src\api\stocks.py
echo from typing import List >> backend\src\api\stocks.py
echo from pydantic import BaseModel >> backend\src\api\stocks.py
echo from datetime import datetime >> backend\src\api\stocks.py
echo. >> backend\src\api\stocks.py
echo router = APIRouter() >> backend\src\api\stocks.py
echo. >> backend\src\api\stocks.py
echo class StockResponse(BaseModel): >> backend\src\api\stocks.py
echo     symbol: str >> backend\src\api\stocks.py
echo     name: str >> backend\src\api\stocks.py
echo     price: float >> backend\src\api\stocks.py
echo     change: float >> backend\src\api\stocks.py
echo     change_percent: float >> backend\src\api\stocks.py
echo. >> backend\src\api\stocks.py
echo @router.get("/", response_model=List[StockResponse]) >> backend\src\api\stocks.py
echo async def get_stocks(): >> backend\src\api\stocks.py
echo     # Mock data for now >> backend\src\api\stocks.py
echo     return [ >> backend\src\api\stocks.py
echo         StockResponse( >> backend\src\api\stocks.py
echo             symbol="000001", >> backend\src\api\stocks.py
echo             name="平安银行", >> backend\src\api\stocks.py
echo             price=15.42, >> backend\src\api\stocks.py
echo             change=0.32, >> backend\src\api\stocks.py
echo             change_percent=2.12 >> backend\src\api\stocks.py
echo         ), >> backend\src\api\stocks.py
echo         StockResponse( >> backend\src\api\stocks.py
echo             symbol="000002", >> backend\src\api\stocks.py
echo             name="万科A", >> backend\src\api\stocks.py
echo             price=12.85, >> backend\src\api\stocks.py
echo             change=-0.15, >> backend\src\api\stocks.py
echo             change_percent=-1.15 >> backend\src\api\stocks.py
echo         ) >> backend\src\api\stocks.py
echo     ] >> backend\src\api\stocks.py
echo. >> backend\src\api\stocks.py
echo @router.get("/{symbol}") >> backend\src\api\stocks.py
echo async def get_stock(symbol: str): >> backend\src\api\stocks.py
echo     return {"symbol": symbol, "message": "Stock details endpoint"} >> backend\src\api\stocks.py

echo.
echo Updating main.py to include stocks router...
echo from .api.stocks import router as stocks_router >> backend\src\main_temp.py
type backend\src\main.py > backend\src\main_backup.py
findstr /v "app.include_router" backend\src\main_backup.py > backend\src\main.py
echo. >> backend\src\main.py
echo app.include_router(stocks_router, prefix="/api/stocks", tags=["stocks"]) >> backend\src\main.py

echo.
echo ========================================
echo DEVELOPMENT STARTED
echo ========================================
echo.
echo Services running:
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo - Frontend: http://localhost:3000
echo - Stocks API: http://localhost:8000/api/stocks
echo.
echo Development tasks: DEV_TASKS.md
echo.
echo Next: Start coding immediately!
echo.
pause