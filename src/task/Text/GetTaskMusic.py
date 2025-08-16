import os
import random
from src.api.music import Musicsum
from src.api.script import UpdateScript
def GetTaskMusic(Info):
    name=Info["Music"]
    print(f'获取音乐{name}')
    Music_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('MusicDirectory')) 
    if name:
        MusicPath=os.path.join(Music_Path,name)
        if os.path.exists(MusicPath):
            Info['MusicPath']=MusicPath
            return Info
    #print(f'获取音乐{name}')
    MusicList=Musicsum()
    random.shuffle(MusicList)
    for Music in MusicList:
        #print(f'获取音乐{Music["name"]}')
        MusicPath=os.path.join(Music_Path,Music["name"])
        if os.path.exists(MusicPath):
            data={'id':Info["id"],"Music_id":Music["id"]}
            #print(f'跟新音乐{Music}')
            UpdateScript(data)
            Info['MusicPath']=MusicPath
            return Info
        
