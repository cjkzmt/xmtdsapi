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
from collections import Counter
import tortoise.exceptions
from tortoise.transactions import in_transaction

AccountTeam_api = APIRouter()

class QueryCondition(Condition):
    number: Optional[int] = None

class TopItem(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

class InItem(TopItem):
    Computer_id: Optional[int] = None
    TeamOwner_id: Optional[int] = None
    Phone_id: Optional[int] = None    
    status: Optional[str] = None
    TypeVideo_id: Optional[int] = None
    TypeCover_id: Optional[int] = None
    TypeSubtitle_id: Optional[int] = None
    
    
class Item(InItem):
    AccountSum: Optional[int] = None
    Computer: Optional[str] = None
    TypeVideo: Optional[str] = None
    shorthand: Optional[str] = None
    Phone: Optional[str] = None
    TypeCover: Optional[str] = None
    TypeSubtitle: Optional[str] = None
    createdTime: Optional[str] = None 
    videoheight: Optional[int] = None
    videowidth: Optional[int] = None    
    fixedtitle: Optional[str] = None    
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 
@AccountTeam_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = AccountTeam.filter().prefetch_related('Phone','TypeVideo','TypeCover','TypeSubtitle','TeamOwner','Computer')
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        rows = await Account.filter(
            AccountTeam_id__in=[s.id for s in iteams],
            name__isnull=False,
            status='ENABLE'
        ).values('AccountTeam_id')
        data_map = Counter(r['AccountTeam_id'] for r in rows)
        iteams_info = [
        Item(
            id=iteam.id,
            AccountSum=data_map[iteam.id],
            number=iteam.number,
            TeamOwner_id=iteam.TeamOwner_id,
            shorthand=iteam.TeamOwner.shorthand if iteam.TeamOwner else None,
            Computer_id=iteam.Computer_id,
            Computer=iteam.Computer.name if iteam.Computer else None,
            Phone_id=iteam.Phone_id,
            Phone=iteam.Phone.name if iteam.Phone else None,
            createdTime=str(iteam.createdTime),
            TypeCover_id=iteam.TypeCover_id,
            TypeCover=iteam.TypeCover.name if iteam.TypeCover else None,
            fixedtitle=iteam.TypeCover.fixedtitle if iteam.TypeSubtitle else None,
            TypeSubtitle_id=iteam.TypeSubtitle_id,
            TypeSubtitle=iteam.TypeSubtitle.name if iteam.TypeSubtitle else None,
            fontsize=iteam.TypeSubtitle.fontsize if iteam.TypeSubtitle else None,
            fontcolor=iteam.TypeSubtitle.fontcolor if iteam.TypeSubtitle else None,            
            TypeVideo_id=iteam.TypeVideo_id,
            TypeVideo=iteam.TypeVideo.name if iteam.TypeVideo else None,
            videoheight=iteam.TypeVideo.videoheight if iteam.TypeCover else None,
            videowidth=iteam.TypeVideo.videowidth if iteam.TypeCover else None,
            status=iteam.status
            ) for iteam in iteams]
        return queryResult(data,QueryResult,iteams_info,total)

@AccountTeam_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('Phone_id', 'TypeCover_id', 'TypeSubtitle_id', 'TypeVideo_id','TeamOwner_id','Computer_id')
    return await SaveUpdate(request,AccountTeam,InItem,fields)

@AccountTeam_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def TopIteams():
    return await GetAll(AccountTeam,TopItem,fields = ('id', 'number'))

@AccountTeam_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(AccountTeam, {"id": id}, "删除成功")