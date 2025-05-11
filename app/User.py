from fastapi import APIRouter
from pydantic import BaseModel
from typing import List,Union
from .models import *
User_api = APIRouter()
@User_api.get("/",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def getallUser():
    users=await User.all()
    return users

class Userin(BaseModel):
    name: str
    password:str='123456'
    number:int
    status : str="Active"

@User_api.post("/", summary='添加一个内容', description='功能描述')
async def add(user_in: Userin):
    user = await User.create(name=user_in.name, password=user_in.password, number=user_in.number, status=user_in.status)
    return user_in
@User_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getOneUser(id:int):
    return {"Hello xmtds"}
@User_api.put("/{id}",summary='更新指定内容',description='功能描述')
async def updateUser(id:int):
    return {"Hello xmtds"}
@User_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteUser(id:int):
    return {"Hello xmtds"}