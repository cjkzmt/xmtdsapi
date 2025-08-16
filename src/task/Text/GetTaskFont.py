import os
import random
from src.api.font import Fontsum
from src.api.script import UpdateScript

def GetTaskFont(Info):
    name=Info["Font"]
    print(f'获取字体{name}')
    Font_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('FontDirectory')) 
    if name:
        FontPath=os.path.join(Font_Path,name)
        if os.path.exists(FontPath):
            Info['FontPath']=FontPath
            return Info
    #print(f'字体')
    FontList=Fontsum()
    random.shuffle(FontList)
    for Font in FontList:
        FontPath=os.path.join(Font_Path,Font["name"])
        if os.path.exists(FontPath):
            #print(f'跟新字体{Font}')
            data={'id':Info["id"],"Font_id":Font["id"]}
            UpdateScript(data)
            Info['FontPath']=FontPath
            return Info
        
