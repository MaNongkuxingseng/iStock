import sqlite3
import os

# 检查数据库文件是否存在
db_path = 'instockdb'
if os.path.exists(db_path):
    print(f'数据库文件存在: {db_path}')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f'数据库中的表:')
        for table in tables:
            print(f'  - {table[0]}')
            
        # 检查关键表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'cn_stock_%';")
        cn_tables = cursor.fetchall()
        print(f'\n中国股票相关表:')
        for table in cn_tables:
            print(f'  - {table[0]}')
            
            # 查看表结构
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            if len(columns) > 5:
                print(f'    列: {[col[1] for col in columns[:5]]}...')
            else:
                print(f'    列: {[col[1] for col in columns]}')
            
        conn.close()
    except Exception as e:
        print(f'连接数据库时出错: {e}')
else:
    print(f'数据库文件不存在: {db_path}')