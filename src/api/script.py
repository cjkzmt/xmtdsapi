
from src.utils.request import *
def getScript(data):
    result = request(Request(
        method='POST',
        url='/api/script/getPages',
        data=data
    ))
    return result


def GetTasklist(data):
    result = request(Request(
        method='POST',
        url='/api/script/TaskList',
        data=data
    ))
    return result

def UpdateScript(data):
    result = request(Request(
        method='POST',
        url='/api/script/saveOrUpdate',
        data=data
    ))
    return result




# def GetTasklist(name=str,DAY=int):
#     data={ 'getinfo':name,'Day':DAY}
#     return getScript(data)['data']['records']


def creatScript(data):
    result = request(Request(
        method='POST',
        url='/api/script/CreatScript',
        data=data
    ))
    return result

def Scriptsum(subtitlepronunciation=None):
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'subtitlepronunciation': subtitlepronunciation,
        'status': 'Unfinished',
            }
        scripts=getScript(data)
        records = scripts['data']['records']
        sum.extend(records)
        if scripts['data']['pages']<=n:
            return sum
        n+=1

