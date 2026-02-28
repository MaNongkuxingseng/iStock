try:
    import pymysql
    print('pymysql已安装')
except ImportError:
    print('pymysql未安装')