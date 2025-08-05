from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from tortoise.expressions import Case, When,Q
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
from tortoise.transactions import in_transaction
from datetime import datetime
Data_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class InItem(BaseModel):
    id : Optional[int] = None
    Script_id : Optional[int] = None
    Account_id : Optional[int] = None
    status : Optional[str] = None
    title: Optional[str] = None
    publishtime : Optional[str] = None
    views: Optional[int] = None
    completion: Optional[int] = None
    comment: Optional[int] = None
    like: Optional[int] = None
    fav: Optional[int] = None
    followers: Optional[int] = None
    share: Optional[int] = None
    watch: Optional[int] = None

class Item(InItem):
    Account: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Data_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Data.filter().prefetch_related( 'Script',Prefetch("Account", queryset=Account.all().prefetch_related("AccountTeam", "Platform")),)
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize

        annotated_query = query.annotate(
            publishtime_isnull=Case(
                When(Script__publishtime__isnull=True, then=1),
                default=0
            )
        ).order_by("publishtime_isnull", "Script__publishtime", "Script__AccountTeam_id")
        iteams = await annotated_query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            Script_id=iteam.Script_id,
            Account_id=iteam.Account_id,
            Account=f'{iteam.Account.Platform.name}{iteam.Account.AccountTeam.number}',
            status=iteam.status,
            title=iteam.title,
            publishtime=iteam.publishtime,
            views=iteam.views,
            completion=iteam.completion,
            comment=iteam.comment,
            like=iteam.like,
            fav=iteam.fav,
            followers=iteam.followers,
            share=iteam.share,
            watch=iteam.watch,
            ) for iteam in iteams
        ]
        return queryResult(data,QueryResult,iteams_info,total)
    
@Data_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Data,InItem)

@Data_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Data, {"id": id}, "删除成功")