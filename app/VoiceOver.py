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

VoiceOver_api = APIRouter()

class VoiceOverin(BaseModel):
    id: Optional[int] = None
    name:Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    update: Optional[str] = None

@VoiceOver_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(VoiceOver_in: VoiceOverin):
    if VoiceOver_in.id is None:
        try:
            VoiceOvering = await TopicCopy.get(name=VoiceOver_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"文案已存在,{VoiceOver_in.name}"
        )
        except:
            pass
        VoiceOvering = await VoiceOver.create(name=VoiceOver_in.name,url=VoiceOver_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=VoiceOvering.name
    )
    VoiceOvering = await VoiceOver.get(id=VoiceOver_in.id)
    if VoiceOver_in.url is not None:
        VoiceOvering.url=VoiceOver_in.url
    if VoiceOver_in.status is not None:
        VoiceOvering.status=VoiceOver_in.status
    await VoiceOvering.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=VoiceOvering.name
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await VoiceOver.filter(**filters).values() 

@VoiceOver_api.get("/", summary='查询 VoiceOver', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(VoiceOver_in: VoiceOverin = Depends()):
    filters = {k: v for k, v in VoiceOver_in.model_dump().items() if v is not None}
    result = await safe_query(filters)
    return  ResponseModel(
    code="000000",
    mesg="查询 VoiceOver 成功",
    time=str(datetime.now()),
    data=result
    )





