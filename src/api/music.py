
from src.utils.request import *
def saveMusicList(data):
    result = request(Request(
        method='POST',
        url='/api/music/saveList',
        data=data
    ))
    return result

def getMusic(data):
    result = request(Request(
        method='POST',
        url='/api/music/getPages',
        data=data
    ))
    return result



def Musicsum(MusicId=None):
    sum=[]
    n=1
    while True:
        data={
            'MusicId':MusicId if MusicId else None,
            'currentPage':n,
            'status': 'ENABLE'}
        Musics=getMusic(data)
        records = Musics['data']['records']
        sum.extend(records)
        if Musics['data']['pages']==n:
            return sum
        n+=1

