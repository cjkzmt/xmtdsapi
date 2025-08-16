
from src.utils.request import *
# 示例用法
def getTeamOwner(data):
    result = request(Request(
        method='POST',
        url='/api/teamowner/getPages',
        data=data
    ))
    return result
def UpdateclipSum(data):
    result = request(Request(
        method='POST',
        url='/api/teamowner/UpdateclipSum',
        data=data
    ))
    return result

def UpdateTeamOwner(data):
    result = request(Request(
        method='POST',
        url='/api/teamowner/saveOrUpdate',
        data=data
    ))
    return result

def TeamOwnersum():
    sum=[]
    n=1
    while True:
        data={
        'currentPage':n,
        'status': 'ENABLE',
            }
        TeamOwners=getTeamOwner(data)
        records = TeamOwners['data']['records']
        sum.extend(records)
        if TeamOwners['data']['pages']==n:
            return sum
        n+=1