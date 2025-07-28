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
TeamOwner_api = APIRouter()

class QueryCondition(Condition):
    number: Optional[int] = None
    
class TopTeamOwner(BaseModel):
    id: Optional[int] = None
    shorthand: Optional[str] = None

class TeamOwnerItem(TopTeamOwner):
    name: Optional[str] = None
    Title: Optional[str] = None
    alias: Optional[str] = None
    number: Optional[int] = None
    email: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None
    path: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[TeamOwnerItem] 

@TeamOwner_api.post("/getTeamOwnerPages", summary='分页查询用户数据', description='功能描述')
async def get_TeamOwner_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
        query = TeamOwner.filter()
        if data.number:
            query = query.filter(number__icontains=data.number)
        if data.statCreateTime and data.endCreateTime:
            try:
                start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
                end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
                query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
            except ValueError:
                return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
        if data.TeamOwner_id:
            query = query.filter(TeamOwner_id=data.TeamOwner_id)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        TeamOwners = await query.offset(offset).limit(data.pageSize)
        TeamOwner_items = [
        TeamOwnerItem(
            id=TeamOwner.id,
            name=TeamOwner.name,
            shorthand=TeamOwner.shorthand,
            Title=TeamOwner.Title,
            email=TeamOwner.email,
            alias=TeamOwner.alias,
            number=TeamOwner.number,
            address=TeamOwner.address,
            path=TeamOwner.path,
            note=TeamOwner.note,
            createdTime=str(TeamOwner.createdTime),
            status=TeamOwner.status,
            ) for TeamOwner in TeamOwners]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[], 
            pages=pages,
            records=TeamOwner_items,
            searchCount=True,
            size=data.pageSize,
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)
@TeamOwner_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTeamOwner(request: Request):
    async with in_transaction():
        info = await parse_request_body(request, TeamOwnerItem)
        print(info)
        data = info.dict(exclude_none=True, exclude={'id', 'createdTime'})
        if info.id:
            TeamOwnering = await TeamOwner.get(id=info.id)
            for field, value in data.items():
                setattr(TeamOwnering, field, value)
            await TeamOwnering.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        data.pop('status', None)
        await TeamOwner.create(**data)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@TeamOwner_api.get("/TopTeamOwners", summary='查找所有内容', description='功能描述')
async def getAllTopTeamOwners():
    async with in_transaction():
        TeamOwners = await TeamOwner.all().values('id', 'shorthand')
        TeamOwner_items = [
            TopTeamOwner(
                id=TeamOwner['id'],
                number=TeamOwner['shorthand'],
            ) for TeamOwner in TeamOwners]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=TeamOwner_items)

@TeamOwner_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteTeamOwner(id:int):
    async with in_transaction():
        try:
            TeamOwnering = await TeamOwner.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await TeamOwnering.delete()
            return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
