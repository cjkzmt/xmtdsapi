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

AiApi_api = APIRouter()#平台

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    port: Optional[int] = None
    model: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = None
    createdTime: Optional[str] = None

@AiApi_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    return await GetAll(AiApi,Item)


@AiApi_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addAiApi(request: Request):
    async with in_transaction():
        info = await parse_request_body(request, Item)
        print(info)
        exclude_fields = ('port')
        data = {k: v for k, v in info.dict(exclude_none=True, exclude={'id', 'createdTime'}).items() 
                    if not (k in exclude_fields and v < 0)}
        if info.id:
            iteam = await AiApi.get(id=info.id)
            for field, value in data.items():
                setattr(iteam, field, value)
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        data.pop('status', None)
        await AiApi.create(**data)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@AiApi_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteAiApi(id:int):
    async with in_transaction():
        try:
            iteam = await AiApi.get(id=id)
        except  Exception as e:
            print(str(e))
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await iteam.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            print(str(e))
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
        