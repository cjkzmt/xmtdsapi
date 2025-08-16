import os
import subprocess
import json
from time import sleep
GPU_SUPPORTED = False  

import time

def CheckPC():
    global GPU_SUPPORTED
    """返回检查结果字典和是否支持GPU加速"""
    检查结果 = {
        "NVIDIA驱动": False,
        "CUDA可用": False,
        "FFmpeg加速": False,
        "编码器支持": False,
        "显存充足": False
    }
    gpu_available = False

    try:
        # NVIDIA驱动检查
        nvidia_smi = subprocess.check_output(['nvidia-smi', '-L'], text=True, stderr=subprocess.DEVNULL)
        检查结果["NVIDIA驱动"] = "NVIDIA" in nvidia_smi

        # CUDA检查
        cuda_path = os.environ.get('CUDA_PATH', '')
        检查结果["CUDA可用"] = os.path.exists(cuda_path)

        # FFmpeg硬件加速检查
        ffmpeg_check = subprocess.run(['ffmpeg', '-hwaccels'], stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)
        检查结果["FFmpeg加速"] = 'cuda' in ffmpeg_check.stdout.lower()

        # 编码器检查
        encoder_check = subprocess.run(['ffmpeg', '-encoders'], stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)
        检查结果["编码器支持"] = 'h264_nvenc' in encoder_check.stdout

        # 显存检查
        mem_info = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'], text=True, stderr=subprocess.DEVNULL)
        总显存 = int(mem_info.strip())
        检查结果["显存充足"] = 总显存 >= 2048

        gpu_available = all(检查结果.values())

    except Exception: gpu_available = False
    print("="*40)
    print("硬件加速环境检查报告：")
    for 项目, 状态 in 检查结果.items():
        status = "✓" if 状态 else "✗"
        print(f"{项目:10}{status}")
    print(f"最终状态：{'GPU加速可用' if gpu_available else '将使用CPU模式'}")
    print("="*40)
    GPU_SUPPORTED = all(检查结果.values())
    return GPU_SUPPORTED

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


def getVoideDuration(path):
    try:
        cmd_duration = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=nw=1:nk=1',
            path
        ]
        return float(subprocess.check_output(cmd_duration).decode().strip())
    except Exception as e:
        print(f"获取时时长失败: {e}")
        return None

def getVoideSize(视频路径):
    try:
        cmd_dimensions = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            视频路径
        ]
        output = subprocess.check_output(cmd_dimensions).decode().strip()
        if not output:
            print("ffprobe 返回空值")
            return None, None
        output = output.rstrip('x')
        dimensions = output.split('x')
        if len(dimensions) != 2 or not all(dimensions):
            print("无法解析视频尺寸")
            return None, None
        return int(dimensions[0]), int(dimensions[1])
    except Exception as e:
        print(f"获取时尺寸失败: {e}")
        return None, None


def deleteBugVoide (folder_path):
    视频类型=tuple(os.getenv("视频类型").split(","))
    for root, __, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(视频类型):
                file_path = os.path.join(root, filename)
                if getVoideSize(file_path)[0] is None:
                    print(f"❌删除损坏的文件: {file_path}")
                    os.remove(file_path)
def Split1(item):
    视频路径, output_path, 起始时间, 结束时间, 输出宽, 输出高 = item

    # —— 动态线程数 —
    cpu_count = os.cpu_count() or 8
    threads = min(cpu_count + 2, 16)

    # —— 基础命令骨架（不含编码器/滤镜，后面按需拼接） —
    base_cmd = [
        'ffmpeg', '-y',
        '-ss', str(起始时间), '-to', str(结束时间),
        '-i', 视频路径,
        '-b:v', '5M', '-async', '1', '-threads', str(threads),
        '-r', '30',
        # 统一色彩标准（BT.709）
        '-colorspace', 'bt709',
        '-color_primaries', 'bt709',
        '-color_trc', 'bt709',
        # 流媒体优化（MP4 快速启动）
        '-movflags', '+faststart',
        # 音频统一参数
        '-channel_layout', 'stereo',
        '-b:a', '128k',
        # 元数据
        '-metadata:s:v', 'title=Processed Video',
        '-metadata:s:a', 'title=Processed Audio',
        # 生成正确时间戳
        '-fflags', '+genpts'
    ]

    if GPU_SUPPORTED:
        # GPU 路径：先上传再 scale_cuda
        base_cmd[1:1] = ['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda']
        vf = f'hwupload,scale_cuda={输出宽}:{输出高}'

        video_codec = [
            '-c:v', 'h264_nvenc',
            '-preset', 'p6',
            '-tune', 'll',
            '-b_ref_mode', 'middle',
            '-bf', '4',
            '-rc-lookahead', '20',
            '-spatial-aq', '1',
            '-temporal-aq', '1',
            '-aq-strength', '8'
        ]
        audio_codec = ['-c:a', 'aac']   # 也可保持 copy，看你需求
    else:
        # CPU 路径
        vf = f'scale={输出宽}:{输出高}'
        video_codec = [
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-x264-params', f'threads={threads}:lookahead-threads=2',
            '-movflags', '+faststart'   # 与 base_cmd 中的重复无妨
        ]
        audio_codec = ['-c:a', 'aac']

    # 组装最终命令
    cmd = base_cmd + ['-vf', vf] + video_codec + audio_codec + [output_path]

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"✅分割成功：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌分割失败: {e.stderr.decode('utf-8')}")
        sleep(1)
        Split(item)


