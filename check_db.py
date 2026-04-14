from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

# 数据库配置
DATABASE_USER = 'root'
DATABASE_PASSWORD = '123456789'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_NAME = 'common_db'

# 创建数据库引擎
db_url = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(db_url)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# 定义用户模型（简化版）
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    is_admin = Column(Boolean, default=False)

# 查询用户数据
try:
    users = session.query(User).all()
    print("用户表数据:")
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 管理员: {user.is_admin}")
    
    print(f"\n用户总数: {len(users)}")
except Exception as e:
    print(f"查询失败: {e}")
finally:
    session.close()

# 检查数据库连接
try:
    with engine.connect() as connection:
        result = connection.execute("SHOW TABLES")
        tables = list(result)
        print("\n数据库中的表:")
        for table in tables:
            print(f"- {table[0]}")
except Exception as e:
    print(f"连接失败: {e}")
