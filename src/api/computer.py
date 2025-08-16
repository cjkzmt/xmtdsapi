
from src.utils.request import *
from src.utils.KeyValue import Kv
# 示例用法
def getComputerinfo():
    result = request(Request(
        method='POST',
        url='/api/computer/getPages',
        data={"ComputerId":Kv.get("PC_ID", 0)}
    ))
    return result
def getComputerPermissions():
    Computerinfo=getComputerinfo()['data']['records']
    if Computerinfo==[]:
        print('请先添加电脑信息')
        exit()
    Computerinfo=Computerinfo[0]
    Create_Text = True if Computerinfo['createtext']=='ENABLE' else False
    Create_Video = True if Computerinfo['createvideo']=='ENABLE' else False
    Publish_Video = True if Computerinfo['publishvideo']=='ENABLE' else False
    Create_Clip = True if Computerinfo['createclip']=='ENABLE' else False
    print(f'创建文字：{Create_Text} 创建视频：{Create_Video} 发布视频：{Publish_Video}')
    return Create_Text,Create_Video,Create_Clip,Publish_Video