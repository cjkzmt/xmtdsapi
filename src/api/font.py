
from src.utils.request import *
def saveFontList(data):
    result = request(Request(
        method='POST',
        url='/api/font/saveList',
        data=data
    ))
    return result
def getFont(data):
    result = request(Request(
        method='POST',
        url='/api/font/getPages',
        data=data
    ))
    return result
def Fontsum(FontId=None):
    sum=[]
    n=1
    while True:
        data={
            'FontId':FontId if FontId else None,
            'currentPage':n,
            'status': 'ENABLE'}
        Fonts=getFont(data)
        records = Fonts['data']['records']
        sum.extend(records)
        if Fonts['data']['pages']==n:
            return sum
        n+=1


def forbidFont(FontId):
    result = request(Request(
        method='POST',
        url='/api/font/saveOrUpdate',
        data= {
        'id': FontId,
        'status': 'DISABLE',}
        ))
    return result