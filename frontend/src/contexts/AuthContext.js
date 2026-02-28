/**
 * 认证上下文
 * 提供全局认证状态管理
 */

import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

// 创建Context
const AuthContext = createContext();

// 自定义Hook
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth必须在AuthProvider内使用');
  }
  return context;
};

// Provider组件
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 初始化时检查登录状态
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        // 验证token有效性
        const response = await api.getCurrentUser();
        setUser(response.data);
        setIsAuthenticated(true);
      }
    } catch (err) {
      console.error('认证状态检查失败:', err);
      // token无效，清除本地存储
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      setError(null);
      const response = await api.login(username, password);
      
      const { access_token, user: userData } = response.data;
      
      // 保存token
      api.setAuthToken(access_token);
      
      // 更新状态
      setUser(userData);
      setIsAuthenticated(true);
      
      return { success: true, user: userData };
    } catch (err) {
      const errorMessage = err.response?.data?.detail || '登录失败，请检查用户名和密码';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await api.register(userData);
      
      // 注册成功后自动登录
      const loginResult = await login(userData.username, userData.password);
      
      return loginResult;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || '注册失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    // 清除本地存储
    localStorage.removeItem('token');
    
    // 清除API认证头
    api.clearAuth();
    
    // 更新状态
    setUser(null);
    setIsAuthenticated(false);
    setError(null);
  };

  const updateUserProfile = async (userData) => {
    try {
      const response = await api.updateUser(userData);
      setUser(response.data);
      return { success: true, user: response.data };
    } catch (err) {
      const errorMessage = err.response?.data?.detail || '更新用户信息失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    updateUserProfile,
    clearError,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;