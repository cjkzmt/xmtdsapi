import os
import shutil
from src.utils.Pan import sync
from app.Script import Upvideostatus
async def Reviewed():
    try:
        taskpath=os.path.join(os.getenv("RootDirectory"),'Task','Reviewed')
        Publishpath=os.path.join(os.getenv("RootDirectory"),'Task','PublishVideo')
        os.makedirs(Publishpath, exist_ok=True)
        videos = [ f for r, _, fs in os.walk(taskpath) for f in fs if f.endswith('.mp4')]
        if len(videos)==0: return
        sync(taskpath, 'PublishVideo',videos)
        idlist=[(os.path.splitext(os.path.basename(video))[0].split('_')[-1],video) for video in videos]
        await Upvideostatus(idlist)
        for video in videos:
            inpath = os.path.join(taskpath, video)
            outpath = os.path.join(Publishpath, video)
            shutil.move(inpath, outpath)
    except Exception as e:
        print(str(e))