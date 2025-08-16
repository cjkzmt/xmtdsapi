
from src.AI.豆包AI import 豆包AI
from src.api.urltext import Updateurltexts
from src.api.topiccopy import *

def Executeurltext(urltextList,TypeTextId):
    for urltext in urltextList:
        url = urltext['url']
        提示词=f'{url}\n提取链接里的视频文案,只输出【视频文案】'
        答案=豆包AI(提示词,1)
        if '【视频文案】' in 答案:
            答案=答案.replace('【视频文案】','').strip()
        print(答案)
        topiccopy_data={
            'text':答案,
            'TypeTextId': TypeTextId,
            'Source': 'urltext',
            'SourceId': urltext['id'],
        }
        try:
            response = Updatetopiccopy(topiccopy_data)
            print(response)
            if 'code'in response:
                print('_'*80)

            urltext_data = {
                'id': urltext['id'],
                'status': 'finished',
            }
            Updateurltexts(urltext_data)

        except Exception as e:
            print(f"An error occurred: {e}")

