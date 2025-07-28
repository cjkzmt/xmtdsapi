from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
from datetime import datetime
import tortoise.exceptions
from tortoise.transactions import in_transaction
Certifier_api = APIRouter()

class QueryCondition(Condition):
    name: Optional[str] = None
    idnumber: Optional[int] = None

class TopCertifier(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Item(BaseModel):
    idnumber: Optional[int] = None
    Owner:Optional[str] = None
    createdTime: Optional[str] = None
    status: Optional[str] = None

class QueryResult(Result):
    records: List[Item] 

@Certifier_api.post("/getCertifierPages", summary='分页查询用户数据', description='功能描述')
async def get_Certifier_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Certifier.filter()
        query = condition(data,query)
        if data.CertifierName:
            query = query.filter(name=data.CertifierName)
        if data.idnumber:
            query = query.filter(idnumber__icontains=data.idnumber)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Certifiers = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=Certifier.id,
            name=Certifier.name,
            Model=Certifier.idnumber,
            Owner=Certifier.Owner,
            createdTime=str(Certifier.createdTime),
            status=Certifier.status
            ) for Certifier in Certifiers]
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
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)



@Certifier_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addCertifier(request: Request):
    async with in_transaction():
        Certifier_in = await parse_request_body(request, Item)
        print(Certifier_in)
        if Certifier_in.id:
            iteam = await Certifier.get(id=Certifier_in.id)
            if Certifier_in.name:
                iteam.name = Certifier_in.name
            if Certifier_in.idnumber:
                iteam.idnumber = Certifier_in.idnumber
            if Certifier_in.Owner:
                iteam.Owner = Certifier_in.Owner
            if Certifier_in.status:
                iteam.status = Certifier_in.status
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await Certifier.create(
            name=Certifier_in.name, 
            idnumber=Certifier_in.idnumber, 
            Owner=Certifier_in.Owner)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@Certifier_api.get("/TopCertifiers", summary='查找所有内容', description='功能描述')
async def getAllTopCertifiers():
    async with in_transaction():
        Certifiers = await Certifier.all().values('id', 'name')
        iteams_info = [
            TopCertifier(
                id=Certifier['id'],
                name=Certifier['name']
            ) for Certifier in Certifiers]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info)

@Certifier_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Certifier, {"id": id}, "删除成功")