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
Account_api = APIRouter()

class QueryCondition(Condition):
    PlatformId: Optional[int] = None
    PNumberId: Optional[int] = None
    PhoneId: Optional[int] = 0

class Item(BaseModel):
    id: Optional[int] = None
    AccountTeamId: Optional[int] = None
    AccountTeam: Optional[int] = None
    PlatformId: Optional[int] = None 
    Platform: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    isDel: Optional[bool] = None
    password: Optional[str] = None
    profile: Optional[str] = None
    PNumberId: Optional[int] = None 
    PNumber: Optional[int] = None 
    CertifierId: Optional[int] = None 
    Certifier: Optional[str] = None
    status: Optional[str] = None
    note:Optional[str] = None
    updatedTime:Optional[str] = None
    createdTime:Optional[str] = None

class QueryResult(Result):
    records: List[Item] 

@Account_api.post("/getAccountPages", summary='分页查询用户数据', description='功能描述')
async def get_Account_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
        query =  Account.filter(isDel=False).prefetch_related('PNumber','Certifier','platform','AccountTeam')
        if data.statCreateTime and data.endCreateTime:
            try:
                start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
                end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
                query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
            except ValueError:
                return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
        if data.id:
            query = query.filter(id=data.id)
        if data.PlatformId:
            query = query.filter(platform_id=data.PlatformId)
        if data.PNumberId:
            query = query.filter(PNumber_id=data.PNumberId)
        if data.PhoneId:
            query = query.filter(Phone_id=data.PhoneId)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Accounts = await query.offset(offset).limit(data.pageSize)
        Account_iteams = [
        Item(
            id=Account.id,
            AccountTeamId=Account.AccountTeam_id,
            AccountTeam=Account.AccountTeam.number if Account.AccountTeam else None,
            PlatformId=Account. platform_id,
            Platform=Account.platform.name if Account.platform else None,
            name=Account.name,
            number=Account.number,
            password=Account.password,
            profile=Account.profile,
            PNumberId=Account. PNumber_id,
            PNumber=Account.PNumber.number if Account.PNumber else None,
            CertifierId=Account.Certifier_id,
            Certifier=Account.Certifier.name if Account.Certifier else None,
            status=Account.status,
            note=Account.note,
            updatedTime=str(Account.updatedTime),
            createdTime=str(Account.createdTime),
            ) for Account in Accounts]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[], 
            pages=pages,
            records=Account_iteams,
            searchCount=True,
            size=data.pageSize,
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)

@Account_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAccount(request: Request):
    fields = ('AccountTeamId', 'PlatformId', 'PNumberId', 'CertifierId')
    return await SaveUpdate(request,Account,Item,fields)

@Account_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Account, {"id": id}, "删除成功")
