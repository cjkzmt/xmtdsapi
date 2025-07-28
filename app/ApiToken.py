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
    AiApiId: Optional[int] = None
    PNumberId: Optional[int] = None

class Item(BaseModel):
    id: Optional[int] = None
    AiApiId: Optional[int] = None
    AiApi: Optional[str] = None
    AiApiname: Optional[str] = None
    PNumberId: Optional[int] = None
    PNumber: Optional[int] = None
    PNumberOwner: Optional[str] = None
    token: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@ApiToken_api.post("/getApiTokenPages", summary='分页查询用户数据', description='功能描述')
async def get_ApiToken_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = ApiToken.filter().prefetch_related("PNumber","AiApi")
        query = condition(data,query)
        if data.PNumberId:
            query = query.filter(PNumber_id=data.PNumberId)
        if data.AiApiId:
            query = query.filter(AiApi_id=data.AiApiId)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            AiApiId=iteam.AiApi_id,
            AiApi=iteam.AiApi.name if iteam.AiApi else None,
            AiApiname=iteam.AiApi.description if iteam.AiApi else None,
            PNumberId=iteam.PNumber_id,
            PNumber=iteam.PNumber.number if iteam.PNumber else None,
            PNumberOwner=iteam.PNumber.Owner if iteam.PNumber else None,
            token=iteam.token,
            createdTime=str(iteam.createdTime),
            status=iteam.status
            ) for iteam in iteams]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[], 
            pages=pages,
            records=iteams_info,
            searchCount=True,
            size=data.pageSize,
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)

@ApiToken_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addApiToken(request: Request):
    async with in_transaction():
        ApiToken_in = await parse_request_body(request, Item)
        print(ApiToken_in)
        if ApiToken_in.id:
            ApiTokening = await ApiToken.get(id=ApiToken_in.id)
            if ApiToken_in.AiApiId and ApiToken_in.AiApiId>0:
                ApiTokening.AiApi_id = ApiToken_in.AiApiId
            if ApiToken_in.PNumberId and ApiToken_in.PNumberId>0:
                ApiTokening.PNumber_id= ApiToken_in.PNumberId
            if ApiToken_in.token:
                ApiTokening.token = ApiToken_in.token
            if ApiToken_in.status:
                ApiTokening.status = ApiToken_in.status
            await ApiTokening.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await ApiToken.create(
        AiApi_id=ApiToken_in.AiApiId if ApiToken_in.AiApiId and ApiToken_in.AiApiId>0 else None,
        PNumber_id=ApiToken_in.PNumberId if ApiToken_in.PNumberId and ApiToken_in.PNumberId>0 else None ,
        token=ApiToken_in.token)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@ApiToken_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(ApiToken, {"id": id}, "删除成功")