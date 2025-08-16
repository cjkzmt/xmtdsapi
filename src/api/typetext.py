
from src.utils.request import *
# 示例用法
def getTypeText():
    result = request(Request(
        method='GET',
        url='/api/typetext/getAll',
    ))
    return result

def UpdateTypeText(data):
    result = request(Request(
        method='POST',
        url='/api/typetext/saveOrUpdate',
        data=data
    ))
    return result