USE instockdb;

-- 创建表（如果不存在）
CREATE TABLE IF NOT EXISTS `cn_stock_indicators_sell` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL COMMENT '股票代码',
  `name` varchar(50) DEFAULT NULL COMMENT '股票名称',
  `date` date NOT NULL COMMENT '日期',
  `macd_golden_fork` tinyint(1) DEFAULT NULL COMMENT 'MACD金叉',
  `kdj_golden_fork` tinyint(1) DEFAULT NULL COMMENT 'KDJ金叉',
  `rsi_overbought` tinyint(1) DEFAULT NULL COMMENT 'RSI超买',
  `volume_ratio` decimal(10,2) DEFAULT NULL COMMENT '量比',
  `price_change_percent` decimal(10,2) DEFAULT NULL COMMENT '涨跌幅',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code_date` (`code`,`date`),
  KEY `idx_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票卖出指标数据';

-- 插入测试数据
INSERT IGNORE INTO cn_stock_indicators_sell (code, name, date, macd_golden_fork, kdj_golden_fork)
VALUES 
  ('603949', '雪龙集团', '2026-02-27', 1, 1),
  ('002415', '海康威视', '2026-02-27', 1, 0),
  ('600519', '贵州茅台', '2026-02-27', 0, 0);

-- 验证创建成功
SELECT 'Table created successfully' as status, COUNT(*) as record_count FROM cn_stock_indicators_sell;