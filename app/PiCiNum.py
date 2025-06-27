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

PiCiNum_api = APIRouter()

class PiCiNumin(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None

@PiCiNum_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(PiCiNum_in: PiCiNumin):
    try:
        if PiCiNum_in.id is None:
            PiCiNuming = await PiCiNum.create(number=PiCiNum_in.number)
            return ResponseModel[int](
            code="000000",
            mesg="创建成功",
            time=str(datetime.now()),
            data=PiCiNuming.number
        )
        PiCiNuming = await PiCiNum.get(id=PiCiNum_in.id)
        if PiCiNum_in.number is not None:
            PiCiNuming.number=PiCiNum_in.number
        await PiCiNuming.save()
        return ResponseModel[int](
            code="000000",
            mesg="修改成功",
            time=str(datetime.now()),
            data=PiCiNuming.number
        )
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=503, detail="数据库连接异常，请稍后重试") from e

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_query(filters):
    return await PiCiNum.filter(**filters).values()

@PiCiNum_api.get("/", summary='查询 PiCiNum', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(PiCiNum_in: PiCiNumin = Depends()):
    try:
        filters = {k: v for k, v in PiCiNum_in.model_dump().items() if v is not None}
        result = await safe_query(filters)
        return ResponseModel(
            code="000000",
            mesg="查询成功",
            time=str(datetime.now()),
            data=[PiCiNumin.model_validate(obj) for obj in result]
        )
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=503, detail="数据库连接异常，请稍后重试") from e
