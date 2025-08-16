import os, shutil
import re
import multiprocessing
from pathlib import Path

def 文件夹移动(path1, path2):
    path1 = Path(path1)
    path2 = Path(path2)
    移动表 = []
    for src_file in path1.rglob('*'):
        if src_file.is_file():
            dst_file = path2 / src_file.relative_to(path1)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            移动表.append((src_file, dst_file))
    with multiprocessing.Pool() as pool:
        pool.starmap(文件移动, 移动表)

def 文件移动(path1, path2):
    if path1 == path2: return
    path1 = Path(path1)
    path2 = Path(path2)
    if path2.exists():
        print(f"目标路径 {path2} 已存在，跳过移动。")
        删除文件(path1)
        return
    path2.parent.mkdir(parents=True, exist_ok=True)
    try: 
        shutil.move(str(path1), str(path2)) 
        # print(f"文件移动成功： {path1} to {path2}")
    except Exception as e:
        print(f"文件移动失败： {path1} to {path2}: {e}")
        
def 删除空文件(directory):
    for root, dirs, __ in os.walk(directory, topdown=False):
        for dir in dirs:
            path = os.path.join(root, dir)
            try: os.rmdir(path)
            except OSError as e: pass 
def 删除文件(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass
def 文件路径(p): return os.path.dirname(p)
def 文件名拓(p): return  os.path.basename(p)
def 文件名(p): return os.path.splitext(文件名拓(p))[0]
def 文件拓(p): return  os.path.splitext(文件名拓(p))[1]
def parse_path(path):
    try:
        if not path or not isinstance(path, str): return None, None, "", ""
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path): return None, None, "", ""
        if os.path.isfile(path): (name,extension),dir_path = os.path.splitext(os.path.basename(path)), os.path.dirname(path)
        elif os.path.isdir(abs_path): name,extension,dir_path = "", "",abs_path
        else: return None, None ,"", ""
        disk, file_path = os.path.splitdrive(dir_path)
        return disk, file_path, name, extension
    except Exception as e:return None, None, "", ""
def 视频类型(path): return re.split(r'_', parse_path(path)[2])[0]
if __name__ == '__main__':

    文件移动( r'D:\新媒体大师\素材\视频请放这里\xyq\小云雀_中式建筑环视之旅_1753084446297_0\3\小云雀_中式建筑环视之旅_1753084446297_0_1_Mirror.mp4', r'D:\新媒体大师\素材\原始素材\原视频\10\0\xyq\小云雀_中式建筑环视之旅_1753084446297_0_1_Mirror.mp4')
