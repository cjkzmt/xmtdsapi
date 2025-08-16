import os
import re

def GetClip():
    info={}
    RootDirectory=os.getenv("RootDirectory")
    制作路径=os.path.join(RootDirectory,'Content','VideoContent','Footage')
    for r, __, fs in os.walk(制作路径):
        paths=re.split(r'\\', r)
        if len(paths) < 6: continue
        Footage=paths[5]
        info[Footage] = info.get(Footage, 0) + len(fs)
    return info
