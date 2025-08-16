from zhmm import *
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # MySQL 驱动
            "credentials": {
                "host": HOST,
                "port": 3306,
                "user": USER,
                "password": PASSWORD,
                "database": DATABASE,
                "charset": "utf8mb4",
                "connect_timeout": 60,  # 连接超时（秒）
                "echo": True,  # 是否输出 SQL 日志（调试用）
            },
            # MySQL 的连接池配置（注意：Tortoise 的 pool 是顶层参数，不在 credentials 里！）
            "pool": {
                "max_size": 20,       # 最大连接数
                "min_size": 5,       # 最小连接数
                "max_queries": 50000, # 单个连接最大查询次数
                "max_inactive_connection_lifetime": 300.0,  # 空闲连接存活时间（秒）
            }
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "app.models"],  # 模型路径
            "default_connection": "default",
        }
    }
}