
from src.utils.request import *
# 示例用法
def getAllKeyword():
    result = request(Request(
        method='GET',
        url='/api/keyword/getAll',
    ))
    return result['data']

def Updateaiapi(data):
    result = request(Request(
        method='POST',
        url='/api/aiapi/saveOrUpdate',
        data=data
    ))
    return result