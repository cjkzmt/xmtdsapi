from  src.api.over import saveOverList
from src.utils.Pan import sync
import asyncio
import os   
def UpdateOverInfo():      
    Over_Path = os.path.join(os.getenv("RootDirectory"),os.getenv('OverDirectory')) 
    print(Over_Path)
    OverList=[{"filename":f} for f in os.listdir(Over_Path) if f.endswith(('.mp3','.MP3'))]
    asyncio.run(sync(Over_Path,"Over"))
    return  saveOverList({"itemList":OverList})
print(UpdateOverInfo())