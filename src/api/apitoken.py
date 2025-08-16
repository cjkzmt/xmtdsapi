
from src.utils.request import *
# 示例用法
def getPages(data):
    result = request(Request(
        method='POST',
        url='/api/apitoken/getPages',
        data=data
    ))
    return result['data']

def saveOrUpdate(data):
    result = request(Request(
        method='POST',
        url='/api/apitoken/saveOrUpdate',
        data=data
    ))
    return result

def ApiTokenssum(AiId=None):
    sum=[]
    n=1
    while True:
        data={
            'AiApiId':AiId if AiId else None,
            'currentPage':n,
            'status': 'ENABLE'}
        ApiTokenss=getPages(data)
        records = ApiTokenss['records']
        sum.extend(records)
        if n >= ApiTokenss['pages']:
            return sum
        n+=1

def forbidApiToken(apitokenId):
    result = request(Request(
        method='POST',
        url='/api/apitoken/saveOrUpdate',
        data= {
        'id': apitokenId,
        'status': 'DISABLE',}
        ))
    return result