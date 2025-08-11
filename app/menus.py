from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
from tortoise.transactions import in_transaction

menus_api = APIRouter()

class MenuItem(BaseModel):
    id: int
    name: str
    description: str
    href: Optional[str] = None
    icon: Optional[str] = None
    level: int
    orderNum: int
    show: bool
    parent_id: Optional[int] = None
    createdBy: str
    createdTime: str
    operator_id: Optional[int] = None
    updatedBy: Optional[str] = None
    updatedTime: Optional[str] = None
# class Item(InItem):
#     createdTime: Optional[str] = None
@menus_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    async with in_transaction():
        menus =await Menu.all()
        menu_items = [
            MenuItem(
                id=menu.id,
                name=menu.name,
                description=menu.description,
                href=menu.href if menu.href else "",
                icon=menu.icon if menu.icon else "",
                level=menu.level,
                orderNum=menu.orderNum,
                show=menu.show,
                parent_id=menu.parent_id if menu.parent_id else None,
                createdBy=(await User.get(id=menu.createdBy_id)).name, 
                createdTime=str(menu.createdTime),
                operator_id=menu.operator_id if menu.operator else None,
                updatedBy=(await User.get(id=menu.operator_id)).name if menu.operator else None,
                updatedTime=str(menu.updatedTime),
            ) for menu in menus
        ]
        return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=menu_items
        )

class Menuin(BaseModel):
    id: Optional[int] = None
    name: str
    href: Optional[str] = ""
    parent_id: Optional[int] = None  # 更符合实际含义的字段名
    description: str = "菜单描述"
    icon: Optional[str] = ""
    show: bool = True
    orderNum: int = 0
    level: Optional[int] = None  # 可选，也可以根据 parent_id 自动计算

@menus_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addMenu(request: Request):
    async with in_transaction():
        try:
            body = await request.json()
            menu_in = Menuin(**body)  # 自动校验和映射字段
        except Exception as e:
            return ResponseModel(code="000001", mesg="参数错误", time=str(datetime.now()), data=False)
        try:
            if menu_in.id is not None:
                menu = await Menu.get(id=menu_in.id)
                menu.name = menu_in.name
                menu.href = menu_in.href
                menu.parent_id = None if menu_in.parent_id == -1 else menu_in.parent_id
                menu.description = menu_in.description
                menu.icon = menu_in.icon
                menu.show = menu_in.show
                menu.orderNum = menu_in.orderNum
                menu.level = 0 if menu_in.parent_id == -1 else 1
                menu.operator_id = int(request.state.user_info.get("user_id"))
                menu.updatedTime = datetime.now()
                await menu.save()
                return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
            else:
                await Menu.create(
                    name=menu_in.name, 
                    href=menu_in.href, 
                    parent_id=None if menu_in.parent_id == -1 else menu_in.parent_id, 
                    description=menu_in.description,
                    icon=menu_in.icon, 
                    show=menu_in.show,
                    orderNum=menu_in.orderNum, 
                    level=0 if menu_in.parent_id == -1 else 1, 
                    createdBy_id=request.state.user_info.get("user_id"))
                return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
        except Exception as e:
            print(f"数据库操作失败: {e}")
            return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
        


@menus_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getMenu(id:int):
    async with in_transaction():
        print(id)
        try:
            menu = await Menu.get(id=id)
            menu_item = MenuItem(
                id=menu.id,
                name=menu.name,
                description=menu.description,
                href=menu.href if menu.href else "",
                icon=menu.icon if menu.icon else "",
                level=menu.level,
                orderNum=menu.orderNum,
                show=menu.show,
                parent_id=menu.parent_id if menu.parent_id else None,
                createdBy=(await User.get(id=menu.createdBy_id)).name,
                createdTime=str(menu.createdTime),
                operator_id=menu.operator_id if menu.operator_id else None,
                updatedBy=(await User.get(id=menu.operator_id)).name if menu.operator_id else None,
                updatedTime=str(menu.updatedTime),
            )
            return  ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=menu_item)
        except  Exception as e:
            print(f"数据库操作失败: {e}")
            return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)


@menus_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteMenu(id:int):
    return await delete(Menu, {"id": id}, "删除成功")