def Split(item):
    视频路径, output_path, 起始时间, 结束时间, 输出宽, 输出高 = item

    # ---------- 动态线程数 ----------
    cpu_count = os.cpu_count() or 8
    threads = min(cpu_count + 2, 16)

    # ---------- 统一目标码率 ----------
    TARGET_V_BPS = '4000k'   # 视频
    TARGET_A_BPS = '128k'    # 音频

    # ---------- 基础命令骨架 ----------
    base_cmd = [
        'ffmpeg', '-y',
        '-ss', str(起始时间), '-to', str(结束时间),
        '-i', 视频路径,
        '-b:v', TARGET_V_BPS,
        '-b:a', TARGET_A_BPS,
        '-async', '1', '-threads', str(threads),
        '-r', '30',
        # 统一色彩标准（BT.709）
        '-colorspace', 'bt709',
        '-color_primaries', 'bt709',
        '-color_trc', 'bt709',
        # 流媒体优化
        '-movflags', '+faststart',
        # 音频声道与元数据
        '-channel_layout', 'stereo',
        '-metadata:s:v', 'title=Processed Video',
        '-metadata:s:a', 'title=Processed Audio',
        '-fflags', '+genpts'
    ]

    # ---------- GPU / CPU 分支 ----------
    if GPU_SUPPORTED:
        # 在索引 1 的位置插入硬件加速参数
        base_cmd[1:1] = ['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda']
        vf = f'hwupload,scale_cuda={输出宽}:{输出高}:format=nv12,setsar=1/1'

        video_codec = [
            '-c:v', 'h264_nvenc',
            '-preset', 'p6',
            '-tune', 'll',
            '-b_ref_mode', 'middle',
            '-bf', '4',
            '-rc-lookahead', '20',
            '-spatial-aq', '1',
            '-temporal-aq', '1',
            '-aq-strength', '8'
        ]
        audio_codec = ['-c:a', 'aac']
    else:
        vf = f'scale={输出宽}:{输出高}:format=yuv420p,setsar=1/1'
        video_codec = [
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-x264-params', f'threads={threads}:lookahead-threads=2',
            '-movflags', '+faststart'
        ]
        audio_codec = ['-c:a', 'aac']

    # ---------- 组装最终命令 ----------
    cmd = base_cmd + ['-vf', vf] + video_codec + audio_codec + [output_path]

    # ---------- 执行 ----------
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"✅分割成功：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌分割失败: {e.stderr.decode('utf-8')}")
        sleep(1)
        Split(item)
def Mirror(iteam):
    try:
        视频路径, output_path=iteam
        if GPU_SUPPORTED:
            ffmpeg_cmd = [
                'ffmpeg', '-hwaccel', 'cuda',
                '-y', '-ss', '0', 
                '-i', 视频路径,
                '-vf', "hflip",
                '-c:v', 'h264_nvenc', '-preset', 'medium',
                '-b:v', '5M', '-c:a', 'copy', output_path]
        else:
            ffmpeg_cmd = [
                'ffmpeg',
                '-y', '-ss', '0', 
                '-i', 视频路径,
                '-vf', "hflip",
                '-c:v', 'libx264', '-preset', 'medium',
                '-b:v', '5M', '-c:a', 'aac', output_path]
        result=subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Error in merging:",result.stderr.decode(errors='ignore'))
            Mirror(iteam)
        print(f"✅镜像成功：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌镜像失败: {e.stderr.decode('utf-8')}") 
