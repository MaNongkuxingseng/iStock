import mysql.connector

try:
    # 连接数据库
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='785091',
        database='instockdb'
    )
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("SHOW TABLES LIKE 'cn_stock_indicators_sell'")
    result = cursor.fetchone()
    
    if result:
        print(f'Table exists: {result[0]}')
        cursor.execute("SELECT COUNT(*) FROM cn_stock_indicators_sell")
        count = cursor.fetchone()[0]
        print(f'Records in table: {count}')
    else:
        print('Table does not exist, creating...')
        
        # 创建表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS cn_stock_indicators_sell (
            id BIGINT NOT NULL AUTO_INCREMENT,
            code VARCHAR(10) NOT NULL COMMENT '股票代码',
            name VARCHAR(50) DEFAULT NULL COMMENT '股票名称',
            date DATE NOT NULL COMMENT '日期',
            macd_golden_fork TINYINT(1) DEFAULT NULL COMMENT 'MACD金叉',
            kdj_golden_fork TINYINT(1) DEFAULT NULL COMMENT 'KDJ金叉',
            rsi_overbought TINYINT(1) DEFAULT NULL COMMENT 'RSI超买',
            volume_ratio DECIMAL(10,2) DEFAULT NULL COMMENT '量比',
            price_change_percent DECIMAL(10,2) DEFAULT NULL COMMENT '涨跌幅',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_code_date (code, date),
            KEY idx_date (date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票卖出指标数据'
        """
        
        cursor.execute(create_table_sql)
        print('Table created successfully')
        
        # 插入测试数据
        test_data = [
            ('603949', '雪龙集团', '2026-02-27', 1, 1),
            ('002415', '海康威视', '2026-02-27', 1, 0),
            ('600519', '贵州茅台', '2026-02-27', 0, 0)
        ]
        
        for data in test_data:
            cursor.execute(
                "INSERT IGNORE INTO cn_stock_indicators_sell (code, name, date, macd_golden_fork, kdj_golden_fork) VALUES (%s, %s, %s, %s, %s)",
                data
            )
        
        cursor.execute("SELECT COUNT(*) FROM cn_stock_indicators_sell")
        count = cursor.fetchone()[0]
        print(f'Records inserted: {count}')
    
    conn.commit()
    cursor.close()
    conn.close()
    print('SUCCESS: Database operation completed')
    
except mysql.connector.Error as e:
    print(f'MySQL Error: {e}')
except Exception as e:
    print(f'General Error: {e}')