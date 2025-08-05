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
Certifier_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None
    idnumber: Optional[int] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class InItem(BaseModel):
    idnumber: Optional[int] = None
    Owner:Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 

@Certifier_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Certifier.filter()
        query = condition(data,query)
        if data.name:
            query = query.filter(name=data.name)
        if data.idnumber:
            query = query.filter(idnumber__icontains=data.idnumber)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Certifiers = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Certifier.id,
            name=Certifier.name,
            Model=Certifier.idnumber,
            Owner=Certifier.Owner,
            createdTime=str(Certifier.createdTime),
            status=Certifier.status
            ) for Certifier in Certifiers]
        return queryResult(data,QueryResult,iteams_info,total)

@Certifier_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Certifier,InItem)

@Certifier_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(Certifier,TopItem,fields= ('id', 'name'))

@Certifier_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Certifier, {"id": id}, "删除成功")