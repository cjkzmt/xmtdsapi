from src.utils.OsPath import *
from src.utils.Ffmpeg import *
def worker(item):
    try:
        ExecuteTask = {
            'split': Split,
            'Mirror': Mirror,
            'trim': Trim}
        ExecuteTask[item[0]](item[1])
    except Exception as e:
        print(f"Error executing task {item}: {e}")

def 视频处理():
    TaskList = 视频处理任务()
    if not TaskList: return False
    for item in TaskList:
        worker(item)
    return True

def 视频处理任务():
    视频高= int(os.getenv('视频高'))
    视频宽= int(os.getenv('视频宽'))
    RootDirectory=os.getenv("RootDirectory")
    视频类型=tuple(os.getenv("视频类型").split(","))
    Mirror=os.path.join(RootDirectory,'Content','TemporaryFootage',"Mirror") 
    os.makedirs(Mirror, exist_ok=True)
    TaskList=[]
    for r, __, fs in os.walk(Mirror):
        wpath=os.path.join(r, '镜像完成.txt')
        if os.path.exists(wpath): continue
        TaskListsum=len(TaskList)
        for f in fs:
            if '_Mirror' in f: continue
            if not f.endswith(视频类型): continue
            name = os.path.splitext(f)[0]
            path=os.path.join(r, f)
            path_Mirror=os.path.join(r,f'{name}_Mirror.mp4')
            if os.path.exists(path_Mirror):continue
            TaskList.append(('Mirror',(path,path_Mirror)))
        if len(TaskList)==TaskListsum:
            with open(wpath, 'w') as f:pass  
    Split = os.path.join(RootDirectory,'Content','TemporaryFootage',"Split")
    ToTrim = os.path.join(Split,'ToTrim')
    for r, __, fs in os.walk(ToTrim):
        wpath=os.path.join(r, '待裁完成.txt')
        if os.path.exists(wpath): continue
        TaskListsum=len(TaskList)
        for f in fs:
            if not f.endswith(视频类型):continue
            path=os.path.join(r, f)
            时长=getVoideDuration(path)
            original_width, original_height = getVoideSize(path)
            if original_width==视频宽 and original_height==视频高:continue
            base_name=os.path.splitext(f)[0]
            新路径=r.replace('Split', 'Trim')
            os.makedirs(新路径, exist_ok=True)
            原宽 = getVoideSize(path)[0]
            比例 = 原宽 / 视频宽
            if 比例 > 1.5: 
                left_path=os.path.join(新路径, f'{base_name}_left.mp4')
                if not os.path.exists(left_path): 
                    TaskList.append(('trim',(path,  视频宽, 视频高,  left_path, 'left')))
                right_path=os.path.join(新路径, f'{base_name}_right.mp4')
                if not os.path.exists(right_path): 
                    TaskList.append(('trim',(path,  视频宽, 视频高,  right_path, 'right')))
            if 比例 >= 2.5 or 比例 < 1.5: 
                center_path=os.path.join(新路径, f'{base_name}_center.mp4')
                if not os.path.exists(center_path): 
                    TaskList.append(('trim',(path,  视频宽, 视频高,  center_path, 'center')))
        if len(TaskList)==TaskListsum:
            with open(wpath, 'w') as f:pass  
    素材目录=os.path.join(RootDirectory,'Content','RawFootage')
    for r, __, fs in os.walk(素材目录):
        for f in fs:
            if not f.endswith(视频类型):continue
            name = os.path.splitext(f)[0]
            wpath = os.path.join(r, f'{name}.txt')
            if os.path.exists(wpath): continue
            path=os.path.join(r, f)
            时长=getVoideDuration(path)
            original_width, original_height = getVoideSize(path)
            if original_width is None or original_height is None:
                print(f"无法获取视频尺寸：{path}")
                continue
            if 时长 is None: return
            target_ratio = 视频宽 / 视频高
            original_ratio = original_width / original_height
            if original_ratio <= target_ratio: 
                输出高 = int((视频宽 / original_width) * original_height)
                输出宽 = 视频宽
            elif original_ratio > target_ratio: 
                输出宽 = int((视频高 / original_height) * original_width)
                输出高 = 视频高
            if 输出宽 % 2 != 0: 输出宽 -= 1
            if 输出高 % 2 != 0: 输出高 -= 1
            Footage=re.split(r'\\', r)[4]
            分割='Trimmed' if 输出高==视频高 and 输出宽 == 视频宽 else 'ToTrim'
            输出文件=os.path.join(Split,分割,Footage, name)
            # if 'ToTrim' in 输出文件:
            #     print(输出宽,输出高)
            #     print(输出文件)
            起始时间 = 结束时间 = 0.0
            i = 0
            n = 0
            分割分段=tuple(os.getenv("分割分段").split(",")) 
            TaskListsum=len(TaskList)
            while 结束时间 < 时长:
                分段时长 = int(分割分段[n % len(分割分段)])
                结束时间 = min(起始时间 + 分段时长, 时长)
                if 时长-结束时间<3:
                    结束时间=时长
                输出路径 = os.path.join(输出文件,str(分段时长), f"{name}_{i}.mp4")
                os.makedirs(os.path.dirname(输出路径), exist_ok=True)
                if not os.path.exists(输出路径): 
                    TaskList.append(('split',(path, 输出路径, 起始时间, 结束时间,输出宽,输出高)))
                起始时间 = 结束时间
                i += 1
                n += 1
            if len(TaskList)==TaskListsum:
                with open(wpath, 'w') as f:pass  
                with open(os.path.join(输出文件, '分割完成.txt'), 'w') as f:pass  
    return TaskList
            

