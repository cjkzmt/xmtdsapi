from src.AI.AI_API import AI对话
from src.AI.Ollama import AI
from src.utils.KeyValue import Kv
from src.api.script import UpdateScript
from typing import Tuple 
from .AiGetText import AiGetText
def 提示词描述(t):
    return f'''假设你是一个专业的自媒体专家。
我是一家旧房改造装修公司，通过抖音短视频找吸引客户咨询。
给写好的【文案】写【描述】为了帮助你进行这项任务，请参考以下加强建议：
写【描述】的要求：
1、一句话说明白这件事情
2、要求吸引眼球，
3、突出【文案】的重点，
4、言简意赅。
只输出新【描述】，不要多余的话
以下是文案：【{t}】
'''
def Createtitle(Info)->Tuple[bool, int]:
    try:
        draftitle=Info['draftitle']
        title=Info['title']
        if title:return True
        if draftitle is None:
            draftitle= AI对话(提示词描述(Info['line']))
            data={'id':Info["id"],"draftitle":draftitle}
            UpdateScript(data)
        title=AiGetText(draftitle)
        data={'id':Info["id"],"title":title}
        UpdateScript(data)
        print(f"✅ {Info["id"]}的 标题描述：更新完成{title} ")
        return True
    except Exception as e:
        #print(e)
        return False
    


