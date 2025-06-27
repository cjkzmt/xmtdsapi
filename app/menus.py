from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions

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
    parentId: Optional[int] = None
    createdBy: str
    createdTime: str
    operatorId: Optional[int] = None
    updatedBy: Optional[str] = None
    updatedTime: Optional[str] = None
@menus_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
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
            parentId=menu.parent_id if menu.parent_id else None,
            createdBy=(await User.get(id=menu.createdBy_id)).name, 
            createdTime=str(menu.createdTime),
            operatorId=menu.operator_id if menu.operator else None,
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
    parentId: Optional[int] = None  # 更符合实际含义的字段名
    description: str = "菜单描述"
    icon: Optional[str] = ""
    show: bool = True
    orderNum: int = 0
    level: Optional[int] = None  # 可选，也可以根据 parentId 自动计算

@menus_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def addMenu(request: Request):
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
            menu.parent_id = None if menu_in.parentId == -1 else menu_in.parentId
            menu.description = menu_in.description
            menu.icon = menu_in.icon
            menu.show = menu_in.show
            menu.orderNum = menu_in.orderNum
            menu.level = 0 if menu_in.parentId == -1 else 1
            menu.operator_id = int(request.state.user_info.get("user_id"))
            menu.updatedTime = datetime.now()
            await menu.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        else:
            await Menu.create(
                name=menu_in.name, 
                href=menu_in.href, 
                parent_id=None if menu_in.parentId == -1 else menu_in.parentId, 
                description=menu_in.description,
                icon=menu_in.icon, 
                show=menu_in.show,
                orderNum=menu_in.orderNum, 
                level=0 if menu_in.parentId == -1 else 1, 
                createdBy_id=request.state.user_info.get("user_id"))
            return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)
    except Exception as e:
        print(f"数据库操作失败: {e}")
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)
    

@menus_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteMenu(id:int):
    try:
        menu = await Menu.get(id=id)
    except  Exception as e:
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    try:
        await menu.delete()
        return ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=True)
    except Exception as e:
        return ResponseModel(code="000002", mesg=str(e), time=str(datetime.now()), data=False)

@menus_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getMenu(id:int):
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
            parentId=menu.parent_id if menu.parent_id else None,
            createdBy=(await User.get(id=menu.createdBy_id)).name,
            createdTime=str(menu.createdTime),
            operatorId=menu.operator_id if menu.operator_id else None,
            updatedBy=(await User.get(id=menu.operator_id)).name if menu.operator_id else None,
            updatedTime=str(menu.updatedTime),
        )
        return  ResponseModel(code="000000", mesg="处理成功", time=str(datetime.now()), data=menu_item)
    except  Exception as e:
        print(f"数据库操作失败: {e}")
        return ResponseModel(code="000001", mesg=str(e), time=str(datetime.now()), data=False)
    