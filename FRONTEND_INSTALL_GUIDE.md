@echo off
echo ========================================
echo iStock前端快速启动脚本
echo ========================================
echo.

echo [1/6] 检查Node.js环境...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
    echo 请访问 https://nodejs.org/ 下载LTS版本
    pause
    exit /b 1
)

for /f %%i in ('node --version') do set "NODE_VERSION=%%i"
echo ✅ Node.js版本: %NODE_VERSION%

where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm未安装
    pause
    exit /b 1
)

for /f %%i in ('npm --version') do set "NPM_VERSION=%%i"
echo ✅ npm版本: %NPM_VERSION%

echo.
echo [2/6] 检查前端目录...
if not exist "frontend" (
    echo ❌ frontend目录不存在
    mkdir frontend
    echo ✅ 创建frontend目录
)

cd frontend

echo.
echo [3/6] 检查package.json...
if not exist "package.json" (
    echo ⚠️  package.json不存在，创建基本配置...
    
    echo { > package.json
    echo   "name": "istock-frontend", >> package.json
    echo   "version": "0.1.0", >> package.json
    echo   "private": true, >> package.json
    echo   "dependencies": { >> package.json
    echo     "react": "^18.2.0", >> package.json
    echo     "react-dom": "^18.2.0", >> package.json
    echo     "react-scripts": "5.0.1" >> package.json
    echo   }, >> package.json
    echo   "scripts": { >> package.json
    echo     "start": "react-scripts start", >> package.json
    echo     "build": "react-scripts build", >> package.json
    echo     "test": "react-scripts test", >> package.json
    echo     "eject": "react-scripts eject" >> package.json
    echo   }, >> package.json
    echo   "eslintConfig": { >> package.json
    echo     "extends": ["react-app"] >> package.json
    echo   }, >> package.json
    echo   "browserslist": { >> package.json
    echo     "production": [ >> package.json
    echo       ">0.2%", >> package.json
    echo       "not dead", >> package.json
    echo       "not op_mini all" >> package.json
    echo     ], >> package.json
    echo     "development": [ >> package.json
    echo       "last 1 chrome version", >> package.json
    echo       "last 1 firefox version", >> package.json
    echo       "last 1 safari version" >> package.json
    echo     ] >> package.json
    echo   } >> package.json
    echo } >> package.json
    
    echo ✅ 创建package.json
)

echo.
echo [4/6] 检查src目录...
if not exist "src" (
    mkdir src
    echo ✅ 创建src目录
)

if not exist "src\App.js" (
    echo 创建基本App.js...
    
    echo import React from "react"; > src\App.js
    echo import "./App.css"; >> src\App.js
    echo. >> src\App.js
    echo function App() { >> src\App.js
    echo   return ( >> src\App.js
    echo     <div className="App"> >> src\App.js
    echo       <h1>iStock - 智能股票分析系统</h1> >> src\App.js
    echo       <p>前端应用加载成功！</p> >> src\App.js
    echo       <p>请检查后端API是否运行: http://localhost:8000</p> >> src\App.js
    echo     </div> >> src\App.js
    echo   ); >> src\App.js
    echo } >> src\App.js
    echo. >> src\App.js
    echo export default App; >> src\App.js
    
    echo ✅ 创建App.js
)

if not exist "src\index.js" (
    echo 创建基本index.js...
    
    echo import React from "react"; > src\index.js
    echo import ReactDOM from "react-dom/client"; >> src\index.js
    echo import "./index.css"; >> src\index.js
    echo import App from "./App"; >> src\index.js
    echo. >> src\index.js
    echo const root = ReactDOM.createRoot(document.getElementById("root")); >> src\index.js
    echo root.render( >> src\index.js
    echo   <React.StrictMode> >> src\index.js
    echo     <App /> >> src\index.js
    echo   </React.StrictMode> >> src\index.js
    echo ); >> src\index.js
    
    echo ✅ 创建index.js
)

if not exist "public" (
    mkdir public
    echo ✅ 创建public目录
)

if not exist "public\index.html" (
    echo 创建基本index.html...
    
    echo ^<!DOCTYPE html^> > public\index.html
    echo ^<html lang="en"^> >> public\index.html
    echo ^<head^> >> public\index.html
    echo   ^<meta charset="utf-8" /^> >> public\index.html
    echo   ^<link rel="icon" href="%PUBLIC_URL%/favicon.ico" /^> >> public\index.html
    echo   ^<meta name="viewport" content="width=device-width, initial-scale=1" /^> >> public\index.html
    echo   ^<meta name="theme-color" content="#000000" /^> >> public\index.html
    echo   ^<meta name="description" content="iStock智能股票分析系统" /^> >> public\index.html
    echo   ^<title^>iStock - 智能股票分析系统^</title^> >> public\index.html
    echo ^</head^> >> public\index.html
    echo ^<body^> >> public\index.html
    echo   ^<noscript^>You need to enable JavaScript to run this app.^</noscript^> >> public\index.html
    echo   ^<div id="root"^>^</div^> >> public\index.html
    echo ^</body^> >> public\index.html
    echo ^</html^> >> public\index.html
    
    echo ✅ 创建index.html
)

echo.
echo [5/6] 安装依赖...
echo 使用淘宝镜像加速...
npm install --registry=https://registry.npmmirror.com

if %errorlevel% neq 0 (
    echo ⚠️  安装失败，清理缓存重试...
    npm cache clean --force
    del package-lock.json 2>nul
    rmdir /s /q node_modules 2>nul
    npm install --registry=https://registry.npmmirror.com
)

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    echo 请手动检查网络或Node.js配置
    pause
    exit /b 1
)

echo ✅ 依赖安装成功

echo.
echo [6/6] 启动开发服务器...
echo 前端应用将在 http://localhost:3000 启动
echo 按 Ctrl+C 停止服务
echo.
npm start

cd ..
pause