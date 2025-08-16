import os
from src.utils.browser import *
from src.utils.Time import convertTime
from .Publish_Video import *
from .verifpublish import *
from app.Data import UpDataStatus
from app.Script import UpScriptsStatus
import asyncio
未登录账号 = set()
已登录账号 = set()
标点符号集合 = {'，', '。', '！', '？', ',', '.', '!', '?'}
def find_split_index(text, max_length, 标点符号集合):
    if len(text) <= max_length: return len(text)
    for i in range(max_length - 1, -1, -1):
        if text[i] in 标点符号集合: return i + 1
    return max_length
def 文字分割(txt, n):
    if len(txt)<=n:
        first_part=txt
        second_part=""
        return first_part, second_part
    else:
        split_index = find_split_index(txt, n, 标点符号集合) 
        first_part = txt[:split_index] + txt[split_index] if txt[split_index] in 标点符号集合 else txt[:split_index]
        second_part = txt[split_index:] if txt[split_index] not in 标点符号集合 else txt[split_index + 1:]
        return first_part, second_part

async def publish_Data(page,info,title,publishtime,videopath,keywords):
        Account_id=info['Account_id']
        if Account_id in 未登录账号:
            return
        Platform=info['Platform']
        character=info['character']
        btitle, atitle = 文字分割(title, character)
        if Account_id not in 已登录账号:
            verification=info['verification']
            loginurl=info['loginurl']
            tab = signurl(page,loginurl)
            if verification in tab('tag:body').text: 
                未登录账号.add(Account_id)
                print(f'❌ 未登录账号:{Account_id}')
                return f'❌ 未登录账号:{Account_id}'
            
            if await VerifLogin(tab,Platform,Account_id):
                已登录账号.add(Account_id)
                print(f'✅ {Platform}登录成功')
            else:
                raise Exception('❌ 登录失败,账号信息有误')
        publishverif=info['publishverif']
        tab = signurl(page,publishverif)
        if VerifPublish(tab,Platform,btitle,publishtime):
            await UpDataStatus(info['id'])
            print(f'✅ {Platform}{info['id']}视频发表成功{publishtime}')
            return f'✅ {Platform}{info['id']}视频发表成功{publishtime}'
        url=info['url']
        tab = signurl(page,url)
        上传视频(tab, Platform,videopath)    
        keycount=info['keycount']
        写入标题(tab, Platform,btitle, atitle, character,keywords[:keycount])
        chooseTime(tab,Platform, publishtime)
        发布(tab,Platform)
        tab.wait(10)
        tab = signurl(page,publishverif)
        await publish_Data(page,info,title,publishtime,videopath,keywords)

async def PublishVideo(Teamlist,keywords,data_map):
    RootDirectory=os.getenv("RootDirectory")
    accountspath=os.path.join(RootDirectory,os.getenv("accountsDirectory"))
    Publishpath=os.path.join(RootDirectory,os.getenv("PublishVideo"))
    os.makedirs(Publishpath, exist_ok=True)
    async def publish_scripts(page,iteam):
        if len(iteam['Data'])>0:
            videoname=iteam['videoname']
            publishtime=convertTime(iteam['publishtime'])
            title=iteam['title']
            print(f'ℹ️  开始发表视频:{videoname}发布时间为{publishtime}')
            videopath=os.path.join(Publishpath,videoname)
            for info in iteam['Data']:
                await publish_Data(page,info,title,publishtime,videopath,keywords)
        await UpScriptsStatus(iteam['id'])
    async def publish_team(team):
        accountTeam=team.number
        print(f"ℹ️  账号组：{team.number} 开始发布")
        page = signbrowser(accountspath,accountTeam)
        for iteam in data_map[team.id]:
            await publish_scripts(page,iteam)
    tasks = [publish_team(team) for team in Teamlist]
    await asyncio.gather(*tasks)
    # for team in Teamlist:
    #     await publish_team(team)

def videonamea(videos):
    RootDirectory=os.getenv("RootDirectory")
    Publishpath=os.path.join(RootDirectory,os.getenv("PublishVideo"))
    for videoname in videos:
        videopath=os.path.join(Publishpath,videoname)
        if not os.path.exists(videopath):
            remote_folder = 'PublishVideo'
            print('⚠️ 正在下载视频文件...')
            from src.utils.Pan import downloaded
            downloaded(Publishpath,remote_folder,videos)
            return True
    return False
        

