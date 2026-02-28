/**
 * 应用头部组件
 */

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Header.css';

function Header() {
  const { isAuthenticated, handleLogout } = useAuth();
  const navigate = useNavigate();

  const handleLogoutClick = () => {
    handleLogout();
    navigate('/login');
  };

  return (
    <header className="app-header">
      <div className="header-container">
        <div className="logo">
          <Link to="/">
            <h1>📈 iStock</h1>
            <span className="logo-subtitle">智能股票分析系统</span>
          </Link>
        </div>
        
        <nav className="main-nav">
          {isAuthenticated ? (
            <>
              <Link to="/" className="nav-link">
                <span className="nav-icon">🏠</span>
                <span className="nav-text">仪表板</span>
              </Link>
              <Link to="/stocks" className="nav-link">
                <span className="nav-icon">📊</span>
                <span className="nav-text">股票</span>
              </Link>
              <Link to="/portfolio" className="nav-link">
                <span className="nav-icon">💰</span>
                <span className="nav-text">投资组合</span>
              </Link>
              <button onClick={handleLogoutClick} className="logout-btn">
                <span className="nav-icon">🚪</span>
                <span className="nav-text">退出</span>
              </button>
            </>
          ) : (
            <Link to="/login" className="nav-link">
              <span className="nav-icon">🔑</span>
              <span className="nav-text">登录</span>
            </Link>
          )}
        </nav>
        
        <div className="user-info">
          {isAuthenticated && (
            <div className="user-profile">
              <span className="user-avatar">👤</span>
              <span className="user-name">用户</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;