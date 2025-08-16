import logging
import os
# 在文件顶部导入后添加
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
# 配置日志系统
log_file = os.path.join(LOG_DIR, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler(log_file, encoding='utf-8')  # 日志写入文件
    ]
)

logger = logging.getLogger(__name__)