# 1、登陆账号获取权限
from app.GetPCInfo import GetPCInfo
import asyncio
import traceback
from src.task.Text.CreateText import CreateText
from src.task.Video.CreateClip import CreateClip
from src.task.Video.Reviewed import Reviewed
from src.task.Video.UpClip import GetClip
from app.TeamOwner import UpdateclipSum
from src.task.Video.CreateVideo import CreateVideo
from src.task.Publish.PublishVideo import PublishVideo, videonamea
from app.Script import getVideoInfo, getPublishInfo
from dotenv import load_dotenv
load_dotenv()
from src.utils.Ffmpeg import CheckPC
GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
if not GPU_SUPPORTED:
    print("注意：将使用CPU模式运行...")
async def main():
    Create_Text, Create_Video, Publish_Video, Create_Clip = await GetPCInfo()
    try:
        if Publish_Video:
            re = await getPublishInfo()
            if re:
                Teamlist, keywords, data_map, videoname = re
                if videonamea(videoname):
                    await main()
                await PublishVideo(Teamlist, keywords, data_map)
        if Create_Video:
            await Reviewed()
            all_scripts = await getVideoInfo()
            if all_scripts:
                await CreateVideo(all_scripts)
            await UpdateclipSum(GetClip())
        if Create_Text:
            await CreateText()
        if Create_Clip:
            await CreateClip()
    except Exception as e:
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {str(e)}")
        print("完整堆栈跟踪:")
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())