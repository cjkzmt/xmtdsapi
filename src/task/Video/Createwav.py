from src.utils.IindexTts import IindexTts
from src.utils.Audio import add_silence_audio
from src.utils.Ffmpeg import speed_up_audio
from pathlib import Path
import asyncio
import os
async def  Createwav(Script):#, retry=0, max_retry=3
    try: 
        reading=Script.reading
        readinglist=reading.split('\n')
        RootDirectory=os.getenv("RootDirectory")
        Overpath = os.path.join( RootDirectory, os.getenv("OverDirectory"), Script.Over.filename)
        # print(Overpath)
        speed=Script.Over.speed
        # print(speed)
        Audio_Path = os.path.join(RootDirectory ,os.getenv("AudioDirectory"),str(Script.Over_id)) 
        # print(Audio_Path)
        Audio_Path_1 = os.path.join(Audio_Path,'1') 
        texts=[]
        for text in readinglist:
            wavpath = os.path.join(Audio_Path_1, f"{text}.wav")
            if os.path.exists(wavpath):continue
            texts.append(text)
        if texts:
            await IindexTts(Overpath,Audio_Path_1, texts)
        Audio_Path_speed = os.path.join(Audio_Path,str(speed))
        for text in readinglist:
            output_path = os.path.join(Audio_Path_speed, f"{text}.wav")
            if os.path.exists(output_path):continue
            input_path= os.path.join(Audio_Path_1, f"{text}.wav")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            speed_up_audio(input_path, output_path, speed)
        input_path=os.path.join(Audio_Path_speed, f"{text}.wav")
        output_path=os.path.join(Audio_Path_speed, f"{text}尾.wav")
        if not os.path.exists(output_path):
            add_silence_audio(input_path, output_path)
        return True
    except Exception as e:
        raise e
