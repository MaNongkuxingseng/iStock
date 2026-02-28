@echo off
echo Creating Minimal Frontend for iStock
echo ====================================
echo.

echo 1. Creating frontend directory structure...
if not exist "frontend" mkdir frontend
cd frontend

echo 2. Creating package.json...
echo {
echo   "name": "istock-frontend",
echo   "version": "1.0.0",
echo   "private": true,
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0",
echo     "react-router-dom": "^6.14.0",
echo     "axios": "^1.4.0",
echo     "chart.js": "^4.3.0",
echo     "react-chartjs-2": "^5.2.0"
echo   },
echo   "scripts": {
echo     "start": "react-scripts start",
echo     "build": "react-scripts build",
echo     "test": "react-scripts test",
echo     "eject": "react-scripts eject"
echo   },
echo   "devDependencies": {
echo     "react-scripts": "5.0.1",
echo     "@types/react": "^18.2.0",
echo     "@types/react-dom": "^18.2.0",
echo     "typescript": "^5.0.0"
echo   },
echo   "browserslist": {
echo     "production": [
echo       ">0.2%%",
echo       "not dead",
echo       "not op_mini all"
echo     ],
echo     "development": [
echo       "last 1 chrome version",
echo       "last 1 firefox version",
echo       "last 1 safari version"
echo     ]
echo   }
echo } > package.json

echo 3. Creating tsconfig.json...
echo {
echo   "compilerOptions": {
echo     "target": "es5",
echo     "lib": ["dom", "dom.iterable", "esnext"],
echo     "allowJs": true,
echo     "skipLibCheck": true,
echo     "esModuleInterop": true,
echo     "allowSyntheticDefaultImports": true,
echo     "strict": true,
echo     "forceConsistentCasingInFileNames": true,
echo     "noFallthroughCasesInSwitch": true,
echo     "module": "esnext",
echo     "moduleResolution": "node",
echo     "resolveJsonModule": true,
echo     "isolatedModules": true,
echo     "noEmit": true,
echo     "jsx": "react-jsx"
echo   },
echo   "include": ["src"]
echo } > tsconfig.json

echo 4. Creating public directory...
mkdir public
cd public

echo 5. Creating index.html...
echo ^<!DOCTYPE html^>
echo ^<html lang="en"^>
echo ^<head^>
echo   ^<meta charset="utf-8" /^>
echo   ^<link rel="icon" href="%PUBLIC_URL%/favicon.ico" /^>
echo   ^<meta name="viewport" content="width=device-width, initial-scale=1" /^>
echo   ^<meta name="theme-color" content="#000000" /^>
echo   ^<meta name="description" content="iStock - Intelligent Stock Analysis System" /^>
echo   ^<title^>iStock - Stock Analysis^</title^>
echo ^</head^>
echo ^<body^>
echo   ^<noscript^>You need to enable JavaScript to run this app.^</noscript^>
echo   ^<div id="root"^>^</div^>
echo ^</body^>
echo ^</html^> > index.html

cd ..

echo 6. Creating src directory...
mkdir src
cd src

echo 7. Creating minimal React app...
echo import React from 'react';
echo import ReactDOM from 'react-dom/client';
echo import './index.css';
echo import App from './App';
echo.
echo const root = ReactDOM.createRoot(
echo   document.getElementById('root') as HTMLElement
echo );
echo root.render(
echo   ^<React.StrictMode^>
echo     ^<App /^>
echo   ^</React.StrictMode^>
echo ); > index.tsx

echo 8. Creating App.tsx...
echo import React from 'react';
echo import './App.css';
echo.
echo function App() {
echo   return (
echo     ^<div className="App"^>
echo       ^<header className="App-header"^>
echo         ^<h1^>iStock - Intelligent Stock Analysis System^</h1^>
echo         ^<p^>
echo           Welcome to iStock! The backend services are starting up.
echo         ^</p^>
echo         ^<div className="status"^>
echo           ^<h2^>System Status^</h2^>
echo           ^<ul^>
echo             ^<li^>Backend API: ^<span className="status-loading"^>Checking...^</span^>^</li^>
echo             ^<li^>Database: ^<span className="status-loading"^>Checking...^</span^>^</li^>
echo             ^<li^>Redis: ^<span className="status-loading"^>Checking...^</span^>^</li^>
echo           ^</ul^>
echo         ^</div^>
echo       ^</header^>
echo     ^</div^>
echo   );
echo }
echo.
echo export default App; > App.tsx

echo 9. Creating CSS files...
echo body {
echo   margin: 0;
echo   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
echo     'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
echo     sans-serif;
echo   -webkit-font-smoothing: antialiased;
echo   -moz-osx-font-smoothing: grayscale;
echo   background-color: #282c34;
echo   color: white;
echo }
echo.
echo code {
echo   font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
echo     monospace;
echo } > index.css

echo .App {
echo   text-align: center;
echo   min-height: 100vh;
echo   display: flex;
echo   flex-direction: column;
echo   align-items: center;
echo   justify-content: center;
echo   font-size: calc(10px + 2vmin);
echo }
echo.
echo .App-header {
echo   padding: 20px;
echo   max-width: 800px;
echo }
echo.
echo .App-header h1 {
echo   color: #61dafb;
echo   margin-bottom: 30px;
echo }
echo.
echo .status {
echo   background-color: #20232a;
echo   padding: 20px;
echo   border-radius: 10px;
echo   margin-top: 30px;
echo   text-align: left;
echo }
echo.
echo .status h2 {
echo   color: #61dafb;
echo   border-bottom: 2px solid #61dafb;
echo   padding-bottom: 10px;
echo }
echo.
echo .status ul {
echo   list-style-type: none;
echo   padding: 0;
echo }
echo.
echo .status li {
echo   padding: 10px 0;
echo   border-bottom: 1px solid #444;
echo }
echo.
echo .status-loading {
echo   color: #ffa500;
echo   font-style: italic;
echo }
echo.
echo .status-ok {
echo   color: #4caf50;
echo }
echo.
echo .status-error {
echo   color: #f44336;
echo } > App.css

cd ..\..

echo.
echo ====================================
echo Minimal Frontend Created!
echo ====================================
echo.
echo Created files:
echo   frontend/package.json
echo   frontend/tsconfig.json
echo   frontend/public/index.html
echo   frontend/src/index.tsx
echo   frontend/src/App.tsx
echo   frontend/src/index.css
echo   frontend/src/App.css
echo.
echo Note: This is a minimal frontend for testing.
echo For production, you'll need to:
echo 1. Run: cd frontend && npm install
echo 2. Or let Docker build it automatically
echo.
echo Next: Run docker-compose up -d to build and start
pause