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
PNumber_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    PNumberId: Optional[str] = None
    number: Optional[int] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class PNumberItem(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    rent: Optional[int] = None
    Owner: Optional[str] = None
    PNumberId: Optional[int] = None  # 如 "2025-04-05T12:34:56Z"
    PNumber: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    status: Optional[str] = None
class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[PNumberItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数
from datetime import datetime


@PNumber_api.post("/getPNumberPages", summary='分页查询用户数据', description='功能描述')
async def get_PNumber_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    if data.currentPage <= 0 or data.pageSize <= 0:
        return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    query = PNumber.filter().prefetch_related("Phone")
   # 替换原有赋值逻辑
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)

    if data.number:
        query = query.filter(number__icontains=data.number)
    if data.PNumberId:
        query = query.filter(PNumber_id=data.PNumberId)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    PNumbers = await query.offset(offset).limit(data.pageSize)
    PNumber_items = [
    PNumberItem(
        id=PNumber.id,
        number=PNumber.number,
        rent=PNumber.rent,
        Owner=PNumber.Owner,
        createdTime=str(PNumber.createdTime),
        status=PNumber.status,
        PNumberId=PNumber.PNumber_id,
        PNumber=PNumber.Phone.name if PNumber.Phone else None
        ) for PNumber in PNumbers
    ]
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    query_result = QueryResult(
        current=data.currentPage,
        hitcount=True,
        optimizeCountSql=False,
        orders=[], 
        pages=pages,
        records=PNumber_items,
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


@PNumber_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deletePNumber(id:int):
    try:
        PNumbering = await PNumber.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await PNumbering.delete()
        return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@PNumber_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPNumber(request: Request):
    PNumber_in = await parse_request_body(request, PNumberItem)

    print(PNumber_in)
    if PNumber_in.id is None:
        await PNumber.create(
        number=PNumber_in.number, 
        rent=PNumber_in.rent, 
        Owner=PNumber_in.Owner,
        PNumber_id=None if PNumber_in.PNumberId == -1 else PNumber_in.PNumberId,
        )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    PNumbering = await PNumber.get(id=PNumber_in.id)
    if PNumber_in.number:
        PNumbering.number = PNumber_in.number
    if PNumber_in.rent:
        PNumbering.rent = PNumber_in.rent
    if PNumber_in.Owner:
        PNumbering.Owner = PNumber_in.Owner
    if PNumber_in.status:
        PNumbering.status = PNumber_in.status
    if PNumber_in.PNumberId>0:
        PNumbering.PNumber_id =PNumber_in.PNumberId
    await PNumbering.save()
    return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)

class TopPNumber(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

@PNumber_api.get("/TopPNumbers", summary='查找所有内容', description='功能描述')
async def getAllTopPNumbers():
    PNumbers = await PNumber.all().values('id', 'number')
    PNumber_items = [
        TopPNumber(
            id=PNumber['id'],
            number=PNumber['number'],
        ) for PNumber in PNumbers
    ]
    return ResponseModel(
        code="000000",
        mesg="获取成功",
        time=str(datetime.now()),
        data=PNumber_items
    )