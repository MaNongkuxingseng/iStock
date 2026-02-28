"""
MySQL数据库会话配置
使用pymysql连接MySQL数据库
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# MySQL数据库连接URL
# 格式: mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/istock?charset=utf8mb4"

# 创建数据库引擎
# 配置连接池以提高性能
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,  # 使用连接池
    pool_size=10,         # 连接池大小
    max_overflow=20,      # 最大溢出连接数
    pool_pre_ping=True,   # 连接前ping检查
    pool_recycle=3600,    # 连接回收时间(秒)
    echo=False,           # 是否输出SQL日志(调试时设为True)
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 声明基类
Base = declarative_base()

# 依赖注入函数
def get_db():
    """
    获取数据库会话
    使用方式: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据库连接测试函数
def test_connection():
    """测试数据库连接是否正常"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ MySQL数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ MySQL数据库连接失败: {e}")
        return False

# 创建数据库表函数
def create_tables():
    """创建所有数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
        return False

if __name__ == "__main__":
    # 测试数据库连接
    if test_connection():
        print("数据库连接正常")
    else:
        print("请检查MySQL配置:")
        print("1. MySQL服务是否运行: net start MySQL80")
        print("2. 数据库是否存在: CREATE DATABASE istock;")
        print("3. 用户名密码是否正确")