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
Account_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    AccountId: Optional[str] = None
    PlatformId: Optional[int] = None
    PNumberId: Optional[int] = None
    PhoneId: Optional[int] = 0
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class AccountItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    number: Optional[str] = None
    isDel: Optional[bool] = None
    password: Optional[str] = None
    profile: Optional[str] = None
    PNumberId: Optional[int] = None 
    PNumber: Optional[int] = None 
    team: Optional[int] = None
    note:Optional[str] = None
    CertifierId: Optional[int] = None 
    Certifier: Optional[str] = None
    PlatformId: Optional[int] = None 
    Platform: Optional[str] = None
    PhoneId: Optional[int] = None 
    Phone: Optional[str] = None
    status: Optional[str] = None
    updatedTime:Optional[str] = None
    createdTime:Optional[str] = None
class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[AccountItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数



@Account_api.post("/getAccountPages", summary='分页查询用户数据', description='功能描述')
async def get_Account_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    if data.currentPage <= 0 or data.pageSize <= 0:
        return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    query = Account.filter(isDel=False).prefetch_related("Phone",'PNumber','Certifier','Platform')
   # 替换原有赋值逻辑
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)

    # if data.number:
    #     query = query.filter(number__icontains=data.number)
    if data.AccountId:
        query = query.filter(id=data.AccountId)
    if data.PlatformId:
        query = query.filter(Platform_id=data.PlatformId)
    if data.PNumberId:
        query = query.filter(PNumber_id=data.PNumberId)
    if data.PhoneId:
        query = query.filter(Phone_id=data.PhoneId)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    Accounts = await query.offset(offset).limit(data.pageSize)
    Account_items = [
    AccountItem(
        id=Account.id,
        name=Account.name,
        number=Account.number,
        password=Account.password,
        profile=Account.profile,
        PNumberId=Account. PNumber_id,
        PNumber=Account.PNumber.number if Account.PNumber else None,
        CertifierId=Account.Certifier_id,
        Certifier=Account.Certifier.name if Account.Certifier else None,
        PlatformId=Account. Platform_id,
        Platform=Account.Platform.name if Account.Platform else None,
        PhoneId=Account.Phone_id,
        Phone=Account.Phone.name if Account.Phone else None,
        status=Account.status,
        team=Account.team,
        note=Account.note,
        updatedTime=str(Account.updatedTime),
        createdTime=str(Account.createdTime),
        ) for Account in Accounts
    ]
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    query_result = QueryResult(
        current=data.currentPage,
        hitcount=True,
        optimizeCountSql=False,
        orders=[], 
        pages=pages,
        records=Account_items,
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

@Account_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteAccount(id:int):
    try:
        Accounting = await Account.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await Accounting.delete()
        return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@Account_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAccount(request: Request):
    Account_in = await parse_request_body(request, AccountItem)
    print(Account_in)
    if Account_in.id:
        Accounting = await Account.get(id=Account_in.id)
        if Account_in.name:
            Accounting.name = Account_in.name
        if Account_in.number:
            Accounting.number = Account_in.number
        if Account_in.password:
            Accounting.password = Account_in.password
        if Account_in.profile:
            Accounting.profile = Account_in.profile
        if Account_in.PNumberId>0:
            Accounting.PNumber_id = Account_in.PNumberId
        if Account_in.CertifierId>0:
            Accounting.Certifier_id = Account_in.CertifierId
        if Account_in.PlatformId>0:
            Accounting.Platform_id = Account_in.PlatformId
        if Account_in.PhoneId>0:
            Accounting.Phone_id =Account_in.PhoneId
        if Account_in.status:
            Accounting.status = Account_in.status
        if Account_in.team>0:
            Accounting.team = Account_in.team
        if Account_in.isDel:
            Accounting.isDel = Account_in.isDel
        if Account_in.note:
            Accounting.note = Account_in.note
        await Accounting.save()
        return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
    await Account.create(
        name=Account_in.name,
        number=Account_in.number, 
        password=Account_in.password,
        profile=Account_in.profile,
        PNumber_id=None if Account_in.PNumberId == -1 else Account_in.PNumberId,
        Certifier_id=None if Account_in.CertifierId == -1 else Account_in.CertifierId,
        Platform_id=None if Account_in.PlatformId == -1 else Account_in.PlatformId,
        Phone_id=None if Account_in.PhoneId == -1 else Account_in.PhoneId,
        team=Account_in.team,
        note=Account_in.note
        )
    return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)