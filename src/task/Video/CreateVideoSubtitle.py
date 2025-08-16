import os
from src.utils.Ffmpeg import *
from src.utils.OsPath import *
from moviepy import *


色值={
    '红': '#ff0000',
    "绿": '#00ff00',
    "蓝": '#0000ff',
    "黄": (254,223,1),
    "紫": '#ff00ff',
    "青": '#00ffff',
    "橙": '#ffa500',
    "粉": '#ff69b4',
    "灰": '#808080',
    "白": (255,255,255),
    "黑": (0,0,0)  
    } 
def CreateVideoSubtitle(Script):
    try: 
        
        RootDirectory=os.getenv("RootDirectory")
        制作路径=os.path.join(RootDirectory,os.getenv("UsedFootage"),str(Script.id))
        FontPath=os.path.join(RootDirectory,os.getenv("FontDirectory"), Script.Font.name)
        fontcolor=Script.AccountTeam.TypeSubtitle.fontcolor
        fontsize=Script.AccountTeam.TypeSubtitle.fontsize
        height=Script.AccountTeam.TypeVideo.videoheight
        Subtitle=Script.subtitle
        Subtitlelist=Subtitle.split('\n')
        sum=len(Subtitlelist)
        for i, text in enumerate(Subtitlelist) :
            video_path=os.path.join(制作路径, f'z{i+1}.mp4')
            if os.path.exists(video_path): continue
            videopath=os.path.join(制作路径, f'{i+1}.mp4')
            videoclip=VideoFileClip(videopath)
            无=len(text.replace(' ',''))
            字幕组=text.split(' ')
            start=end=0
            段s=[]
            视频时长=videoclip.duration
            音频时长=视频时长-0.6-(1 if i==sum-1 else 0)
            for n, 字 in enumerate(字幕组):
                段长=音频时长*len(字)/无
                end=start+段长+(0.3 if start==0 else 0)
                if n==len(字幕组)-1: 
                    段长+=0.3
                    end=视频时长
                段=videoclip.subclipped(start,end)
                txt_clip = TextClip(
                    font=FontPath, text=字, font_size=fontsize, color=色值[fontcolor[0]],stroke_color=色值[fontcolor[-1]],  
                    stroke_width=3 if len(fontcolor)>1 else 0, 
                    interline=fontsize//5
                )
                txt_clip = txt_clip.with_position(('center',height*2/3)).with_duration(段长)
                video=CompositeVideoClip([段, txt_clip])
                start=end
                段s.append(video)
            video = concatenate_videoclips(段s)
            video.write_videofile(
                video_path,
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
            # 显式关闭所有 clips 以避免句柄错误
            for 段 in 段s:
                段.close()
            video.close()
            videoclip.close()  # 显式关闭videoclip以避免句柄错误
        return True
    except Exception as e:
        print(str(e))
        return False