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

TopicCopy_api = APIRouter()

class QueryCondition(Condition):
    TypeText_id: Optional[int] = None

class InItem(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    url : Optional[str] = None
    Author_id: Optional[int] = None
    TypeText_id: Optional[int] = None
    topicnum: Optional[int] = None
    copynum: Optional[int] = None
    status: Optional[str] = None

class Item(InItem):
    Author: Optional[str] = None
    TypeText: Optional[str] = None
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@TopicCopy_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = TopicCopy.filter().prefetch_related("TypeText","Author")
        query = condition(data,query)
        if data.TypeText_id:
            query = query.filter(TypeText_id=data.TypeText_id)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.order_by("-id").offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            text=iteam.text,
            url=iteam.url,
            Author_id=iteam.Author_id,
            Author=iteam.Author.name if iteam.Author else None,
            TypeText_id=iteam.TypeText_id,
            TypeText=iteam.TypeText.name if iteam.TypeText else None,
            topicnum=iteam.topicnum,
            copynum=iteam.copynum,
            createdTime=str(iteam.createdTime),
            status=iteam.status
            ) for iteam in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)

@TopicCopy_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('Author_id', 'TypeText_id', 'topicnum', 'copynum')
    return await SaveUpdate(request,TopicCopy,InItem,fields)
    #  if TopicCopy_in.text:
    #         txt=TopicCopy_in.text
    #         txt=txt.replace('\n', '')
    #         txt=txt.replace(' ', '')
    #         try:
    #             typetext = await TopicCopy.get(text=txt)
    #             return ResponseModel[str](
    #             code="000001",
    #             mesg="添加TopicCopy 失败",
    #             time=str(datetime.now()),
    #             data=f"文案已存在,{typetext.id}"
    #         )
    #         except:
    #             pass
    #         await TopicCopy.create(
    #         text=TopicCopy_in.text, 
    #         url=TopicCopy_in.url,
    #         Author_id=TopicCopy_in.Author_id,
    #         TypeText_id=TopicCopy_in.TypeText_id,
    #         )
    #         return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    #     urls=TopicCopy_in.url.split('\n').strip()
    #     if len(urls)>1:
    #         for url in urls:
    #             try:
    #                 await TopicCopy_in.get(url=url)
    #             except Exception as e:
    #                 Author_id= TopicCopy_in.Author_id if TopicCopy_in.Author_id and TopicCopy_in.Author_id>0 else None
    #                 await TopicCopy_in.create(url=url,Author_id=Author_id)
    #         return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@TopicCopy_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(TopicCopy, {"id": id}, "删除成功")