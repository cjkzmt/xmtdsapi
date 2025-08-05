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
from tortoise.transactions import in_transaction

NAME='关键词'

Keyword_api = APIRouter()

class Item(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    sort: Optional[int] = None

@Keyword_api.get("/getAll",summary=f'查找所有{NAME}',description='功能描述')
async def getAll(info: Item = Depends()):
    return await GetAll(Keyword,Item,info)

@Keyword_api.post("/saveOrUpdate", summary=f'添加一个{NAME}', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Keyword,Item)
@Keyword_api.delete("/{id}",summary=f'删除指定{NAME}',description='功能描述')
async def deleteKeyword(id:int):
    return await delete(Keyword, {"id": id}, f"{NAME}删除成功")