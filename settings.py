from zhmm import *
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': HOST,
                'port': 3306,
                'user': USER,
                'password': PASSWORD,
                'database': DATABASE,
                'charset': 'utf8mb4',
                "pool_recycle": 3600,  # 每隔1小时回收连接
                "connect_timeout": 30,  # 连接超时时间
                'minsize': 0,
                'maxsize': 10,
                'echo': True,
            }
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', 'app.models'],  # 根据你的模型路径调整
            'default_connection': 'default',
        }
    }
}
