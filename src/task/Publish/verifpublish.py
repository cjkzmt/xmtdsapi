def douyinVerif(tab,btitle,publishtime):
    bnote=tab(f'tx:{btitle}')
    if not bnote:return False
    xx=bnote.parent('@class=video-card-info-aglKIQ').text
    veriftime= publishtime.strftime('%Y年%m月%d日 %H')
    if veriftime not in xx :
        tab.wait(5)
        print(f'⚠️  在{xx}//未找到发布时间{veriftime}')
        douyinVerif(tab,btitle,publishtime)
    return True 
def weixnVerif(tab,btitle,publishtime):
    body =tab('.wujie_iframe').shadow_root
    btitle=btitle[:30]
    bnote=body(f'tx:{btitle}')
    if not bnote:return False
    xx=bnote.parent().text
    veriftime= publishtime.strftime('%Y年%m月%d日 %H')
    if veriftime not in xx :
        tab.wait(5)
        print(f'⚠️  在{xx}//未找到发布时间{veriftime}')
        weixnVerif(tab,btitle,publishtime)
    return True 
def kuaishouVerif(tab,btitle,publishtime):
    bnote=tab(f'tx:{btitle}')
    if not bnote:return False
    xx=bnote.parent('@class=video-item__detail__top').text
    veriftime= publishtime.strftime('%Y-%m-%d %H')
    if veriftime not in xx :
        tab.wait(5)
        print(f'⚠️  在{xx}//未找到发布时间{veriftime}')
        kuaishouVerif(tab,btitle,publishtime)
    return True 
def xiaohongshuVerif(tab,btitle,publishtime):
    bnote=tab(f'tx:{btitle}')
    if not bnote:return False
    xx=bnote.parent('@class=info').text
    veriftime= publishtime.strftime('%Y年%m月%d日 %H')
    if veriftime not in xx :
        tab.wait(5)
        print(f'⚠️  在{xx}//未找到发布时间{veriftime}')
        xiaohongshuVerif(tab,btitle,publishtime)
    return True 
def VerifPublish(tab,Platform,btitle,publishtime):
    # print(f'🤔 {Platform}视频发表验证')
    平台 = {
        '抖音':douyinVerif,
        '小红书':xiaohongshuVerif,
        '视频号':weixnVerif,
        '快手':kuaishouVerif
        }
    return 平台[Platform](tab,btitle,publishtime)

async def douyinLogin(tab) -> bool:
    nanme=tab("@class=name-_lSSDc").text
    number=tab("@class=unique_id-EuH8eA").text.replace("抖音号：","")
    # print(f'✅ 抖音 账号:{nanme} 账号:{number}')
    profileN=tab("@class=signature-HLGxt7")
    profile= profileN.text if profileN else None
    newFans= tab("@class=number-No6ev9").text 
    return {
        'name':nanme,
        'number':number,
        'profile':profile,
        'newFans':newFans
        }
async def xiaohongshuLogin(tab) -> bool:
    tab.wait.load_start()
    nanme=tab("@class=account-name").text
    number=tab("小红书账号:").text.replace("小红书账号:","")
    print(f'✅ 小红书 账号:{nanme} 账号:{number}')
    newFans= tab("@class=numerical").text 
    return {
        'name':nanme,
        'number':number,
        'profile':None,
        'newFans':newFans
        }
async def weixnLogin(tab) -> bool:
    nanme=tab("@class=finder-nickname").text
    number=tab("@class=finder-uniq-id").text
    # print(f'✅ 视频号 账号:{nanme} 账号:{number}')
    newFans= tab("@class=finder-info-num").text 
    return {
        'name':nanme,
        'number':number,
        'profile':None,
        'newFans':newFans
        }
async def kuaishouLogin(tab) -> bool:
    tab("@class=user-info-name").click()
    nanme=tab("@class=user-name").text
    number=tab("@class=user-kwai-id").text
    # print(f'✅ 快手 账号:{nanme} 账号:{number}')
    profileN=tab("@class=user-desc")
    profile= profileN.text if profileN else None
    newFans= tab("@class=user-cnt__item").text.replace("粉丝","")
    # print(f'✅ 粉丝数:{newFans}')
    return {
        'name':nanme,
        'number':number,
        'profile':profile,
        'newFans':newFans
        }
from app.Account import UpAccount
async def VerifLogin(tab,Platform,Account_id):
    平台 = {
        '抖音':douyinLogin,
        '小红书':xiaohongshuLogin,
        '视频号':weixnLogin,
        '快手':kuaishouLogin
        }
    info= await 平台[Platform](tab)
    return await UpAccount(Account_id,info)