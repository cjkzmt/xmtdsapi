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
Author_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    AuthorId: Optional[str] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class AuthorItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    number: Optional[str] = None
    url : Optional[str] = None
    urlnum : Optional[int] = None
    PlatformId: Optional[int] = None
    Platform : Optional[str] = None
    createdTime : Optional[str] = None
    updatedTime : Optional[str] = None
    status: Optional[str] = None

class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[AuthorItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数

@Author_api.post("/getAuthorPages", summary='分页查询用户数据', description='功能描述')
async def get_Author_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    if data.currentPage <= 0 or data.pageSize <= 0:
        return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    query = Author.filter().prefetch_related("Platform")
   # 替换原有赋值逻辑
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
    if data.AuthorId:
        query = query.filter(Author_id=data.AuthorId)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    Authors = await query.offset(offset).limit(data.pageSize)
    Author_items = [
    AuthorItem(
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
        records=Author_items,
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

@Author_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteAuthor(id:int):
    try:
        Authoring = await Author.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await Authoring.delete()
        return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@Author_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAuthor(request: Request):
    Author_in = await parse_request_body(request, AuthorItem)
    if Author_in.id:
        Authoring = await Author.get(id=Author_in.id)
        if Author_in.name:
            Authoring.name = Author_in.name
        if Author_in.number:
            Authoring.number = Author_in.number
        if Author_in.url:
            Authoring.url = Author_in.url
        if Author_in.urlnum:
            Authoring.urlnum = Author_in.urlnum
        if Author_in.PlatformId>0:
            Authoring.Platform_id = Author_in.PlatformId
        if Author_in.status:
            Authoring.status =Author_in.status
        await Authoring.save()
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

class TopAuthor(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

@Author_api.get("/TopAuthors", summary='查找所有内容', description='功能描述')
async def getAllTopAuthors():
    Authors = await Author.all().values('id', 'number')
    Author_items = [
        TopAuthor(
            id=Author['id'],
            number=Author['number'],
        ) for Author in Authors
    ]
    return ResponseModel(
        code="000000",
        mesg="获取成功",
        time=str(datetime.now()),
        data=Author_items
    )