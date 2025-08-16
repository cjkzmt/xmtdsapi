import os
import threading
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import psutil
import GPUtil
import time
import logging
from typing import Optional
from src.task.task import fetch_new_tasks, worker
from src.utils.Ffmpeg import *
x={'taskname': 'reading', 'id': 513}
GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
if not GPU_SUPPORTED: print("注意：将使用CPU模式运行...")
worker(x)

# from src.task.Text.Createreading import *

# xxx='''这房子我住了二十年，感情深，但确实老了。这次翻新我就认三个死理：冬天不用抖，夏天不用扇；能种花、能种菜；朋友来了必须能坐下撸串喝啤酒。 师傅问我用啥材料？我说别跟我扯这个，我就要结果。三个月后交钥匙那天，人家撂下一句话："两年内哪儿不合适，随叫随到。" 现在每天推门进屋就乐——早知道这么舒坦，早该折腾了！算笔账更惊喜：要是自己跑材料盯工人，花的钱和时间够我再装半套房。 昨儿大雪，我在新铺的地暖上光脚溜达；夏天暴雨，坐在落地窗前啃西瓜看菜苗疯长。上周发小来，院里炭火刚架上肉串，屋里火锅已经咕嘟冒泡。 要我说啊，日子就得这么过：城里上班十分钟回鹿泉，推门是花香，抬头是蓝天，朋友来了有酒有肉。啥叫好生活？就是活成邻居嘴里那句"瞧人家这院子装的！"'''


# subtitle= RemovePunctuation(xxx)
# print(subtitle)