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

ReleasePlan_api = APIRouter()

class ReleasePlanItem(BaseModel):
    id: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
@ReleasePlan_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        ReleasePlans =await ReleasePlan.all()
        ReleasePlan_items = [
            ReleasePlanItem(
                id=ReleasePlan.id,
                hour=ReleasePlan.hour,
                minute=ReleasePlan.minute
            ) for ReleasePlan in ReleasePlans
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=ReleasePlan_items
        )

@ReleasePlan_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addReleasePlan(request: Request):
    async with in_transaction():
        ReleasePlan_in = await parse_request_body(request, ReleasePlanItem)
        print(ReleasePlan_in)
        if ReleasePlan_in.id:
            ReleasePlaning = await ReleasePlan.get(id=ReleasePlan_in.id)
            if ReleasePlan_in.hour  is not None:
                ReleasePlaning.hour = ReleasePlan_in.hour
            if ReleasePlan_in.minute  is not None:
                ReleasePlaning.minute = ReleasePlan_in.minute
            await ReleasePlaning.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await ReleasePlan.create(
            hour=ReleasePlan_in.hour)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@ReleasePlan_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteReleasePlan(id:int):
    async with in_transaction():
        try:
            ReleasePlan = await ReleasePlan.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await ReleasePlan.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
    