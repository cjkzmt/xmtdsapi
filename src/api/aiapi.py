
from src.utils.request import *
# 示例用法
def getAll():
    result = request(Request(
        method='GET',
        url='/api/aiapi/getAll',
    ))
    return result['data']

def Updateaiapi(data):
    result = request(Request(
        method='POST',
        url='/api/aiapi/saveOrUpdate',
        data=data
    ))
    return result