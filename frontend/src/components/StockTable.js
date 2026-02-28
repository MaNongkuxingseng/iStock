/**
 * 股票表格组件
 */

import React from 'react';
import './StockTable.css';

function StockTable({ stocks, onStockSelect, selectedStock }) {
  const formatNumber = (num) => {
    if (num >= 1000000000) {
      return `$${(num / 1000000000).toFixed(2)}B`;
    } else if (num >= 1000000) {
      return `$${(num / 1000000).toFixed(2)}M`;
    } else if (num >= 1000) {
      return `$${(num / 1000).toFixed(2)}K`;
    }
    return `$${num.toFixed(2)}`;
  };

  const formatVolume = (volume) => {
    return volume.toLocaleString();
  };

  const handleRowClick = (stock) => {
    onStockSelect(stock);
  };

  if (!stocks || stocks.length === 0) {
    return (
      <div className="empty-table">
        <div className="empty-icon">📊</div>
        <p>暂无股票数据</p>
      </div>
    );
  }

  return (
    <div className="stock-table-container">
      <table className="stock-table">
        <thead>
          <tr>
            <th>代码</th>
            <th>名称</th>
            <th>市场</th>
            <th>价格</th>
            <th>涨跌</th>
            <th>涨跌幅</th>
            <th>成交量</th>
            <th>市值</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr
              key={stock.id}
              className={`stock-row ${selectedStock?.id === stock.id ? 'selected' : ''}`}
              onClick={() => handleRowClick(stock)}
            >
              <td className="stock-symbol">
                <span className="symbol">{stock.symbol}</span>
              </td>
              <td className="stock-name">{stock.name}</td>
              <td className="stock-market">
                <span className={`market-badge ${stock.market.toLowerCase()}`}>
                  {stock.market}
                </span>
              </td>
              <td className="stock-price">
                ${stock.price?.toFixed(2) || '0.00'}
              </td>
              <td className={`stock-change ${stock.change >= 0 ? 'positive' : 'negative'}`}>
                {stock.change >= 0 ? '↗' : '↘'} 
                {Math.abs(stock.change?.toFixed(2) || 0)}
              </td>
              <td className={`stock-change-percent ${stock.change_percent >= 0 ? 'positive' : 'negative'}`}>
                {stock.change_percent?.toFixed(2) || '0.00'}%
              </td>
              <td className="stock-volume">
                {formatVolume(stock.volume || 0)}
              </td>
              <td className="stock-market-cap">
                {formatNumber(stock.market_cap || 0)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <div className="table-footer">
        <span className="row-count">
          共 {stocks.length} 条记录
        </span>
        <div className="table-legend">
          <span className="legend-item">
            <span className="legend-color positive"></span>
            上涨
          </span>
          <span className="legend-item">
            <span className="legend-color negative"></span>
            下跌
          </span>
        </div>
      </div>
    </div>
  );
}

export default StockTable;