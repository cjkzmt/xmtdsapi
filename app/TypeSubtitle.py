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

TypeSubtitle_api = APIRouter()#平台

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None

@TypeSubtitle_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll(info: Item = Depends()):
    return await GetAll(TypeSubtitle,Item,info)

@TypeSubtitle_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('fontsize')
    return await SaveUpdate(request,TypeSubtitle,Item,fields)
    
@TypeSubtitle_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteIteam(id:int):
    return await delete(TypeSubtitle, {"id": id}, "删除成功")
