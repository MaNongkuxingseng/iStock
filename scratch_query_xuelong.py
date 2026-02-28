import pymysql
conn=pymysql.connect(host='127.0.0.1',user='root',password='785091',database='instockdb',charset='utf8mb4')
cur=conn.cursor()
cur.execute('SHOW TABLES')
for (t,) in cur.fetchall():
    try:
        cur.execute(f"SHOW COLUMNS FROM `{t}`")
        cols=[c[0] for c in cur.fetchall()]
        if 'name' in cols:
            cur.execute(f"SELECT * FROM `{t}` WHERE `name`=%s LIMIT 3",('雪龙集团',))
            rows=cur.fetchall()
            if rows:
                print('TABLE',t)
                print('COLS',cols)
                for r in rows:
                    print('ROW',r)
    except Exception:
        pass
conn.close()
