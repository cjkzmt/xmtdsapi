
from src.utils.request import *
# 示例用法
def TopIteams():
    result = request(Request(
        method='GET',
        url='/api/pnumber/TopIteams',
    ))
    return result['data']



