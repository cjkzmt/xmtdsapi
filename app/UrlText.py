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
UrlText_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    UrlTextId: Optional[str] = None
    status: Optional[str] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class UrlTextItem(BaseModel):
    id: Optional[int] = None
    url : Optional[str] = None
    AuthorId: Optional[int] = None
    Author: Optional[str] = None
    createdTime : Optional[str] = None
    status: Optional[str] = None

class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[UrlTextItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数

@UrlText_api.post("/getUrlTextPages", summary='分页查询用户数据', description='功能描述')
async def get_UrlText_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    if data.currentPage <= 0 or data.pageSize <= 0:
        return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    query = UrlText.filter().prefetch_related("Author")
   # 替换原有赋值逻辑
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
    if data.UrlTextId:
        query = query.filter(id=data.UrlTextId)
    if data.status:
        query = query.filter(status=data.status)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    UrlTexts = await query.offset(offset).limit(data.pageSize)
    UrlText_items = [
    UrlTextItem(
        id=UrlText.id,
        url=UrlText.url,
        AuthorId=UrlText.Author_id,
        Author=UrlText.Author.name if UrlText.Author else None,
        createdTime=str(UrlText.createdTime),
        status=UrlText.status,
        ) for UrlText in UrlTexts
    ]
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    query_result = QueryResult(
        current=data.currentPage,
        hitcount=True,
        optimizeCountSql=False,
        orders=[], 
        pages=pages,
        records=UrlText_items,
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

@UrlText_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteUrlText(id:int):
    try:
        UrlTexting = await UrlText.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await UrlTexting.delete()
        return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@UrlText_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addUrlText(request: Request):
    UrlText_in = await parse_request_body(request, UrlTextItem)
    if UrlText_in.id:
        UrlTexting = await UrlText.get(id=UrlText_in.id)
        if UrlText_in.url:
            UrlTexting.url = UrlText_in.url
        if UrlText_in.AuthorId>0:
            UrlTexting.Author_id = UrlText_in.AuthorId
        if UrlText_in.status:
            UrlTexting.status =UrlText_in.status
        await UrlTexting.save()
        return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
    urls=UrlText_in.url.split('/n')
    for url in urls:
        if url:
            await UrlText.create(url=url)
    return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
