from src.task.Clip.视频处理  import *
import time
from dotenv import load_dotenv
load_dotenv()

GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
if not GPU_SUPPORTED: print("注意：将使用CPU模式运行...")
# deleteBugVoide(os.path.join(os.getenv("RootDirectory"),'Content','RawFootage'))
# deleteBugVoide(os.path.join(os.getenv("RootDirectory"),'Content','TemporaryFootage'))
while 视频处理():
    time.sleep(1)
    
