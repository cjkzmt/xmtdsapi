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

def Verification():
    # 获取硬件序列号
    cpu_serial = get_hardware_serial_number(['wmic', 'cpu', 'get', 'processorid'])
    hdd_serial = get_hardware_serial_number(['wmic', 'diskdrive', 'where', 'index=0', 'get', 'serialnumber'])
    motherboard_serial = get_hardware_serial_number(['wmic', 'baseboard', 'get', 'serialnumber'])

    # 检查是否成功获取所有序列号
    if cpu_serial and hdd_serial and motherboard_serial:
        # 生成唯一识别码
        unique_id = generate_unique_id([cpu_serial, hdd_serial, motherboard_serial])
        #print(f"The unique hardware ID is: {unique_id}")
        return str(unique_id)
    else:
        print("Failed to retrieve all hardware serial numbers.")
        return None

if __name__ == '__main__':
    pass
