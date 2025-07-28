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

class TypeSubtitleItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None

@TypeSubtitle_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll(TypeSubtitle_in: TypeSubtitleItem = Depends()):
    async with in_transaction():
        filters = {k: v for k, v in TypeSubtitle_in.model_dump().items() if v is not None}
        TypeSubtitles =await TypeSubtitle.filter(**filters).values() 
        TypeSubtitle_items = [
            TypeSubtitleItem(
                id=subtitle['id'],
                fontsize=subtitle['fontsize'],
                name=subtitle['name'],
                fontcolor=subtitle['fontcolor']
            ) for subtitle in TypeSubtitles]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=TypeSubtitle_items)

@TypeSubtitle_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTypeSubtitle(request: Request):
    async with in_transaction():
        TypeSubtitle_in = await parse_request_body(request, TypeSubtitleItem)
        print(TypeSubtitle_in)
        if TypeSubtitle_in.id:
            TypeSubtitleing = await TypeSubtitle.get(id=TypeSubtitle_in.id)
            if TypeSubtitle_in.fontsize:
                TypeSubtitleing.fontsize = TypeSubtitle_in.fontsize
            if TypeSubtitle_in.name:
                TypeSubtitleing.name = TypeSubtitle_in.name
            if TypeSubtitle_in.fontcolor:
                TypeSubtitleing.fontcolor = TypeSubtitle_in.fontcolor
            await TypeSubtitleing.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await TypeSubtitle.create(
            name=TypeSubtitle_in.name,
            fontsize=TypeSubtitle_in.fontsize,
            fontcolor=TypeSubtitle_in.fontcolor,
            )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    
@TypeSubtitle_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteTypeSubtitle(id:int):
    async with in_transaction():
        try:
            TypeSubtitleing = await TypeSubtitle.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await TypeSubtitleing.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)