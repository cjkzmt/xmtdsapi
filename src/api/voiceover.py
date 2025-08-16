
from src.utils.request import *
def saveVoiceOverList(data):
    result = request(Request(
        method='POST',
        url='/api/voiceover/saveList',
        data=data
    ))
    return result