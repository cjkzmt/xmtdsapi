from src.AI.Ollama import AI
from src.AI.AI_API import AI对话
from src.utils.KeyValue import Kv
from src.api.script import UpdateScript
import re
from src.utils.Str import RemovePunctuation
def 提示词封面(t):
    return f'''假设你是一个专业的自媒体专家。
我是一家旧房改造装修公司，通过抖音短视频找吸引客户咨询。
给写好的【文案】写 【标题第一句】、【标题第二句】为了帮助你进行这项任务，请参考以下加强建议：
写【标题第一句】、【标题第二句】的要求.
1、【标题第一句】、【标题第二句】两句话组成一个完成的意思。
2、【标题第一句】、【标题第二句】必须在14字以内
3、要求吸引眼球，
请依照上述建议，根据【文案】开始你的创作
分别输出【标题第一句】、【标题第二句】
以下是文案：【{t}】
'''
def create_cover(subtitlecopy):
    t=提示词封面(subtitlecopy)
    标题第一句=标题第二句=''
    while True:
        答案=AI对话(t)#对话
        if 答案:
            try:
                if '第一句' in 答案:
                    for b in 答案.split('\n'):
                        if '标题第一句' in b: 
                            标题第一句 = b.replace('标题第一句', '').strip()
                        if '标题第二句' in b: 
                            标题第二句 = b.replace('标题第二句', '').strip()
                else:
                    ww=答案.split("【",1)[1]
                    bqb=ww.split("】")[:-1]
                    if len(bqb)==1: 
                        标题第一句,标题第二句=bqb[0].split(',')
                    else: 
                        标题第一句,标题第二句=bqb
                标题第一句 = re.sub(r'[【】：: ！？，]|标题第一句,', '', 标题第一句).strip()
                标题第二句 = re.sub(r'[【】：: ！？，]|标题第二句,', '', 标题第二句).strip()
                if 3<len(标题第一句)<15 and 3<len(标题第二句)<15:
                     return 答案,(标题第一句 + '\n' + 标题第二句)
                ##print(答案)
            except Exception as e:
                print(f'错误：{e} {答案}')
                pass
                ##

def Createcover(Info):
    try:
        #print(f'开始获取__封面：{Info["id"]}')
        cover=Info['cover']
        # print(f"开始获取__封面：{Info['id']}")
        # print(cover)
        if cover:return True
        drafcover,cover=create_cover(Info['line'])
        print(f"✅ {drafcover}的 封面：{cover} ")
        cover=RemovePunctuation(cover)
        data={'id':Info["id"],"cover":cover,"drafcover":drafcover}
        UpdateScript(data)

        print(f"✅ {Info["id"]}的 封面：更新完成{cover} ")
        return True
    except Exception as e:
        ##print(e)
        return False

