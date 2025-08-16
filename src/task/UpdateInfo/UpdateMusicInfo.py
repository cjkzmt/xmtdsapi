from src.api.music import saveMusicList
from src.utils.Audio import get_music_info
from src.utils.Pan import sync
import asyncio
import os
def UpdateMusicInfo():
    print(os.getenv("RootDirectory"))
    print(os.getenv('MusicDirectory'))
    Music_Path = os.path.join(os.getenv("RootDirectory"),os.getenv('MusicDirectory')) 
    MusicList=[f for f in os.listdir(Music_Path) if f.endswith(('.mp3','.MP3'))]
    MusicListdata=[]
    asyncio.run(sync(Music_Path,'Music'))
    for music in MusicList:
        musicpath=os.path.join(Music_Path,music)
        duration=get_music_info(musicpath)['duration']
        seconds = int(duration // 1000)  # 计算剩余的秒数
        MusicListdata.append({"name":music,"duration":seconds})
    return  saveMusicList({"itemList":MusicListdata})
print(UpdateMusicInfo())
