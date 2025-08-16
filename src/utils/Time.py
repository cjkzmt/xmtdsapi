import pytz
from datetime import datetime
def convertTime(time_str):
    """
    将UTC时间字符串转换为北京时间
    
    Args:
        utc_time_str (str): UTC时间字符串，格式如 '2025-08-01 11:00:00+00:00'
    
    Returns:
        str: 北京时间，格式为 'YYYY-MM-DD HH:MM:SS'
    """
    # 解析时间字符串并转换为 UTC 时间
    utc_time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    
    # 设置时区为北京时间（UTC+8）
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_time.astimezone(beijing_tz)
    
    # 格式化为指定格式并返回
    x=beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
