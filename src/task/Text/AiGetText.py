from src.AI.Ollama import AI
from src.AI.AI_API import AI对话
def AiGetText(text:str)->str:
    提炼提示词=f'提取文案正文，删除非正文的的内容:【{text}】'
    return AI对话(提炼提示词)#AI(提炼提示词,'qwen2.5:72b')
