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

UrlText_api = APIRouter()

class UrlTextin(BaseModel):
    id: Optional[int] = None
    url:Optional[str] = None
    Author_id: Optional[int] = None
    update: Optional[str] = None
    status: Optional[str] = None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await UrlText.filter(**filters).all().limit(10)

@UrlText_api.get("/", summary='查询 UrlText', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(UrlText_in: UrlTextin = Depends()):
    try:
        filters = {k: v for k, v in UrlText_in.model_dump().items() if v is not None}
        result = await safe_query(filters)
        return result
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=503, detail="数据库连接异常，请稍后重试") from e
@UrlText_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(UrlText_in: UrlTextin):
    if UrlText_in.id is None:
        try:
            await Author.get(url=UrlText_in.url)  
            return 'url已存在'
        except Exception as e:
            pass
        new_url_author = await UrlText.create(
            url=UrlText_in.url,
            Author_id=UrlText_in.Author_id,
            )
        return new_url_author
    UrlTexting = await UrlText.get(id=UrlText_in.id)
    if UrlText_in.Author_id is not None:
        UrlTexting.Author_id=UrlText_in.Author_id
    if UrlText_in.update is not None:
        UrlTexting.status=UrlText_in.update
    if UrlText_in.status is not None:
        UrlTexting.status=UrlText_in.status
    await UrlTexting.save()
    return UrlTexting.id