def Trim(item):
    video_path, crop_width, crop_height, output_path, position = item
    
    # 获取视频尺寸
    width, height = getVoideSize(video_path)
    if width is None or height is None:
        print(f"无法获取视频尺寸: {video_path}")
        return

    # 计算裁剪位置
    if position == 'center':
        x = (width - crop_width) // 2
        y = (height - crop_height) // 2
    elif position == 'left':
        x = 0
        y = (height - crop_height) // 2
    elif position == 'right':
        x = width - crop_width
        y = (height - crop_height) // 2
    else:
        print(f"未知的裁剪位置: {position}")
        return

    # 构建FFmpeg命令
    if GPU_SUPPORTED:
        # 对于GPU支持情况，将hwaccel参数放在输入前
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-hwaccel', 'cuda',
            '-threads', '4',
            '-i', video_path,
            '-vf', f'crop={crop_width}:{crop_height}:{x}:{y}',
            '-c:v', 'h264_nvenc',
            '-preset', 'medium',
            '-c:a', 'copy',
            output_path
        ]
    else:
        # CPU模式
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-threads', '4',
            '-i', video_path,
            '-vf', f'crop={crop_width}:{crop_height}:{x}:{y}',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-c:a', 'copy',
            output_path
        ]

    try:
        # 运行FFmpeg命令
        subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE)
        print(f"✅裁剪成功：{output_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else '未知错误'
        print(f"❌裁剪失败: {error_msg}")
        sleep(1)
        Trim(item)

def _probe_duration1(path: str) -> float:
    """返回媒体时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'format=duration',
        '-of', 'json', path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


def Merge_Audio1(temp_video, output_path, duration=None,audio=True, music_path=None, volume=1.0):
    start_time = time.time()
    video_dur_cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'json', temp_video
    ]
    video_duration = float(json.loads(subprocess.run(
        video_dur_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    ).stdout)['format']['duration'])
    target_dur = duration if duration is not None else video_duration
    music_duration = _probe_duration1(music_path)
    if music_duration < target_dur:
        # 需要循环：aloop=loop=-1:size=最长采样数
        bg_filter = f"[1:a]volume={volume},aloop=loop=-1:size=2e9,atrim=0:{target_dur},asetpts=PTS-STARTPTS[a2]"
    else:
        # 直接截断
        bg_filter = f"[1:a]volume={volume},atrim=0:{target_dur},asetpts=PTS-STARTPTS[a2]"

    # 混音或仅使用背景音乐
    if audio:
        filter_complex = f"[0:a]volume=1.0[a1];{bg_filter};[a1][a2]amix=inputs=2:duration=first[a]"
    else:
        filter_complex = f"{bg_filter};[a2]anull[a]"

    cmd = [
        'ffmpeg', '-y',
        '-i', temp_video,
        '-i', music_path,
        '-filter_complex', filter_complex,
        '-map', '0:v:0',
        '-map', '[a]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-t', str(target_dur),   # 保证输出严格等于 target_dur
        output_path
    ]

    # print("Final merge:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_time = time.time() - start_time
        print(f"✅音频合并成功，耗时: {audio_time:.2f}秒{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌音频合并成功失败: {e}")
        raise






def _probe_duration(path: str) -> float:
    """返回媒体时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'format=duration',
        '-of', 'json', path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


def Merge_Audio(temp_video, output_path, duration=None, audio=True, music_path=None, volume=1.0):
    start_time = time.time()
    
    # 获取视频时长
    video_dur_cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'json', temp_video
    ]
    video_duration = float(json.loads(subprocess.run(
        video_dur_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    ).stdout)['format']['duration'])
    
    target_dur = duration if duration is not None else video_duration
    
    # 处理背景音乐
    if music_path:
        music_duration = _probe_duration(music_path)
        if music_duration < target_dur:
            # 需要循环
            bg_filter = f"[1:a]volume={volume},aloop=loop=-1:size=2e9,atrim=0:{target_dur},asetpts=PTS-STARTPTS[a2]"
        else:
            # 直接截断
            bg_filter = f"[1:a]volume={volume},atrim=0:{target_dur},asetpts=PTS-STARTPTS[a2]"
    else:
        bg_filter = ""

    # 混音或仅使用背景音乐
    if audio and music_path:
        filter_complex = f"[0:a]volume=1.0[a1];{bg_filter};[a1][a2]amix=inputs=2:duration=first[a]"
    elif music_path:
        filter_complex = f"{bg_filter};[a2]anull[a]"
    elif audio:
        filter_complex = f"[0:a]volume=1.0,atrim=0:{target_dur},asetpts=PTS-STARTPTS[a]"
    else:
        filter_complex = ""

    # 构建基本命令
    cmd = ['ffmpeg', '-y']
    
    # 添加GPU加速支持
    if GPU_SUPPORTED:
        cmd.extend([
            '-hwaccel', 'cuda',
            '-hwaccel_output_format', 'cuda'
        ])
    
    # 添加输入文件
    cmd.extend(['-i', temp_video])
    if music_path:
        cmd.extend(['-i', music_path])
    
    # 添加滤镜
    if filter_complex:
        cmd.extend(['-filter_complex', filter_complex])
    
    # 添加映射和编码参数
    cmd.extend(['-map', '0:v:0'])
    if filter_complex:
        cmd.extend(['-map', '[a]'])
    elif audio and not music_path:
        cmd.extend(['-map', '0:a:0'])
    
    # 视频编码设置
    if GPU_SUPPORTED:
        cmd.extend([
            '-c:v', 'h264_nvenc',
            '-preset', 'fast'
        ])
    else:
        cmd.extend(['-c:v', 'copy'])
    
    # 音频编码设置
    cmd.extend(['-c:a', 'aac'])
    
    # 添加时长限制
    cmd.extend(['-t', str(target_dur)])
    
    # 输出文件
    cmd.append(output_path)

    # print("Final merge:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_time = time.time() - start_time
        print(f"✅音频合并成功，耗时: {audio_time:.2f}秒 {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌音频合并失败: {e}")
        return False

