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
from datetime import datetime
from tortoise.transactions import in_transaction

PNumber_api = APIRouter()

class QueryCondition(Condition):
    number: Optional[int] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

class InItem(TopItem):
    rent: Optional[int] = None
    Owner: Optional[str] = None
    code: Optional[int] = None
    Phone_id: Optional[int] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None
    Phone: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@PNumber_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = PNumber.filter().prefetch_related("Phone")
        query = condition(data,query)
        if data.number:
            query = query.filter(number__icontains=data.number)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            number=iteam.number,
            code=iteam.code,
            rent=iteam.rent,
            Owner=iteam.Owner,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            Phone_id=iteam.Phone_id,
            Phone=iteam.Phone.name if iteam.Phone else None
            ) for iteam in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)

@PNumber_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,PNumber,InItem,('code', 'Phone_id','rent'))

@PNumber_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(PNumber,TopItem,fields= ('id', 'number'))

@PNumber_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(PNumber, {"id": id}, "删除成功")