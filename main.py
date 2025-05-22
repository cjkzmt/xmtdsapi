from fastapi import FastAPI,Response,APIRouter,Query,Request, HTTPException, Header, Response  
from tortoise.contrib.fastapi import register_tortoise
from fastapi.responses import JSONResponse 
from settings import TORTOISE_ORM
from app.UrlVDKey import UrlVDKey_api
from app.UrlVD import UrlVD_api
from app.User import User_api
from app.menus import menus_api
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.auth import *
load_dotenv() 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境请按需配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def set_content_type_header(request, call_next):
    response = await call_next(request)
    if isinstance(response, Response) and "content-type" not in response.headers:
        response.headers["content-type"] = "application/json"
    return response


# @app.middleware("http")
# async def verify_token_and_get_user(request: Request, call_next):
#     try:
#         # 修改main.py中的中间件验证条件
#         if (request.url.path.startswith("/api/") 
#             and not request.url.path.startswith("/cs/")  # 新增cs路径排除
#             and request.url.path not in ["/api/user/login", "/api/user/refresh_token"]):
#             authorization = request.headers.get("Authorization")
#             if not authorization:
#                 raise HTTPException(
#                     status_code=401,
#                     detail={
#                         "success": False,
#                         "message": "未提供 Authorization",
#                         "state": 401,
#                         "content": None
#                     }
#                 )
#             user_info = get_user_token(authorization)
#             if not user_info:
#                 raise HTTPException(
#                     status_code=401,
#                     detail={
#                         "success": False,
#                         "message": "无效的 Token",
#                         "state": 401,
#                         "content": None
#                     }
#                 )
#             request.state.user_id = user_info.get("user_id")
#         return await call_next(request)
#     except HTTPException as he:
#         return he
#     except ValueError as ve:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "success": False,
#                 "message": str(ve),
#                 "state": 401,
#                 "content": None
#             }
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "success": False,
#                 "message": "服务器内部错误",
#                 "state": 500,
#                 "content": None
#             }
#         )

@app.middleware("http")
async def verify_token_and_get_user(request: Request, call_next):
    # 排除不需要验证 Token 的路径
    if not request.url.path.startswith("/api/") or request.url.path in ["/api/user/login", "/api/user/refresh_token"]:
        return await call_next(request)
    # 需要验证 Token 的路径
    try:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "message": "未提供 Authorization",
                    "state": 401,
                    "content": None
                }
            )
        
        user_info = get_user_token(authorization)
        if not user_info:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "message": "无效的 Token",
                    "state": 401,
                    "content": None
                }
            )
        
        request.state.user_id = user_info.get("user_id")
    except HTTPException as he:
        # 重新抛出 HTTPException，而不是直接返回
        raise he
    except ValueError as ve:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": str(ve),
                "state": 401,
                "content": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "服务器内部错误",
                "state": 500,
                "content": None
            }
        )
    
    return await call_next(request)



register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)
@app.get("/api",tags=['项目介绍'])
async def home():
    return {"Hello xmtds"}
app.include_router(User_api,prefix="/api/user",tags=['操作用户'])
app.include_router(UrlVDKey_api,prefix="/api/UrlVDKey",tags=['视频采集链接'])
app.include_router(UrlVD_api,prefix="/api/UrlVD",tags=['视频下载链接'])
app.include_router(menus_api,prefix="/api/menu",tags=['web菜单'])
app.include_router(menus_api,prefix="/cs/menu",tags=['web菜单'])
if __name__ == "__main__":
    pass
    import uvicorn
    uvicorn.run("main:app", port=8080, log_level="debug", reload=True, workers=1)# host="0.0.0.0",
'''
cd be       
aerich init -t settings.TORTOISE_ORM
aerich init-db
aerich migrate 
aerich upgrade
'''

