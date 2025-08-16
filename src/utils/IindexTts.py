from gradio_client import Client, handle_file
import asyncio
import shutil
import os
import asyncio
from functools import partial

async def renAudio(result, text, Audio_Path):
    path=result['value']
    os.makedirs(Audio_Path, exist_ok=True)
    Exten = '.wav'
    ttspath = os.path.dirname(path)
    path1 = os.path.join(ttspath, f"{text}{Exten}")
    if not os.path.exists(path1):
        os.rename(path, path1)
    path2 = os.path.join(Audio_Path, f"{text}{Exten}")
    shutil.move(path1, path2)
async def tts_task(client, text, Audio):
    text = text.replace(' ', '，')
    # 使用 partial 把参数绑定为一个可调用对象，并放入线程执行
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, partial(
        client.predict,
        prompt=handle_file(Audio),
        text=text,
        infer_mode="普通推理",#普通推理,批次推理
        max_text_tokens_per_sentence=120,
        sentences_bucket_max_size=4,
        param_5=True,
        param_6=0.8,
        param_7=30,
        param_8=1,
        param_9=0,
        param_10=3,
        param_11=10,
        param_12=600,
        api_name="/gen_single"
    ))
    return result

async def IindexTts(Audio,Audio_Path,textlist):
    # print(Audio,Audio_Path,textlist)
    client = Client("http://127.0.0.1:7860/")
    tasks = []
    for text in textlist:
        task = asyncio.create_task(tts_task(client, text, Audio))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    for result, text in zip(results, textlist):
        await renAudio(result, text, Audio_Path)



