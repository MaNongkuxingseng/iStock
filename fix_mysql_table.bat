@echo off
echo Checking MySQL connection...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 -e "SHOW DATABASES;" > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Cannot connect to MySQL
    exit /b 1
)

echo Checking if table exists...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SHOW TABLES LIKE 'cn_stock_indicators_sell'" > table_check.txt 2>&1
findstr /i "cn_stock_indicators_sell" table_check.txt > nul
if %errorlevel% equ 0 (
    echo Table already exists
    goto :end
)

echo Table does not exist, creating...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "CREATE TABLE IF NOT EXISTS cn_stock_indicators_sell (id BIGINT NOT NULL AUTO_INCREMENT, code VARCHAR(10) NOT NULL, name VARCHAR(50) DEFAULT NULL, date DATE NOT NULL, macd_golden_fork TINYINT(1) DEFAULT NULL, kdj_golden_fork TINYINT(1) DEFAULT NULL, rsi_overbought TINYINT(1) DEFAULT NULL, volume_ratio DECIMAL(10,2) DEFAULT NULL, price_change_percent DECIMAL(10,2) DEFAULT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id), UNIQUE KEY uk_code_date (code, date), KEY idx_date (date)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4" > create_table.txt 2>&1

echo Inserting test data...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "INSERT IGNORE INTO cn_stock_indicators_sell (code, name, date, macd_golden_fork, kdj_golden_fork) VALUES ('603949', '雪龙集团', '2026-02-27', 1, 1), ('002415', '海康威视', '2026-02-27', 1, 0), ('600519', '贵州茅台', '2026-02-27', 0, 0)" > insert_data.txt 2>&1

echo Verifying creation...
"C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -uroot -p785091 instockdb -e "SELECT COUNT(*) as record_count FROM cn_stock_indicators_sell" > verify.txt 2>&1
type verify.txt

:end
echo Operation completed
del table_check.txt create_table.txt insert_data.txt verify.txt 2>nul