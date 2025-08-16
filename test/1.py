import subprocess
import os
from pathlib import Path

def speed_up_audio(input_path, output_path, speed=1.2):
    """
    加速音频文件（保持音调）
    :param input_path: 输入音频路径（如 input.mp3）
    :param output_path: 输出音频路径（如 output.wav）
    :param speed: 加速倍数（默认 1.2 倍）
    """
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        'ffmpeg', '-y',           # -y 覆盖输出文件
        '-i', input_path,         # 输入文件
        '-filter:a', f'atempo={speed}',  # 音频变速
        '-vn',                    # 禁用视频
        '-c:a', 'pcm_s16le',      # 编码为 WAV（16位PCM）
        '-ar', '44100',           # 采样率44.1kHz
        '-ac', '2',               # 双声道立体声
        output_path               # 输出文件
    ]
    
    try:
        # 检查FFmpeg是否可用
        subprocess.run(['ffmpeg', '-version'], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 运行命令，使用UTF-8编码处理输出
        result = subprocess.run(cmd, check=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              encoding='utf-8', 
                              errors='replace')
        
        print(f"✅ 音频加速成功：{output_path} ({speed}x)")
        return True
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        print(f"❌ 音频加速失败：{error_msg}")
        
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"⚠ 输入文件不存在：{input_path}")
            
        return False
    except FileNotFoundError:
        print("❌ 未找到FFmpeg，请先安装FFmpeg并添加到系统路径")
        return False
    except Exception as e:
        print(f"❌ 发生未知错误：{str(e)}")
        return False

# 使用示例
input_path = r'D:\XMTDS\Content\OtherContent\Audio\3\1\别总想着大富大贵 老屋亮堂 父母舒坦.wav' 
output_path = r'D:\XMTDS\Content\OtherContent\Audio\3\1.2\别总想着大富大贵 老屋亮堂 父母舒坦.wav'
speed = 1.2

# 确保输出目录存在
Path(output_path).parent.mkdir(parents=True, exist_ok=True)

speed_up_audio(input_path, output_path, speed)