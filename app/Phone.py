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
from tortoise.transactions import in_transaction#async with in_transaction():
from datetime import datetime
Phone_api = APIRouter()

class QueryCondition(Condition):
    PhoneName: Optional[str] = None
    Brand: Optional[str] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None

class InItem(TopItem):
    Model: Optional[str] = None
    Brand: Optional[str] = None
    Owner: Optional[str] = None
    status: Optional[str] = None
    Verification: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Phone_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Phone.filter()
        query = condition(data,query)
        if data.PhoneName:
            query = query.filter(name=data.PhoneName)
        if data.Brand:
            query = query.filter(Brand=data.Brand)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            name=iteam.name,
            Model=iteam.Model,
            Brand=iteam.Brand,
            Owner=iteam.Owner,
            sort=iteam.sort,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            Verification=iteam.Verification,
            ) for iteam in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)

@Phone_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Phone,InItem)

@Phone_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(Phone,TopItem,fields=('id', 'name', 'sort'))

@Phone_api.post("/Verify", summary='查找所有内容', description='功能描述')
async def Verifyiteam(info: VerifyItem):
    return await Verify(info,Phone,'Phone')
    
@Phone_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Phone, {"id": id}, "删除成功")