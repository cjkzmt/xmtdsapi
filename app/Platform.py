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

Platform_api = APIRouter()

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None
    English: Optional[str] = None
    publish:Optional[str] = None
    character:Optional[int] = None
    keycount:Optional[int] = None
    verification:Optional[str] = None
    publishurl:Optional[str] = None
    Scrapeurl:Optional[str] = None
    publishverif:Optional[str] = None
    advance:Optional[int] = None

@Platform_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll(info: Item = Depends()):
    return await GetAll(Platform,Item,info)

@Platform_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,Platform,Item)

@Platform_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deletePlatform(id:int):
    return await delete(Platform, {"id": id}, "删除成功")