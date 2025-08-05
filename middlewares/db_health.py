from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise import Tortoise
from tortoise.exceptions import OperationalError
from settings import TORTOISE_ORM

class DBHealthCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            conn = Tortoise.get_connection("default")
            await conn.execute_query("SELECT 1")
        except OperationalError:
            await Tortoise.close_connections()
            await Tortoise.init(config=TORTOISE_ORM)  # 重新初始化连接
        response = await call_next(request)
        return response