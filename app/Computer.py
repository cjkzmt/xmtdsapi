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
Computer_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class InItem(TopItem):
    Verification: Optional[str] = None
    createtext: Optional[str] = None
    createvideo: Optional[str] = None
    publishvideo: Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Computer_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Computer.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Computers = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Computer.id,
            name=Computer.name,
            Verification=Computer.Verification,
            createdTime=str(Computer.createdTime),
            status=Computer.status,
            createtext= Computer.createtext,
            createvideo = Computer.createvideo,
            publishvideo = Computer.publishvideo
            ) for Computer in Computers
        ]
        return queryResult(data,QueryResult,iteams_info,total)
    
@Computer_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Computer,InItem)

@Computer_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(Computer,TopItem,fields= ('id', 'name'))

@Computer_api.post("/Verify", summary='查找所有内容', description='功能描述')
async def Verifyiteam(info: VerifyItem):
    return await Verify(info,Computer,'Computer')

@Computer_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Computer, {"id": id}, "删除成功")