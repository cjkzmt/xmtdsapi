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

TypeText_api = APIRouter()

class TypeTextItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    topicSW: Optional[str] = None
    copySW: Optional[str] = None
    status: Optional[str] = None
    createdTime: Optional[str] = None

@TypeText_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        TypeTexts =await TypeText.all()
        TypeText_items = [
            TypeTextItem(
                id=TypeText.id,
                name=TypeText.name,
                description=TypeText.description,
                topicSW=TypeText.topicSW,
                copySW=TypeText.copySW,
                status=TypeText.status,
                createdTime=str(TypeText.createdTime)
            ) for TypeText in TypeTexts
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=TypeText_items
        )

@TypeText_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTypeText(request: Request):
    async with in_transaction():
        TypeText_in = await parse_request_body(request, TypeTextItem)
        print(TypeText_in)
        if TypeText_in.id:
            TypeTexting = await TypeText.get(id=TypeText_in.id)
            if TypeText_in.name:
                TypeTexting.name = TypeText_in.name
            if TypeText_in.description:
                TypeTexting.description = TypeText_in.description
            if TypeText_in.topicSW:
                TypeTexting.topicSW = TypeText_in.topicSW
            if TypeText_in.copySW:
                TypeTexting.copySW = TypeText_in.copySW
            if TypeText_in.status:
                TypeTexting.status = TypeText_in.status
            await TypeTexting.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await TypeText.create(
            name=TypeText_in.name,
            description=TypeText_in.description
            )
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@TypeText_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteTypeText(id:int):
    async with in_transaction():
        try:
            TypeText = await TypeText.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await TypeText.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
        