import subprocess
import json
from moviepy import *

def xuanzheng(视频路径):
    video_clip = VideoFileClip(视频路径)
    if video_clip.rotation not in [90, 270]:return
    video_clip = video_clip.resized(newsize=(video_clip.h, video_clip.w))
    video_clip.write_videofile(视频路径)#gpu 加速
path = r'D:\XMTDS\Content\RawFootage\hnluyi\室外视频2\512e0a2d04a17464c91ed01ba5a6d045_raw.mp4'
xuanzheng(path,'2.mp4')