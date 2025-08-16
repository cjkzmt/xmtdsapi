import os
from src.utils.Ffmpeg import getVoideDuration,Merge
from src.utils.OsPath import *
from moviepy import *
import random

def ClipSynthesis(Script):
    try:
        reading=Script.reading
        视频类型=tuple(os.getenv("视频类型").split(","))
        RootDirectory=os.getenv("RootDirectory")
        制作路径=os.path.join(RootDirectory,os.getenv("UsedFootage"),str(Script.id))
        视频素材=os.path.join(RootDirectory,os.getenv("FootageDirectory"))
        Audio_Path = os.path.join(RootDirectory , os.getenv("AudioDirectory"),str(Script.Over_id),str(Script.Over.speed) ) 
        readinglist=reading.split('\n')
        clips=[]
        for i, text in enumerate(readinglist) :
            output_path=os.path.join(制作路径, f'{i+1}.mp4')
            if os.path.exists(output_path): continue
            Overpath=os.path.join(Audio_Path, f"{text}{'尾' if i==len(readinglist)-1 else '' }.wav")
            adc=AudioFileClip(Overpath)
            duration=adc.duration
            n=0
            paths=[Script.AccountTeam.TeamOwner.path]
            l = 0
            while l<duration: 
                if n>=len(paths): n=0
                old_dir = os.path.join(视频素材, paths[n])
                原素材表 = [os.path.join(r, f) for r, _, fs in os.walk(old_dir) for f in fs if f.endswith(视频类型)]
                new_dir = os.path.join(制作路径, str(i), paths[n])
                os.makedirs(new_dir, exist_ok=True)
                cliplist = [os.path.join(r, f) for r, _, fs in os.walk(new_dir) for f in fs if f.endswith(视频类型)]
                l=0
                if cliplist :
                    for 素材路径 in cliplist:
                        l += getVoideDuration(素材路径)
                if l>=duration:
                    for 素材路径 in cliplist:
                        clip=VideoFileClip(素材路径)
                        clips.append(clip)
                    break
                if 原素材表:
                    video_file=random.choice(原素材表)
                    new_file=os.path.join(new_dir, os.path.basename(video_file))
                    文件移动(video_file, new_file)
                else: 
                    print(f"{old_dir}用完请及时补充")
                    return False
                n+=1
            # print(cliplist, output_path, duration,False,Overpath)
            Merge(cliplist, output_path, duration,False,Overpath)
            # 显式关闭所有 clips 以避免句柄错误
            for clip in clips:
                clip.close()
            adc.close()  # 显式关闭adc以避免句柄错误
        return True
    except Exception as e:
        print('合成错误',str(e))
        return False