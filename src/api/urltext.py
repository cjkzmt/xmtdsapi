
from src.utils.request import *
# 示例用法
def geturltexts():
    result = request(Request(
        method='POST',
        url='/api/urltext/getPages',
        data={
            'status': 'Unfinished',
        }
    ))
    return result

def Updateurltexts(data):
    result = request(Request(
        method='POST',
        url='/api/urltext/saveOrUpdate',
        data=data
    ))
    return result