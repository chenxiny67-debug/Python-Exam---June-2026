import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 提取为模块常量，避免每次调用重建列表，也便于外部复用
DEFAULT_CHARTS = ('daily', 'city', 'category', 'city_bar')


def visualize(df, charts=None) -> None:
    """销售数据仪表板

    Args:
        df: 销售数据DataFrame，需包含 order_date/city/category/amount 列
        charts: 要展示的图表元组/列表，传None则展示全部默认图表
    """
    # 用独立变量承接，不污染原始入参；转为set提升后续 in 判断效率
    active_charts = set(DEFAULT_CHARTS if charts is None else charts)

    # 按需聚合：只计算当前激活图表所需的数据，避免无效计算和潜在报错
    daily_sales = None
    city_sales = None
    category_sales = None
    city_stats = None

    if 'daily' in active_charts:
        daily_sales = df.groupby(df["order_date"].dt.date)["amount"].sum().reset_index()

    if 'city' in active_charts:
        city_sales = (df.groupby("city")["amount"]
                      .sum().sort_values(ascending=False).reset_index())

    if 'category' in active_charts:
        category_sales = (df.groupby("category")["amount"]
                          .sum().sort_values(ascending=False).reset_index())

    if 'city_bar' in active_charts:
        city_stats = df.groupby("city").agg({"amount": ["sum", "mean", "count"]}).round(2)
        city_stats.columns = ["总销售", "平均订单", "订单数"]
        city_stats = city_stats.reset_index()

    # 创建2x2子图布局，右上角指定为饼图类型
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("每日销售趋势", "城市销售占比", "品类销售排名", "城市总销售额对比"),
        specs=[[{"secondary_y": False}, {"type": "pie"}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12, horizontal_spacing=0.12
    )

    # 左上：每日销售趋势折线图(带面积填充)
    if 'daily' in active_charts:
        fig.add_trace(go.Scatter(
            x=daily_sales["order_date"], y=daily_sales["amount"],
            mode="lines+markers", name="日销售额",
            line=dict(color="#4a90e2", width=3),
            marker=dict(size=6, color="#4a90e2", line=dict(width=2, color="#ffffff")),
            fill="tozeroy", fillcolor="rgba(74, 144, 226, 0.15)",
            hovertemplate="<b>%{x}</b><br>销售额: ¥%{y:,.0f}<extra></extra>"
        ), row=1, col=1)

    # 右上：各城市销售占比饼图
    if 'city' in active_charts:
        fig.add_trace(go.Pie(
            labels=city_sales["city"], values=city_sales["amount"], name="城市销售",
            marker=dict(colors=["#4a90e2", "#50c878", "#f5a623", "#b8e986", "#d0021b"],
                        line=dict(color="#ffffff", width=2)),
            textposition="inside", textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>销售额: ¥%{value:,.0f}<extra></extra>"
        ), row=1, col=2)

    # 左下：品类销售排名柱状图
    if 'category' in active_charts:
        fig.add_trace(go.Bar(
            x=category_sales["category"], y=category_sales["amount"], name="品类销售",
            marker=dict(color=["#4a90e2", "#357edd", "#2d68cc", "#1f4f99", "#0c3466"],
                        line=dict(color="rgba(0,0,0,0)", width=0)),
            text=category_sales["amount"].round(0), textposition="outside",
            hovertemplate="<b>%{x}</b><br>销售额: ¥%{y:,.0f}<extra></extra>"
        ), row=2, col=1)

    # 右下：城市总销售额对比柱状图
    if 'city_bar' in active_charts:
        fig.add_trace(go.Bar(
            x=city_stats["city"], y=city_stats["总销售"], name="总销售额",
            marker=dict(color="#50c878", line=dict(width=0)),
            text=city_stats["总销售"].round(0), textposition="outside",
            hovertemplate="<b>%{x}</b><br>总销售: ¥%{y:,.0f}<extra></extra>"
        ), row=2, col=2)

    # 统一设置全局布局样式
    fig.update_layout(
        title=dict(text="<b>品类销售趋势变化分析</b>", font=dict(size=26, color="#1a1a1a"),
                   x=0.5, xanchor="center"),
        height=900, width=1600, template="plotly_white", showlegend=True,
        hovermode="closest",
        font=dict(family="Arial, sans-serif", size=12, color="#444444"),
        plot_bgcolor="rgba(250, 250, 250, 0.5)", paper_bgcolor="white",
        margin=dict(l=60, r=60, t=120, b=60)
    )

    # 统一设置网格线样式
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200, 200, 200, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200, 200, 200, 0.2)")

    # 仅对非饼图子图设置坐标轴标签（饼图无直角坐标系，设置无效且可能警告）
    fig.update_xaxes(title_text="日期", row=1, col=1, title_font=dict(size=11, color="#666"))
    fig.update_yaxes(title_text="销售额 (¥)", row=1, col=1, title_font=dict(size=11, color="#666"))
    fig.update_xaxes(title_text="品类", row=2, col=1, title_font=dict(size=11, color="#666"))
    fig.update_yaxes(title_text="销售额 (¥)", row=2, col=1, title_font=dict(size=11, color="#666"))
    fig.update_xaxes(title_text="城市", row=2, col=2, title_font=dict(size=11, color="#666"))
    fig.update_yaxes(title_text="销售额 (¥)", row=2, col=2, title_font=dict(size=11, color="#666"))

    fig.show()
