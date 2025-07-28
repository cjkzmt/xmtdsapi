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

AccountTeam_api = APIRouter()

class QueryCondition(Condition):
    number: Optional[int] = None

class TopTeam(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    scope: Optional[str] = None

class Item(TopTeam):
    Phone_id: Optional[int] = None
    TypeVideo_id: Optional[int] = None
    videoheight: Optional[int] = None
    videowidth: Optional[int] = None
    TypeCover_id: Optional[int] = None
    fixedtitle: Optional[str] = None
    TypeSubtitle_id: Optional[int] = None
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None
    createdTime: Optional[str] = None 
    status: Optional[str] = None
    TypeVideo: Optional[str] = None
    Phone: Optional[str] = None
    TypeCover: Optional[str] = None
    TypeSubtitle: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 
@AccountTeam_api.post("/getAccountTeamPages", summary='分页查询用户数据', description='功能描述')
async def get_AccountTeam_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = AccountTeam.filter().prefetch_related('Phone','TypeVideo','TypeCover','TypeSubtitle')
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            number=iteam.number,
            scope=iteam.scope,
            PhoneId=iteam.Phone_id,
            Phone=iteam.Phone.name if iteam.Phone else None,
            createdTime=str(iteam.createdTime),
            TypeCoverId=iteam.TypeCover_id,
            TypeCover=iteam.TypeCover.name if iteam.TypeCover else None,
            fixedtitle=iteam.TypeCover.fixedtitle if iteam.TypeSubtitle else None,
            TypeSubtitleId=iteam.TypeSubtitle_id,
            TypeSubtitle=iteam.TypeSubtitle.name if iteam.TypeSubtitle else None,
            fontsize=iteam.TypeSubtitle.fontsize if iteam.TypeSubtitle else None,
            fontcolor=iteam.TypeSubtitle.fontcolor if iteam.TypeSubtitle else None,            
            TypeVideoId=iteam.TypeVideo_id,
            TypeVideo=iteam.TypeVideo.name if iteam.TypeVideo else None,
            videoheight=iteam.TypeVideo.videoheight if iteam.TypeCover else None,
            videowidth=iteam.TypeVideo.videowidth if iteam.TypeCover else None,
            status=iteam.status
            ) for iteam in iteams]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[], 
            pages=pages,
            records=iteams_info,
            searchCount=True,
            size=data.pageSize,
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)

@AccountTeam_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAccountTeam(request: Request):
    fields = ('Phone_id', 'TypeCover_id', 'TypeSubtitle_id', 'TypeVideo_id')
    return await SaveUpdate(request,AccountTeam,Item,fields)

@AccountTeam_api.get("/TopIteams", summary='查找所有内容', description='功能描述')
async def getAllTopTeams():
    fields = ('id', 'number', 'scope')
    return await GetAll(AccountTeam,TopTeam,fields)

@AccountTeam_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(AccountTeam, {"id": id}, "删除成功")