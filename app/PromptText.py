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
PromptText_api = APIRouter()

class QueryCondition(Condition):
    text: Optional[str] = None

class Item(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@PromptText_api.post("/getPromptTextPages", summary='分页查询用户数据', description='功能描述')
async def get_PromptText_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = PromptText.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            text=iteam.text,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
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


@PromptText_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPromptText(request: Request):
    async with in_transaction():
        PromptText_in = await parse_request_body(request, Item)
        print(PromptText_in)
        if PromptText_in.id:
            iteam = await PromptText.get(id=PromptText_in.id)
            if PromptText_in.text:
                iteam.text = PromptText_in.text
            if PromptText_in.status:
                iteam.status = PromptText_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        try:
            await TopicCopy.get(text=PromptText_in.text)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"已存在,{PromptText_in.text}")
        except:pass
        await PromptText.create(text=PromptText_in.text)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@PromptText_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(PromptText, {"id": id}, "删除成功")