import datetime
from pydantic import BaseModel
from typing import TypeVar, Generic
import tortoise.exceptions
from fastapi import HTTPException, Request
from typing import Type, Union
from pydantic import ValidationError

T = TypeVar('T')
class ResponseModel(BaseModel, Generic[T]):
    code: str
    mesg: str
    time: str
    data: T
async def parse_request_body(request: Request, model_class: type):
    try:
        body = await request.json()
        return model_class(**body)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"请求体解析失败: {str(e)}")