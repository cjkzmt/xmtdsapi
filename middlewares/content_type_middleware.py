from fastapi.responses import JSONResponse
from starlette.responses import Response
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Union

class ContentTypeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            
            # 确保响应对象有headers属性
            if not hasattr(response, "headers"):
                return response
                
            # 为所有JSON响应设置Content-Type
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type.lower():
                if isinstance(response, JSONResponse):
                    response.headers["content-type"] = "application/json"
                elif hasattr(response, "body") and isinstance(response.body, (str, bytes)):
                    try:
                        # 检查body是否是JSON
                        import json
                        json.loads(response.body)
                        response.headers["content-type"] = "application/json"
                    except (json.JSONDecodeError, TypeError):
                        pass
            
            return response
            
        except Exception as e:
            # 记录错误但不要中断请求
            # 在实际应用中应该使用日志记录器
            print(f"ContentTypeMiddleware error: {str(e)}")
            return await call_next(request)