from fastapi import APIRouter,Query,Request, HTTPException, Header, Response  
from pydantic import BaseModel
from typing import Optional
from typing import List,Union
from .models import *
from .auth import *
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
# 响应模型
class ResponseModel(BaseModel):
    code: str
    mesg: str
    time: str
    data: List[MenuItem]
@menus_api.get("/getAll",summary='查找所有内容',description='功能描述')
async def getAll():
    menus =await Menu.all()
    print(menus[0])
    menu_items = [
        MenuItem(
            id=menu.id,
            name=menu.name,
            description=menu.description,
            href=menu.href if menu.href else "",
            icon=menu.icon if menu.icon else "",
            level=menu.level,
            orderNum=menu.orderNum,
            show=menu.show,  # 修正字段名
            parentId=menu.Parent_id if menu.Parent_id else None,
            createdBy=(await User.get(id=menu.createdBy_id)).name,  # 获取用户名而非ID
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
    name: str
    description: str="菜单描述"
    href: str=None
    icon: str=None
    level: int
    orderNum: int=0#"排序"
    Parent: Optional[int] = None#父级菜单
    show: bool=True
    createdBy: str="cui"


@menus_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def add(menu_in: Menuin):
    try:
        createdBy = await User.get(name=menu_in.createdBy)
        try:
            parent = await Menu.get(id=menu_in.Parent)
        except:
            parent = None
        menu = await Menu.create(
            name=menu_in.name, 
            description=menu_in.description,
            href=menu_in.href, 
            icon=menu_in.icon, 
            level=menu_in.level, 
            orderNum=menu_in.orderNum, 
            Parent_id= parent.id if parent else None, 
            show=menu_in.show,
            createdBy_id=createdBy.id)
        return menu
    except :
        return{"message": "链接已存在"}