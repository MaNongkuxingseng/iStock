CREATE TABLE IF NOT EXISTS cn_stock_indicators_sell (
    id BIGINT NOT NULL AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) DEFAULT NULL,
    date DATE NOT NULL,
    macd_golden_fork TINYINT(1) DEFAULT NULL,
    kdj_golden_fork TINYINT(1) DEFAULT NULL,
    rsi_overbought TINYINT(1) DEFAULT NULL,
    volume_ratio DECIMAL(10,2) DEFAULT NULL,
    price_change_percent DECIMAL(10,2) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_code_date (code, date),
    KEY idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO cn_stock_indicators_sell (code, name, date, macd_golden_fork, kdj_golden_fork)
VALUES 
    ('603949', '雪龙集团', '2026-02-27', 1, 1),
    ('002415', '海康威视', '2026-02-27', 1, 0),
    ('600519', '贵州茅台', '2026-02-27', 0, 0);

SELECT COUNT(*) as record_count FROM cn_stock_indicators_sell;