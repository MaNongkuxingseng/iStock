import pymysql
fields=['date','code','name','new_price','change_rate','volume_ratio','turnoverrate','pe9','pbnewmrq','roe_weight','debt_asset_ratio','netprofit_yoy_ratio','deduct_netprofit_growthrate','toi_yoy_ratio','sale_npr','macd_golden_fork','kdj_golden_fork','breakup_ma_20days','breakup_ma_60days','long_avg_array','short_avg_array','upnday','downnday','net_inflow','netinflow_3days','netinflow_5days','ddx','ddx_3d','ddx_5d','changerate_3days','changerate_5days','changerate_10days','high_recent_20days','low_recent_20days','win_market_20days']
conn=pymysql.connect(host='127.0.0.1',user='root',password='785091',database='instockdb',charset='utf8mb4')
cur=conn.cursor()
sel=','.join([f'`{f}`' for f in fields])
cur.execute(f"SELECT {sel} FROM `cn_stock_selection` WHERE code=%s ORDER BY date DESC LIMIT 1",('603949',))
row=cur.fetchone()
print(dict(zip(fields,row)) if row else None)
conn.close()
