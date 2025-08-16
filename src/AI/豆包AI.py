
from src.utils.browser import *
import os
def 豆包AI(prompt,编号=None):
    try:
        主文件=os.getenv('主文件')
        AI目录=os.getenv('AI目录')
        目录=None if 编号 is None else os.path.join(主文件,AI目录) 
        page=signbrowser(目录,编号)
        url=os.getenv('官网doubao')
        tab=signurl(page,url)
        tab('tag=textarea').input(prompt)
        tab('#flow-end-msg-send').click()
        tab.wait(3)
        while len(tab.eles('@data-testid=message_content'))<2: tab.wait(1)
        while True:
            答案=tab.eles('@data-testid=message_content')[-1].text
            tab.wait(2)
            答案2=tab.eles('@data-testid=message_content')[-1].text
            if 答案==答案2:return 答案
    except Ellipsis as e: 
        print(f'豆包/{编号}/{e}')
        return None
if __name__=='__main__':
    import os
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".evn")
    load_dotenv(dotenv_path=dotenv_path)
    x=豆包AI('https://www.douyin.com/video/7495411932522876211\n提取链接里的视频文案,只输出【视频文案】')
    print(x)
