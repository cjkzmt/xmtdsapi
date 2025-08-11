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
Over_api = APIRouter()

class QueryCondition(Condition):
    sex: Optional[str] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class InItem(TopItem):
    filename: Optional[str] = None
    sex: Optional[str] = None
    speed: Optional[float] = None
    url: Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Over_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Over.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Over.id,
            name=Over.name,
            filename=Over.filename,
            sex=Over.sex,
            speed=Over.speed,
            url=Over.url,
            createdTime=str(Over.createdTime),
            status=Over.status,
            ) for Over in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)

@Over_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Over,InItem)

@Over_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(Over,TopItem,fields=('id', 'name'))
    
class OverList(BaseModel):
    itemList: List[Item]
@Over_api.post("/saveList", summary="批量保存字体列表")
async def saveList(request: Request):
    return await save_list(request,Over,OverList,("filename"),'配音')

@Over_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Over, {"id": id}, "删除成功")