import psycopg
from config.db_config import get_conn_params


def save_to_db(df, replace: bool = True) -> None:
    """将订单DataFrame批量写入PostgreSQL数据库

    Args:
        df: 包含 city, category, amount, order_date 列的订单数据
        replace: True=写入前清空表(全量替换), False=追加写入
    """
    # 从配置文件获取数据库连接
    conn_params = get_conn_params()

    try:
        # 建立数据库连接
        with psycopg.connect(**conn_params) as conn:
            # 创建游标对象，执行SQL语句
            with conn.cursor() as cur:
                # 建表
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,      -- 自增主键
                        city VARCHAR(20),           -- 城市
                        category VARCHAR(20),       -- 品类
                        amount DECIMAL(10,2),       -- 金额
                        order_date TIMESTAMP        -- 下单时间
                    )
                """)

                # 全量替换模式：清空旧数据并将自增ID重置为1
                if replace:
                    cur.execute("TRUNCATE TABLE orders RESTART IDENTITY;")

                # 将DataFrame转为元组列表，适配psycopg的copy接口
                records = [tuple(row) for row in df.to_numpy()]

                # 批量写入
                with cur.copy("COPY orders (city, category, amount, order_date) FROM STDIN") as copy:
                    for record in records:
                        copy.write_row(record)

                conn.commit()
                print(f"成功写入 {len(records)} 条订单数据")

    except Exception as e:
        print(f"数据库写入失败: {e}")
        raise
