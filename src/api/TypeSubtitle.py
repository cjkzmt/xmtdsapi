from src.utils.request import *
def getTypeSubtitlelist(id=None):
    result = request(Request(
        method='GET',
        url='/api/typesubtitle/getAll',
        params={'id': id}
    ))
    return result