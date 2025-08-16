import os
import random
from openai import OpenAI
from src.api.aiapi import getAll
from src.api.apitoken import ApiTokenssum,forbidApiToken
from tkinter import messagebox
def 对话(Prompt,Within=None,Outside=None,Token=None):
    #print(f'Prompt:{Prompt}')
    可用模型=[]

    for iteam in AiApi:
        name=iteam['name']
        if Outside and name in Outside: continue
        if Within and name not in Within: continue
        可用模型.append(iteam)
    
    if len(可用模型)==0: 
        print("没有可用的AI")
        return None,'没有可用的AI',None
    #print(f'可用模型:{可用模型}')
    AIiteam=random.choice(可用模型)
    # print(f'可用模型:{AIiteam}')
    
    AI名=AIiteam['name']
    AiId=AIiteam['id']
    端口=AIiteam['port']
    模型=AIiteam['model']
    # print('-'*80)
    # print(Token)
    if Token:
        print('+'*80)
        print('使用指定token')
        # forbidApiToken(ApiTokenId)
        token=Token
        ApiTokenId=0
    else:
        # print('*'*80)
        # print(Tokens)
        tokens = [t for t in Tokens if t['AiApi_id'] == AiId]
        # print(f'tokens:{tokens}')
        tokeniteam=random.choice(tokens)
        token=tokeniteam['token']
        ApiTokenId=tokeniteam['id']
    # print('/'*80)
    apiulr=os.getenv(f"apiulr")
    # print(f'模型:{模型}{AI名}{token}' )
    url=f"http://{apiulr}:800{端口}/v1"
    # print(f'AI名:{AI名},ApiTokenId:{ApiTokenId}')
    client = OpenAI(
        base_url=url, 
        api_key=token
    )
    messages = [
        {"role": "user", "content": Prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=模型,
            messages=messages,
            stream=False  
        )
        # print(response)
        答案=response.choices[0].message.content
        # print(答案)
        return 答案,AI名,ApiTokenId
    except Exception as e:
        #print('------------------------ai错误-------------------------------------------')
        
        error_msg = str(e)
        if 'Connection error' in error_msg:

            messagebox.showinfo("提示", "未开启AI 服务器")
            exit()
        #print(f'错误信息: {error_msg}')
        if hasattr(e, 'response'):
            error_msg += f" | Status: {e.response.status_code} | Body: {e.response.text}"
        #print(f"Error: {error_msg}")
        #print(f"{AI名}/{端口}/{模型}/{token}/{ApiTokenId}")

        return None,AI名,ApiTokenId

AiApi=getAll()
Tokens=ApiTokenssum()
if len(Tokens)==0:
    print("'没有可用的api token'")
    exit()

def AI对话(Prompt,a=None,r=None):
    #print(f'Prompt:{Prompt}')
    r= r or ''
    while True:
        答案,AI名,ApiTokenId=对话(Prompt,a,r)
        print(f'答案:{答案},AI名:{AI名},ApiTokenId:{ApiTokenId}')
        if '没有可用的AI'==AI名:
            return None
        if ApiTokenId=='没有可用的api token':
            r+=AI名
        elif 答案 is None: 
            forbidApiToken(ApiTokenId)
        elif '内容由于不合规被停止生成，我们换个话题吧' in 答案: r+=AI名
        elif 答案 and'服务器繁忙，请稍后再试。' not in 答案: return 答案
    