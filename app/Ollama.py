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

class OllamaModelItem(BaseModel):
    id: Optional[int] = None
    urlId: Optional[int] = None
    url: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    isDel : Optional[bool] = False


class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[OllamaModelItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数


@Ollama_api.post("/getOllamaPages", summary='分页查询用户数据', description='功能描述')
async def get_Ollama_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = OllamaModel.filter().prefetch_related("OllamaUrl")
        if data.model:
            query = query.filter(model=data.model)
        query = query.filter(OllamaUrl__isDel=False)
        if data.OllamaId:
            query = query.filter(id=data.OllamaId)
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
        Ollama_items = [
        OllamaModelItem(
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
            records=Ollama_items,
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
        Ollama_in = await parse_request_body(request, OllamaModelItem)
        print(Ollama_in)
        if Ollama_in.id:
            Ollamaing = await OllamaModel.get(id=Ollama_in.id)
            if Ollama_in.status:
                Ollamaing.status = Ollama_in.status
            await Ollamaing.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
@Ollama_api.get("/Updates", summary='添加一个内容', description='功能描述')
async def addOllama():
    try:
        Ollamalist = crawl_ollama_servers()
        for url,OllamaModels in Ollamalist:
            try:
                OllamaUrling=await OllamaUrl.get(url=url)
            except:
                OllamaUrling=await OllamaUrl.create(url=url)
            if OllamaUrling.isDel:continue
            for model in OllamaModels:
                try:
                    await OllamaModel.get(model=model,OllamaUrl_id=OllamaUrling.id)
                except:
                    await OllamaModel.create(model=model,OllamaUrl_id=OllamaUrling.id)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    except Exception as e:
        print("错误详情:", str(e))
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    
@Ollama_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(OllamaModel, {"id": id}, "删除成功")