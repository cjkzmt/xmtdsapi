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
    Random: Optional[bool] = False

class Item(BaseModel):
    id: Optional[int] = None
    urlId: Optional[int] = None
    url: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    isDel : Optional[bool] = False

class QueryResult(Result):
    records: List[Item]

@Ollama_api.get("/getAllUrl", summary='分页查询用户数据', description='功能描述')
async def getAllUrl(request: Request):
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

@Ollama_api.post("/getOllamaPages", summary='分页查询用户数据', description='功能描述')
async def get_Ollama_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = OllamaModel.filter(OllamaUrl__isDel=False).prefetch_related("OllamaUrl")
        if data.model:
            query = query.filter(model=data.model)
        query = condition(data,query)
        total = await query.count()
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
                urlId=Ollama.OllamaUrl_id,
                url=Ollama.OllamaUrl.url if Ollama.OllamaUrl else None, 
                model=Ollama.model,
                status=Ollama.status,
                isDel=Ollama.OllamaUrl.isDel
            ) for Ollama in Ollamas]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[],  # 可根据需求添加排序逻辑
            pages=pages,
            records=iteams_info,
            searchCount=True,
            size=data.pageSize,
            total=total        )
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result    )




@Ollama_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addOllama(request: Request):
    async with in_transaction():
        Ollama_in = await parse_request_body(request, Item)
        print(Ollama_in)
        if Ollama_in.id:
            iteam = await OllamaModel.get(id=Ollama_in.id)
            if Ollama_in.status:
                iteam.status = Ollama_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)

@Ollama_api.delete("/{id}", summary='删除指定内容', description='功能描述')
async def delete_iteam(id: int):
    return await delete(OllamaModel, {"id": id}, "模型删除成功")

