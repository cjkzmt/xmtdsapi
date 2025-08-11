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
Music_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class InItem(TopItem):
    duration: Optional[int] = None
    url: Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Music_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Music.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            name=iteam.name,
            duration=iteam.duration,
            url=iteam.url,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            ) for iteam in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)

@Music_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Music,InItem,('duration'))

@Music_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(Music,TopItem,fields= ('id', 'name'))

class MusicListIn(BaseModel):
    itemList: List[Item]
@Music_api.post("/saveList", summary="批量保存音乐列表")
async def saveList(request: Request):
    return await save_list(request,Music,MusicListIn,("name", "duration"),'音乐')

@Music_api.delete("/{id}", summary='删除指定内容', description='功能描述')
async def delete_music(id: int):
    return await delete(Music, {"id": id}, "音乐删除成功")