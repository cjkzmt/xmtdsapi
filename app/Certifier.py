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
Certifier_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    CertifierName: Optional[str] = None
    idnumber: Optional[int] = None
    CertifierId: Optional[int] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class CertifierItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    idnumber: Optional[int] = None
    Owner:Optional[str] = None
    createdTime: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    status: Optional[str] = None
class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[CertifierItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数



@Certifier_api.post("/getCertifierPages", summary='分页查询用户数据', description='功能描述')
async def get_Certifier_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    if data.currentPage <= 0 or data.pageSize <= 0:
        return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    query = Certifier.filter()
   # 替换原有赋值逻辑
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)

    if data.CertifierName:
        #打印的值 是(None,) 要求提前处理  data 里的数据 打印  None
        query = query.filter(name=data.CertifierName)
    if data.idnumber:
        query = query.filter(idnumber__icontains=data.idnumber)
    if data.CertifierId:
        query = query.filter(id=data.CertifierId)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    Certifiers = await query.offset(offset).limit(data.pageSize)
    Certifier_items = [
    CertifierItem(
        id=Certifier.id,
        name=Certifier.name,
        Model=Certifier.idnumber,
        Owner=Certifier.Owner,
        createdTime=str(Certifier.createdTime),
        status=Certifier.status
        ) for Certifier in Certifiers
    ]
    # print(Certifier_items[0].createdTime)
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    # 创建分页结果
    query_result = QueryResult(
        current=data.currentPage,
        hitcount=True,
        optimizeCountSql=False,
        orders=[],  # 可根据需求添加排序逻辑
        pages=pages,
        records=Certifier_items,
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


@Certifier_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteCertifier(id:int):
    try:
        Certifiering = await Certifier.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await Certifiering.delete()
        return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@Certifier_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addCertifier(request: Request):
    Certifier_in = await parse_request_body(request, CertifierItem)
    print(Certifier_in)
    if Certifier_in.id is None:
        await Certifier.create(
        name=Certifier_in.name, 
        idnumber=Certifier_in.idnumber, 
        Owner=Certifier_in.Owner
        )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    Certifiering = await Certifier.get(id=Certifier_in.id)
    if Certifier_in.name:
        Certifiering.name = Certifier_in.name
    if Certifier_in.idnumber:
        Certifiering.idnumber = Certifier_in.idnumber
    if Certifier_in.Owner:
        Certifiering.Owner = Certifier_in.Owner
    if Certifier_in.status:
        Certifiering.status = Certifier_in.status
    await Certifiering.save()
    return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)


class TopCertifier(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

@Certifier_api.get("/TopCertifiers", summary='查找所有内容', description='功能描述')
async def getAllTopCertifiers():
    Certifiers = await Certifier.all().values('id', 'name')
    Certifier_items = [
        TopCertifier(
            id=Certifier['id'],
            name=Certifier['name']
        ) for Certifier in Certifiers
    ]
    return ResponseModel(
        code="000000",
        mesg="获取成功",
        time=str(datetime.now()),
        data=Certifier_items
    )