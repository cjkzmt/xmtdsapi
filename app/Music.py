from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
from tortoise.transactions import in_transaction
from datetime import datetime
Music_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None

class TopMusic(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Item(TopMusic):
    duration: Optional[int] = None
    url: Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item]

@Music_api.post("/getMusicPages", summary='分页查询用户数据', description='功能描述')
async def get_Music_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Music.filter()
        query = condition(data,query)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            name=iteam.name,
            duration=iteam.duration,
            url=iteam.url,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            ) for iteam in iteams
        ]
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[],
            pages=pages,
            records=iteams_info,
            searchCount=True,
            size=data.pageSize,
            total=total
        )
        
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result
    )

@Music_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addMusic(request: Request):
    async with in_transaction():
        Music_in = await parse_request_body(request, Item)
        print(Music_in)
        if Music_in.id:
            iteam = await Music.get(id=Music_in.id)
            if Music_in.name:
                iteam.name = Music_in.name
            if Music_in.duration and Music_in.duration>0:
                iteam.duration = Music_in.duration
            if Music_in.url:
                iteam.url = Music_in.url
            if Music_in.status:
                iteam.status = Music_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        try:
            await TopicCopy.get(name=Music_in.name)
            return ResponseModel[str](
            code="000001",
            mesg="添加失败",
            time=str(datetime.now()),
            data=f"已存在,{Music_in.name}")
        except:pass
        await Music.create(name=Music_in.name)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@Music_api.get("/TopMusics", summary='查找所有内容', description='功能描述')
async def getAllTopMusics():
    async with in_transaction():
        Musics = await Music.all().values('id', 'name')
        iteams_info = [
            TopMusic(
                id=Music['id'],
                name=Music['name']
            ) for Music in Musics
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info
        )
class MusicList(BaseModel):
    MusicList: List[Item]
@Music_api.post("/saveList", summary='添加一个内容', description='功能描述')
async def saveList(request: Request):
    async with in_transaction():
        Musics = await parse_request_body(request, MusicList)
        sum=len(Musics.MusicList)
        Success=Failure=0
        for Music_in in Musics.MusicList:
            try:
                await Music.create(name=Music_in.name,duration=Music_in.duration)
                Success+=1
            except:
                Failure+=1
    return ResponseModel(code="000000", mesg=f"一共{sum}个音乐，添加成功{Success}，失败{Failure}", time=str(datetime.now()), data=True)

@Music_api.delete("/{id}", summary='删除指定内容', description='功能描述')
async def delete_music(id: int):
    return await delete(Music, {"id": id}, "音乐删除成功")