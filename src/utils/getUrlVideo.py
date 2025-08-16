from browser import ChromiumPage
import json
import os
import re
from DrissionPage import *
from Ffmpeg import merge_video,CheckPC

import requests
headers={
    # 'referer':'https://v.youku.com/v_show/id_XMzY3ODMyMTUwMA==.html?sharefrom=iphone&sharekey=ff1e20ddb6c90041ac3695d217bb227c2',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
if not GPU_SUPPORTED: print("注意：将使用CPU模式运行...")
listst = [
    ("https://v.youku.com/v_show/id_XMzY3MTI5NjYxNg==.html?sharefrom=iphone&sharekey=7909b835a0cb088f14fe92a55909b5675","0000"),
    ("https://v.youku.com/v_show/id_XMzY3MTM4NzIyOA==.html?sharefrom=iphone&sharekey=e96c8833ea3319da266bf95f7dda83e84","0000"),
]

for url,pow in listst:
    dp=ChromiumPage()
    dp.get(url)
    dp.wait(1)
    dp('x://*[@id="kui_layer_password-layer_passwordInput"]').input(pow)
    dp.listen.start('h5/mtop.youku.play.ups.appinfo.ge')
    dp('@text()=确定').click()
    r=dp.listen.wait()
    json_data=r.response.body
    json_match = re.search(r'^[^(]+\((.*)\)$', json_data)
    if json_match:
        json_str = json_match.group(1)
        data = json.loads(json_str)
        title=data['data']['data']['video']['title'] 
        print(title)
        temp_video=f"{title}.mp4"
        if os.path.exists(temp_video):continue
        cliplist=[]
        info_list = data['data']['data']['stream'][4]['segs']
        for index, info in enumerate(info_list) :
            print(f'下载第{index}个片段')
            path=f"{title}{index}.mp4"
            cliplist.append(path)
            if os.path.exists(path):continue
            url=info['cdn_url']
            video=requests.get(url=url,headers=headers).content
            with open(path, "wb") as f:
                f.write(video)
        merge_video(cliplist, temp_video)
    else:
        print("无法解析 JSONP 数据")