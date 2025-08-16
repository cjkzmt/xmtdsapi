from moviepy import *
import numpy as np
from src.utils.Image import *
import os
from PIL import Image
def 无框封面(背景,Script):
    总宽, 总高 = 背景.size
    print(Script.Font.name)
    封面字体 =os.path.join(os.getenv("RootDirectory"),os.getenv('FontDirectory'), Script.Font.name)
    标题=Script.cover.split("\n")
    封面字色 = "白"
    封面偏移y = 0
    封面偏移x = 0
    x=总宽/2+封面偏移x
    y=总高/2+封面偏移y
    顶标题字号 = 80
    顶标题= Script.AccountTeam.TypeCover.fixedtitle
    顶标题宽,顶标题高=get_str_info(顶标题, 顶标题字号, 封面字体)
    标题字号=50
    渐变透明度= 0.5
    方形高= 顶标题高+标题字号*1.5+标题字号*len(标题)*1.5+标题字号/2
    背景 = 低图(背景,总宽,总高,方形高,渐变透明度)
    y1=(总高 - 方形高) / 2
    y1 = y1+标题字号/2
    dy = y1
    dx = (总宽 - 顶标题宽) / 2
    绘字(背景,(dx,dy,顶标题,封面字体,顶标题字号,封面字色) )
    y1 =y1+顶标题高+标题字号/2
    下划线y1 = y1
    下划线x2 = 总宽*3/4
    下划线宽=2
    下划线y2 = 下划线y1 + 下划线宽
    下划线x1=总宽/4
    方形(背景,(下划线x1,下划线y1,下划线x2,下划线y2,封面字色,下划线宽))
    y1+=标题字号/2
    for b in 标题:
        标题宽=get_str_info(b, 标题字号, 封面字体)[0]
        x=(总宽-标题宽)//2
        绘字(背景,(x,y1,b,封面字体,标题字号,"白") )
        y1+=标题字号*1.5
    return 背景


封面模板 = {
    '无框黑底':无框封面,
}

def 视频封面制作(img,path,Script):
    # print(Script['TypeCover'])
    封面=封面模板[Script.AccountTeam.TypeCover.name](img,Script)
    图转视频 = np.array(封面)
    clip = ImageClip(图转视频).with_duration(0.2).with_fps(30)
    clip.write_videofile(
                path,
                codec='h264_nvenc',#'libx264' if 
                audio_codec='aac',  # 比libmp3lame更高效
                threads=4,  # 使用多线程
                preset='fast',  # 平衡速度和质量
                ffmpeg_params=[
                    '-movflags', '+faststart',  # 流媒体优化
                    '-profile:v', 'main', 
                    '-pix_fmt', 'yuv420p'
                ]
            )
    clip.close()  # 显式关闭clip以避免句柄错误

def CreateVideoCover(Script):
    try: 
        RootDirectory=os.getenv("RootDirectory")
        制作路径=os.path.join(RootDirectory,os.getenv("UsedFootage"),str(Script.id))
        path=os.path.join(制作路径, 'z0.mp4')
        if not os.path.exists(path):
            videopath=os.path.join(制作路径, f'1.mp4')
            clip=VideoFileClip(videopath)
            第一帧 = clip.get_frame(0)
            img = Image.fromarray(第一帧)
            视频封面制作(img,path,Script)
            clip.close()  # 显式关闭clip以避免句柄错误
        return True
    except Exception as e:
        return False