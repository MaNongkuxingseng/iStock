import pymysql
conn=pymysql.connect(host='127.0.0.1',user='root',password='785091',database='instockdb',charset='utf8mb4')
cur=conn.cursor()
cur.execute("SELECT date, COUNT(*) FROM cn_stock_selection WHERE date BETWEEN %s AND %s GROUP BY date ORDER BY date",('2026-02-12','2026-02-26'))
print('selection_by_date',cur.fetchall())
for t in ['cn_stock_indicators','cn_stock_indicators_buy','cn_stock_indicators_sell','cn_stock_pattern']:
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",('instockdb',t))
    print(t, 'exists=', cur.fetchone()[0]==1)
conn.close()
