from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions

TextTemplate_api = APIRouter()
class TextTemplatein(BaseModel):
    id: Optional[int] = None
    number: str
    text: str
    PromptText_id: Optional[int] = None
    Topic_id: Optional[int] = None
    Copy_id: Optional[int] = None
    status: str = "Active"
@TextTemplate_api.get("/getAllWithTotal")
async def getAllWithTotal(page: int = 1, page_size: int = 200):
    offset = (page - 1) * page_size
    query = TextTemplate.all().offset(offset).limit(page_size)
    TextTemplates = await query
    total = await TextTemplate.all().count()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": TextTemplates,
    }
@TextTemplate_api.post("/", summary='添加一个内容', description='功能描述')
async def add(TextTemplate_in: TextTemplatein):
    # print("Received data:", TextTemplate_in)  # 添加调试信息
    txt = TextTemplate_in.text
    nub = TextTemplate_in.number
    try:
        texttemplate = await TextTemplate.get(text=txt)
        return f" 文案已存在,{nub}"
    except:
        pass
    try:
        texttemplate = await TextTemplate.get(number=nub)
        return f" 编号------已存在,{nub}"
    except:
        pass

    texttemplate = await TextTemplate.create(
        number=nub, 
        text=txt,
        PromptText_id=TextTemplate_in.PromptText_id if TextTemplate_in.PromptText_id else None,
        Topic_id=TextTemplate_in.Topic_id if TextTemplate_in.Topic_id else None,
        Copy_id=TextTemplate_in.Copy_id if TextTemplate_in.Copy_id else None,
        status=TextTemplate_in.status
        )
    return texttemplate.number
