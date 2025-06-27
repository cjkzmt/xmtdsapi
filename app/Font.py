from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
from tortoise.transactions import in_transaction#async with in_transaction():
import tortoise.exceptions

Font_api = APIRouter()

class Fontin(BaseModel):
    id: Optional[int] = None
    name:Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    update: Optional[str] = None

@Font_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(Font_in: Fontin):
    if Font_in.id is None:
        try:
            Fonting = await TopicCopy.get(name=Font_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"文案已存在,{Font_in.name}"
        )
        except:
            pass

        Fonting = await Font.create(name=Font_in.name,url=Font_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=Fonting.name
    )
    Fonting = await Font.get(id=Font_in.id)
    if Font_in.url is not None:
        Fonting.url=Font_in.url
    if Font_in.status is not None:
        Fonting.status=Font_in.status
    await Fonting.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=Fonting.name
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await Font.filter(**filters).values() 

@Font_api.get("/", summary='查询 Font', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(Font_in: Fontin = Depends()):
    filters = {k: v for k, v in Font_in.model_dump().items() if v is not None}
    result = await safe_query(filters)
    return ResponseModel(
        code="000000",
        mesg="查询 Font 成功",
        time=str(datetime.now()),
        data=result
        )


