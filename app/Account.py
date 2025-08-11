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
from tortoise.expressions import Case, When,Q
from tortoise.transactions import in_transaction

NAME='账号'

Account_api = APIRouter()

class QueryCondition(Condition):
    Platform_id: Optional[int] = None
    PNumber_id: Optional[int] = None
    Phone_id: Optional[int] = 0

class InItem(BaseModel):
    id: Optional[int] = None
    AccountTeam_id: Optional[int] = None
    Platform_id: Optional[int] = None 
    name: Optional[str] = None
    number: Optional[str] = None
    isDel: Optional[bool] = None
    password: Optional[str] = None
    profile: Optional[str] = None
    PNumber_id: Optional[int] = None 
    Certifier_id: Optional[int] = None 
    status: Optional[str] = None
    note:Optional[str] = None

class Item(InItem):
    shorthand: Optional[str] = None
    AccountTeam: Optional[int] = None
    Platform: Optional[str] = None
    createdTime:Optional[str] = None
    updatedTime:Optional[str] = None
    PNumber: Optional[int] = None 
    Certifier: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 

@Account_api.post("/getPages", summary=f'分页查询{NAME}', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
        query =  Account.filter(isDel=False).prefetch_related('PNumber','Certifier','Platform',Prefetch("AccountTeam", queryset=AccountTeam.all().prefetch_related("TeamOwner")))
        if data.statCreateTime and data.endCreateTime:
            try:
                start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
                end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
                query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
            except ValueError:
                return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
        if data.id:
            query = query.filter(id=data.id)
        if data.Platform_id:
            query = query.filter(Platform_id=data.Platform_id)
        if data.PNumber_id:
            query = query.filter(PNumber_id=data.PNumber_id)
        if data.Phone_id:
            query = query.filter(Phone_id=data.Phone_id)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        query = query.order_by('AccountTeam_id')
        Accounts = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Account.id,
            AccountTeam_id=Account.AccountTeam_id,
            AccountTeam=Account.AccountTeam.number if Account.AccountTeam else None,
            Platform_id=Account. Platform_id,
            Platform=Account.Platform.name if Account.Platform else None,
            shorthand=Account.AccountTeam.TeamOwner.shorthand if Account.AccountTeam.TeamOwner else None,
            name=Account.name,
            number=Account.number,
            password=Account.password,
            profile=Account.profile,
            PNumber_id=Account. PNumber_id,
            PNumber=Account.PNumber.number if Account.PNumber else None,
            Certifier_id=Account.Certifier_id,
            Certifier=Account.Certifier.name if Account.Certifier else None,
            status=Account.status,
            note=Account.note,
            updatedTime=str(Account.updatedTime),
            createdTime=str(Account.createdTime),
            ) for Account in Accounts]
        return queryResult(data,QueryResult,iteams_info,total)

@Account_api.post("/saveOrUpdate", summary=f'添加一个{NAME}', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('AccountTeam_id', 'Platform_id', 'PNumber_id', 'Certifier_id')
    return await SaveUpdate(request,Account,InItem,fields)

@Account_api.post("/CreateIteams", summary=f'添加一个{NAME}', description='功能描述')
async def saveOrUpdate(request: Request):
    account_teams = await AccountTeam.all()
    platforms = await Platform.filter(publish='ENABLE')
    for account_team in account_teams:
        for platform in platforms:
            query = Account.filter(AccountTeam_id=account_team.id, Platform_id=platform.id)
            total = await query.count()
            if total == 0:
                await Account.create(AccountTeam_id=account_team.id, Platform_id=platform.id)
    return ResponseModel(
        code="000000",
        mesg="批量创建账号成功",
        time=str(datetime.now()),
        data=True)

@Account_api.delete("/{id}",summary=f'删除指定{NAME}',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Account, {"id": id}, f"{NAME}删除成功")
