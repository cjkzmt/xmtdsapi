
from src.utils.request import *
# 示例用法
def getAccount(data):
    result = request(Request(
        method='POST',
        url='/api/account/getPages',
        data=data
    ))
    return result

def UpdateAccount(data):
    result = request(Request(
        method='POST',
        url='/api/account/saveOrUpdate',
        data=data
    ))
    return result

def Accountsum():
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'status': 'ENABLE',
            }
        Accounts=getAccount(data)
        records = Accounts['data']['records']
        sum.extend(records)
        if Accounts['data']['pages']==n:
            return sum
        n+=1