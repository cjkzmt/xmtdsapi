
from src.api.script import UpdateScript
from src.AI.AI_API import AI对话
from .GetTaskFont import GetTaskFont
from .GetTaskMusic import GetTaskMusic
from .GetTaskOver import GetTaskOver
from src.utils.LOG import *
from .AiGetText import AiGetText
def Createline(Info)->bool:
    try:
        print(f"开始生成文案{Info['id']}")
        Info=GetTaskFont(Info)
        Info=GetTaskMusic(Info)
        Info=GetTaskOver(Info)
        drafline=Info['drafline']
        print(f'-{drafline}-')
        print(f"-"*80)
        if drafline  is None:
            print("无文案")
            topictext=Info['topictext']
            copytext=Info['copytext']
            promptText=Info['promptText']
            scope=Info['scope']
            ai_prompt=f'选题：【{topictext}】业务范围为：{scope},如果新文案中需要提到地理位置。酌情替换{promptText}【{copytext}】只输出新【文案】，不要多余的话'
            print("ai_prompt:"+ai_prompt)
            drafline=AI对话(ai_prompt,'deepseek')
            #logger.info(f"脚本文案{drafline}")
            data={'id':Info["id"],"drafline":drafline}
            UpdateScript(data)
        line=AiGetText(drafline)
        data={'id':Info["id"],"line":line}
        UpdateScript(data)
        print(f"✅ {Info["id"]}的 脚本")
        return True
    except Exception as e:
        #print(e)
        return False
