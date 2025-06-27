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

UrlAuthor_api = APIRouter()

class UrlAuthorin(BaseModel):
    id: Optional[int] = None
    url:Optional[str] = None
    Authorname: Optional[str] = None
    Authornum: Optional[str] = None
    update: Optional[str] = None
    status: Optional[str] = None
@UrlAuthor_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(UrlAuthor_in: UrlAuthorin):
    if UrlAuthor_in.id is None:
        new_url_author = await UrlAuthor.create(url=UrlAuthor_in.url)
        return new_url_author
    UrlAuthoring = await UrlAuthor.get(id=UrlAuthor_in.id)
    if UrlAuthor_in.Authorname is not None:
        if "douyin" in UrlAuthor_in.url:
            platform, created = await Platform.get_or_create(name="抖音")
            author, created = await Author.get_or_create(name=UrlAuthor_in.Authorname,Platform_id=platform.id,number=UrlAuthor_in.Authornum)
            UrlAuthoring.Author_id=author.id
    if UrlAuthor_in.update is not None:
        UrlAuthoring.status=UrlAuthor_in.update
    if UrlAuthor_in.status is not None:
        UrlAuthoring.status=UrlAuthor_in.status
    await UrlAuthoring.save()
    return UrlAuthoring
@UrlAuthor_api.get("/", summary='查询 UrlAuthor', description='根据 id, url, Author, update, status 等条件查询')
async def query_url_author(
    id: Optional[int] = None,
    url: Optional[str] = None,
    Author: Optional[int] = None,
    update: Optional[str] = None,
    status: Optional[str] = None
):
    # filters = {}
    # if id is not None:
    #     filters["id"] = id
    # if url is not None:
    #     filters["url__icontains"] = url
    # if Author is not None:
    #     filters["Author_id"] = Author
    # if update is not None:
    #     filters["update"] = update
    # if status is not None:
    #     filters["status"] = status
    filters = {k: v for k, v in locals().items() if v is not None}
    result = await UrlAuthor.filter(**filters).all()
    return result