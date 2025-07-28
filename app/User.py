from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional, List, Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions
from .response_model import *
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from tortoise.transactions import in_transaction

User_api = APIRouter()
portraiturl= 'https://p9-flow-imagex-sign.byteimg.com/ocean-cloud-tos/image_skill/d43d8b27-7ab6-4e25-872c-81a99596cdea_1747727922613428843_origin~tplv-a9rns2rl98-image-dark-watermark.png?rk3s=b14c611d&x-expires=1779263922&x-signature=2ZAZigEWOL4lPbeA7WhpbDHbou0%3D'
        
class Userin(BaseModel):
    number:Optional[int] = None
    id: Optional[int] = None
    isDel: Optional[bool] = False
    name: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    portrait: Optional[str] = None
    regIp: Optional[str] = None
    status: Optional[str] = "ENABLE"
    updatedTime: Optional[str] = None

@User_api.get("/getUserInfo", summary='获取用户信息', description='功能描述')
async def get_user_info(request: Request):
    async with in_transaction():
        user_id = request.state.user_info.get("user_id")
        user = await User.get(id=user_id)
        if not user:
            raise HTTPException(
            status_code=404,
            detail={
                'success': False,
                'message': '用户不存在',
                'state': 404,
                'content': None})
        return {
        'success': True,
        'message': '成功收到请求',
        'state': 200,
        'content': {
            'userName': user.name,
            'isUpdatePassword': user.password == '123456',  # 可简化条件判断
            'portrait': user.portrait or portraiturl}}

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
                'content': None})

class LogoutResponse(BaseModel):
    success: bool
    state: int
    message: str
    content: str
@User_api.post("/logout", description="用户退出")
async def logout(authorization: str = Header(...)):
    if not authorization: raise HTTPException(status_code=401, detail="未提供授权信息")
    return LogoutResponse(
        success=True,
        state=0,  # 假设0表示成功
        message="用户成功退出",
        content="用户成功退出")
class uselogin(BaseModel):
    name : str
    password : str
@User_api.post("/login",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def Userlogin(user_in:uselogin):
    async with in_transaction():
        try:
            user = await User.get(name=user_in.name,password=user_in.password)
            return {'success': True,
                    "message": "登录成功",
                    "state": 200,
                    "content": create_user_token(data={"user_id":int(user.id),'Role':'user' }),}
        except :
            return {'success': False,
                    "message": "用户不存在",
                    "state": 401,
                    "content":"",}

@User_api.post("/", summary='添加一个内容', description='功能描述')
async def add(user_in: Userin):
    print(user_in)
    user = await User.create(name=user_in.name, password=user_in.password, number=user_in.number, status=user_in.status)
    return user_in

class QueryCondition(BaseModel):
    currentPage: Optional[int] = 1#// 查询的当前页码
    pageSize: Optional[int] = 10#// 每页显示的记录数
    userName: Optional[str] = None
    phone: Optional[str] = None
    userId: Optional[int] = None
    statCreateTime: Optional[str] = None#// 开始创建时间，用于筛选创建时间范围的起始时间
    endCreateTime: Optional[str] = None#// 结束创建时间，用于筛选创建时间范围的结束时间
class UserItem(BaseModel):
    accountNonExpired: bool
    accountNonLocked: bool
    createdTime: Optional[str] = None  # 如 "2025-04-05T12:34:56Z"
    credentialsNonExpired: bool
    id: int
    isDel: bool
    name: str
    password: str
    phone: Optional[str] = None
    portrait: Optional[str] = None
    regIp: Optional[str] = None
    status: str
    updatedTime: Optional[str] = None
class QueryResult(BaseModel):
    current: int  # 当前页码
    hitcount: bool  # 是否命中计数
    optimizeCountSql: bool  # 是否优化计数SQL
    orders: List  # 排序条件数组
    pages: int  # 总页数
    records: List[UserItem]  # 当前页的用户记录列表
    searchCount: bool  # 是否进行搜索计数
    size: int  # 每页显示的记录数
    total: int  # 总记录数

@User_api.post("/getUserPages", summary='分页查询用户数据', description='功能描述')
async def get_user_pages(request: Request):
    async with in_transaction():
        data = await parse_request_body(request, QueryCondition)
        print(data)
        if data.currentPage <= 0 or data.pageSize <= 0:
            return ResponseModel(code="000002", mesg="分页参数无效", time=str(datetime.now()), data=False)
        query = User.filter(isDel=False)
        if data.statCreateTime and data.endCreateTime:
            try:
                start_time = datetime.fromisoformat(data.statCreateTime.replace("Z", "+00:00"))
                end_time = datetime.fromisoformat(data.endCreateTime.replace("Z", "+00:00"))
                query = query.filter(createdTime__gt=start_time, createdTime__lt=end_time)
            except ValueError:
                return ResponseModel(code="000003", mesg="时间格式无效", time=str(datetime.now()), data=False)
        if data.userName:
            query = query.filter(name=data.userName)
        if data.phone:
            query = query.filter(phone__icontains=data.phone)
        if data.userId:
            query = query.filter(id=data.userId)
        total = await query.count()
        users = await query.offset((0) * 1).limit(10)
        user_items = [
            UserItem(
                accountNonExpired=False if user.status == 'DISABLE' else True,
                accountNonLocked=True,
                createdTime=str(user.createdTime),
                credentialsNonExpired=True,
                id=user.id,
                isDel=user.isDel,
                name=user.name,
                password=user.password,
                phone=user.phone,
                portrait=user.portrait or portraiturl,
                regIp=user.regIp,
                status=user.status,
                updatedTime=user.modified_at.isoformat() if hasattr(user, 'modified_at') and user.modified_at else None,
                ) for user in users]

        pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
        query_result = QueryResult(
            current=data.currentPage,
            hitcount=True,
            optimizeCountSql=False,
            orders=[],
            pages=pages,
            records=user_items,
            searchCount=True,
            size=data.pageSize,
            total=total)
        return ResponseModel(
            code="000000",
            mesg="操作成功",
            time=str(datetime.now()),
            data=query_result)

@User_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(request: Request):
    async with in_transaction():
        User_in=await parse_request_body(request, Userin)
        if User_in.id:
            Usering = await User.get(id=User_in.id)
            if User_in.status is not None:
                Usering.status=User_in.status
            await Usering.save()
            return ResponseModel[bool](
                code="000000",
                mesg="修改成功",
                time=str(datetime.now()),
                data=True)
        try:
            Usering = await TopicCopy.get(
                number=User_in.number
                )
            return ResponseModel[bool](
            code="000001",
            mesg=f"添加失败文案已存在,{User_in.name}",
            time=str(datetime.now()),
            data=False )
        except:
            pass
        Usering = await User.create(name=User_in.name,url=User_in.url)
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=True)


