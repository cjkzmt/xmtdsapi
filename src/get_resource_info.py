import os
def get_video_count():
    主文件=os.getenv("主文件")
    发布目录=os.getenv("发布目录")
    path=os.path.join(主文件,发布目录)
    mp4_files = [f for f in os.listdir(path) if f.endswith('.mp4')]
    return len(mp4_files)
def get_clips_count():
    主文件=os.getenv("主文件")
    视频素材=os.getenv("视频素材")
    path=os.path.join(主文件,视频素材)
    mp4_files=[]
    for  root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(file)
    return len(mp4_files)
def get_scrips_count():
    主文件=os.getenv("主文件")
    成片目录=os.getenv("成片目录")
    path=os.path.join(主文件,成片目录)
    txt_files=[]
    for  root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(file)
    return len(txt_files)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    x=get_scrips_count()
    print(x)