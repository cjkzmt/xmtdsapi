
from src.utils.request import *
# 示例用法
def getData(data):
    result = request(Request(
        method='POST',
        url='/api/data/getPages',
        data=data
    ))
    return result

def UpdateData(data):
    result = request(Request(
        method='POST',
        url='/api/data/saveOrUpdate',
        data=data
    ))
    return result

def Datasum():
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'status': 'ENABLE',
            }
        Datas=getData(data)
        records = Datas['data']['records']
        sum.extend(records)
        if Datas['data']['pages']==n:
            return sum
        n+=1