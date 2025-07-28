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

class TopAuthor(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

class Item(TopAuthor):
    number: Optional[str] = None
    url : Optional[str] = None
    urlnum : Optional[int] = None
    PlatformId: Optional[int] = None
    Platform : Optional[str] = None
    createdTime : Optional[str] = None
    updatedTime : Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Author_api.post("/getAuthorPages", summary='分页查询用户数据', description='功能描述')
async def get_Author_pages(request: Request):
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
            PlatformId=Author.Platform_id,
            Platform=Author.Platform.name if Author.Platform else None,
            createdTime=str(Author.createdTime),
            updatedTime=str(Author.updatedTime),
            status=Author.status,
            ) for Author in Authors
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

@Author_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAuthor(request: Request):
    async with in_transaction():
        Author_in = await parse_request_body(request, Item)
        if Author_in.id:
            iteam = await Author.get(id=Author_in.id)
            if Author_in.name:
                iteam.name = Author_in.name
            if Author_in.number:
                iteam.number = Author_in.number
            if Author_in.url:
                iteam.url = Author_in.url
            if Author_in.urlnum:
                iteam.urlnum = Author_in.urlnum
            if Author_in.PlatformId>0:
                iteam.Platform_id = Author_in.PlatformId
            if Author_in.status:
                iteam.status =Author_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        urls=Author_in.url.split('/n')
        for url in urls:
            if url:
                Platform=await Platform.get(name="抖音") if 'douyin' in url else None
                await UrlText.create(
                url=url, 
                Platform_id=Platform.id if Platform else None,
                )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)



@Author_api.get("/TopAuthors", summary='查找所有内容', description='功能描述')
async def getAllTopAuthors():
    async with in_transaction():
        Authors = await Author.all().values('id', 'number')
        iteams_info = [
            TopAuthor(
                id=Author['id'],
                number=Author['number'],
            ) for Author in Authors
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info
        )



@Author_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Author, {"id": id}, "模型删除成功")
