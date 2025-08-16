
from src.utils.browser import *
from src.utils.getToken import *
from src.api.pnumber import TopIteams
from src.api.aiapi import getAll
from src.api.apitoken import getPages,saveOrUpdate

List=TopIteams()
aiList=getAll()
for item in List:
    number=item['number']
    path="D:\XMTDS\Content\OtherContent\AI"
    page=signbrowser(path,item['code'])
    for ai in aiList:
        data={
            'AiApi_id': ai['id'],
            'PNumber_id':item['id']}
        token=getPages(data)['records']
        lr='未录入'
        token_id = None
        if token:
            lr='已录入'

            token_id = token[0].get('id')
            status=token[0].get('status')
            token_v=token[0].get('token')
            if token_v and  status=='ENABLE':continue

        # print(number,ai['name'],lr,item['code'])
        url=ai['url']
        name=ai['name']
        tab=signurl(page,url)
        token_v=getToken(tab,name) or '未登录'

        token_data={
            'id':token_id,
            'AiApi_id': ai['id'],
            'PNumber_id':item['id'],
            'token':token_v,
            'status':'ENABLE' if token != '未登录' else 'DISABLE'
        }
        print(token_data)
        saveOrUpdate(token_data)
