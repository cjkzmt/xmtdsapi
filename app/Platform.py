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

Platform_api = APIRouter()

class PlatformItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None
@Platform_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    Platforms =await Platform.all()
    Platform_items = [
        PlatformItem(
            id=Platform.id,
            name=Platform.name,
            sort=Platform.sort
        ) for Platform in Platforms
    ]
    return ResponseModel(
        code="000000",
        mesg="获取成功",
        time=str(datetime.now()),
        data=Platform_items
    )

@Platform_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPlatform(request: Request):
    Platform_in = await parse_request_body(request, PlatformItem)
    print(Platform_in)
    if Platform_in.id:
        Platforming = await Platform.get(id=Platform_in.id)
        if Platform_in.name:
            Platforming.name = Platform_in.name
        if Platform_in.sort is not None:
            print(Platform_in.sort)
            Platforming.sort = Platform_in.sort
        await Platforming.save()
        return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
    await Platform.create(
        name=Platform_in.name)
    return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@Platform_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deletePlatform(id:int):
    try:
        Platform = await Platform.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await Platform.delete()
        return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
    