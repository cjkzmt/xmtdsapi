
from src.utils.request import *
from src.api.TypeSubtitle import getTypeSubtitlelist
# 示例用法
def getAccountTeam(data):
    result = request(Request(
        method='POST',
        url='/api/accountteam/getPages',
        data=data
    ))
    return result

def UpdateAccountTeam(data):
    result = request(Request(
        method='POST',
        url='/api/accountteam/saveOrUpdate',
        data=data
    ))
    return result


def AccountTeamsum(id=None):
    sum=[]
    n=1
    while True:
        data={
        'AccountTeamId':id if id else None,
        'currentPage':n,
        'status': 'ENABLE'}
        AccountTeams=getAccountTeam(data)
        records = AccountTeams['data']['records']
        sum.extend(records)
        if AccountTeams['data']['pages']==n:
            return sum
        n+=1