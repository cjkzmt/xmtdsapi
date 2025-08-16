import os
import subprocess
GPU_SUPPORTED=False
def Merge(cliplist, output_path):
    """
    cliplist: 视频列表
    output_path: 合并后的输出路径
    """
    # 1. 构造输入列表：N 个视频
    inputs = []
    for v in cliplist:
        inputs += ['-i', v.strip('\x00')]

    # 2. 构造 filter_complex
    #   2.1 先把所有视频无音频 concat 成一路 [v]
    concat = f"concat=n={len(cliplist)}:v=1:a=0[v]"
    
    # 2.2 合并音频 (假设每个视频都有音频流)
    # 这里添加音频合并逻辑，比如:
    audio_concat = f"concat=n={len(cliplist)}:v=0:a=1[a]"
    
    filter_complex = f"{concat};{audio_concat}"

    # 3. 构造 ffmpeg 命令
    if GPU_SUPPORTED:
        cmd = ['ffmpeg', '-y', '-hwaccel', 'cuda']
    else:
        cmd = ['ffmpeg', '-y']

    cmd += inputs
    cmd += [
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'h264_nvenc' if GPU_SUPPORTED else 'libx264',
        '-c:a', 'aac',
        output_path  # Removed the undefined '-t' parameter
    ]
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print("合并成功：", output_path)
    except subprocess.CalledProcessError as e:
        print("合并失败：", e.stderr.decode(errors='ignore'))

if __name__ == "__main__":
    cliplist=['儿推第十二课外劳宫-阳池认识0.mp4', '儿推第十二课外劳宫-阳池认识1.mp4']
    output_path=r'D:\新媒体大师\17.mp4'
    Merge(cliplist, output_path)

