from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
from datetime import datetime
import tortoise.exceptions
from tortoise.transactions import in_transaction
Author_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

class InItem(TopItem):
    number: Optional[str] = None
    url : Optional[str] = None
    urlnum : Optional[int] = None
    Platform_id: Optional[int] = None
    status: Optional[str] = None
    
class Item(InItem):
    createdTime: Optional[str] = None
    Platform : Optional[str] = None
    updatedTime : Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Author_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Author.filter().prefetch_related("Platform")
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Authors = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Author.id,
            name=Author.name,
            number=Author.number,
            url=Author.url,
            urlnum=Author.urlnum,
            Platform_id=Author.Platform_id,
            Platform=Author.Platform.name if Author.Platform else None,
            createdTime=str(Author.createdTime),
            updatedTime=str(Author.updatedTime),
            status=Author.status,
            ) for Author in Authors
        ]
        return queryResult(data,iteams_info,total)

@Author_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Author,InItem,('Platform_id'))

@Author_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    fields = ('id', 'number', 'scope')
    return await GetAll(Author,TopItem,fields=fields)

@Author_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Author, {"id": id}, "模型删除成功")
