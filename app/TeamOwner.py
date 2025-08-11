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
from collections import defaultdict
from collections import Counter
TeamOwner_api = APIRouter()

class QueryCondition(Condition):
    number: Optional[int] = None
    
class TopItem(BaseModel):
    id: Optional[int] = None
    shorthand: Optional[str] = None

class ItemB(BaseModel):
    path: Optional[str] = None
    clipSum: Optional[int] = None

class InItem(TopItem,ItemB):
    name: Optional[str] = None
    Title: Optional[str] = None
    alias: Optional[str] = None
    number: Optional[int] = None
    email: Optional[str] = None
    address: Optional[str] = None
    scope: Optional[str] = None
    note: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[str] = None

class Item(InItem):
    AccountSum: Optional[int] = None
    teamSum: Optional[int] = None
    createdTime: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 

@TeamOwner_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = TeamOwner.filter()
        query = condition(data,query)
        if data.number:
            query = query.filter(number__icontains=data.number)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize











        iteams = await query.offset(offset).limit(data.pageSize)

        rows = await AccountTeam.filter(
            TeamOwner_id__in=[s.id for s in iteams], status='ENABLE'
        ).values('TeamOwner_id')

        data_map = Counter(r['TeamOwner_id'] for r in rows)

        rowss = await Account.filter(
            AccountTeam__TeamOwner_id__in=[s.id for s in iteams],
            name__isnull=False,
            status='ENABLE'
        ).values('AccountTeam__TeamOwner_id')
        dataa_map = Counter(r['AccountTeam__TeamOwner_id'] for r in rowss)



        iteams_info = [
        Item(
            id=TeamOwner.id,
            name=TeamOwner.name,
            shorthand=TeamOwner.shorthand,
            Title=TeamOwner.Title,
            email=TeamOwner.email,
            alias=TeamOwner.alias,
            scope=TeamOwner.scope,
            number=TeamOwner.number,
            address=TeamOwner.address,
            clipSum=TeamOwner.clipSum,
            path=TeamOwner.path,
            note=TeamOwner.note,
            sort=TeamOwner.sort,
            teamSum=data_map.get(TeamOwner.id, 0),
            AccountSum=dataa_map.get(TeamOwner.id, 0),
            createdTime=str(TeamOwner.createdTime),
            status=TeamOwner.status,
            ) for TeamOwner in iteams]
        return queryResult(data,QueryResult,iteams_info,total)
@TeamOwner_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,TeamOwner,InItem)

class clipSumList(BaseModel):
    clipSumlist:List[ItemB]
@TeamOwner_api.post("/UpdateclipSum", summary='添加一个内容', description='功能描述')
async def UpdateclipSum(request: Request):
    async with in_transaction():
        info = await parse_request_body(request, clipSumList)
        print(info)
        for iteam in info.clipSumlist:
            try:
                iteaming = await TeamOwner.get(path=iteam.path)  # 修改这里
                iteaming.clipSum = iteam.clipSum
                await iteaming.save()
            except tortoise.exceptions.DoesNotExist:
                ResponseModel(code="000010", mesg="更新失败{iteam.path}未录入", time=str(datetime.now()), data=False)
        return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
    
@TeamOwner_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(TeamOwner,TopItem,fields= ('id', 'shorthand','sort'))

@TeamOwner_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteIteam(id:int):
    return await delete(TeamOwner, {"id": id}, "删除成功")
