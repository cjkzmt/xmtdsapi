
from src.utils.request import *
def saveOverList(data):
    result = request(Request(
        method='POST',
        url='/api/over/saveList',
        data=data
    ))
    return result
def getOver(data):
    result = request(Request(
        method='POST',
        url='/api/over/getPages',
        data=data
    ))
    return result
def Oversum(OverId=None):
    sum=[]
    n=1
    while True:
        data={
            'OverId':OverId if OverId else None,
            'currentPage':n,
            'status': 'ENABLE'}
        Overs=getOver(data)
        records = Overs['data']['records']
        sum.extend(records)
        if Overs['data']['pages']==n:
            return sum
        n+=1