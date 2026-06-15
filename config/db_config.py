import os
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
load_dotenv()

def get_conn_params() -> dict:
    """安全获取数据库连接参数，避免硬编码"""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "dbname": os.getenv("DB_NAME", "exat"),
        "user": os.getenv("DB_USER", "YAN"),
        "password": os.getenv("DB_PASSWORD", "YAN@2039361436")
    }
