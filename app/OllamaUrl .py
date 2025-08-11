from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .crawl_ollama_servers import crawl_ollama_servers
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
import random
from datetime import datetime
from tortoise.transactions import in_transaction#async with in_transaction():
Ollama_api = APIRouter()

class Item(BaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    status: Optional[str] = None
    isDel : Optional[bool] = False

@Ollama_api.get("/getAll", summary='分页查询用户数据', description='功能描述')
async def getAll(info: Item = Depends()):
    return await GetAll(TypeSubtitle,Item,info)

@Ollama_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,AccountTeam,Item)

@Ollama_api.delete("/{id}", summary='删除指定内容', description='功能描述')
async def delete_iteam(id: int):
    return await delete(OllamaUrl, {"id": id}, "删除成功")

