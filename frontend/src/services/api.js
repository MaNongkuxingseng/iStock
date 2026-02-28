/**
 * iStock API 服务
 * 提供与后端API通信的接口
 */

import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // 服务器返回错误状态码
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          console.error('权限不足');
          break;
        case 404:
          console.error('资源不存在');
          break;
        case 500:
          console.error('服务器内部错误');
          break;
        default:
          console.error('请求失败:', error.response.status);
      }
    } else if (error.request) {
      // 请求发送但没有收到响应
      console.error('网络错误，请检查网络连接');
    } else {
      // 请求配置错误
      console.error('请求配置错误:', error.message);
    }
    return Promise.reject(error);
  }
);

// ==================== 用户相关API ====================

/**
 * 用户注册
 * @param {Object} userData - 用户数据
 */
export const register = (userData) => {
  return api.post('/users/register', userData);
};

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 */
export const login = (username, password) => {
  return api.post('/users/login', { username, password });
};

/**
 * 获取当前用户信息
 */
export const getCurrentUser = () => {
  return api.get('/users/me');
};

/**
 * 更新用户信息
 * @param {Object} userData - 用户数据
 */
export const updateUser = (userData) => {
  return api.put('/users/me', userData);
};

// ==================== 股票相关API ====================

/**
 * 获取股票列表
 * @param {Object} params - 查询参数
 */
export const getStocks = (params = {}) => {
  return api.get('/stocks', { params });
};

/**
 * 获取单个股票信息
 * @param {number} stockId - 股票ID
 */
export const getStock = (stockId) => {
  return api.get(`/stocks/${stockId}`);
};

/**
 * 搜索股票
 * @param {string} query - 搜索关键词
 */
export const searchStocks = (query) => {
  return api.get(`/stocks/search/${query}`);
};

/**
 * 获取股票日线数据
 * @param {number} stockId - 股票ID
 * @param {Object} params - 查询参数
 */
export const getStockDaily = (stockId, params = {}) => {
  return api.get(`/stocks/${stockId}/daily`, { params });
};

/**
 * 获取股票技术指标
 * @param {number} stockId - 股票ID
 * @param {Object} params - 查询参数
 */
export const getStockIndicators = (stockId, params = {}) => {
  return api.get(`/stocks/${stockId}/indicators`, { params });
};

// ==================== 投资组合相关API ====================

/**
 * 获取投资组合项列表
 * @param {string} userId - 用户ID
 */
export const getPortfolioItems = (userId) => {
  return api.get(`/portfolio/${userId}/items`);
};

/**
 * 获取投资组合摘要
 * @param {string} userId - 用户ID
 */
export const getPortfolioSummary = (userId) => {
  return api.get(`/portfolio/${userId}/summary`);
};

/**
 * 获取投资组合详情
 * @param {string} userId - 用户ID
 */
export const getPortfolioDetails = (userId) => {
  return api.get(`/portfolio/${userId}/details`);
};

/**
 * 添加投资组合项
 * @param {string} userId - 用户ID
 * @param {Object} itemData - 投资组合项数据
 */
export const addPortfolioItem = (userId, itemData) => {
  return api.post(`/portfolio/${userId}/items`, itemData);
};

/**
 * 更新投资组合项
 * @param {string} userId - 用户ID
 * @param {number} stockId - 股票ID
 * @param {Object} updateData - 更新数据
 */
export const updatePortfolioItem = (userId, stockId, updateData) => {
  return api.put(`/portfolio/${userId}/items/${stockId}`, updateData);
};

/**
 * 删除投资组合项
 * @param {string} userId - 用户ID
 * @param {number} stockId - 股票ID
 */
export const deletePortfolioItem = (userId, stockId) => {
  return api.delete(`/portfolio/${userId}/items/${stockId}`);
};

// ==================== 数据相关API ====================

/**
 * 获取数据源列表
 */
export const getDataSources = () => {
  return api.get('/data/sources');
};

/**
 * 触发数据同步
 * @param {Object} syncData - 同步数据
 */
export const triggerSync = (syncData) => {
  return api.post('/data/sync', syncData);
};

/**
 * 获取同步日志
 * @param {Object} params - 查询参数
 */
export const getSyncLogs = (params = {}) => {
  return api.get('/data/sync/logs', { params });
};

/**
 * 获取数据统计
 */
export const getDataStats = () => {
  return api.get('/data/stats/overview');
};

// ==================== 系统相关API ====================

/**
 * 健康检查
 */
export const healthCheck = () => {
  return api.get('/health');
};

/**
 * 获取系统状态
 */
export const getSystemStatus = () => {
  return api.get('/system/status');
};

// ==================== 模拟数据API（开发用） ====================

/**
 * 获取市场概览（模拟）
 */
export const getMarketOverview = () => {
  // 在实际开发中，这里应该调用真实API
  // 这里返回模拟数据
  return Promise.resolve({
    data: {
      shanghai: { change: 1.2, status: 'up' },
      shenzhen: { change: 0.8, status: 'up' },
      nasdaq: { change: -0.5, status: 'down' },
      sp500: { change: 0.3, status: 'up' }
    }
  });
};

/**
 * 获取实时行情（模拟）
 * @param {string} symbol - 股票代码
 */
export const getRealtimeQuote = (symbol) => {
  // 模拟实时数据
  const basePrice = 100 + (symbol.charCodeAt(0) % 100);
  const change = (Math.random() - 0.5) * basePrice * 0.02;
  
  return Promise.resolve({
    data: {
      symbol,
      price: basePrice + change,
      change,
      change_percent: (change / basePrice) * 100,
      volume: Math.floor(Math.random() * 10000000),
      timestamp: new Date().toISOString()
    }
  });
};

// ==================== 工具函数 ====================

/**
 * 设置认证token
 * @param {string} token - JWT token
 */
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  }
};

/**
 * 清除认证信息
 */
export const clearAuth = () => {
  localStorage.removeItem('token');
  delete api.defaults.headers.common['Authorization'];
};

/**
 * 检查是否已认证
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// 导出所有API方法
export default {
  // 用户相关
  register,
  login,
  getCurrentUser,
  updateUser,
  
  // 股票相关
  getStocks,
  getStock,
  searchStocks,
  getStockDaily,
  getStockIndicators,
  
  // 投资组合相关
  getPortfolioItems,
  getPortfolioSummary,
  getPortfolioDetails,
  addPortfolioItem,
  updatePortfolioItem,
  deletePortfolioItem,
  
  // 数据相关
  getDataSources,
  triggerSync,
  getSyncLogs,
  getDataStats,
  
  // 系统相关
  healthCheck,
  getSystemStatus,
  
  // 模拟数据
  getMarketOverview,
  getRealtimeQuote,
  
  // 工具函数
  setAuthToken,
  clearAuth,
  isAuthenticated
};