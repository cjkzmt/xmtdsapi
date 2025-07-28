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

TypeVideo_api = APIRouter()#平台

class TypeVideoItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    videoheight: Optional[int] = None
    videowidth: Optional[int] = None

@TypeVideo_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        TypeVideos =await TypeVideo.all()
        TypeVideo_items = [
            TypeVideoItem(
                id=TypeVideo.id,
                name=TypeVideo.name,
                videoheight=TypeVideo.videoheight,
                videowidth=TypeVideo.videowidth,
            ) for TypeVideo in TypeVideos]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=TypeVideo_items)

@TypeVideo_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addTypeVideo(request: Request):
    async with in_transaction():
        TypeVideo_in = await parse_request_body(request, TypeVideoItem)
        print(TypeVideo_in)
        if TypeVideo_in.id:
            TypeVideoing = await TypeVideo.get(id=TypeVideo_in.id)
            if TypeVideo_in.name:
                TypeVideoing.name = TypeVideo_in.name
            if TypeVideo_in.videoheight and TypeVideo_in.videoheight > 0:
                TypeVideoing.videoheight = TypeVideo_in.videoheight
            if TypeVideo_in.videowidth and TypeVideo_in.videowidth > 0:
                TypeVideoing.videowidth = TypeVideo_in.videowidth
            await TypeVideoing.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await TypeVideo.create(
            name=TypeVideo_in.name,
            videoheight=TypeVideo_in.videoheight if TypeVideo_in.videoheight and TypeVideo_in.videoheight > 0 else 1280,
            videowidth=TypeVideo_in.videowidth if TypeVideo_in.videowidth and TypeVideo_in.videowidth > 0 else 720)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
@TypeVideo_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteTypeVideo(id:int):
    async with in_transaction():
        try:
            TypeVideoing = await TypeVideo.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await TypeVideoing.delete()
            return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)