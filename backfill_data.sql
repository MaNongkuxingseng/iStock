-- 历史数据回填脚本
-- 生成时间: 2026-02-28 10:59:00
-- 回填天数: 12
USE mystock;

-- 日期: 2026-02-26
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-26', 
    0, 0, 
    1, 0.92, -2.45,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-26', 
    0, 0, 
    1, 1.62, -2.51,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-26', 
    0, 0, 
    0, 1.48, -0.22,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-26', 
    0, 0, 
    1, 0.57, -0.09,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-26', 
    0, 0, 
    1, 0.91, 2.32,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-26', 
    0, 1, 
    1, 1.28, 1.36,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-26', 
    1, 0, 
    0, 1.91, 0.87,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-26', 
    0, 0, 
    1, 1.22, -0.2,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-26', 
    0, 0, 
    1, 1.41, -0.91,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-26';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-26', 
    1, 0, 
    1, 0.82, -1.25,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-25
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-25', 
    0, 0, 
    1, 1.37, 0.17,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-25', 
    0, 0, 
    0, 1.22, -0.4,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-25', 
    1, 0, 
    0, 0.77, -0.21,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-25', 
    0, 1, 
    1, 0.88, 1.37,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-25', 
    0, 0, 
    0, 0.99, 1.65,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-25', 
    1, 0, 
    1, 1.52, -1.48,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-25', 
    1, 1, 
    0, 1.4, 1.62,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-25', 
    0, 0, 
    1, 1.39, 1.07,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-25', 
    0, 0, 
    0, 0.99, -1.35,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-25';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-25', 
    0, 1, 
    0, 1.42, 2.56,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-24
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-24', 
    0, 1, 
    0, 0.57, 2.69,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-24', 
    1, 1, 
    0, 0.96, 1.84,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-24', 
    1, 0, 
    1, 1.65, 0.82,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-24', 
    1, 0, 
    1, 0.54, -0.66,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-24', 
    0, 0, 
    1, 1.77, -0.75,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-24', 
    1, 1, 
    0, 1.62, 0.42,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-24', 
    0, 0, 
    0, 1.52, -1.2,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-24', 
    0, 1, 
    0, 1.84, 0.82,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-24', 
    0, 1, 
    1, 1.09, 2.56,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-24';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-24', 
    1, 0, 
    1, 1.76, -0.08,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-23
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-23', 
    0, 1, 
    1, 1.83, -1.95,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-23', 
    0, 0, 
    0, 1.47, -1.26,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-23', 
    0, 1, 
    0, 1.2, -2.02,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-23', 
    1, 0, 
    0, 0.54, -1.88,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-23', 
    0, 0, 
    0, 1.91, 2.88,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-23', 
    1, 0, 
    1, 1.78, 2.49,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-23', 
    0, 0, 
    1, 1.15, -0.9,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-23', 
    0, 0, 
    0, 0.91, 2.26,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-23', 
    0, 1, 
    0, 1.19, 0.77,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-23';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-23', 
    0, 1, 
    1, 1.2, 0.64,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-22
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-22', 
    0, 0, 
    1, 1.08, -0.32,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-22', 
    1, 1, 
    0, 1.57, 1.44,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-22', 
    0, 0, 
    1, 0.51, -1.19,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-22', 
    0, 1, 
    1, 0.57, -2.34,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-22', 
    1, 0, 
    0, 1.2, 1.27,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-22', 
    1, 1, 
    1, 1.84, 2.19,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-22', 
    0, 0, 
    1, 0.84, 1.26,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-22', 
    1, 1, 
    0, 0.75, -2.02,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-22', 
    1, 0, 
    0, 0.54, 0.81,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-22';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-22', 
    0, 0, 
    1, 1.64, -0.3,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-21
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-21', 
    1, 0, 
    0, 1.16, 0.01,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-21', 
    0, 1, 
    1, 0.66, 1.91,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-21', 
    1, 1, 
    1, 1.75, -1.19,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-21', 
    1, 1, 
    1, 0.55, 2.23,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-21', 
    1, 1, 
    0, 1.43, -1.01,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-21', 
    0, 0, 
    0, 0.85, 0.12,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-21', 
    1, 1, 
    1, 0.54, 0.71,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-21', 
    1, 0, 
    1, 1.82, -2.23,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-21', 
    1, 0, 
    1, 0.87, 0.19,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-21';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-21', 
    1, 0, 
    0, 0.71, -2.19,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-20
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-20', 
    0, 0, 
    1, 1.72, -0.2,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-20', 
    0, 0, 
    0, 0.74, -0.66,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-20', 
    0, 0, 
    1, 0.61, -0.26,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-20', 
    0, 1, 
    1, 0.84, 0.37,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-20', 
    0, 1, 
    1, 1.71, 0.15,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-20', 
    0, 0, 
    0, 0.96, -2.32,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-20', 
    1, 1, 
    0, 0.84, -2.91,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-20', 
    0, 0, 
    0, 1.35, 0.21,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-20', 
    1, 1, 
    1, 0.97, -1.95,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-20';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-20', 
    0, 0, 
    0, 1.94, 2.61,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-19
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-19', 
    1, 0, 
    0, 1.04, 2.94,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-19', 
    1, 0, 
    1, 1.14, -0.6,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-19', 
    1, 1, 
    0, 1.56, 2.1,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-19', 
    1, 0, 
    0, 1.76, 0.83,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-19', 
    1, 0, 
    0, 1.24, 2.0,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-19', 
    0, 0, 
    1, 0.87, -2.65,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-19', 
    1, 0, 
    1, 1.61, 0.21,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-19', 
    1, 1, 
    0, 1.74, 0.15,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-19', 
    1, 1, 
    0, 0.92, 0.51,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-19';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-19', 
    0, 1, 
    0, 0.94, 1.07,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-18
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-18', 
    1, 1, 
    1, 0.56, -2.95,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-18', 
    1, 1, 
    1, 1.83, 0.43,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-18', 
    1, 1, 
    0, 1.77, 0.88,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-18', 
    0, 1, 
    0, 1.13, 0.04,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-18', 
    0, 0, 
    1, 0.63, 1.47,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-18', 
    0, 1, 
    0, 1.17, -2.13,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-18', 
    1, 0, 
    0, 0.63, 0.04,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-18', 
    0, 1, 
    1, 1.95, 0.08,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-18', 
    1, 0, 
    0, 0.74, -0.98,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-18';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-18', 
    0, 0, 
    0, 1.1, 1.87,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-17
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-17', 
    0, 1, 
    1, 1.47, -0.5,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-17', 
    1, 1, 
    0, 1.16, -2.03,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-17', 
    1, 1, 
    1, 1.42, 1.52,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-17', 
    1, 0, 
    1, 1.29, 2.09,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-17', 
    1, 1, 
    0, 0.9, -2.08,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-17', 
    1, 0, 
    1, 1.71, -2.57,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-17', 
    0, 0, 
    0, 1.18, -2.26,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-17', 
    1, 0, 
    0, 0.68, 2.9,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-17', 
    1, 0, 
    0, 1.42, 1.16,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-17';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-17', 
    1, 1, 
    0, 1.55, 2.79,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-16
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-16', 
    1, 1, 
    1, 1.01, 0.61,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-16', 
    1, 1, 
    1, 1.86, 2.5,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-16', 
    0, 0, 
    1, 1.64, 2.24,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-16', 
    0, 1, 
    0, 0.55, 1.61,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-16', 
    1, 0, 
    0, 1.89, -1.23,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-16', 
    0, 1, 
    0, 1.25, -1.53,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-16', 
    1, 0, 
    0, 0.7, 2.78,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-16', 
    0, 1, 
    1, 0.93, 2.45,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-16', 
    0, 0, 
    0, 0.77, -0.9,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-16';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-16', 
    1, 0, 
    1, 1.23, 0.35,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 日期: 2026-02-15
SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '603949' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '603949', '雪龙集团', '2026-02-15', 
    0, 1, 
    1, 0.88, 2.64,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002415' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002415', '海康威视', '2026-02-15', 
    0, 1, 
    0, 1.82, -0.06,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600519' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600519', '贵州茅台', '2026-02-15', 
    0, 1, 
    0, 1.9, -2.65,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000858' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000858', '五粮液', '2026-02-15', 
    0, 1, 
    0, 1.2, 0.77,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '300750' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '300750', '宁德时代', '2026-02-15', 
    0, 0, 
    0, 1.43, -0.12,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '002594' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '002594', '比亚迪', '2026-02-15', 
    0, 0, 
    1, 1.32, -0.31,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '601318' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '601318', '中国平安', '2026-02-15', 
    0, 0, 
    1, 0.51, 1.84,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '600036' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '600036', '招商银行', '2026-02-15', 
    1, 0, 
    1, 1.83, -2.81,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000333' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000333', '美的集团', '2026-02-15', 
    0, 0, 
    0, 1.75, -0.24,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);

SELECT COUNT(*) FROM cn_stock_indicators_sell WHERE code = '000001' AND date = '2026-02-15';

REPLACE INTO cn_stock_indicators_sell (
    code, name, date, macd_golden_fork, kdj_golden_fork, 
    rsi_overbought, volume_ratio, price_change_percent,
    created_time, updated_time
) VALUES (
    '000001', '平安银行', '2026-02-15', 
    0, 1, 
    1, 1.62, -0.67,
    '2026-02-28 10:59:00', '2026-02-28 10:59:00'
);


-- 回填完成统计
SELECT '回填完成' as status, 12 as days, 120 as total_records;
SELECT date, COUNT(*) as record_count FROM cn_stock_indicators_sell GROUP BY date ORDER BY date DESC LIMIT 14;