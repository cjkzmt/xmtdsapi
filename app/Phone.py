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
from tortoise.transactions import in_transaction#async with in_transaction():
from datetime import datetime
Phone_api = APIRouter()

class QueryCondition(Condition):
    PhoneName: Optional[str] = None
    Brand: Optional[str] = None

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    Model: Optional[str] = None
    Brand: Optional[str] = None
    Owner: Optional[str] = None
    sort: Optional[int] = None
    createdTime: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    status: Optional[str] = None
    deviceid: Optional[str] = None

class QueryResult(Result):
    records: List[Item]



@Phone_api.post("/getPhonePages", summary='分页查询用户数据', description='功能描述')
async def get_Phone_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        query = Phone.filter()
        query = condition(data,query)
        if data.PhoneName:
            query = query.filter(name=data.PhoneName)
        if data.Brand:
            query = query.filter(Brand=data.Brand)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        iteams = await query.offset(offset).limit(data.pageSize)
        iteams_info = [
        Item(
            id=iteam.id,
            name=iteam.name,
            Model=iteam.Model,
            Brand=iteam.Brand,
            Owner=iteam.Owner,
            sort=iteam.sort,
            createdTime=str(iteam.createdTime),
            status=iteam.status,
            deviceid=iteam.deviceid,
            ) for iteam in iteams
        ]
        # print(iteams_info[0].createdTime)
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        # 创建分页结果
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[],  # 可根据需求添加排序逻辑
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

@Phone_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPhone(request: Request):
    async with in_transaction():
        Phone_in = await parse_request_body(request, Item)
        print(Phone_in)
        if Phone_in.id:
            iteam = await Phone.get(id=Phone_in.id)
            if Phone_in.name:
                iteam.name = Phone_in.name
            if Phone_in.Model:
                iteam.Model = Phone_in.Model
            if Phone_in.Brand:
                iteam.Brand = Phone_in.Brand
            if Phone_in.Owner:
                iteam.Owner = Phone_in.Owner
            if Phone_in.sort is not None:
                iteam.sort = Phone_in.sort
            if Phone_in.status:
                iteam.status = Phone_in.status
            if Phone_in.deviceid:
                iteam.deviceid = Phone_in.deviceid
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await Phone.create(
            name=Phone_in.name, 
            Model=Phone_in.Model, 
            Brand=Phone_in.Brand,
            sort=Phone_in.sort,
            Owner=Phone_in.Owner)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)


class TopPhone(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None

@Phone_api.get("/TopPhones", summary='查找所有内容', description='功能描述')
async def getAllTopPhones():
    async with in_transaction():
        
        Phones = await Phone.all().values('id', 'name','sort')
        iteams_info = [
            TopPhone(
                id=phone['id'],
                name=phone['name'],
                sort=phone['sort']
            ) for phone in Phones
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=iteams_info
        )
    

class VerifyPhone(BaseModel):
    id: Optional[int] = None
    deviceid: Optional[str] = None

@Phone_api.post("/Verify", summary='查找所有内容', description='功能描述')
async def VerifyPhones(Phone_in: VerifyPhone):
    async with in_transaction():
        print(Phone_in )
        try:
            iteam = await Phone.get(id=Phone_in.id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        if iteam.deviceid is None:
            iteam.deviceid = Phone_in.deviceid
            await iteam.save()            
        elif iteam.deviceid != Phone_in.deviceid:            
            return ResponseModel(
                code="00001",
                mesg="匹配失败",
                time=str(datetime.now()),
                data=False
            )
        return ResponseModel(
            code="000000",
            mesg="匹配成功",
            time=str(datetime.now()),
            data=create_user_token(data={"user_id":int(Phone_in.id) ,'Role':'Phone'})
            )

@Phone_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Phone, {"id": id}, "删除成功")