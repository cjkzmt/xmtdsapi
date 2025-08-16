import os
from typing import Dict
from src.utils.Ffmpeg import Merge
from src.task.Video.Createwav import Createwav
from src.task.Video.CreateVideoCover import CreateVideoCover
from src.task.Video.CreateVideoSubtitle import CreateVideoSubtitle
from src.task.Video.ClipSynthesis import ClipSynthesis
from src.utils.Ffmpeg import *

GPU_SUPPORTED = False

async def CreateVideo(all_scripts) -> bool:
    try:
        for Script in all_scripts:
            # 添加类型检查
            if not hasattr(Script, 'copystatus'):
                print(f'❌ 跳过任务，Script不是有效对象: {Script}')
                continue
            if  Script.copystatus != 'ENABLE':
                print('❌ 跳过任务，程序错误')
                raise '❌ 跳过任务，程序错误'
            id = Script.id
            print(f'开始处理任务：{id}')
            shorthand = Script.AccountTeam.TeamOwner.shorthand
            
            team=Script.AccountTeam.number
            RootDirectory = os.getenv("RootDirectory")
            taskpath=os.path.join(RootDirectory,os.getenv("ReviewVideo"))
            os.makedirs(taskpath, exist_ok=True)
            output_path = os.path.join(taskpath, f'{shorthand}_{team}_{id}.mp4')
            if os.path.exists(output_path):
                print("视频已存在")
                continue
            print("开始制作视频",id)
            if await Createwav(Script) == False: 
                print("音频制作失败",Script)
                continue
            print("音频制作：完成")
            if ClipSynthesis(Script) == False: 
                print("视频片段制作失败",Script)
                continue
            if CreateVideoCover(Script) == False: 
                print("视频封面制作失败",Script)
                continue
            if CreateVideoSubtitle(Script) == False: 
                print("字幕制作失败",Script)
            
            work_dir = os.path.join(RootDirectory,os.getenv("UsedFootage"),str(id))
            music_path = os.path.join(RootDirectory,os.getenv("MusicDirectory"), Script.Music.name)
            Subtitle=Script.subtitle
            Subtitlelist=Subtitle.split('\n')
            sum=len(Subtitlelist)
            videolist=[os.path.join(work_dir, f'z{i}.mp4') for i in range(sum+1)]
            Merge(videolist, output_path, audio=True, music_path=music_path, volume=0.4)
        return True
    except Exception as e:
        raise e
    