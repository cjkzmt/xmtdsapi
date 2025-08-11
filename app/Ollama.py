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

class QueryCondition(Condition):
    model: Optional[str] = None
    Random: Optional[bool] = None

class InItem(BaseModel):
    id: Optional[int] = None
    url_id: Optional[int] = None
    model: Optional[str] = None
    status: Optional[str] = None
    
class Item(InItem):
    url: Optional[str] = None
    isDel : Optional[bool] = False

class QueryResult(Result):
    records: List[Item]

@Ollama_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = OllamaModel.filter().prefetch_related("OllamaUrl")
        if data.model:
            query = query.filter(model=data.model)
        query = query.filter(OllamaUrl__isDel=False)
        if data.status:
            query = query.filter(status=data.status)
        total = await query.count()
        print(total)
        offset = (data.currentPage - 1) * data.pageSize
        Ollamas = await query.offset(offset).limit(data.pageSize)
        if data.Random:
            Ollamas = await query.all()
            if Ollamas:
                Ollamas = [random.choice(Ollamas)]
            else:
                Ollamas = []
        iteams_info = [
        Item(
                id=Ollama.id,
                url_id=Ollama.OllamaUrl_id,
                url=Ollama.OllamaUrl.url if Ollama.OllamaUrl else None, 
                model=Ollama.model,
                status=Ollama.status,
                isDel=Ollama.OllamaUrl.isDel
            ) for Ollama in Ollamas]
        return queryResult(data,QueryResult,iteams_info,total)

@Ollama_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    return await SaveUpdate(request,OllamaModel,InItem)

@Ollama_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(OllamaModel, {"id": id}, "删除成功")