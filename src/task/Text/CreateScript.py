
from src.api.topiccopy import TopicCopysum
from src.api.accountteam import AccountTeamsum,getAccountTeam
from src.api.prompttext import PromptTextsum
from src.api.script import getScript,creatScript,UpdateScript,Scriptsum
from src.api.topiccopy import gettopiccopy
from src.api.prompttext import getPromptText
from src.AI.AI_API import AI对话
from src.AI.Ollama import AI
from src.utils.KeyValue import Kv
from src.ExecuteTask.Executeurltext import Executeurltext

def CreateScript(Info):
    print(f'开始执行任务：脚本文案任务')
    print(f'任务参数：{Info}')