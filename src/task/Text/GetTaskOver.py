import os
import random
from src.api.over import Oversum
from src.api.script import UpdateScript
def GetTaskOver(Info):
    name=Info["Over"]
    print(f'获取配音{name}')
    Over_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('OverDirectory')) 
    if name:
        OverPath=os.path.join(Over_Path,name)
        if os.path.exists(OverPath):
            Info['OverPath']=OverPath
            return Info
    OverList=Oversum()
    random.shuffle(OverList)
    for Over in OverList:
        #print(f'获取配音{Over["filename"]}')
        OverPath=os.path.join(Over_Path,Over["filename"])
        if os.path.exists(OverPath):
            data={'id':Info["id"],"Over_id":Over["id"]}
            #print(f'跟新配音{Over}')
            UpdateScript(data)
            Info['OverPath']=OverPath
            return Info
        
