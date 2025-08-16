from .models import *
from tortoise.transactions import in_transaction
from zhmm import *
from datetime import datetime, timedelta, timezone
from tortoise.query_utils import Prefetch
from tortoise.exceptions import OperationalError
from collections import defaultdict
from .db_connector import tortoise_tx
import asyncio
@tortoise_tx()
async def UpdateclipSum(info):
    # 构建批量更新操作
    updates = []
    for path, clipSum in info.items():
        updates.append(TeamOwner.filter(path=path).update(clipSum=clipSum))
    
    # 使用 gather 并行执行所有更新
    await asyncio.gather(*updates)

