from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch

PromptText_api = APIRouter()

class PromptTextin(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    status : Optional[str] = None

@PromptText_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(PromptText_in: PromptTextin):
    if PromptText_in.id is None:
        try:
            PromptTexting = await TopicCopy.get(text=PromptText_in.text)
            return ResponseModel[str](
            code="000001",
            mesg="添加PromptText失败",
            time=str(datetime.now()),
            data=f"文案已存在,{PromptText_in.id}"
        )
        except:
            pass
        PromptTexting = await PromptText.create(text=PromptText_in.text)
        return ResponseModel[str](
        code="000000",
        mesg="创建PromptText成功",
        time=str(datetime.now()),
        data=PromptTexting.id
    )
    PromptTexting = await PromptText.get(id=PromptText_in.id)
    if PromptText_in.text is not None:
        PromptTexting.text=PromptText_in.text
    if PromptText_in.status is not None:
        PromptTexting.status=PromptText_in.status
    await PromptTexting.save()
    return ResponseModel[int](
        code="000000",
        mesg="修改PromptText成功",
        time=str(datetime.now()),
        data=PromptTexting.id
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await PromptText.filter(**filters).values() 

@PromptText_api.get("/", summary='查询 PromptText', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(PromptText_in: PromptTextin = Depends()):
    filters = {k: v for k, v in PromptText_in.model_dump().items() if v is not None}
    result = await safe_query(filters)
    return ResponseModel(
        code="000000",
        mesg="获取 PromptText 成功",
        time=str(datetime.now()),
        data=result
    )
