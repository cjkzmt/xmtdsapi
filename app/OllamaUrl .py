from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .crawl_ollama_servers import crawl_ollama_servers
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
import random
from datetime import datetime
from tortoise.transactions import in_transaction#async with in_transaction():
Ollama_api = APIRouter()

class OllamaUrlItem(BaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    status: Optional[str] = None
    isDel : Optional[bool] = False

@Ollama_api.get("/getAllUrl", summary='分页查询用户数据', description='功能描述')
async def getAllUrl():
    Ollamas = await OllamaUrl.filter(isDel=False, status="DISABLE").all()
    iteams_info = [
            OllamaUrlItem(
                id=Ollama.id,
                url=Ollama.url,
                status=Ollama.status,
            ) for Ollama in Ollamas]
    return ResponseModel(
        code="000000",
        mesg="获取成功",
        time=str(datetime.now()),
        data=iteams_info)


@Ollama_api.post("/UpdateUrl", summary='添加一个内容', description='功能描述')
async def UpdateUrl(request: Request):
    async with in_transaction():
        Ollama_in = await parse_request_body(request, OllamaUrlItem)
        print(Ollama_in)
        iteam = await OllamaUrl.get(id=Ollama_in.id)
        if  Ollama_in.status:
            iteam.status = Ollama_in.status
        if Ollama_in.isDel is not None:
            iteam.isDel = Ollama_in.isDel
        await iteam.save()
        return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)

@Ollama_api.delete("/{id}", summary='删除指定内容', description='功能描述')
async def delete_iteam(id: int):
    return await delete(OllamaUrl, {"id": id}, "音乐删除成功")

