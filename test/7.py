import subprocess

GPU_SUPPORTED = True

def merge_video(cliplist, output_path, duration=None, audio=True):
    """
    合并视频文件（自动处理有无音频流的情况）
    :param cliplist: 视频文件路径列表
    :param output_path: 输出文件路径
    :param duration: 限制输出时长（秒）
    :param audio: 是否包含音频流（True/False）
    """
    # 1. 构建输入参数
    inputs = []
    for v in cliplist:
        inputs += ['-i', v.strip('\x00')]

    # 2. 检测音频流
    audio_streams = []
    if audio:  # 只有需要音频时才检测
        for i, input_file in enumerate(cliplist):
            # 使用ffprobe检测是否有音频流
            cmd = [
                'ffprobe', '-v', 'error', '-select_streams', 'a',
                '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', input_file
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stdout.decode().strip() == 'audio':
                audio_streams.append(i)

    # 3. 构建滤镜图
    # 视频部分（所有输入都有视频流）
    video_filter = f"{  ''.join([f'[{i}:v]' for i in range(len(cliplist))])}concat=n={len(cliplist)}:v=1:a=0[v]"
    
    # 音频部分（只有有音频的输入才处理）
    if audio and audio_streams:
        audio_filter = f"{' '.join([f'[{i}:a]' for i in audio_streams])}concat=n={len(audio_streams)}:v=0:a=1[a]"
        filter_complex = f"{video_filter};{audio_filter}"
        map_audio = ['-map', '[a]']
    else:
        filter_complex = video_filter
        map_audio = []

    # 4. 构建完整命令
    cmd = ['ffmpeg', '-y']
    if GPU_SUPPORTED:
        cmd.extend(['-hwaccel', 'cuda'])
    
    cmd += inputs + [
        '-filter_complex', filter_complex,
        '-map', '[v]',
        *map_audio,
        '-c:v', 'h264_nvenc' if GPU_SUPPORTED else 'libx264',
    ]
    
    if audio and audio_streams:
        cmd.extend(['-c:a', 'aac'])
    
    if duration:
        cmd.extend(['-t', str(duration)])
    
    cmd.append(output_path)
    silent=True
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL if silent else None,
            stderr=subprocess.DEVNULL if silent else None
        )

        print(f"视频合并成功: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"视频合并失败: {e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}")
        return False












# 使用示例
if __name__ == "__main__":
    clips = [
        r'D:\XMTDS\Content\VideoContent\UsedFootage\142\20\xyq\91b51e39c5e41f9b9ec59b4bf896e74c_19.mp4',
        r'D:\XMTDS\Content\VideoContent\UsedFootage\142\20\xyq\WeChat_20240909175203_0_center.mp4'
    ]
    output = r'D:\XMTDS\Content\VideoContent\UsedFootage\142\20_output2.mp4'
    merge_video(clips, output, duration=3.82,audio=False)