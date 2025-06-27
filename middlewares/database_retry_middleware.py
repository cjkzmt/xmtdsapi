from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.exceptions import OperationalError,DBConnectionError, TransactionManagementError
import anyio

class DatabaseRetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        max_retries = 3
        retry_delay = 1
        
        retryable_errors = (
            OperationalError,
            DBConnectionError,
            TransactionManagementError,
            anyio.ClosedResourceError
        )
        
        for attempt in range(max_retries):
            try:
                response = await call_next(request)
                return response
                
            except retryable_errors as e:
                if attempt < max_retries - 1:
                    await anyio.sleep(retry_delay)
                    continue
                raise