from src.data_generator import generate_orders
from src.db_connector import save_to_db
from src.visualizer import visualize

if __name__ == "__main__":
    # 生成随机数据（可选分布类型）
    # distribution 选项: 'normal'(正态), 'uniform'(均匀), 'mixed'(混合), 'wide'(宽范围) 
    orders_df = generate_orders(n=1000, distribution="uniform")

    # 存入数据库
    save_to_db(orders_df)

    # 可视化
    visualize(orders_df)
