import psutil
import GPUtil
import subprocess
import hashlib

def get_hardware_serial_number(command):
    """执行wmic命令并返回硬件序列号"""
    try:
        # 使用wmic命令获取硬件信息
        # 改用列表形式传递命令参数，增加安全性
        result = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
        # 处理输出结果，提取序列号
        return result.split('\n')[1].strip()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")
        return None

def generate_unique_id(parts):
    """根据硬件序列号生成唯一识别码（MD5）"""
    # 将序列号拼接为一个字符串
    unique_string = "-".join(parts)
    # 使用MD5生成哈希值
    md5_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    return md5_hash

def 硬件序列号():
    # 获取硬件序列号
    cpu_serial = get_hardware_serial_number(['wmic', 'cpu', 'get', 'processorid'])
    hdd_serial = get_hardware_serial_number(['wmic', 'diskdrive', 'where', 'index=0', 'get', 'serialnumber'])
    motherboard_serial = get_hardware_serial_number(['wmic', 'baseboard', 'get', 'serialnumber'])
    # print(f"CPU Serial: {cpu_serial}")
    # print(f"HDD Serial: {hdd_serial}")
    # print(f"Motherboard Serial: {motherboard_serial}")

    # 检查是否成功获取所有序列号
    if cpu_serial and hdd_serial and motherboard_serial:
        # 生成唯一识别码
        unique_id = generate_unique_id([cpu_serial, hdd_serial, motherboard_serial])
        #print(f"The unique hardware ID is: {unique_id}")
        return str(unique_id)
    else:
        print("Failed to retrieve all hardware serial numbers.")
        return None

def get_PC_info():
    内存 = f"{psutil.virtual_memory().total / (1024**3):.2f}"  # 总内存（GB）
    线程 = psutil.cpu_count(logical=True)  # 逻辑处理器数量（线程数）

    # 获取显存（假设是 NVIDIA GPU）
    try:
        gpus = GPUtil.getGPUs()
        显存 = f"{gpus[0].memoryTotal}" if gpus else 0
    except Exception:
        显存 = "无法获取"
    
    return 线程,内存,显存,硬件序列号()

import psutil
import GPUtil
import time

def get_system_info():
    # 获取CPU使用情况
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_cores = psutil.cpu_count(logical=False)

    # 获取内存使用情况
    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 ** 3)
    memory_used = memory.used / (1024 ** 3)
    memory_usage = memory.percent

    print(f"CPU使用率: {cpu_usage}%")
    print(f"CPU线程数: {cpu_threads}")
    print(f"物理核心数: {cpu_cores}")
    print(f"内存总量: {memory_total:.2f} GB")
    print(f"已用内存: {memory_used:.2f} GB")
    print(f"内存使用率: {memory_usage}%")

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"GPU ID: {gpu.id}")
        print(f"GPU名称: {gpu.name}")
        print(f"GPU负载: {gpu.load * 100:.2f}%")
        print(f"显存总量: {gpu.memoryTotal} MB")
        print(f"已用显存: {gpu.memoryUsed} MB")
        print(f"显存使用率: {gpu.memoryUtil * 100:.2f}%")
        print(f"显存温度: {gpu.temperature}°C")
        print("-" * 40)



if __name__ == '__main__':
    pass
    # 实时更新
    while True:
        print("系统信息：")
        get_system_info()
        print("显卡信息：")
        get_gpu_info()
        time.sleep(1)  # 每隔1秒更新一次
