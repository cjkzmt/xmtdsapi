from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist

TopicCopy_api = APIRouter()
class TopicCopyin(BaseModel):
    id: Optional[int] = None
    number: Optional[Union[str, int]] = None
    text: Optional[str] = None
    topicnum:Optional[int] = None
    copynum:Optional[int] = None
    TypeTextID: Optional[int] = None
    TypeText: Optional[str] = None
    Source_id: Optional[str] = None
    Source_description: Optional[str] = None
    status : Optional[str] = None

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),  # 等待1秒后重试
    retry=retry_if_exception_type(tortoise.exceptions.OperationalError)
)




async def safe_query(filters):
    return await TopicCopy.filter(**filters).all().prefetch_related("TypeText")
@TopicCopy_api.get("/", summary='查询 TopicCopy', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(TopicCopy_in: TopicCopyin = Depends()):
    
    if 'number' in TopicCopy_in.model_dump().keys()and TopicCopy_in.number == 'max':
        topiccopies = await TopicCopy.all().values('number')
        if not topiccopies:
            raise HTTPException(status_code=404, detail="没有找到相关内容")
        max_number = max(topiccopies, key=lambda x: int(x['number']))['number']
        return ResponseModel[int](
            code="000000",
            mesg="获取最大编号成功",
            time=str(datetime.now()),
            data=max_number
        )
    filters = {k: v for k, v in TopicCopy_in.model_dump().items() if v is not None}
    topiccopys = await safe_query(filters)
    topiccopy_items = []
    for topiccopy in topiccopys:
        topiccopy_items.append(
            TopicCopyin(
                id=topiccopy.id,
                number=topiccopy.number,
                text=topiccopy.text,
                topicnum= topiccopy.topicnum,
                copynum= topiccopy.copynum ,
                TypeText=getattr(topiccopy.TypeText, "name", None),
                Source_description=topiccopy.Source_description,
                Source_id=topiccopy.Source_id,
                status=topiccopy.status
            )
        )
    return ResponseModel(
            code="000000",
            mesg="获取TopicCopy 数据 成功",
            time=str(datetime.now()),
            data=topiccopy_items
        )
   
@TopicCopy_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def add(TopicCopy_in: TopicCopyin):
    # print(TopicCopy_in)
    if TopicCopy_in.id is None:
        txt=TopicCopy_in.text
        txt=txt.replace('\n', '')
        txt=txt.replace(' ', '')
        if len(txt) < 100:
            return ResponseModel[str](
            code="000001",
            mesg="添加TopicCopy 失败",
            time=str(datetime.now()),
            data="文案过短"
            )
        try:
            typetext = await TopicCopy.get(text=txt)
            return ResponseModel[str](
            code="000001",
            mesg="添加TopicCopy 失败",
            time=str(datetime.now()),
            data=f"文案已存在,{typetext.number}"
        )
        except:
            pass
        try:
            typetext = await TopicCopy.get(number=TopicCopy_in.number)
            return ResponseModel[str](
            code="000001",
            mesg="添加TopicCopy 失败",
            time=str(datetime.now()),
            data=f" 编号------已存在,{typetext.number}"
        )
        except:
            pass
        typetext = await TypeText.get(name=TopicCopy_in.TypeText)
        topiccopy = await TopicCopy.create(
            number=TopicCopy_in.number, 
            text=txt,
            TypeText_id=typetext.id,
            Source_description=TopicCopy_in.Source_description if TopicCopy_in.Source_description else None,
            Source_id=TopicCopy_in.Source_id if TopicCopy_in.Source_id else None,
            status=TopicCopy_in.status
            )
        return ResponseModel[str](
            code="000000",
            mesg="添加TopicCopy 成功",
            time=str(datetime.now()),
            data=f" 编号是{topiccopy.number}"
        )
    try:
        TopicCopying = await TopicCopy.get(id=TopicCopy_in.id)
    except DoesNotExist:
        return ResponseModel[str](
            code="000001",
            mesg="修改失败",
            time=str(datetime.now()),
            data="未找到该ID的数据"
        )
    if 'topicnum'in  TopicCopy_in:
        TopicCopying.topicnum=TopicCopy_in.topicnum
    if 'copynum'in  TopicCopy_in:
        TopicCopying.copynum=TopicCopy_in.copynum
    if 'text'in  TopicCopy_in:
        TopicCopying.text=TopicCopy_in.text
    if  'TypeText' in  TopicCopy_in:
        TypeText, created = await Music.get_or_create(name=TopicCopy_in.TypeText)
        TopicCopying.TypeText_id=TypeText.id
    
    if 'Source_description'in  TopicCopy_in:
        TopicCopying.Source_description=TopicCopy_in.Source_description
    if 'Source_id'in  TopicCopy_in:
        TopicCopying.Source_id=TopicCopy_in.Source_id
    if 'status'in  TopicCopy_in:
        TopicCopying.status=TopicCopy_in.status
    await TopicCopying.save()
    return ResponseModel[int](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=TopicCopying.id
    )

