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

ApiToken_api = APIRouter()

class QueryCondition(Condition):
    AiApi_id: Optional[int] = None
    PNumber_id: Optional[int] = None

class InItem(BaseModel):
    id: Optional[int] = None
    AiApi_id: Optional[int] = None
    PNumber_id: Optional[int] = None
    token: Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None
    AiApi: Optional[str] = None
    PNumber: Optional[int] = None
    AiApiname: Optional[str] = None
    PNumberOwner: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@ApiToken_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = ApiToken.filter().prefetch_related("PNumber","AiApi")
        query = condition(data,query)
        if data.PNumber_id:
            query = query.filter(PNumber_id=data.PNumber_id)
        if data.AiApi_id:
            query = query.filter(AiApi_id=data.AiApi_id)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        query=query.order_by("PNumber_id")
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            AiApi_id=iteam.AiApi_id,
            AiApi=iteam.AiApi.name if iteam.AiApi else None,
            AiApiname=iteam.AiApi.description if iteam.AiApi else None,
            PNumber_id=iteam.PNumber_id,
            PNumber=iteam.PNumber.number if iteam.PNumber else None,
            PNumberOwner=iteam.PNumber.Owner if iteam.PNumber else None,
            token=iteam.token,
            createdTime=str(iteam.createdTime),
            status=iteam.status
            ) for iteam in iteams]
        return queryResult(data,QueryResult,iteams_info,total)

@ApiToken_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('AiApi_id', 'PNumber_id')
    return await SaveUpdate(request,ApiToken,InItem,fields)
       
@ApiToken_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(ApiToken, {"id": id}, "删除成功")