from src.task.Video.CreateVideo import CreateVideo
from src.task.Publish.PublishVideo import PublishVideo
from src.task.Text.Createline import Createline
from src.task.Text.Createtitle import Createtitle
from src.task.Text.Createcover import Createcover
from src.task.Text.Createreading import Createreading
from src.api.script import GetTasklist,getScript
from typing import Dict, Any, List,Tuple 
import os

ExecuteTask = {
    'line':    Createline,
    'title':   Createtitle,
    'cover':   Createcover,
    'reading': Createreading,

}

task_set = set()
task_id_set = set()
def fetch_new_tasks(max_task=None) -> List[Dict[str, Any]]:
    cpu_cnt = os.cpu_count() or 4
    max_task =max_task if max_task else max(1, cpu_cnt - 1)
    used_ids = list(task_id_set)
    print(f'used_ids: {used_ids}')
    raw = GetTasklist({'pageSize': max_task*2, 'unScripList': used_ids})['data']
    print(f'raw: {raw}')
    print(f'used_ids: {[t['id'] for t in raw]}')
    new_tasks=[]
    for t in raw:
        id=t['id']
        taskname = t['taskname']
        tt=taskname+str(id)
        if tt not in task_set:
            new_tasks.append(t)
            task_set.add(tt)
            task_id_set.add(id)
    return new_tasks

def worker(task: Dict[str, Any]) ->Tuple[bool, int]:
    id = task['id']
    taskname = task['taskname']
    info = getScript({'id': id})['data']['records'][0]
    #print(info)
    return  ExecuteTask[taskname](info),task

