
from src.utils.request import *
# 示例用法
def getPromptText(data):
    result = request(Request(
        method='POST',
        url='/api/prompttext/getPages',
        data=data
    ))
    return result

def Updateprompttext(data):
    result = request(Request(
        method='POST',
        url='/api/prompttext/saveOrUpdate',
        data=data
    ))
    return result
def creatprompttext(data):
    result = request(Request(
        method='POST',
        url='/api/prompttext/Creatprompttext',
        data=data
    ))
    return result
    
def PromptTextsum():
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'status': 'ENABLE',
            }
        prompttexts=getPromptText(data)
        records = prompttexts['data']['records']
        sum.extend(records)
        if prompttexts['data']['pages']==n:
            return sum
        n+=1