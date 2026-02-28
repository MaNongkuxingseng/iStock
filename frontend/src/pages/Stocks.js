/**
 * 股票页面
 */

import React, { useState, useEffect } from 'react';
import './Stocks.css';
import StockTable from '../components/StockTable';
import StockFilter from '../components/StockFilter';
import StockChart from '../components/StockChart';
import api from '../services/api';

function Stocks() {
  const [stocks, setStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    market: '',
    industry: '',
    search: ''
  });

  useEffect(() => {
    fetchStocks();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [stocks, filters]);

  const fetchStocks = async () => {
    try {
      setLoading(true);
      const response = await api.getStocks();
      setStocks(response.data);
      setFilteredStocks(response.data);
    } catch (err) {
      setError('加载股票数据失败');
      console.error('Stocks fetch error:', err);
      
      // 使用模拟数据
      const mockStocks = generateMockStocks();
      setStocks(mockStocks);
      setFilteredStocks(mockStocks);
    } finally {
      setLoading(false);
    }
  };

  const generateMockStocks = () => {
    const symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'BABA', 'JD'];
    const names = ['苹果', '谷歌', '微软', '亚马逊', '特斯拉', '英伟达', 'Meta', '奈飞', '阿里巴巴', '京东'];
    const markets = ['NASDAQ', 'NYSE', 'SH', 'SZ'];
    const industries = ['科技', '电商', '汽车', '娱乐', '金融', '医疗'];
    
    return symbols.map((symbol, index) => ({
      id: index + 1,
      symbol,
      name: names[index % names.length],
      market: markets[index % markets.length],
      industry: industries[index % industries.length],
      sector: '信息技术',
      price: 100 + Math.random() * 900,
      change: (Math.random() - 0.5) * 20,
      change_percent: (Math.random() - 0.5) * 10,
      volume: Math.floor(Math.random() * 10000000),
      market_cap: Math.floor(Math.random() * 1000000000000)
    }));
  };

  const applyFilters = () => {
    let filtered = [...stocks];

    if (filters.market) {
      filtered = filtered.filter(stock => stock.market === filters.market);
    }

    if (filters.industry) {
      filtered = filtered.filter(stock => stock.industry === filters.industry);
    }

    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(stock =>
        stock.symbol.toLowerCase().includes(searchLower) ||
        stock.name.toLowerCase().includes(searchLower)
      );
    }

    setFilteredStocks(filtered);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
  };

  const handleRefresh = () => {
    fetchStocks();
  };

  if (loading) {
    return (
      <div className="stocks-loading">
        <div className="spinner"></div>
        <p>加载股票数据...</p>
      </div>
    );
  }

  return (
    <div className="stocks-page">
      <div className="stocks-header">
        <h2>📈 股票市场</h2>
        <div className="stocks-actions">
          <button className="refresh-btn" onClick={handleRefresh}>
            🔄 刷新数据
          </button>
          <span className="data-count">
            共 {filteredStocks.length} 只股票
          </span>
        </div>
      </div>

      {error && (
        <div className="stocks-error">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
          <button onClick={fetchStocks} className="retry-btn">
            重试
          </button>
          <p className="demo-notice">正在显示演示数据</p>
        </div>
      )}

      <div className="stocks-content">
        {/* 左侧：筛选和列表 */}
        <div className="stocks-left">
          <div className="filter-section">
            <StockFilter 
              filters={filters}
              onFilterChange={handleFilterChange}
              stocks={stocks}
            />
          </div>

          <div className="stocks-list-section">
            <h3>股票列表</h3>
            <StockTable 
              stocks={filteredStocks}
              onStockSelect={handleStockSelect}
              selectedStock={selectedStock}
            />
          </div>
        </div>

        {/* 右侧：详情和图表 */}
        <div className="stocks-right">
          {selectedStock ? (
            <>
              <div className="stock-detail-section">
                <h3>股票详情</h3>
                <div className="stock-detail-card">
                  <div className="stock-header">
                    <div className="stock-symbol-name">
                      <span className="stock-symbol">{selectedStock.symbol}</span>
                      <span className="stock-name">{selectedStock.name}</span>
                    </div>
                    <div className="stock-price">
                      <span className="price">${selectedStock.price.toFixed(2)}</span>
                      <span className={`change ${selectedStock.change >= 0 ? 'positive' : 'negative'}`}>
                        {selectedStock.change >= 0 ? '↗' : '↘'} 
                        {selectedStock.change.toFixed(2)} ({selectedStock.change_percent.toFixed(2)}%)
                      </span>
                    </div>
                  </div>

                  <div className="stock-info-grid">
                    <div className="info-item">
                      <span className="info-label">市场</span>
                      <span className="info-value">{selectedStock.market}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">行业</span>
                      <span className="info-value">{selectedStock.industry}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">板块</span>
                      <span className="info-value">{selectedStock.sector}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">成交量</span>
                      <span className="info-value">
                        {selectedStock.volume.toLocaleString()}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">市值</span>
                      <span className="info-value">
                        ${(selectedStock.market_cap / 1000000000).toFixed(2)}B
                      </span>
                    </div>
                  </div>

                  <div className="stock-actions">
                    <button className="action-btn buy-btn">
                      💹 买入
                    </button>
                    <button className="action-btn sell-btn">
                      📉 卖出
                    </button>
                    <button className="action-btn analyze-btn">
                      🔍 分析
                    </button>
                    <button className="action-btn watch-btn">
                      👁️ 加入关注
                    </button>
                  </div>
                </div>
              </div>

              <div className="stock-chart-section">
                <h3>价格走势</h3>
                <div className="chart-container">
                  <StockChart stock={selectedStock} />
                </div>
              </div>
            </>
          ) : (
            <div className="no-selection">
              <div className="no-selection-icon">👈</div>
              <h3>选择一只股票查看详情</h3>
              <p>从左侧列表中选择一只股票，查看详细信息和价格走势图</p>
            </div>
          )}
        </div>
      </div>

      {/* 市场概览 */}
      <div className="market-overview-section">
        <h3>市场概览</h3>
        <div className="market-cards">
          <div className="market-card shanghai">
            <div className="market-header">
              <span className="market-name">上证指数</span>
              <span className="market-change positive">+1.2%</span>
            </div>
            <div className="market-price">3,250.45</div>
            <div className="market-volume">成交量: 3.2B</div>
          </div>
          <div className="market-card shenzhen">
            <div className="market-header">
              <span className="market-name">深证成指</span>
              <span className="market-change positive">+0.8%</span>
            </div>
            <div className="market-price">11,450.32</div>
            <div className="market-volume">成交量: 2.8B</div>
          </div>
          <div className="market-card nasdaq">
            <div className="market-header">
              <span className="market-name">纳斯达克</span>
              <span className="market-change negative">-0.5%</span>
            </div>
            <div className="market-price">14,250.67</div>
            <div className="market-volume">成交量: 4.5B</div>
          </div>
          <div className="market-card sp500">
            <div className="market-header">
              <span className="market-name">标普500</span>
              <span className="market-change positive">+0.3%</span>
            </div>
            <div className="market-price">4,550.89</div>
            <div className="market-volume">成交量: 3.8B</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Stocks;