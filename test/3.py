import os
import subprocess

GPU_SUPPORTED = True

def Merge(cliplist, output_path):
    cliplist = [v.strip('\x00') for v in cliplist if v and os.path.exists(v)]
    if not cliplist:
        print("错误：视频列表为空或文件不存在！")
        return

    # 强制输入帧率（关键修复）
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'info']
    if GPU_SUPPORTED:
        cmd += ['-hwaccel', 'cuda', '-c:v', 'h264_cuvid']

    for v in cliplist:
        cmd += ['-r', '30', '-i', v]  # 强制按 30fps 读取

    video_concat = ''.join([f"[{i}:v]" for i in range(len(cliplist))]) + f"concat=n={len(cliplist)}:v=1:a=0[v]"
    audio_concat = ''.join([f"[{i}:a]" for i in range(len(cliplist))]) + f"concat=n={len(cliplist)}:v=0:a=1[a]"
    filter_complex = f"{video_concat};{audio_concat}"

    cmd += [
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'h264_nvenc' if GPU_SUPPORTED else 'libx264',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-preset', 'fast',
        '-cq', '23',
        '-rc', 'vbr',
        '-b:v', '5M',
        '-maxrate:v', '8M',
        '-bufsize:v', '10M',
        '-r', '30',  # 强制输出帧率 30fps
        output_path
    ]

    print("执行命令：\n", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("✅ 合并成功：", output_path)
    except subprocess.CalledProcessError as e:
        print("❌ 合并失败：", e)


# === 测试用例 ===
if __name__ == "__main__":
    cliplist = [
        r'D:\新媒体大师\素材\视频请放这里\已用视频\142\17\xyq\7月23日 (1)_26.mp4',
        r'D:\新媒体大师\素材\视频请放这里\已用视频\142\17\xyq\a3cfca733d7f8b898203c8bc2a6203af_0_center_Mirror.mp4',
        r'D:\新媒体大师\素材\视频请放这里\已用视频\142\17\xyq\b8199ac9a7e447acecc2c07dbfe19742_8_center.mp4'
    ]
    output_path = r'D:\新媒体大师\素材\视频请放这里\已用视频\142\17_合并优化.mp4'
    Merge(cliplist, output_path)


