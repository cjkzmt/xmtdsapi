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

ResourceCategory_api = APIRouter()

class ResourceCategoryItem(BaseModel):
    id: Optional[int] = None
    name: str
    selected: Optional[bool] = True 
    sort: int
    createdBy: Optional[str] = None
    createdTime: Optional[str] = None
    operator_id: Optional[int] = None
    updatedBy: Optional[str] = None
    updatedTime: Optional[str] = None

@ResourceCategory_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        resourcecategorys =await ResourceCategory.all()
        ResourceCategory_items = [
            ResourceCategoryItem(
                id=ResourceCategory.id,
                name=ResourceCategory.name,
                selected=ResourceCategory.selected, 
                sort=ResourceCategory.sort,
                createdBy=(await User.get(id=ResourceCategory.createdBy_id)).name,  # 获取用户名而非ID
                createdTime=str(ResourceCategory.createdTime),
                operator_id=ResourceCategory.operator_id if ResourceCategory.operator else None,
                updatedBy=(await User.get(id=ResourceCategory.operator_id)).name if ResourceCategory.operator else None,
                updatedTime=str(ResourceCategory.updatedTime),
            ) for ResourceCategory in resourcecategorys
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=ResourceCategory_items
        )

@ResourceCategory_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addResourceCategory(request: Request):
    async with in_transaction():
        try:
            body = await request.json()
            ResourceCategory_in = ResourceCategoryItem(**body)  # 自动校验和映射字段
        except Exception as e:
            return ResponseModel(code="000001", mesg="参数错误", time=str(datetime.now()), data=False)
        if ResourceCategory_in.id:
            
            ResourceCategorying = await ResourceCategory.get(id=ResourceCategory_in.id)
            ResourceCategorying.name = ResourceCategory_in.name
            ResourceCategorying.selected = ResourceCategory_in.selected
            ResourceCategorying.sort = ResourceCategory_in.sort
            ResourceCategorying.operator_id = int(request.state.user_info.get("user_id"))
            ResourceCategorying.updatedTime = datetime.now()
            await ResourceCategorying.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await ResourceCategory.create(
            name=ResourceCategory_in.name, 
            selected=ResourceCategory_in.selected, 
            sort=ResourceCategory_in.sort,
            createdBy_id=request.state.user_info.get("user_id"))
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@ResourceCategory_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getResourceCategory(id:int):
    async with in_transaction():
        print(id)
        try:
            ResourceCategory = await ResourceCategory.get(id=id)
            ResourceCategory_item = ResourceCategoryItem(
                id=ResourceCategory.id,
                name=ResourceCategory.name,
                description=ResourceCategory.description,
                href=ResourceCategory.href if ResourceCategory.href else "",
                icon=ResourceCategory.icon if ResourceCategory.icon else "",
                level=ResourceCategory.level,
                orderNum=ResourceCategory.orderNum,
                show=ResourceCategory.show,
                parent_id=ResourceCategory.parent_id if ResourceCategory.parent_id else None,
                createdBy=(await User.get(id=ResourceCategory.createdBy_id)).name,
                createdTime=str(ResourceCategory.createdTime),
                operator_id=ResourceCategory.operator_id if ResourceCategory.operator_id else None,
                updatedBy=(await User.get(id=ResourceCategory.operator_id)).name if ResourceCategory.operator_id else None,
                updatedTime=str(ResourceCategory.updatedTime),
            )
            return  ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=ResourceCategory_item)
        except  Exception as e:
            print(f"数据库操作失败: {e}")
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)

@ResourceCategory_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteResourceCategory(id:int):
    return await delete(ResourceCategory, {"id": id}, "删除成功")