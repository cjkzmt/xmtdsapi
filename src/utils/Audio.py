from pydub import AudioSegment

def get_music_info(music_path):
    try:
        audio = AudioSegment.from_file(music_path)
        duration_ms = len(audio)  # 音频时长（毫秒）
        return{"duration": duration_ms}
    except Exception as e:
        print(f"无法读取文件 {music_path}: {e}")
        return{"duration": 0}

def add_silence_audio(input_path, output_path):
    try:
        original = AudioSegment.from_mp3(input_path)
    except Exception as e:
        raise RuntimeError(f"无法加载音频文件 {input_path}: {e}")

    silence = AudioSegment.silent(duration=1000)  # 1秒静音
    combined = original + silence
    combined.export(output_path, format="wav")

