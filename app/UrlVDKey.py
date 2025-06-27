from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions

UrlVDKey_api = APIRouter()
@UrlVDKey_api.get("/",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def getallUrlVDKey():
    Urls=await UrlVDKey.all()
    return Urls
#url= ('https://www.youtube.com/watch?v=ZzClIviqsas&pp=ygUGY3lwcnVz0gcJCU8JAYcqIYzv', 'Cyprus 2024 ', 'Mark C ', '78次', '13天前', '4分钟58秒钟', '4', None)

class UrlVDKeyin(BaseModel):
    url : str
    key : str
    update : str
    status : str
    User_Agent : str="root"
@UrlVDKey_api.post("/",summary='添加一个内容',description='功能描述')
async def addUrlVDKey (UrlVDKeyin_in: UrlVDKeyin):
    Urls=await UrlVDKey.create
    return Urls
@UrlVDKey_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getOneUrlVDKey(id:int):
    return {"Hello xmtds"}
@UrlVDKey_api.put("/{id}",summary='更新指定内容',description='功能描述')
async def updateUrlVDKey(id:int):
    return {"Hello xmtds"}
@UrlVDKey_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteUrlVDKey(id:int):
    return {"Hello xmtds"}