# 销售数据可视化
+ 项目介绍

```plain
生成各地区的随机订单数据
连接数据库并存储
绘制饼图、柱状图展示数据
```

+ 流程

```plain
numpy生成数据 → pandas处理 → psycopg存储到PostgreSQL → plotly绘制图表
```

# 环境
| **类别** | **名称** | **版本号** |
| --- | --- | --- |
| <font style="background-color:rgba(255, 255, 255, 0);">容器</font> | [Docker](https://docs.docker.com/desktop/setup/install/linux/) / [Podman](https://podman.io/docs/installation) | <font style="background-color:rgba(255, 255, 255, 0);">29.5.3 / 5.8.2</font> |
| <font style="background-color:rgba(255, 255, 255, 0);">容器管理工具</font> | [Docker](https://docs.docker.com/desktop/setup/install/linux/) / [Podman](https://podman-desktop.io/) | <font style="background-color:rgba(255, 255, 255, 0);">4.77.0 / 1.27.2</font> |
| <font style="background-color:rgba(255, 255, 255, 0);">编程</font> | <font style="background-color:rgba(255, 255, 255, 0);">Python</font> | <font style="background-color:rgba(255, 255, 255, 0);">3.14 (虚拟环境)</font> |
| <font style="background-color:rgba(255, 255, 255, 0);">数据库</font> | [PostgreSQL ](https://hub.docker.com/_/postgres) | <font style="background-color:rgba(255, 255, 255, 0);">16.14</font> |


## 依赖库
| 库名 | 版本 | 用途 |
| --- | --- | --- |
| numpy | 2.4.6 | 数值计算(随机数生成) |
| pandas | 3.0.3 | 数据分析与聚合 |
| plotly | 6.8.0 | 图表可视化 |
| psycopg | 3.3.4 | 数据库 PostgreSQL 连接 |
| python-dotenv | 1.2.2 | 环境变量管理 |
| .... |  | 必要依赖捆绑 |


# 目录介绍
```bash
├── config/                   # 配置
│   └── db_config.py          # 数据库连接配置（读取.env）
├── src/                      # 代码目录
│   ├── __init__.py           # 标识为Python包，目录可被导入
│   ├── data_generator.py     # 随机数生成
│   ├── db_connector.py       # 数据库操作
│   └── visualizer.py         # 可视化图表
├── .env                      # 数据库环境变量
├── run.py                    # 主入口
├── requirements.txt          # 依赖清单
└── README.md                 # 说明文档
```

## PostgreSQL 容器配置
+ [容器操作文档](https://github.com/chenxiny67-debug/-Podman-User-Documentation)

```bash
# Docker
docker run -d \
  --name postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=YAN \
  -e POSTGRES_PASSWORD=YAN@2039361436 \
  -e POSTGRES_DB=exat \
  -p 5432:5432 \
  postgres:16.14


# Podman
podman run -d \
  --name postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=YAN \
  -e POSTGRES_PASSWORD=YAN@2039361436 \
  -e POSTGRES_DB=exat \
  -p 5432:5432 \
  docker.io/library/postgres:16.14
```

```bash
# 启动容器
docker start postgres
# 停止容器
docker stop postgres 
# 删除容器
docker rm postgres 
# 删除镜像
docker rmi postgres:16.14
```

## Python 虚拟环境配置
```bash
# 更新系统软件包索引
sudo apt update

# 安装 Python 3.14 虚拟环境
sudo apt install python3.14-venv -y

# 创建名为 .venv 虚拟环境 (当前项目录)
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 虚拟环境中安装依赖库
pip install "psycopg[binary]" numpy plotly pandas python-dotenv

# 安装的库及版本号导出到 requirements.txt
pip freeze > requirements.txt
```

```bash
git clone
```



