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

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    uniqueId: Optional[str] = None
    createtext: Optional[str] = None
    createvideo: Optional[str] = None
    publishvideo: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Computer_api.post("/getComputerPages", summary='分页查询用户数据', description='功能描述')
async def get_Computer_pages(request: Request):
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
            uniqueId=Computer.uniqueId,
            createdTime=str(Computer.createdTime),
            status=Computer.status,
            createtext= Computer.createtext,
            createvideo = Computer.createvideo,
            publishvideo = Computer.publishvideo
            ) for Computer in Computers
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

@Computer_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addComputer(request: Request):
    async with in_transaction():
        Computer_in = await parse_request_body(request, Item)
        print(Computer_in)
        if Computer_in.id:
            iteam = await Computer.get(id=Computer_in.id)
            if Computer_in.name:
                iteam.name = Computer_in.name
            if Computer_in.uniqueId:
                iteam.uniqueId = Computer_in.uniqueId
            if Computer_in.createtext:
                iteam.createtext = Computer_in.createtext
            if Computer_in.createvideo:
                iteam.createvideo = Computer_in.createvideo
            if Computer_in.publishvideo:
                iteam.publishvideo = Computer_in.publishvideo
            if Computer_in.status:
                iteam.status = Computer_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await Computer.create(name=Computer_in.name)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)


class VerifyComputer(BaseModel):
    id: Optional[int] = None
    uniqueId: Optional[str] = None

@Computer_api.post("/Verify", summary='查找所有内容', description='功能描述')
async def VerifyComputers(Computer_in: VerifyComputer):
    async with in_transaction():
        print(Computer_in )
        try:
            iteam = await Computer.get(id=Computer_in.id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        if iteam.uniqueId is None:
            iteam.uniqueId = Computer_in.uniqueId
            await iteam.save()            
        elif iteam.uniqueId != Computer_in.uniqueId:            
            return ResponseModel(
                code="00001",
                mesg="匹配失败",
                time=str(datetime.now()),
                data=False
            )
        return ResponseModel(
            code="000000",
            mesg="匹配成功",
            time=str(datetime.now()),
            data=create_user_token(data={"user_id":int(Computer_in.id),'Role':'Computer' })
            )

@Computer_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Computer, {"id": id}, "删除成功")