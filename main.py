import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from app.UrlVDKey import UrlVDKey_api
from app.UrlVD import UrlVD_api
from app.User import User_api
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境请按需配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)
@app.get("/",tags=['项目介绍'])
async def home():
    return {"Hello xmtds"}
app.include_router(User_api,prefix="/User",tags=['操作用户'])
app.include_router(UrlVDKey_api,prefix="/UrlVDKey",tags=['视频采集链接'])
app.include_router(UrlVD_api,prefix="/UrlVD",tags=['视频下载链接'])
if __name__ == "__main__":
    pass
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8010, log_level="debug",reload=True,workers=1)#
'''
cd be       
aerich init -t settings.TORTOISE_ORM
aerich init-db
aerich migrate 
aerich upgrade
'''

