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

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    filename: Optional[str] = None
    sex: Optional[str] = None
    speed: Optional[float] = None
    url: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Over_api.post("/getOverPages", summary='分页查询用户数据', description='功能描述')
async def get_Over_pages(request: Request):
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
            ) for Over in Overs
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

@Over_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addOver(request: Request):
    async with in_transaction():
        Over_in = await parse_request_body(request, Item)
        print(Over_in)
        if Over_in.id:
            iteam = await Over.get(id=Over_in.id)
            if Over_in.name:
                iteam.name = Over_in.name
            if Over_in.filename:
                iteam.filename = Over_in.filename
            if Over_in.sex:
                iteam.sex = Over_in.sex
            if Over_in.speed:
                iteam.speed = Over_in.speed
            if Over_in.url:
                iteam.url = Over_in.url
            if Over_in.status:
                iteam.status = Over_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        try:
            await TopicCopy.get(name=Over_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"已存在,{Over_in.name}")
        except:pass
        await Over.create(name=Over_in.name)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)


class TopOver(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

@Over_api.get("/TopOvers", summary='查找所有内容', description='功能描述')
async def getAllTopOvers():
    async with in_transaction():
        Overs = await Over.all().values('id', 'name')
        iteams_info = [
            TopOver(
                id=Over['id'],
                name=Over['name']
            ) for Over in Overs
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info
        )
class OverList(BaseModel):
    OverList: List[Item]
@Over_api.post("/saveList", summary='添加一个内容', description='功能描述')
async def saveList(request: Request):
    async with in_transaction():
        Overs = await parse_request_body(request, OverList)
        sum=len(Overs.OverList)
        Success=Failure=0
        for Over_in in Overs.OverList:
            try:
                await Over.create(filename=Over_in.filename)
                Success+=1
            except:
                Failure+=1
    return ResponseModel(code="000000", mesg=f"一共{sum}个配音，添加成功{Success}，失败{Failure}", time=str(datetime.now()), data=True)



@Over_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Over, {"id": id}, "删除成功")