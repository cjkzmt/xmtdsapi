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

TypeCover_api = APIRouter()#平台

class TypeCoverItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    fixedtitle: Optional[str] = None
@TypeCover_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        TypeCovers =await TypeCover.all()
        TypeCover_items = [
            TypeCoverItem(
                id=TypeCover.id,
                name=TypeCover.name,
                fixedtitle=TypeCover.fixedtitle,
            ) for TypeCover in TypeCovers]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=TypeCover_items)

@TypeCover_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTypeCover(request: Request):
    async with in_transaction():
        TypeCover_in = await parse_request_body(request, TypeCoverItem)
        print(TypeCover_in)
        if TypeCover_in.id:
            TypeCovering = await TypeCover.get(id=TypeCover_in.id)
            if TypeCover_in.name:
                TypeCovering.name = TypeCover_in.name
            if TypeCover_in.fixedtitle :
                TypeCovering.fixedtitle = TypeCover_in.fixedtitle

            await TypeCovering.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await TypeCover.create(
            name=TypeCover_in.name,
            fixedtitle=TypeCover_in.fixedtitle)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@TypeCover_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteTypeCover(id:int):
    async with in_transaction():
        try:
            TypeCovering = await TypeCover.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await TypeCovering.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)