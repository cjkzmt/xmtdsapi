from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.auth import get_user_token  # 假设这是你的 Token 验证函数

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # print("Request Headers:", request.headers)
        # 排除不需要验证 Token 的路径
        if not request.url.path.startswith("/api/") or request.url.path in ["/api/user/login", "/api/user/refresh_token","/api/phone/Verify"]:
            return await call_next(request)
        
        # 需要验证 Token 的路径
        try:
            authorization = request.headers.get("Authorization")
            if not authorization:
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "未提供 Authorization",
                        "state": 401,
                        "content": "未提供 Authorization"
                    }
                )
            
            user_info = get_user_token(authorization)
            if not user_info:
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "无效的 Token",
                        "state": 401,
                        "content": "无效的 Token"
                    }
                )
            
            request.state.user_info = user_info
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

'''Request Headers: Headers({'host': '192.168.0.118:8180', 'user-agent': 'python-requests/2.32.3', 'accept-encoding': 'gzip, deflate', 'accept': '*/*', 'connection': 'keep-alive', 'authorization': 'access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3NTA2NTM4NDUsInRva2VuX3R5cGUiOiJCZWFyZXIiLCJleHBpcmVzX2luIjo5MDB9.G7R03_iprmcHi4OLHYQ1EjSX1rCFa04iyu_GamcPL8Y', 'content-length': '0'})'''
'''Request Headers: Headers({'host': '192.168.0.118:8180', 'connection': 'close', 'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NTA2NTM5NjIsInRva2VuX3R5cGUiOiJCZWFyZXIiLCJleHBpcmVzX2luIjo5MDB9.HMvWL4Kl9YqbS-ZSBcrCJxG0c2HlxBIZK1Rhr3Yq6ww', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36', 'accept': 'application/json, text/plain, */*', 'dnt': '1', 'referer': 'http://192.168.0.116:5173/', 'accept-encoding': 'gzip, deflate', 'accept-language': 'zh-CN,zh;q=0.9'})'''
'''Request Headers: Headers({'host': '192.168.0.118:8180', 'user-agent': 'python-requests/2.32.3', 'accept-encoding': 'gzip, deflate', 'accept': '*/*', 'connection': 'keep-alive', 'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3NTA2NTQwOTQsInRva2VuX3R5cGUiOiJCZWFyZXIiLCJleHBpcmVzX2luIjo5MDB9.zXwpn6iAJr3usxcauqMzLPaXk81ADRnU851VHpjFgZs', 'content-length': '0'})'''