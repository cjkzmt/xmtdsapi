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
Phone_api = APIRouter()

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 30#// 每页显示的记录数
    PhoneName: Optional[str] = None
    Brand: Optional[str] = None
    PhoneId: Optional[int] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间

class PhoneItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    Model: Optional[str] = None
    Brand: Optional[str] = None
    Owner: Optional[str] = None
    sort: Optional[int] = None
    createdTime: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    status: Optional[str] = None
    deviceid: Optional[str] = None
class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[PhoneItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数
from datetime import datetime


@Phone_api.post("/getPhonePages", summary='分页查询用户数据', description='功能描述')
async def get_Phone_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
        query = Phone.filter()
    # 替换原有赋值逻辑
        if data.statCreateTime and data.endCreateTime:
            try:
                start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
                end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
                query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
            except ValueError:
                return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)

        if data.PhoneName:
            #打印的值 是(None,) 要求提前处理  data 里的数据 打印  None
            query = query.filter(name=data.PhoneName)
        if data.Brand:
            query = query.filter(Brand=data.Brand)
        if data.PhoneId:
            query = query.filter(id=data.PhoneId)
        total = await query.count()
        offset = (data.currentPage - 1) * data.pageSize
        Phones = await query.offset(offset).limit(data.pageSize)
        Phone_items = [
        PhoneItem(
            id=Phone.id,
            name=Phone.name,
            Model=Phone.Model,
            Brand=Phone.Brand,
            Owner=Phone.Owner,
            sort=Phone.sort,
            createdTime=str(Phone.createdTime),
            status=Phone.status,
            deviceid=Phone.deviceid,
            ) for Phone in Phones
        ]
        # print(Phone_items[0].createdTime)
        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        # 创建分页结果
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[],  # 可根据需求添加排序逻辑
            pages=pages,
            records=Phone_items,
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


@Phone_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deletePhone(id:int):
    async with in_transaction():
        try:
            Phoneing = await Phone.get(id=id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        try:
            await Phoneing.delete()
            return ResponseModel(code="000000", mesg="删除成功", time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
@Phone_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addPhone(request: Request):
    async with in_transaction():
        Phone_in = await parse_request_body(request, PhoneItem)
        print(Phone_in)
        if Phone_in.id:
            Phoneing = await Phone.get(id=Phone_in.id)
            if Phone_in.name:
                Phoneing.name = Phone_in.name
            if Phone_in.Model:
                Phoneing.Model = Phone_in.Model
            if Phone_in.Brand:
                Phoneing.Brand = Phone_in.Brand
            if Phone_in.Owner:
                Phoneing.Owner = Phone_in.Owner
            if Phone_in.sort is not None:
                Phoneing.sort = Phone_in.sort
            if Phone_in.status:
                Phoneing.status = Phone_in.status
            if Phone_in.deviceid:
                Phoneing.deviceid = Phone_in.deviceid
            await Phoneing.save()
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
        Phone_items = [
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
            data=Phone_items
        )
    

class VerifyPhone(BaseModel):
    id: Optional[int] = None
    deviceid: Optional[str] = None

@Phone_api.post("/Verify", summary='查找所有内容', description='功能描述')
async def VerifyPhones(Phone_in: VerifyPhone):
    async with in_transaction():
        print(Phone_in )
        try:
            Phoneing = await Phone.get(id=Phone_in.id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        if Phoneing.deviceid is None:
            Phoneing.deviceid = Phone_in.deviceid
            await Phoneing.save()            
        elif Phoneing.deviceid != Phone_in.deviceid:            
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
            data=create_user_token(data={"user_id":int(Phone_in.id) })
            )