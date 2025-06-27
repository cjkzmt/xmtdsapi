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

VideoClips_api = APIRouter()

class VideoClipsin(BaseModel):
    id: Optional[int] = None
    name:Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    update: Optional[str] = None

@VideoClips_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(VideoClips_in: VideoClipsin):
    if VideoClips_in.id is None:
        try:
            VideoClipsing = await TopicCopy.get(name=VideoClips_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"文案已存在,{VideoClips_in.name}"
        )
        except:
            pass
        VideoClipsing = await VideoClips.create(name=VideoClips_in.name,url=VideoClips_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=VideoClipsing.name
    )
    VideoClipsing = await VideoClips.get(id=VideoClips_in.id)
    if VideoClips_in.url is not None:
        VideoClipsing.url=VideoClips_in.url
    if VideoClips_in.status is not None:
        VideoClipsing.status=VideoClips_in.status
    await VideoClipsing.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=VideoClipsing.name
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await VideoClips.filter(**filters).values() 

@VideoClips_api.get("/", summary='查询 VideoClips', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(VideoClips_in: VideoClipsin = Depends()):
    filters = {k: v for k, v in VideoClips_in.model_dump().items() if v is not None}
    result = await safe_query(filters)
    return ResponseModel(
    code="000000",
    mesg="查询 VideoClips 成功",
    time=str(datetime.now()),
    data=result
    )






