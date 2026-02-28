#!/usr/bin/env python3
"""
数据库初始化脚本
创建iStock数据库和表结构
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.session_mysql import engine, Base, test_connection
from src.database.models import create_all_tables
import mysql.connector
from mysql.connector import Error


def create_database():
    """创建iStock数据库"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # 根据实际情况修改密码
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 创建数据库
            cursor.execute("CREATE DATABASE IF NOT EXISTS istock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ 数据库 'istock' 创建成功或已存在")
            
            # 切换到istock数据库
            cursor.execute("USE istock")
            
            # 检查表是否存在
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"✅ 数据库中有 {len(tables)} 个表:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("ℹ️  数据库为空，将创建表结构")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Error as e:
        print(f"❌ 数据库创建失败: {e}")
        print("\n请检查:")
        print("1. MySQL服务是否运行: net start MySQL80")
        print("2. MySQL root密码是否正确")
        print("3. 网络连接是否正常")
        return False


def create_tables_with_sql():
    """使用SQL直接创建表"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="istock"
        )
        
        cursor = connection.cursor()
        
        # 创建stocks表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            market VARCHAR(20),
            industry VARCHAR(50),
            full_name VARCHAR(200),
            listing_date DATETIME,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_symbol (symbol),
            INDEX idx_market (market),
            INDEX idx_industry (industry)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ 创建表: stocks")
        
        # 创建stock_daily表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_daily (
            id INT AUTO_INCREMENT PRIMARY KEY,
            stock_id INT NOT NULL,
            date DATETIME NOT NULL,
            open_price DECIMAL(10,2),
            close_price DECIMAL(10,2),
            high_price DECIMAL(10,2),
            low_price DECIMAL(10,2),
            pre_close DECIMAL(10,2),
            volume BIGINT,
            amount DECIMAL(15,2),
            change DECIMAL(10,2),
            change_percent DECIMAL(6,2),
            turnover_rate DECIMAL(6,2),
            amplitude DECIMAL(6,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_stock_date (stock_id, date),
            INDEX idx_date (date),
            FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ 创建表: stock_daily")
        
        # 创建technical_indicators表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS technical_indicators (
            id INT AUTO_INCREMENT PRIMARY KEY,
            stock_id INT NOT NULL,
            daily_id INT NOT NULL,
            date DATETIME NOT NULL,
            ma5 DECIMAL(10,2),
            ma10 DECIMAL(10,2),
            ma20 DECIMAL(10,2),
            ma30 DECIMAL(10,2),
            ma60 DECIMAL(10,2),
            macd DECIMAL(10,4),
            macd_signal DECIMAL(10,4),
            macd_histogram DECIMAL(10,4),
            k DECIMAL(6,2),
            d DECIMAL(6,2),
            j DECIMAL(6,2),
            rsi6 DECIMAL(6,2),
            rsi12 DECIMAL(6,2),
            rsi24 DECIMAL(6,2),
            boll_upper DECIMAL(10,2),
            boll_middle DECIMAL(10,2),
            boll_lower DECIMAL(10,2),
            volume_ma5 BIGINT,
            volume_ma10 BIGINT,
            buy_signal BOOLEAN DEFAULT FALSE,
            sell_signal BOOLEAN DEFAULT FALSE,
            signal_strength INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_stock_date (stock_id, date),
            INDEX idx_signals (buy_signal, sell_signal, date),
            FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE,
            FOREIGN KEY (daily_id) REFERENCES stock_daily(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ 创建表: technical_indicators")
        
        # 创建users表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            notification_enabled BOOLEAN DEFAULT TRUE,
            risk_level VARCHAR(20) DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            last_login DATETIME,
            INDEX idx_username (username),
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ 创建表: users")
        
        # 创建user_portfolios表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_portfolios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            stock_id INT NOT NULL,
            quantity INT DEFAULT 0,
            avg_cost DECIMAL(10,2),
            current_value DECIMAL(15,2),
            profit_loss DECIMAL(15,2),
            profit_loss_percent DECIMAL(8,2),
            first_buy_date DATETIME,
            last_buy_date DATETIME,
            last_sell_date DATETIME,
            is_watching BOOLEAN DEFAULT TRUE,
            target_price DECIMAL(10,2),
            stop_loss_price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_stock (user_id, stock_id),
            INDEX idx_watching (is_watching),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ 创建表: user_portfolios")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ 表创建失败: {e}")
        return False


def insert_sample_data():
    """插入示例数据"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="istock"
        )
        
        cursor = connection.cursor()
        
        # 检查是否有数据
        cursor.execute("SELECT COUNT(*) FROM stocks")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📊 插入示例股票数据...")
            
            # 插入示例股票
            sample_stocks = [
                ("000001", "平安银行", "深交所", "银行", "平安银行股份有限公司", "1991-04-03"),
                ("000002", "万科A", "深交所", "房地产", "万科企业股份有限公司", "1991-01-29"),
                ("000858", "五粮液", "深交所", "白酒", "宜宾五粮液股份有限公司", "1998-04-27"),
                ("600519", "贵州茅台", "上交所", "白酒", "贵州茅台酒股份有限公司", "2001-08-27"),
                ("601318", "中国平安", "上交所", "保险", "中国平安保险(集团)股份有限公司", "2007-03-01"),
            ]
            
            for stock in sample_stocks:
                cursor.execute("""
                INSERT INTO stocks (symbol, name, market, industry, full_name, listing_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), market=VALUES(market), industry=VALUES(industry)
                """, stock)
            
            connection.commit()
            print(f"✅ 插入 {len(sample_stocks)} 条股票数据")
            
            # 插入示例用户
            cursor.execute("""
            INSERT INTO users (username, email, hashed_password, full_name)
            VALUES ('demo', 'demo@istock.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '演示用户')
            ON DUPLICATE KEY UPDATE email=VALUES(email)
            """)
            
            connection.commit()
            print("✅ 插入示例用户数据")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ 示例数据插入失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("iStock 数据库初始化工具")
    print("=" * 60)
    
    # 步骤1: 创建数据库
    print("\n[1/4] 创建数据库...")
    if not create_database():
        print("❌ 数据库创建失败，请检查MySQL配置")
        return
    
    # 步骤2: 测试连接
    print("\n[2/4] 测试数据库连接...")
    if not test_connection():
        print("❌ 数据库连接失败")
        print("请确保:")
        print("1. MySQL服务正在运行")
        print("2. 数据库 'istock' 已创建")
        print("3. 连接配置正确")
        return
    
    # 步骤3: 创建表
    print("\n[3/4] 创建数据库表...")
    if not create_tables_with_sql():
        print("❌ 表创建失败")
        return
    
    # 步骤4: 插入示例数据
    print("\n[4/4] 插入示例数据...")
    insert_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ 数据库初始化完成!")
    print("=" * 60)
    print("\n数据库信息:")
    print("- 数据库名: istock")
    print("- 主机: localhost:3306")
    print("- 用户: root")
    print("- 表数量: 5个核心表")
    print("\n下一步:")
    print("1. 启动后端服务: python -m uvicorn src.main:app --reload")
    print("2. 访问API文档: http://localhost:8000/docs")
    print("3. 测试API端点: http://localhost:8000/api/stocks")


if __name__ == "__main__":
    main()