def merge_video(cliplist, temp_video, duration=None, audio=True):
    # print(f"开始合并视频文件: {cliplist}")
    # print(f"输出文件路径: {temp_video}")
    start_time = time.time()
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
    
    cmd.append(temp_video)
    silent=True
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL if silent else None,
            stderr=subprocess.DEVNULL if silent else None
        )
        audio_time = time.time() - start_time
        print(f"✅视频合并成功，耗时: {audio_time:.2f}秒 {temp_video}")
        return True
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"❌视频合并失败: {e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}")
        return False
def Merge(cliplist, output_path, duration=None,audio=True, music_path=None, volume=1.0):

    """
    合并视频和音频，自动循环或截断背景音乐到指定 duration。
    """
    temp_video='temp_video.mp4' if music_path else output_path
    merge_video(cliplist, temp_video, duration, audio)
    if music_path:
        Merge_Audio(temp_video, output_path, duration,audio, music_path, volume)


# cliplist=['儿推第十二课外劳宫-阳池认识0.mp4', '儿推第十二课外劳宫-阳池认识1.mp4', '儿推第十二课外劳宫-阳池认识2.mp4', '儿推第十二课外劳宫-阳池认识3.mp4', '儿推第十二课外劳宫-阳池认识4.mp4', '儿推第十二课外劳宫-阳池认识5.mp4', '儿推第十二课外劳宫-阳池认识6.mp4', '儿推第十二课外劳宫-阳池认识7.mp4', '儿推第十二课外劳宫-阳池认识8.mp4', '儿推第十二课外劳宫-阳池认识9.mp4', '儿推第十二课外劳宫-阳池认识10.mp4', '儿推第十二课外劳宫-阳池认识11.mp4', '儿推第十二课外劳宫-阳池认识12.mp4', '儿推第十二课外劳宫-阳池认识13.mp4', '儿推第十二课外劳宫-阳池认识14.mp4', '儿推第十二课外劳宫-阳池认识15.mp4', '儿推第十二课外劳宫-阳池认识16.mp4', '儿推第十二课外劳宫-阳池认识17.mp4', '儿推第十二课外劳宫-阳池认识18.mp4', '儿推第十二课外劳宫-阳池认识19.mp4', '儿推第十二课外劳宫-阳池认识20.mp4', '儿推第十二课外劳宫-阳池认识21.mp4', '儿推第十二课外劳宫-阳池认识22.mp4', '儿推第十二课外劳宫-阳池认识23.mp4', '儿推第十二课外劳宫-阳池认识24.mp4', '儿推第十二课外劳宫-阳池认识25.mp4']
# temp_video='儿推第十二课外劳宫-阳池认识.mp4'

# merge_video(cliplist, temp_video, duration=None, audio=True)
