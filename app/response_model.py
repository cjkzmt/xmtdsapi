from pydantic import BaseModel
from typing import TypeVar, Generic
from fastapi import HTTPException, Request
from typing import List,Optional, Type
from pydantic import ValidationError
from datetime import datetime
from tortoise.transactions import in_transaction
from .auth import *
import re
from fastapi import Depends

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: str
    mesg: str
    time: str
    data: T

class Result(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数
    
class Condition(BaseModel):
    currentPage: Optional[int] = 1
    pageSize: Optional[int] = 30
    id: Optional[int] = None
    statCreateTime: Optional[str] = None
    endCreateTime: Optional[str] = None
    status: Optional[str] = None

class VerifyItem(BaseModel):
    id: Optional[int] = None
    Verification: Optional[str] = None

async def parse_request_body(request: Request, model_class: type):
    try:
        body = await request.json()
        return model_class(**body)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"请求体解析失败: {str(e)}")
def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))
def condition(data,query):
    if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
    if data.statCreateTime and data.endCreateTime:
        try:
            start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
            query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
        except ValueError:
            return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
    if data.status:
        query = query.filter(status=data.status)
    if data.id:
        query = query.filter(id=data.id)
    return query
async def delete(model, filter_kwargs: dict, success_msg: str = "删除成功"):
    async with in_transaction():
        try:
            item = await model.get(**filter_kwargs)
        except Exception as e:
            return ResponseModel(code="000001", mesg=f"查询失败: {str(e)}", time=str(datetime.now()), data=False)
        try:
            await item.delete()
            return ResponseModel(code="000000", mesg=success_msg, time=str(datetime.now()), data=True)
        except Exception as e:
            return ResponseModel(code="000002", mesg=f"删除失败: {str(e)}", time=str(datetime.now()), data=False)

async def GetAll(
    model,                       # Tortoise-ORM 模型类
    model_class: Type[BaseModel],  # Pydantic 模型类
    filters_in: Optional[BaseModel] = None,  # 过滤条件模型（可缺省）
    fields: Optional[List[str]] = None       # 仅返回字段（可缺省）
):
    async with in_transaction():
        filters = {k: v for k, v in filters_in.model_dump().items() if v is not None} if filters_in else {}
        if fields:
            items = await model.filter(**filters).values(*fields)
            data = [model_class(**{f: item.get(f) for f in fields})
                for item in items]
        else:
            items = await model.filter(**filters)
            processed_items = []
            for item in items:
                item_dict = item.__dict__.copy()
                if 'createdTime' in item_dict and item_dict['createdTime']:
                    if isinstance(item_dict['createdTime'], datetime):
                        item_dict['createdTime'] = item_dict['createdTime'].isoformat()
                processed_items.append(model_class(**item_dict))
            data = processed_items
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=data)
async def SaveUpdate(request,model,Item: type,fields=()):
    async with in_transaction():
        info = await parse_request_body(request, Item)
        print(info)
        data = {k: v for k, v in info.dict(exclude_none=True, exclude={'id'}).items() if not (k in fields and v < 1)}
        if info.id:
            iteam = await model.get(id=info.id)
            for field, value in data.items():
                setattr(iteam, field, value)
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        data.pop('status', None)
        await model.create(**data)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    
def queryResult(data,model_class: Type[BaseModel],iteams_info,total):
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    query_result = model_class(
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

async def save_list(request: Request,model,ItemList:type,fields,name) -> ResponseModel:
    body = await parse_request_body(request, ItemList)
    print(body)
    total = len(body.itemList)
    success = 0
    async with in_transaction():
        for item in body.itemList:
            try:
                data = {field: getattr(item, field) for field in fields}
                await model.create(**data)
                success += 1
            except Exception:
                pass
    return ResponseModel(
        code="000000",
        mesg=f"共 {total} 个{name}，成功 {success} 个，失败 {total - success} 个",
        time=str(datetime.now()),
        data=True)

async def Verify(info,model,Role):
    async with in_transaction():
        print(info )
        try:
            iteam = await model.get(id=info.id)
        except  Exception as e:
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
        if iteam.Verification is None:
            iteam.Verification = info.Verification
            await iteam.save()            
        elif iteam.Verification != info.Verification:            
            return ResponseModel(
                code="00001",
                mesg="匹配失败",
                time=str(datetime.now()),
                data=False)
        return ResponseModel(
            code="000000",
            mesg="匹配成功",
            time=str(datetime.now()),
            data=create_user_token(data={"user_id":int(info.id) ,'Role':Role}))