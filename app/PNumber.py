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

class Item(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    rent: Optional[int] = None
    Owner: Optional[str] = None
    code: Optional[int] = None
    PhoneId: Optional[int] = None  # 如 "2025-04-05T12:34:56Z"
    Phone: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@PNumber_api.post("/getPNumberPages", summary='分页查询用户数据', description='功能描述')
async def get_PNumber_pages(request: Request):
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
            PhoneId=iteam.Phone_id,
            Phone=iteam.Phone.name if iteam.Phone else None
            ) for iteam in iteams
        ]
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
            total=total
        )
        
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result
    )


@PNumber_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPNumber(request: Request):
    async with in_transaction():
        PNumber_in = await parse_request_body(request, Item)
        print(PNumber_in)
        if PNumber_in.id:
            iteam = await PNumber.get(id=PNumber_in.id)
            if PNumber_in.number:
                iteam.number = PNumber_in.number
            if PNumber_in.code is not  None and PNumber_in.code>-1:
                print("code")
                iteam.code = PNumber_in.code
            if PNumber_in.rent:
                iteam.rent = PNumber_in.rent
            if PNumber_in.Owner:
                iteam.Owner = PNumber_in.Owner
            if PNumber_in.status:
                iteam.status = PNumber_in.status
            if PNumber_in.PhoneId and PNumber_in.PhoneId>0:
                iteam.Phone_id =PNumber_in.PhoneId
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await PNumber.create(
            number=PNumber_in.number, 
            code=PNumber_in.code if PNumber_in.code is not  None and PNumber_in.code>-1 else None,
            rent=PNumber_in.rent, 
            Owner=PNumber_in.Owner,
            PNumber_id=PNumber_in.PhoneId if PNumber_in.PhoneId and PNumber_in.PhoneId>0 else None,
            )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

class TopPNumber(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

@PNumber_api.get("/TopPNumbers", summary='查找所有内容', description='功能描述')
async def getAllTopPNumbers():
    async with in_transaction():
        PNumbers = await PNumber.all().values('id', 'number')
        iteams_info = [
            TopPNumber(
                id=PNumber['id'],
                number=PNumber['number'],
            ) for PNumber in PNumbers
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info
        )


@PNumber_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(PNumber, {"id": id}, "删除成功")