from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
from tortoise.transactions import in_transaction
from datetime import datetime
VideoClips_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class InItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    clipsum: Optional[int] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@VideoClips_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = VideoClips.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            name=iteam.name,
            clipsum=iteam.clipsum,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            ) for iteam in iteams]
        return queryResult(data,QueryResult,iteams_info,total)


@VideoClips_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('clipsum', 'TypeCover_id', 'TypeSubtitle_id', 'TypeVideo_id')
    return await SaveUpdate(request,AccountTeam,InItem,fields)

@VideoClips_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteiteam(id: int):
    return await delete(VideoClips, {"id": id}, "删除成功")