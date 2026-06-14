import numpy as np
import pandas as pd


def generate_orders(n: int = 1000, distribution: str = "mixed") -> pd.DataFrame:
    """生成模拟电商订单数据"""
    cities = ["北京", "上海", "广州", "深圳", "杭州"]
    categories = ["数码", "服饰", "食品", "家居", "美妆"]

    if distribution == "normal":
        # 正态分布：均值300、标准差150，abs截断负数保证金额非负
        amount = np.abs(np.random.normal(300, 150, n)).round(2)
    elif distribution == "uniform":
        # 均匀分布：50~1000区间内每个值出现概率相等
        amount = np.random.uniform(50, 1000, n).round(2)
    elif distribution == "mixed":
        # 混合分布：按20%/50%/30%比例模拟低/中/高三个价位段
        amount = np.zeros(n)
        amount[:n // 5] = np.random.uniform(50, 200, n // 5)              # 低价位: 50~200
        amount[n // 5: n // 5 + n // 2] = np.random.uniform(200, 500, n // 2)  # 中价位: 200~500
        amount[n // 5 + n // 2:] = np.random.uniform(500, 1500, n - n // 5 - n // 2)  # 高价位: 500~1500
        # 打乱顺序
        np.random.shuffle(amount)
        amount = amount.round(2)
    elif distribution == "wide":
        # 宽范围均匀分布：10~2000，覆盖极端低价和高价订单
        amount = np.random.uniform(10, 2000, n).round(2)
    else:
        raise ValueError(f"未知的分布类型: {distribution}")

    # 组装各字段为DataFrame并返回
    return pd.DataFrame({
        # 从候选池中有放回地随机抽取城市和品类
        "city": np.random.choice(cities, n),
        "category": np.random.choice(categories, n),
        "amount": amount,
        # 以当前时间为终点，向前生成n个每小时递增的时间戳
        "order_date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="h"),
    })
