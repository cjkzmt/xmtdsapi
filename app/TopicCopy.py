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
    TypeTextId: Optional[int] = None

class Item(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    url : Optional[str] = None
    AuthorId: Optional[int] = None
    Author: Optional[str] = None
    TypeTextId: Optional[int] = None
    TypeText: Optional[str] = None
    topicnum: Optional[int] = None
    copynum: Optional[int] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@TopicCopy_api.post("/getTopicCopyPages", summary='分页查询用户数据', description='功能描述')
async def get_TopicCopy_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = TopicCopy.filter().prefetch_related("TypeText","Author")
        query = condition(data,query)
        if data.TypeTextId:
            query = query.filter(TypeText_id=data.TypeTextId)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.order_by("-id").offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            text=iteam.text,
            url=iteam.url,
            AuthorId=iteam.Author_id,
            Author=iteam.Author.name if iteam.Author else None,
            TypeTextId=iteam.TypeText_id,
            TypeText=iteam.TypeText.name if iteam.TypeText else None,
            topicnum=iteam.topicnum,
            copynum=iteam.copynum,
            createdTime=str(iteam.createdTime),
            status=iteam.status
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

@TopicCopy_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTopicCopy(request: Request):
    async with in_transaction():
        TopicCopy_in = await parse_request_body(request, Item)
        print(TopicCopy_in)
        if TopicCopy_in.id:
            TopicCopying = await TopicCopy.get(id=TopicCopy_in.id)
            if TopicCopy_in.text:
                TopicCopying.text = TopicCopy_in.text
            if TopicCopy_in.url:
                TopicCopying.url = TopicCopy_in.url
            if TopicCopy_in.AuthorId and TopicCopy_in.AuthorId>0:
                TopicCopying.Author_id = TopicCopy_in.AuthorId
            if TopicCopy_in.TypeTextId:
                TopicCopying.TypeText_id= TopicCopy_in.TypeTextId
            if TopicCopy_in.topicnum and TopicCopy_in.topicnum >0:
                TopicCopying.topicnum = TopicCopy_in.topicnum
            if TopicCopy_in.copynum and TopicCopy_in.copynum>0:
                TopicCopying.copynum = TopicCopy_in.copynum
            if TopicCopy_in.status:
                TopicCopying.status = TopicCopy_in.status
            await TopicCopying.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        if TopicCopy_in.text:
            txt=TopicCopy_in.text
            txt=txt.replace('\n', '')
            txt=txt.replace(' ', '')
            try:
                typetext = await TopicCopy.get(text=txt)
                return ResponseModel[str](
                code="000001",
                mesg="添加TopicCopy 失败",
                time=str(datetime.now()),
                data=f"文案已存在,{typetext.id}"
            )
            except:
                pass
            await TopicCopy.create(
            text=TopicCopy_in.text, 
            url=TopicCopy_in.url,
            Author_id=TopicCopy_in.AuthorId,
            TypeText_id=TopicCopy_in.TypeTextId,
            )
            return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
        urls=TopicCopy_in.url.split('\n').strip()
        if len(urls)>1:
            for url in urls:
                try:
                    await TopicCopy_in.get(url=url)
                except Exception as e:
                    AuthorId= TopicCopy_in.AuthorId if TopicCopy_in.AuthorId and TopicCopy_in.AuthorId>0 else None
                    await TopicCopy_in.create(url=url,Author_id=AuthorId)
            return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@TopicCopy_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(TopicCopy, {"id": id}, "删除成功")