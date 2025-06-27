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

Music_api = APIRouter()

class Musicin(BaseModel):
    id: Optional[int] = None
    name:Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    update: Optional[str] = None

@Music_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(Music_in: Musicin):
    if Music_in.id is None:
        try:
            Musicing = await TopicCopy.get(name=Music_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"文案已存在,{Music_in.name}"
        )
        except:
            pass
        Musicing = await Music.create(name=Music_in.name,url=Music_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=Musicing.name
    )
    Musicing = await Music.get(id=Music_in.id)
    if Music_in.url is not None:
        Musicing.url=Music_in.url
    if Music_in.status is not None:
        Musicing.status=Music_in.status
    await Musicing.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=Musicing.name
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await Music.filter(**filters).values() 

@Music_api.get("/", summary='查询 Music', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(Music_in: Musicin = Depends()):
    filters = {k: v for k, v in Music_in.model_dump().items() if v is not None}
    result = await safe_query(filters)
    return ResponseModel(
        code="000000",
        mesg="查询 Music 成功",
        time=str(datetime.now()),
        data=result
    )

@Music_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(Music_in: Musicin):
    if Music_in.id is None:
        try:
            Musicing = await TopicCopy.get(name=Music_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"文案已存在,{Music_in.name}"
        )
        except:
            pass
        Musicing = await Music.create(name=Music_in.name,url=Music_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=Musicing.name
    )
    Musicing = await Music.get(id=Music_in.id)
    if Music_in.url is not None:
        Musicing.url=Music_in.url
    if Music_in.status is not None:
        Musicing.status=Music_in.status
    await Musicing.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=Musicing.name
    )