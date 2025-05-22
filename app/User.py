from fastapi import APIRouter,Query,Request, HTTPException, Header, Response  
from pydantic import BaseModel
from typing import List,Union
from .models import *
from .auth import *
User_api = APIRouter()


@User_api.get("/getUserInfo", summary='获取用户信息', description='功能描述')
async def get_user_info(request: Request):
    user_id = request.state.user_id 
    user = await User.get(id=user_id)
    if not user:
        raise HTTPException(
        status_code=404,
        detail={
            'success': False,
            'message': '用户不存在',
            'state': 404,
            'content': None
        }
    )
    return {
    'success': True,
    'message': '成功收到请求',
    'state': 200,
    'content': {
        'userName': user.name,
        'isUpdatePassword': user.password == '123456',  # 可简化条件判断
        'portrait': user.portrait or 'https://p9-flow-imagex-sign.byteimg.com/ocean-cloud-tos/image_skill/d43d8b27-7ab6-4e25-872c-81a99596cdea_1747727922613428843_origin~tplv-a9rns2rl98-image-dark-watermark.png?rk3s=b14c611d&x-expires=1779263922&x-signature=2ZAZigEWOL4lPbeA7WhpbDHbou0%3D'
        }
    }

@User_api.post("/refresh_token", summary='获取新的token', description='功能描述')
async def refresh_token(refreshtoken: str = Query(...)):
    try:
        new_token = get_new_access_token(refreshtoken)
        return {
            'success': True,
            'message': '成功收到请求',
            'state': 200,
            'content': new_token
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=401,
            detail={
                'success': False,
                'message': str(ve),
                'state': 401,
                'content': None
            }
        )


class LogoutResponse(BaseModel):
    success: bool
    state: int
    message: str
    content: str
@User_api.post("/logout", description="用户退出")
async def logout(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供授权信息")
    
    # 假设验证通过，执行用户退出逻辑
    # 这里可以添加实际的用户退出逻辑，例如清除会话或令牌等
    
    # 返回退出成功的响应
    return LogoutResponse(
        success=True,
        state=0,  # 假设0表示成功
        message="用户成功退出",
        content="用户成功退出"
    )

class uselogin(BaseModel):
    name : str
    password : str

@User_api.post("/login",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def Userlogin(user_in:uselogin):
    try:
        user = await User.get(name=user_in.name,password=user_in.password)
        return {
                'success': True,
                "message": "登录成功",
                "state": 200,
                "content": create_user_token(data={"user_id":int(user.id) }),
                }
    except :
         return {
                'success': False,
                "message": "用户不存在",
                "state": 401,
                "content":"",
                }

@User_api.get("/",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def getallUser():
    users=await User.all()
    return users

class Userin(BaseModel):
    name: str
    password:str='123456'
    number:int
    portrait:str=""
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