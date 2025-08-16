import os
import subprocess
import tempfile
import math

GPU_SUPPORTED = True   # 自动检测可以写成：GPU_SUPPORTED = check_gpu()

def _loop_bg_music(bg_path, target_duration, tmp_dir):
    """
    把背景音乐循环到 target_duration 秒，返回循环后的临时文件路径。
    如果 bg_path 本来就比 target_duration 长，则直接返回原文件。
    """
    # 先取出原音乐时长
    probe_cmd = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'csv=p=0', bg_path
    ]
    bg_dur = float(subprocess.check_output(probe_cmd).decode().strip())

    if bg_dur >= target_duration:
        return bg_path

    loops = math.ceil(target_duration / bg_dur)
    concat_file = os.path.join(tmp_dir, 'bg_loop.txt')
    with open(concat_file, 'w', encoding='utf-8') as f:
        for _ in range(loops):
            f.write(f"file '{bg_path}'\n")

    looped_path = os.path.join(tmp_dir, 'looped_bg.aac')
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
        '-c', 'copy', looped_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return looped_path


def Merge(cliplist, output_path, duration=None, audio=True,
          music_path=None, volume=1.0):
    """
    cliplist      : 视频文件列表
    output_path   : 合并后的输出路径
    duration      : 最终时长(秒)，None 表示不裁剪
    audio         : True  保留原声 + 可选背景音乐
                   False 去掉原声，只留背景音乐(或静音)
    music_path    : 背景音乐文件路径
    volume        : 背景音乐音量比例 0.1~10.0
    """
    if not cliplist:
        raise ValueError("Empty video list provided")

    # ---------- 1. 构造输入 ----------
    inputs = []
    for v in cliplist:
        inputs += ['-i', v.strip('\x00')]

    # ---------- 2. 计算 / 裁剪 ----------
    # 先把所有视频无音频地拼接起来，得到总时长
    probe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                 '-show_entries', 'format=duration', '-of', 'csv=p=0']
    total = 0.0
    for v in cliplist:
        t = float(subprocess.check_output(probe_cmd + [v]).decode().strip())
        total += t
    final_duration = duration if duration is not None else total

    # ---------- 3. 构造 filter_complex ----------
    n = len(cliplist)

    # 视频部分：拼接到一起，如果设定了 duration 再裁剪
    video_chain = f"concat=n={n}:v=1:a=0[vraw]"
    if duration is not None:
        video_chain += f";[vraw]trim=duration={final_duration}[v]"
    else:
        video_chain += ";[vraw]null[v]"

    filter_complex = video_chain

    map_video = ['-map', '[v]']
    map_audio = []

    # ---------- 4. 音频处理 ----------
    if audio or music_path:
        # 先把原声拼起来，再裁剪
        audio_chain = f"concat=n={n}:v=0:a=1[araw]"
        if duration is not None:
            audio_chain += f";[araw]atrim=duration={final_duration}[aorig]"
        else:
            audio_chain += ";[araw]anull[aorig]"

        filter_complex += ";" + audio_chain

        if music_path:   # 需要背景音乐
            with tempfile.TemporaryDirectory() as tmp:
                looped_music = _loop_bg_music(music_path, final_duration, tmp)

                # 再加一个输入：背景音乐
                inputs += ['-i', looped_music]

                # 音量调节
                vol_filter = f"volume={volume:.2f}"
                # 混合原声 + 背景音乐，或仅背景音乐
                if audio:  # 保留原声
                    filter_complex += (
                        ";[aorig][2:a]amix=inputs=2:duration=first:dropout_transition=2[a]"
                    )
                else:      # 去掉原声
                    filter_complex += f";[2:a]{vol_filter}[a]"
        else:
            # 没有背景音乐，只处理原声
            if audio:
                filter_complex += ";[aorig]anull[a]"
            else:
                # 完全静音，不映射音频
                pass

        if audio or music_path:
            map_audio = ['-map', '[a]']

    # ---------- 5. 构造并执行 ffmpeg 命令 ----------
    cmd = ['ffmpeg', '-y']
    if GPU_SUPPORTED:
        cmd += ['-hwaccel', 'cuda']

    cmd += inputs
    cmd += [
        '-filter_complex', filter_complex,
        *map_video,
        *map_audio,
        '-t', str(final_duration),  # 保险起见再截一次
        '-c:v', 'h264_nvenc' if GPU_SUPPORTED else 'libx264',
    ]

    # 音频编码器
    if audio or music_path:
        cmd += ['-c:a', 'aac']

    cmd.append(output_path)

    print(" ".join(cmd))

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print("合并成功：", output_path)
        return True
    except subprocess.CalledProcessError as e:
        print("合并失败：")
        print(e.stderr.decode(errors='ignore'))
        return False

cliplist=['D:\\新媒体大师\\素材\\视频请放这里\\已用视频\\142\\0\\xyq\\46c1f03459481329fc5ec6a972ffe18f_1.mp4', 'D:\\新媒体大师\\素材\\视频请放这里\\已用视频\\142\\0\\xyq\\WeChat_20231016111730_4_center_Mirror.mp4']
music_path=r' D:\新媒体大师\素材\其他素材\音频\在这新年之际，祝大家新年快乐\欢迎您来看看我爸妈住了二十年的老屋.wav'
duration=4.18
output_path=r'D:\新媒体大师\素材\视频请放这里\已用视频\142\0.mp4'
Merge(cliplist, output_path, duration=None, audio=False,music_path=None, volume=1.0)