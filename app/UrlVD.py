from fastapi import APIRouter
from pydantic import BaseModel
from typing import List,Union
from .models import *
UrlVD_api = APIRouter()
@UrlVD_api.get("/",summary='查找所有内容',description='功能描述')#deprecated=True#废弃的接口
async def getallUrlVD():
    Urls=await UrlVD.all()
    return Urls
class UrlVDin(BaseModel):
    url : str
    name : str#视频标题
    Author: str#作者"): str#作者")
    views: str#浏览量")
    duration: str#时长")
    uploaddate: str#上传时间")
    status: str="待下载"
    UrlVDKey: str=None

@UrlVD_api.post("/", summary='添加一个内容', description='功能描述')
async def addUrlVD(UrlVDin_in: UrlVDin):
    try:
        urlvdkey = await UrlVD.get(url=UrlVDin_in.url)
        return {"message": "链接已存在"}
    except :
        pass
    platform, created = await Platform.get_or_create(name="youtube")
    author, created = await Author.get_or_create(name=UrlVDin_in.Author,Platform_id=platform.id)
    try:
        if UrlVDKey:
            urlvdkey = await UrlVDKey.get(key=UrlVDin_in.UrlVDKey)
    except :
        urlvdkey = None
    try:
        urls = await UrlVD.create(
            url=UrlVDin_in.url,
            name=UrlVDin_in.name,
            Author_id= author.id ,
            views=UrlVDin_in.views,
            duration=UrlVDin_in.duration,
            uploaddate=UrlVDin_in.uploaddate,
            status=UrlVDin_in.status,
            UrlVDKey_id= urlvdkey.id if urlvdkey else None
        )
        return {"message": "添加成功", "data": urls}
    except Exception as e:
        # 如果创建失败，返回错误信息
        return {"message": f"{UrlVDin_in.url}添加失败", "error": str(e)}
@UrlVD_api.get("/{id}",summary='查找指定内容',description='功能描述')
async def getOneUrlVD(id:int):
    return {"Hello xmtds"}
@UrlVD_api.put("/{id}",summary='更新指定内容',description='功能描述')
async def updateUrlVD(id:int):
    return {"Hello xmtds"}
@UrlVD_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def deleteUrlVD(id:int):
    return {"Hello xmtds"}