from src.AI.Ollama import AI
from src.AI.AI_API import AI对话
from src.utils.KeyValue import Kv
from src.api.script import UpdateScript
from src.utils.Str import 数转汉,RemovePunctuation
from src.utils.Image import get_str_info
import re
import os

尾='''关注我 我来帮你
城里有楼 乡下有院'''

def 短句合并(b):
    视频字体=os.getenv("视频字体")
    字幕字号=int(os.getenv("字幕字号"))
    总宽=int(os.getenv("视频宽"))
    i = 0
    while i < len(b) - 1:
        nq=get_str_info(b[i]+" "+b[i+1], 字幕字号,视频字体)[0]
        if nq < 总宽 or len(b[i]) < 5 or len(b[i+1]) < 5: 
            b[i] += " " + b.pop(i + 1)
        else: i += 1
    return b
def 去除短句(b):
    i = 0
    while i < len(b) - 1:
        if  len(b[i]) < 6 or len(b[i+1]) < 6: 
            b[i] += " " + b.pop(i + 1)
        else: i += 1
    b = [m.strip() for m in b if m.strip()]
    return b

def AI拆分(b):
    视频字体=os.getenv("视频字体")
    字幕字号=int(os.getenv("字幕字号"))
    总宽=int(os.getenv("视频宽"))
    while True:
        bb=b.split(" ")
        完成=True
        for n, item in enumerate(bb): 
            if get_str_info(item, 字幕字号,视频字体)[0]>总宽:
                完成=False
                t=f'''给以下【文案】断句：
                1、总字数不变。
                2、【第一句】、【第二句】字数相近
                3、每句话不得少于6个字
                文案：【{item}】
                直接输出结果【第一句】、【第二句】
                '''
                答案=AI对话(t)
                try:
                    if '【第一句】' in 答案:
                        答案=答案.split('第一句')[1]
                        bqb=答案.split("第二句")
                    else:
                        ww=答案.split("【",1)[1]
                        bqb=ww.split("】")[:-1]
                    for i, t in enumerate(bqb): bqb[i]=RemovePunctuation(t)
                    bqb=去除短句(bqb)
                    bb[n]=" ".join(bqb)
                except IndexError:
                    bb[n]=item
        b=" ".join(bb)
        if 完成: return b
        #print(b)

def 拆分(b):
    视频字体=os.getenv("视频字体")
    字幕字号=int(os.getenv("字幕字号"))
    视频宽=int(os.getenv("视频宽"))
    字幕拆分标点=os.getenv("字幕拆分标点")
    # #print(视频字体)
    # #print(字幕字号)
    # #print(视频宽)
    # #print(字幕拆分标点)
    for bd in 字幕拆分标点:
        c=[]
        for item in b:
            item=item.strip()
            if item=="": continue
            if get_str_info(item, 字幕字号,视频字体)[0]<视频宽:
                c.append(item)
                continue
            if bd not in item:
                c.append(item)
                continue
            bb=item.split(bd)
            bb=短句合并(bb)
            for s in bb:
                s=s.strip()
                if s=="": continue
                c.append(s)
        b=c
    return b
def create_subtitle(subtitlecopy):
    subtitlecopy = re.sub(r'[✅🛳️🏖️🚀️⃣]■*', ' ', subtitlecopy)
    subtitlecopy = re.sub(r'\s*-\s*', '-', subtitlecopy)
    b=subtitlecopy.split('\n')
    字幕s=拆分(b)
    for i, t in enumerate(字幕s): 字幕s[i]=RemovePunctuation(t)
    for i, t in enumerate(字幕s): 字幕s[i]=AI拆分(t)
    subtitles='\n'.join(字幕s)
    if 尾 not in subtitles: subtitles+="\n"+尾
    return subtitles

def 提示词封面(t):
    return f'''文案：【{t}】假设你是一个专业的自媒体专家。
我是一个旧房改造装修公司，通过抖音短视频找吸引客户咨询。
给写好的【文案】写 【标题第一句】、【标题第二句】为了帮助你进行这项任务，请参考以下加强建议：
写【标题第一句】、【标题第二句】的要求.
1、【标题第一句】、【标题第二句】两句话组成一个完成的意思。
2、【标题第一句】、【标题第二句】必须在14字以内
3、要求吸引眼球，
请依照上述建议，根据【文案】开始你的创作
分别输出【标题第一句】、【标题第二句】
'''
def 替换至(text):
    # 使用正则表达式进行替换
    #添加 5% -7%
    pattern = r"(\d+%?)-(\d+%?)"  # #添加 1.2% - 21%在 - 左右可能有空格
    replacement = lambda match: f"{match.group(1)}至{match.group(2)}"  # 动态替换为 "数字至数字"
    return re.sub(pattern, replacement, text)
def 替换分之(text):
    pattern = r"(\d+%?)/(\d+%?)"  # 匹配形如 "数字-数字" 的模式
    replacement = lambda match: f"{match.group(2)}分之{match.group(1)}"  # 动态替换为 "数字至数字"
    return re.sub(pattern, replacement, text)
def 替换百分号(text):
    pattern = r"(\d+(\.\d+)?%?)%" 
    replacement = lambda match: f"百分之{match.group(1)}"
    return re.sub(pattern, replacement, text)
def 转数字(t):
    t = t.replace('985', '九八五')
    t = t.replace('BUFF', '霸福')
    t = t.replace('BUG', '霸哥')
    t = t.replace('211', '二幺幺')
    t = t.replace('996', '九九六')
    t = t.replace('kg', '千克')
    t = t.replace('+', '加')
    t = t.replace('=', '等于')
    t = t.replace('≠', '不等于')
    t = t.replace('℃', '度')
    t = t.replace('battle', '掰头')
    t = t.replace('€', '欧')
    t = t.replace('㎡', '平米')
    t = 替换至(t)
    t = 替换分之(t)
    t = 替换百分号(t)
    def replace(match):
        num = match.group()
        position = match.end()
        unit = t[position] if position < len(t) else ""
        return 数转汉(num, unit)
    t = re.sub(r'\d+\/\d+|\d+(\.\d+)?', replace, t)#加上能识别4-6
    t = t.replace('/', ' ')
    return t

def Getsubtitle(Info):
    subtitle=Info['subtitle']
    if subtitle:return Info
    Font_Path=os.path.join(os.getenv("RootDirectory"),os.getenv('FontDirectory')) 
    os.environ['视频字体'] = os.path.join(Font_Path, Info["Font"])
    os.environ['字幕字号'] = str(Info["fontsize"])  # 确保为字符串
    os.environ['视频宽'] = str(Info["videowidth"])  # 确保为字符串
    #print(f'开始获取__显示字幕：{Info["id"]}')
    subtitle= create_subtitle(Info['line'])
    
    data={'id':Info["id"],"subtitle":subtitle}
    UpdateScript(data)
    Info['subtitle']=subtitle
    return Info
def Createreading(Info):
    try:  
        #print(f'开始获取__字幕/读音：{Info["id"]}')
        Info=Getsubtitle(Info)
        
        subtitle=Info['subtitle']
        reading=Info['reading']
        if reading and subtitle:return True
        #print(f'开始获取__字幕读音：{Info["id"]}')
        reading=转数字(subtitle)
        data={'id':Info["id"],"reading":reading}
        UpdateScript(data)

        print(f"✅ {Info["id"]}的 读音")
        return True
    except Exception as e:
        #print(e)
        return False


