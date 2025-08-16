
from src.utils.request import *
# 示例用法
def gettopiccopy(data):
    result = request(Request(
        method='POST',
        url='/api/topiccopy/getPages',
        data=data
    ))
    return result

def Updatetopiccopy(data):
    result = request(Request(
        method='POST',
        url='/api/topiccopy/saveOrUpdate',
        data=data
    ))
    return result
def TopicCopysum():
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'status': 'ENABLE',
            }
        topiccopys=gettopiccopy(data)
        records = topiccopys['data']['records']
        sum.extend(records)
        if topiccopys['data']['pages']==n:
            return sum
        n+=1