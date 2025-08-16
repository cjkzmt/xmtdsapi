from src.api.font import saveFontList
from src.utils.Pan import sync
import asyncio
import os   
def UpdateFontInfo():      
    Font_Path = os.path.join(os.getenv("RootDirectory"),os.getenv('FontDirectory')) 
    FontList=[{"name":f} for f in os.listdir(Font_Path) if f.endswith('.otf')]
    asyncio.run(sync(Font_Path,"Font"))
    return  saveFontList({"itemList":FontList})
print(UpdateFontInfo())