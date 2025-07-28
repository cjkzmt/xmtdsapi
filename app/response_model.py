from pydantic import BaseModel
from typing import TypeVar, Generic
from fastapi import HTTPException, Request
from typing import List,Optional
from pydantic import ValidationError
from datetime import datetime
from tortoise.transactions import in_transaction
import re

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

async def GetAll(model, model_class: type, fields=None):
    async with in_transaction():
        if fields:
            items = await model.all().values(*fields)
            data = [model_class(**{f: item[f] for f in fields}) for item in items]
        else:
            data = [model_class(**item.dict()) for item in await model.all()]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=data
        )
async def SaveUpdate(request,model,Item: type,fields):
    exclude={'id', 'createdTime'}
    for i in fields:
        exclude.add(i.replace('_id','')) 
    async with in_transaction():
        info = await parse_request_body(request, Item)
        print(info)
        data = {k: v for k, v in info.dict(exclude_none=True, exclude=exclude).items() if not (k in fields and v < 1)}
        if info.id:
            iteam = await model.get(id=info.id)
            for field, value in data.items():
                setattr(iteam, field, value)
            await iteam.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        data.pop('status', None)
        await model.create(**data)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)