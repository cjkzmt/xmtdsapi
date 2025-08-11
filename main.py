from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from app.response_model import *
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from middlewares.database_retry_middleware import DatabaseRetryMiddleware
from middlewares.content_type_middleware import ContentTypeMiddleware
from middlewares.auth_middleware import AuthMiddleware
from middlewares.db_health import DBHealthCheckMiddleware
from datetime import datetime
from app.UrlVDKey import UrlVDKey_api
from app.UrlVD import UrlVD_api
from app.User import User_api
from app.menus import menus_api
from app.TypeText import TypeText_api
from app.PromptText import PromptText_api
from app.TopicCopy import TopicCopy_api
from app.Script import Script_api
from app.UrlAuthor import UrlAuthor_api
from app.Author import Author_api
from app.AccountTeam import AccountTeam_api
from app.Font import Font_api
from app.Music import Music_api
from app.Over import Over_api
from app.VideoClips import VideoClips_api
from app.ResourceCategory import ResourceCategory_api
from app.Phone import Phone_api
from app.PNumber import PNumber_api
from app.Certifier import Certifier_api
from app.Platform import Platform_api
from app.ReleasePlan import ReleasePlan_api
from app.Account import Account_api
from app.Computer import Computer_api
from app.AiApi import AiApi_api
from app.ApiToken import ApiToken_api
from app.Ollama import Ollama_api
from app.TypeVideo import TypeVideo_api
from app.TypeCover import TypeCover_api
from app.TypeSubtitle import TypeSubtitle_api
from app.TeamOwner import TeamOwner_api
from app.Keyword import Keyword_api
from app.Data import Data_api

load_dotenv() 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境请按需配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBHealthCheckMiddleware)
app.add_middleware(DatabaseRetryMiddleware)  # 最先注册，最后执行
app.add_middleware(AuthMiddleware)          # 第二注册
app.add_middleware(ContentTypeMiddleware)   # 最后注册，最先执行

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)
@app.get("/api",tags=['项目介绍'])
async def home():
    return ResponseModel(code="000000", mesg="欢迎使用新媒体大师", time=str(datetime.now()), data="欢迎使用新媒体大师")
app.include_router(User_api,prefix="/api/user",tags=['操作用户'])
app.include_router(UrlVDKey_api,prefix="/api/UrlVDKey",tags=['视频采集链接'])
app.include_router(UrlVD_api,prefix="/api/UrlVD",tags=['视频下载链接'])
app.include_router(menus_api,prefix="/api/menu",tags=['web菜单'])
app.include_router(ResourceCategory_api,prefix="/api/resource/category",tags=['资源类别'])
app.include_router(Script_api,prefix="/api/script",tags=['脚本'])
app.include_router(Phone_api,prefix="/api/phone",tags=['手机'])
app.include_router(PNumber_api,prefix="/api/pnumber",tags=['手机号码'])
app.include_router(Certifier_api,prefix="/api/certifier",tags=['认证人'])
app.include_router(Platform_api,prefix="/api/platform",tags=['平台'])
app.include_router(ReleasePlan_api,prefix="/api/releaseplan",tags=['发布计划'])
app.include_router(Account_api,prefix="/api/account",tags=['新媒体账号'])
app.include_router(TypeText_api,prefix="/api/typetext",tags=['文案类型'])
app.include_router(TopicCopy_api,prefix="/api/topiccopy",tags=['选题文案'])
app.include_router(Author_api,prefix="/api/author",tags=['作者'])
app.include_router(AccountTeam_api,prefix="/api/accountteam",tags=['账号组'])
app.include_router(Computer_api,prefix="/api/computer",tags=['电脑'])
app.include_router(Font_api,prefix="/api/font",tags=['视频字体'])
app.include_router(Over_api,prefix="/api/over",tags=['视频配音'])
app.include_router(VideoClips_api,prefix="/api/videoclips",tags=['视频素材'])
app.include_router(Music_api,prefix="/api/music",tags=['背景音乐'])
app.include_router(PromptText_api,prefix="/api/prompttext",tags=['提示词'])
app.include_router(AiApi_api,prefix="/api/aiapi",tags=['逆向AI'])
app.include_router(ApiToken_api,prefix="/api/apitoken",tags=['逆向AI'])
app.include_router(Ollama_api,prefix="/api/ollama",tags=['Ollama'])
app.include_router(TypeVideo_api,prefix="/api/typevideo",tags=['视频样式'])
app.include_router(TypeCover_api,prefix="/api/typecover",tags=['封面样式'])
app.include_router(TypeSubtitle_api,prefix="/api/typesubtitle",tags=['字幕样式'])
app.include_router(UrlAuthor_api,prefix="/api/UrlAuthor",tags=['作者链接'])
app.include_router(TeamOwner_api,prefix="/api/teamowner",tags=['团队拥有者'])
app.include_router(Keyword_api,prefix="/api/keyword",tags=['关键词'])
app.include_router(Data_api,prefix="/api/data",tags=['视频数据'])

# app.include_router(User_api,prefix="/cs/user",tags=['操作用户'])

if __name__ == "__main__":
    pass
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0", port=8180, log_level="debug", reload=True, workers=1)
'''
/docs
cd be       
python -m aerich init -t settings.TORTOISE_ORM
python -m aerich init-db
aerich migrate 
aerich upgrade
python -m aerich migrate
python -m aerich upgrade
'''

