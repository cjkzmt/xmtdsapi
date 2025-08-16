from src.utils.Pan import downloaded
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()
Font_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('FontDirectory')) 
asyncio.run(downloaded(Font_Path,'Font')) 
Over_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('OverDirectory')) 
asyncio.run(downloaded(Over_Path,'Over'))
Music_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('MusicDirectory')) 
asyncio.run(downloaded(Music_Path,'Music'))