/**
 * iStock 主应用组件
 */

import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Stocks from './pages/Stocks';
import Portfolio from './pages/Portfolio';
import Login from './pages/Login';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // 检查用户登录状态
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  // 处理登录
  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  // 处理登出
  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>加载中...</p>
      </div>
    );
  }

  return (
    <AuthProvider value={{ isAuthenticated, handleLogin, handleLogout }}>
      <Router>
        <div className="App">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/login" element={
                !isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/" />
              } />
              <Route path="/" element={
                isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
              } />
              <Route path="/stocks" element={
                isAuthenticated ? <Stocks /> : <Navigate to="/login" />
              } />
              <Route path="/portfolio" element={
                isAuthenticated ? <Portfolio /> : <Navigate to="/login" />
              } />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
          <footer className="app-footer">
            <p>iStock &copy; 2026 - 智能股票分析系统</p>
            <p>版本 1.0.0 | 开发中</p>
          </footer>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;