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

AiApi_api = APIRouter()

class InItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    port: Optional[int] = None
    model: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = None

class Item(InItem):
    createdTime: Optional[str] = None

@AiApi_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    return await GetAll(AiApi,Item)

@AiApi_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    fields = ('port')
    return await SaveUpdate(request,AiApi,InItem,fields)

@AiApi_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(AiApi, {"id": id}, "删除成功")