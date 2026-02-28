import pymysql

try:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='instockdb')
    cur = conn.cursor()
    
    # 检查目标表
    cur.execute("SHOW TABLES LIKE 'cn_stock_indicators_sell'")
    result = cur.fetchone()
    
    if result:
        print('✅ 表 cn_stock_indicators_sell 存在')
    else:
        print('❌ 表 cn_stock_indicators_sell 不存在')
        
        # 检查所有包含indicators的表
        cur.execute("SHOW TABLES LIKE '%indicators%'")
        tables = cur.fetchall()
        print('📊 相关indicators表:')
        for table in tables:
            print(f'  - {table[0]}')
            
        # 检查所有表
        cur.execute("SHOW TABLES")
        all_tables = cur.fetchall()
        print(f'\n📈 数据库中共有 {len(all_tables)} 张表')
        
    conn.close()
    
except pymysql.err.OperationalError as e:
    print(f'❌ 数据库连接失败: {e}')
    print('请检查:')
    print('1. MySQL服务是否运行')
    print('2. 数据库instockdb是否存在')
    print('3. 用户名/密码是否正确')
except Exception as e:
    print(f'❌ 错误: {e}')