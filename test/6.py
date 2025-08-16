import os
import subprocess
from typing import List, Optional

def check_gpu_support() -> bool:
    """检查系统是否支持NVIDIA GPU加速"""
    try:
        subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def Merge(cliplist: List[str], 
          output_path: str,
          duration: Optional[float] = None, 
          audio: bool = True,
          music_path: Optional[str] = None,
          volume: float = 1.0) -> bool:
    """
    合并多个视频文件并添加可选背景音乐
    
    参数:
        cliplist: 视频文件路径列表
        output_path: 输出文件路径
        duration: 总时长(秒)。如果合并视频超过此时长则截断，None表示不限制
        audio: True保留原音频，False移除原音频
        music_path: 背景音乐路径，None表示不加背景音乐
        volume: 背景音乐音量(0.1-10.0)
    
    返回:
        bool: 是否合并成功
    """
    
    if not cliplist:
        raise ValueError("视频列表不能为空")
    
    if volume < 0.1 or volume > 10:
        raise ValueError("音量参数必须在0.1到10.0之间")
    
    # 1. 构造基础命令
    gpu_supported = check_gpu_support()
    cmd = ['ffmpeg', '-y']
    if gpu_supported:
        cmd.extend(['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda'])
    
    # 2. 添加所有输入视频
    inputs = []
    for video in cliplist:
        inputs.extend(['-i', video.strip('\x00')])
    
    # 3. 构建filter_complex
    filter_complex = []
    map_args = []
    
    # 视频合并
    filter_complex.append(f"concat=n={len(cliplist)}:v=1:a=0[vout]")
    map_args.extend(['-map', '[vout]'])
    
    # 音频处理
    if audio or music_path:
        # 如果有原音频
        if audio:
            filter_complex.append(f"concat=n={len(cliplist)}:v=0:a=1[aorig]")
        
        # 如果有背景音乐
        if music_path:
            inputs.extend(['-i', music_path])
            music_filter = f"volume={volume}"  # 音量调节
            if duration:  # 如果设置了总时长，循环音乐
                music_filter += ",aloop=loop=-1:size=1e9"
            music_filter += "[amusic]"
            filter_complex.append(music_filter)
            
            # 混合音频
            if audio:
                filter_complex.append("[aorig][amusic]amix=inputs=2:duration=first[aout]")
            else:
                filter_complex.append("[amusic]acopy[aout]")
            
            map_args.extend(['-map', '[aout]'])
        elif audio:
            filter_complex.append("[aorig]acopy[aout]")
            map_args.extend(['-map', '[aout]'])
    
    # 4. 构建完整命令
    cmd += inputs
    cmd += ['-filter_complex', ";".join(filter_complex)]
    cmd += map_args
    
    # 视频编码设置
    if gpu_supported:
        cmd.extend(['-c:v', 'h264_nvenc', '-preset', 'fast'])
    else:
        cmd.extend(['-c:v', 'libx264', '-preset', 'medium'])
    
    # 音频编码
    if audio or music_path:
        cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
    
    # 时长限制
    if duration:
        cmd.extend(['-t', str(duration)])
    
    # 输出文件
    cmd.append(output_path)
    
    # 5. 执行命令
    try:
        print("执行命令: " + " ".join(cmd))
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f"视频合并成功: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print("视频合并失败:")
        print(e.stderr.decode(errors='ignore'))
        return False
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return False


# 使用示例
if __name__ == "__main__":
    # 示例1: 简单合并

    
    # 示例3: 限制时长并去除原声
    Merge(
        cliplist=['D:\\新媒体大师\\素材\\视频请放这里\\已用视频\\142\\1\\xyq\\WeChat_20240420151701_2_Mirror.mp4'],
        output_path=r"D:\新媒体大师\素材\视频请放这里\已用视频\142\1.mp4",
        duration=2.05,
        audio=False,
        music_path=r"D:\新媒体大师\素材\其他素材\音频\在这新年之际，祝大家新年快乐\改造真没啥复杂的.wav"
    )