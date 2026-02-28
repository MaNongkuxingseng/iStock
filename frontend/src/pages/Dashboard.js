/**
 * 仪表板页面
 */

import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import StockChart from '../components/StockChart';
import PortfolioSummary from '../components/PortfolioSummary';
import MarketOverview from '../components/MarketOverview';
import api from '../services/api';

function Dashboard() {
  const [portfolioData, setPortfolioData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // 获取投资组合数据
      const portfolioResponse = await api.getPortfolioSummary();
      setPortfolioData(portfolioResponse.data);
      
      // 获取市场概览数据
      const marketResponse = await api.getMarketOverview();
      setMarketData(marketResponse.data);
      
    } catch (err) {
      setError('加载数据失败，请检查网络连接');
      console.error('Dashboard data fetch error:', err);
      
      // 使用模拟数据
      setPortfolioData({
        total_value: 125000.50,
        total_cost: 100000.00,
        total_profit_loss: 25000.50,
        total_profit_loss_percent: 25.0,
        item_count: 8,
        last_updated: new Date().toISOString()
      });
      
      setMarketData({
        shanghai: { change: 1.2, status: 'up' },
        shenzhen: { change: 0.8, status: 'up' },
        nasdaq: { change: -0.5, status: 'down' },
        sp500: { change: 0.3, status: 'up' }
      });
      
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>加载仪表板数据...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <div className="error-icon">⚠️</div>
        <h3>数据加载失败</h3>
        <p>{error}</p>
        <button onClick={fetchDashboardData} className="retry-btn">
          重试
        </button>
        <p className="demo-notice">正在显示演示数据</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>📊 投资仪表板</h2>
        <div className="dashboard-actions">
          <button className="refresh-btn" onClick={fetchDashboardData}>
            🔄 刷新数据
          </button>
          <span className="last-updated">
            最后更新: {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* 投资组合概览 */}
        <div className="dashboard-card portfolio-card">
          <h3>💰 投资组合概览</h3>
          {portfolioData && <PortfolioSummary data={portfolioData} />}
        </div>

        {/* 股票图表 */}
        <div className="dashboard-card chart-card">
          <h3>📈 股票走势</h3>
          <StockChart />
        </div>

        {/* 市场概览 */}
        <div className="dashboard-card market-card">
          <h3>🌍 市场概览</h3>
          {marketData && <MarketOverview data={marketData} />}
        </div>

        {/* 快速操作 */}
        <div className="dashboard-card quick-actions-card">
          <h3>⚡ 快速操作</h3>
          <div className="quick-actions">
            <button className="action-btn buy-btn">
              💹 买入股票
            </button>
            <button className="action-btn sell-btn">
              📉 卖出股票
            </button>
            <button className="action-btn analyze-btn">
              🔍 分析股票
            </button>
            <button className="action-btn report-btn">
              📄 生成报告
            </button>
          </div>
        </div>

        {/* 最近交易 */}
        <div className="dashboard-card recent-trades-card">
          <h3>🔄 最近交易</h3>
          <div className="recent-trades">
            <div className="trade-item">
              <span className="trade-symbol">AAPL</span>
              <span className="trade-action buy">买入</span>
              <span className="trade-quantity">10 股</span>
              <span className="trade-price">$175.50</span>
              <span className="trade-time">10:30 AM</span>
            </div>
            <div className="trade-item">
              <span className="trade-symbol">TSLA</span>
              <span className="trade-action sell">卖出</span>
              <span className="trade-quantity">5 股</span>
              <span className="trade-price">$210.25</span>
              <span className="trade-time">09:15 AM</span>
            </div>
            <div className="trade-item">
              <span className="trade-symbol">MSFT</span>
              <span className="trade-action buy">买入</span>
              <span className="trade-quantity">15 股</span>
              <span className="trade-price">$415.80</span>
              <span className="trade-time">昨天</span>
            </div>
          </div>
        </div>

        {/* 系统状态 */}
        <div className="dashboard-card system-status-card">
          <h3>🛠️ 系统状态</h3>
          <div className="status-items">
            <div className="status-item">
              <span className="status-label">API 服务</span>
              <span className="status-value active">正常</span>
            </div>
            <div className="status-item">
              <span className="status-label">数据库</span>
              <span className="status-value active">正常</span>
            </div>
            <div className="status-item">
              <span className="status-label">数据同步</span>
              <span className="status-value warning">同步中</span>
            </div>
            <div className="status-item">
              <span className="status-label">系统负载</span>
              <span className="status-value normal">42%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;